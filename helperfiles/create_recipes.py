# Using GW2 api, get all recipes, calculated used items, output valid recipes, output all used items in supported languages

import asyncio
import sys
import time

import aiohttp
from datetime import datetime
from pyrate_limiter import *
from good_items import good_items, good_vendor
from good_recipes import good_recipes

# import monkey patch for aiohttp to allow response headers > 8190 bytes
from helperfiles.aiohttp_monkey import set_response_params
aiohttp.client_proto.ResponseHandler.set_response_params = set_response_params


# Globals are bad, oh well
GUILD_ITEM_OFFSET = 10000000

# api request limit.  stored in a queue.Queue
limiter = Limiter(RequestRate(20, Duration.SECOND), RequestRate(575, Duration.MINUTE))


@limiter.ratelimit('api', delay=True, max_delay=128)
async def _api_call(session, endpoint, first=False):
	x = 1
	while True:
		print(f"Running: {endpoint[:100]}")
		async with session.get(endpoint) as req:
			reply = await req.json()
			if req.status not in [200, 206]:
				# attempt to sleep with a too many requests response.  Fail if backoff limit reached
				if req.status == 429 and x < 65:
					print(f"API Get sleeping for {x} second(s).")
					time.sleep(x)
					x *= 2
					continue
				raise Exception('API response: {} {}'.format(req.status, req.content))
			if first:
				return int(req.headers['x-page-total']), reply
			return reply


# check that a recipe is one we care about
def validate_recipe(item):
	if (('LearnedFromItem' in item['flags'] and item['id'] not in good_recipes)  # only consider allow listed recipes that are learned from an item
			or not len(item['disciplines'])
			# 24838 at lvl 375 is a bugged recipe(Major Rune of Water, Tailoring)
			or item['output_item_id'] == 24838
			# or (item['type'] in ['Feast', 'Backpack'] and 'Scribe' not in item['disciplines'])
			or (all(x in ['Scribe', 'Jeweler'] for x in item['disciplines']) and item['min_rating'] >= 400)
			or item['min_rating'] >= 500):
		return False
	return True


# get all available recipes
async def get_recipes(session):
	# first request, getting number of pages in result
	print("Grabbing first page")
	recipes = {}
	pages, task = await _api_call(session, '/v2/recipes?page=0&page_size=200', True)
	print(f"{pages} recipes")
	for val in task:
		if validate_recipe(val):
			recipes[val['id']] = val
	jobs = (asyncio.ensure_future(_api_call(session, f'/v2/recipes?page={page}&page_size=200')) for page in range(1, pages))
	# get the rest of the recipes
	tasks = await asyncio.gather(*jobs)

	for p in tasks:
		for val in p:
			if validate_recipe(val):
				recipes[val['id']] = val

	return recipes


# get all referenced items
async def get_items(session, item_ids):
	items = {}
	item_sets = (','.join(item_ids[i:i+200]) for i in range(0, len(item_ids), 200))
	jobs = (asyncio.ensure_future(_api_call(session, f'/v2/items?lang=en&ids={page}')) for page in item_sets)
	tasks = await asyncio.gather(*jobs)
	for p in tasks:
		for val in p:
			items[val['id']] = val

	return items


# get all referenced guild items
async def get_guild(session, guild_ids):
	guild_items = {}
	guild_sets = (','.join(guild_ids[i:i+200]) for i in range(0, len(guild_ids), 200))
	jobs = (asyncio.ensure_future(_api_call(session, f'/v2/guild/upgrades?lang=en&ids={page}')) for page in guild_sets)
	tasks = await asyncio.gather(*jobs)
	for p in tasks:
		for val in p:
			guild_items[val['id']] = val

	return guild_items


# Write to file all the recipes we are tracking
def write_recipes(recipes, items):
	crafts = {'Weaponsmith': {}, 'Chef': {}, 'Chef_karma': {}, 'Huntsman': {},
	          'Armorsmith': {}, 'Jeweler': {}, 'Artificer': {}, 'Tailor': {},
	          'Leatherworker': {}, 'Scribe': {}}
	for _recipe, data in list(recipes.items()):
		min_rating = data['min_rating']
		item_id = data['output_item_id']
		item_count = data['output_item_count']
		ingredient_set = set(int(i['item_id']) for i in data['ingredients'])

		for it in data['disciplines']:
			key = it
			# We don't want recipe items.  Except for karma cooking and known good recipes
			if 'LearnedFromItem' in data['flags'] and not (it == 'Chef' or int(item_id) in good_recipes):
				continue
			if it == 'Chef' and (set(good_items) & ingredient_set or 'LearnedFromItem' in data['flags']):
				key = 'Chef_karma'

			crafts[key].setdefault(min_rating, {})
			crafts[key][min_rating][item_id] = data['ingredients']
			items[item_id]['output_item_count'] = item_count

	for craft in crafts:
		page = ['# Created: {} PST'.format(datetime.now().strftime('%Y-%m-%dT%H:%M')), 'recipes = {']
		for lvl in sorted(crafts[craft]):
			page.append(f"\t{lvl}: {{")
			for obj in sorted(crafts[craft][lvl]):
				mystr = []
				for part in sorted(crafts[craft][lvl][obj], key=lambda k: k['item_id']):
					mystr.append(f"{part['item_id']}: {part['count']}")
				r_part = ', '.join(mystr)
				page.append(f"\t\t{obj}: {{{r_part}}},  # {items[obj]['name']}")
			page.append("\t},")
		page.append("}\n")
		with open(f"../autogen\\{craft.lower()}.py", "w", encoding="utf-8") as f:
			f.write('\n'.join(page))


# Allow list learned recipes, and make sure that recipes/etc only contain valid items
def validate_data(recipes, items, guild):
	clean_items(recipes, items)
	outputs = {recipes[x]['output_item_id'] for x in recipes}
	inputs = {x['item_id'] for y in recipes for x in recipes[y]['ingredients']}

	for item in list(items.keys()):
		if item not in outputs | inputs and not ('details' in items[item] and 'recipe_id' in items[item]['details'] and items[item]['details']['recipe_id'] in recipes):
			del items[item]


# removes invalid items and recipes based on rules and allow lists
def clean_items(recipes, items):
	removed = True
	while removed:
		removed = False
		allowed_bound_items = {recipes[x]['output_item_id'] for x in recipes} | good_items | {x for x in good_vendor}
		for recipe in sorted(recipes):
			for x in recipes[recipe]['ingredients']:
				if x['item_id'] < GUILD_ITEM_OFFSET and 'AccountBound' in items[x['item_id']]['flags'] and x['item_id'] not in allowed_bound_items:
					removed = True
					del recipes[recipe]
					break


# get more information on every item the recipes use
# Currently supported languages: en, fr, de, es, zh
async def itemlist(items, guild, session, lang="en"):
	print("Starting {}".format(lang))
	flags = {}

	if lang == "en":
		page = ['# Created: {} PST\n'.format(datetime.now().strftime('%Y-%m-%dT%H:%M')), 'ilist = {']
		# sorted is only so we can easily spot new items with diff
		for i in sorted(items):  # otherwise output is semi random order
			flags[i] = items[i]['name']
			if "NoSell" in items[i]["flags"]:
				items[i]['vendor_value'] = 0
			else:
				items[i]['vendor_value'] = int(items[i]['vendor_value'])
			if items[i]['flags']:
				items[i]['discover'] = 0
			if 'output_item_count' not in items[i]:
				items[i]['output_item_count'] = 0
			page.append(f"\t{i}: {{'output_item_count': {items[i]['output_item_count']}, 'type': '{items[i]['type']}', 'rarity': '{items[i]['rarity']}', 'vendor_value': {items[i]['vendor_value']}, 'img_url': '{items[i]['icon']}'}},  # {items[i]['name']}")
		page.append('}\n')
		with open("../autogen/items.py", "w", encoding="utf-8") as f:
			f.write('\n'.join(page))
	else:
		item_ids = [str(x) for x in items if x < GUILD_ITEM_OFFSET]
		item_sets = (','.join(item_ids[i:i + 200]) for i in range(0, len(item_ids), 200))
		jobs = (asyncio.ensure_future(_api_call(session, f'/v2/items?lang={lang}&ids={page}')) for page in item_sets)
		tasks = await asyncio.gather(*jobs)
		for p in tasks:
			for val in p:
				flags[val['id']] = val['name']

		guild_ids = [str(x) for x in guild]
		guild_sets = (','.join(guild_ids[i:i + 200]) for i in range(0, len(guild_ids), 200))
		jobs = (asyncio.ensure_future(_api_call(session, f'/v2/guild/upgrades?lang={lang}&ids={page}')) for page in guild_sets)
		tasks = await asyncio.gather(*jobs)
		for p in tasks:
			for val in p:
				flags[val['id'] + GUILD_ITEM_OFFSET] = val['name']

	page = ['# Created: {} PST\n'.format(datetime.now().strftime('%Y-%m-%dT%H:%M')), 'ilist = {']
	# sorted is only so we can easily spot new items with diff
	for i in sorted(flags):  # otherwise output is semi random order
		page.append(f'\t{i}: {repr(flags[i])},')
	page.append('}\n')
	with open(f"../autogen\\items_{lang}.py", "w", encoding="utf-8") as f:
		f.write('\n'.join(page))


# generate lists guild items (Scribe) and update item ids as appropriate
def get_guild_items(recipes):
	outputs = {recipes[x]['output_item_id'] for x in recipes}
	inputs = {x['item_id'] for y in recipes for x in recipes[y]['ingredients']}
	recipe_ids = [good_recipes[recipe] for recipe in good_recipes]
	# needs to be str since we will be using join later to create urls
	item_ids = [str(x) for x in list(inputs | outputs) + recipe_ids]

	guild_ids = []
	for item in recipes:
		if 'Scribe' in recipes[item]['disciplines']:
			if "guild_ingredients" in recipes[item]:
				for i in recipes[item]['guild_ingredients']:
					if i['upgrade_id'] not in guild_ids:
						guild_ids.append(str(i['upgrade_id']))
					recipes[item]['ingredients'].append({"count": i['count'], "item_id": i['upgrade_id'] + GUILD_ITEM_OFFSET})
			if 'output_upgrade_id' in recipes[item]:
				if recipes[item]['output_upgrade_id'] not in guild_ids:
					guild_ids.append(str(recipes[item]['output_upgrade_id']))
				recipes[item]['output_item_id'] = recipes[item]['output_upgrade_id'] + GUILD_ITEM_OFFSET
	return item_ids, guild_ids


# merge guild items in to item list now that we have finished preprocessing
def merge_items_guild(items, guild):
	for item in list(guild.keys()):
		items[item + GUILD_ITEM_OFFSET] = {'name': guild[item]["name"], "icon": guild[item]["icon"], 'rarity': "Basic", 'flags': ["NoSell"], "vendor_value": 0, 'type': guild[item]['type']}


async def main():
	api_root = "https://api.guildwars2.com"
	async with aiohttp.ClientSession(api_root) as session:
		recipes = await get_recipes(session)
		item_ids, guild_ids = get_guild_items(recipes)
		items = await get_items(session, item_ids)
		guild = await get_guild(session, guild_ids)

		validate_data(recipes, items, guild)
		merge_items_guild(items, guild)
		write_recipes(recipes, items)

		for lang in ['en', 'de', 'es', 'fr']:  # , 'zh']:
			await itemlist(items, guild, session, lang)


# If ran directly, call main
if __name__ == '__main__':
	# Special exception for windows.
	if (4, 0, 0) > sys.version_info >= (3, 8, 0) and sys.platform.startswith('win'):
		asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
	asyncio.run(main())
