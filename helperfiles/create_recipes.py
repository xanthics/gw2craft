"""Using the GW2 api, output valid recipes and all used items in supported languages."""

import asyncio
import datetime
import enum
import http
import operator
import pathlib
import sys
import time

import aiohttp
import more_itertools
import pyrate_limiter

from aiohttp_monkeypatch import set_response_params
from good_items import good_items
from good_recipes import good_recipes

GUILD_ITEM_OFFSET = 10000000
PAGE_SIZE = 200
MAX_BACKOFF_LIMIT = 65

aiohttp.client_proto.ResponseHandler.set_response_params = set_response_params  # noqa
limiter = pyrate_limiter.Limiter(
    pyrate_limiter.RequestRate(20, pyrate_limiter.Duration.SECOND),
    pyrate_limiter.RequestRate(575, pyrate_limiter.Duration.MINUTE),
)


@limiter.ratelimit("api", delay=True, max_delay=128)
async def _api_call(session, endpoint, first=False):
    backoff_limit = 1
    while True:
        print(f"Running: {endpoint[:100]}")
        async with session.get(endpoint) as request:
            reply = await request.json()
            if (
                request.status == http.HTTPStatus.TOO_MANY_REQUESTS
                and backoff_limit < MAX_BACKOFF_LIMIT
            ):
                print(f"API Get sleeping for {backoff_limit} second(s).")
                time.sleep(backoff_limit)
                backoff_limit *= 2
                continue
            if request.status not in {
                http.HTTPStatus.OK,
                http.HTTPStatus.PARTIAL_CONTENT,
            }:
                raise Exception(f"API response: {request.status} {request.content}")
            if first:
                return int(request.headers["x-page-total"]), reply
            return reply


def parse_recipes():
    """Parse only recipes that we care about."""

    recipes = {}
    while True:
        recipe = yield
        if recipe is None:
            yield recipes
        # only consider allow listed recipes that are learned from an item
        if "LearnedFromItem" in recipe["flags"] and recipe["id"] not in good_recipes:
            continue
        elif not recipe["disciplines"]:
            continue
        # 24838 at lvl 375 is a bugged recipe(Major Rune of Water, Tailoring)
        elif recipe["output_item_id"] == 24838:
            continue
        elif (
            all(x in {"Scribe", "Jeweler"} for x in recipe["disciplines"])
            and recipe["min_rating"] >= 400
        ):
            continue
        elif recipe["min_rating"] >= 500:
            continue
        recipes[recipe["id"]] = recipe


async def get_recipes(session):
    """Get all available recipes."""

    parser = parse_recipes()
    next(parser)
    # First request, getting number of pages in result
    print("Grabbing first page")
    pages, task = await _api_call(session, "/v2/recipes?page=0&page_size=200", True)
    print(f"{pages} recipes")
    for recipe in task:
        parser.send(recipe)
    jobs = (
        asyncio.ensure_future(
            _api_call(session, f"/v2/recipes?page={page}&page_size=200")
        )
        for page in range(1, pages)
    )
    # Get the rest of the recipes
    tasks = await asyncio.gather(*jobs)
    for task in tasks:
        for recipe in task:
            parser.send(recipe)
    return parser.send(None)


async def get_items(session, item_ids):
    """Get all referenced items."""

    item_sets = (",".join(i) for i in more_itertools.chunked(item_ids, PAGE_SIZE))
    jobs = (
        asyncio.ensure_future(_api_call(session, f"/v2/items?lang=en&ids={page}"))
        for page in item_sets
    )
    tasks = await asyncio.gather(*jobs)
    return {item["id"]: item for task in tasks for item in task}


async def get_guild(session, guild_ids):
    """Get all referenced guild items."""

    guild_sets = (",".join(i) for i in more_itertools.chunked(guild_ids, PAGE_SIZE))
    jobs = (
        asyncio.ensure_future(
            _api_call(session, f"/v2/guild/upgrades?lang=en&ids={page}")
        )
        for page in guild_sets
    )
    tasks = await asyncio.gather(*jobs)
    return {guild_item["id"]: guild_item for task in tasks for guild_item in task}


def write_recipes(recipes, items):
    """Write to file all the recipes we are tracking."""

    keys = [
        "Weaponsmith",
        "Chef",
        "Chef_karma",
        "Huntsman",
        "Armorsmith",
        "Jeweler",
        "Artificer",
        "Tailor",
        "Leatherworker",
        "Scribe",
    ]
    crafts = {key: {} for key in keys}
    for data in recipes.values():
        min_rating = data["min_rating"]
        item_id = data["output_item_id"]
        item_count = data["output_item_count"]
        ingredients = {int(i["item_id"]) for i in data["ingredients"]}

        for it in data["disciplines"]:
            key = it
            # We don't want recipe items.  Except for karma cooking and known good recipes
            if "LearnedFromItem" in data["flags"] and not (
                it == "Chef" or int(item_id) in good_recipes
            ):
                continue
            if it == "Chef" and (
                set(good_items) & ingredients or "LearnedFromItem" in data["flags"]
            ):
                key = "Chef_karma"

            crafts[key].setdefault(min_rating, {})
            crafts[key][min_rating][item_id] = data["ingredients"]
            items[item_id]["output_item_count"] = item_count

    for craft in crafts:
        page = [
            f"# Created: {datetime.datetime.now().strftime('%Y-%m-%dT%H:%M')} PST",
            "recipes = {",
        ]
        for lvl in sorted(crafts[craft]):
            page.append(f"\t{lvl}: {{")
            for obj in sorted(crafts[craft][lvl]):
                r_part = ", ".join(
                    [
                        f"{part['item_id']}: {part['count']}"
                        for part in sorted(
                            crafts[craft][lvl][obj], key=operator.itemgetter("item_id")
                        )
                    ]
                )
                page.append(f"\t\t{obj}: {{{r_part}}},  # {items[obj]['name']}")
            page.append("\t},")
        page.append("}\n")
        path = pathlib.Path().cwd().parent / "autogen" / f"{craft}.py"
        with open(path, "w", encoding="utf-8") as f:
            f.write("\n".join(page))


def validate_data(recipes, items):
    """Allow list learned recipes, and make sure that recipes/etc only contain valid items."""

    removed = True
    while removed:
        removed = False
        outputs = {recipes[x]["output_item_id"] for x in recipes}
        for recipe in sorted(recipes):
            for x in recipes[recipe]["ingredients"]:
                if (
                    x["item_id"] < GUILD_ITEM_OFFSET
                    and "AccountBound" in items[x["item_id"]]["flags"]
                    and x["item_id"] not in outputs | good_items
                ):
                    removed = True
                    del recipes[recipe]
                    break

    outputs = {recipes[x]["output_item_id"] for x in recipes}
    inputs = {x["item_id"] for y in recipes for x in recipes[y]["ingredients"]}

    for item in items:
        if item not in outputs | inputs and not (
            "details" in items[item]
            and "recipe_id" in items[item]["details"]
            and items[item]["details"]["recipe_id"] in recipes
        ):
            del items[item]


class Language(str, enum.Enum):
    """Current supported languages: en, fr, de, es, zh."""

    def __str__(self):
        return self.value.lower()

    def _generate_next_value_(self, *_):
        return self

    EN = enum.auto()
    FR = enum.auto()
    DE = enum.auto()
    ES = enum.auto()
    ZH = enum.auto()


async def item_list(items, guild, session, lang=Language.EN):
    """Get more information on every item the recipes use."""

    print(f"Starting {lang}")
    flags = {}

    if lang == Language.EN:
        page = [
            f"# Created: {datetime.datetime.now().strftime('%Y-%m-%dT%H:%M')} PST\n",
            "ilist = {",
        ]
        # Sorted, so we can easily spot new items with deterministic diff
        for i in sorted(items):
            flags[i] = items[i]["name"]
            if "NoSell" in items[i]["flags"]:
                items[i]["vendor_value"] = 0
            else:
                items[i]["vendor_value"] = int(items[i]["vendor_value"])
            if items[i]["flags"]:
                items[i]["discover"] = 0
            if "output_item_count" not in items[i]:
                items[i]["output_item_count"] = 0
            page.append(
                f"\t{i}: {{'output_item_count': {items[i]['output_item_count']}, 'type': '{items[i]['type']}', 'rarity': '{items[i]['rarity']}', 'vendor_value': {items[i]['vendor_value']}, 'img_url': '{items[i]['icon']}'}},  # {items[i]['name']}"
            )
        page.append("}\n")
        path = pathlib.Path().cwd().parent / "auto_gen2" / "Items.py"
        with open(path, "w", encoding="utf-8") as f:
            f.write("\n".join(page))
    else:
        item_ids = (str(x) for x in items if x < GUILD_ITEM_OFFSET)
        item_sets = (",".join(i) for i in more_itertools.chunked(item_ids, PAGE_SIZE))
        jobs = (
            asyncio.ensure_future(
                _api_call(session, f"/v2/items?lang={lang}&ids={page}")
            )
            for page in item_sets
        )
        tasks = await asyncio.gather(*jobs)
        for task in tasks:
            for item in task:
                flags[item["id"]] = item["name"]

        guild_ids = (str(x) for x in guild)
        guild_sets = (",".join(i) for i in more_itertools.chunked(guild_ids, PAGE_SIZE))
        jobs = (
            asyncio.ensure_future(
                _api_call(session, f"/v2/guild/upgrades?lang={lang}&ids={page}")
            )
            for page in guild_sets
        )
        tasks = await asyncio.gather(*jobs)
        for task in tasks:
            for item in task:
                flags[item["id"] + GUILD_ITEM_OFFSET] = item["name"]

    page = [
        f"# Created: {datetime.datetime.now().strftime('%Y-%m-%dT%H:%M')} PST\n",
        "ilist = {",
    ]
    # Sorted, so we can easily spot new items with deterministic diff
    for i in sorted(flags):
        page.append(f"\t{i}: {repr(flags[i])},")
    page.append("}\n")
    path = pathlib.Path().cwd().parent / "auto_gen2" / f"Items_{lang}.py"
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(page))


def get_guild_items(recipes):
    """Generate lists guild items (Scribe) and update item IDs as appropriate."""

    outputs = {recipes[x]["output_item_id"] for x in recipes}
    inputs = {x["item_id"] for y in recipes for x in recipes[y]["ingredients"]}
    recipe_ids = [good_recipes[recipe] for recipe in good_recipes]
    # needs to be str since we will be using join later to create urls
    item_ids = [str(x) for x in list(inputs | outputs) + recipe_ids]

    guild_ids = []
    for item in recipes:
        if "Scribe" not in recipes[item]["disciplines"]:
            continue
        if "guild_ingredients" in recipes[item]:
            for i in recipes[item]["guild_ingredients"]:
                if i["upgrade_id"] not in guild_ids:
                    guild_ids.append(str(i["upgrade_id"]))
                recipes[item]["ingredients"].append(
                    {
                        "count": i["count"],
                        "item_id": i["upgrade_id"] + GUILD_ITEM_OFFSET,
                    }
                )
        if "output_upgrade_id" in recipes[item]:
            if recipes[item]["output_upgrade_id"] not in guild_ids:
                guild_ids.append(str(recipes[item]["output_upgrade_id"]))
            recipes[item]["output_item_id"] = (
                recipes[item]["output_upgrade_id"] + GUILD_ITEM_OFFSET
            )
    return item_ids, guild_ids


def merge_items_guild(items, guild):
    """Merge guild items in to item list now that we have finished preprocessing."""

    for item in guild:
        items[item + GUILD_ITEM_OFFSET] = {
            "name": guild[item]["name"],
            "icon": guild[item]["icon"],
            "rarity": "Basic",
            "flags": ["NoSell"],
            "vendor_value": 0,
            "type": guild[item]["type"],
        }


async def main():
    api_root = "https://api.guildwars2.com"
    async with aiohttp.ClientSession(api_root) as session:
        recipes = await get_recipes(session)
        item_ids, guild_ids = get_guild_items(recipes)
        items = await get_items(session, item_ids)
        guild = await get_guild(session, guild_ids)

        validate_data(recipes, items)
        merge_items_guild(items, guild)
        write_recipes(recipes, items)

        for lang in Language:
            await item_list(items, guild, session, lang)


if __name__ == "__main__":
    # Special exception for Windows.
    if (4, 0, 0) > sys.version_info >= (3, 8, 0) and sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())
