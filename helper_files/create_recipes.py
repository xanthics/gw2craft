import asyncio
import sys
import aiohttp
from datetime import datetime
from pyrate_limiter import *
import pickle


# Special exception for windows.
if (4, 0, 0) > sys.version_info >= (3, 8, 0) and sys.platform.startswith('win'):
	asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


# api request limit.  stored in a queue.Queue
limiter = Limiter(RequestRate(20, Duration.SECOND), RequestRate(600, Duration.MINUTE))


@limiter.ratelimit('api', delay=True, max_delay=120)
async def _api_call(session, endpoint, first=False):
	print(f"Running: {endpoint[:100]}")
	async with session.get(endpoint) as req:
		reply = await req.json()
		if req.status not in [200, 206]:
			raise Exception('API response: {} {}'.format(req.status, req.content))
		if first:
			return int(req.headers['x-page-total']), reply
		return reply


# check that a recipe is one we care about
def validate_recipe(item):
	# if the recipe doesn't have a discipline, is a feast or back, is a 400+ scribe/jeweler only recipe, or is 500+, ignore it.
	if not len(item['disciplines']) or item['type'] in ['Feast', 'Backpack'] or (all(x in ['Scribe', 'Jeweler'] for x in item['disciplines']) and item['min_rating'] >= 400) or item['min_rating'] >= 500:
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
	jobs = [asyncio.ensure_future(_api_call(session, f'/v2/recipes?page={page}&page_size=200')) for page in range(1, pages)]
	# get the rest of the recipes
	tasks = await asyncio.gather(*jobs)

	for p in tasks:
		for val in p:
			if validate_recipe(val):
				recipes[val['id']] = val

	return recipes


# get all available items
async def get_items(session):
	# first request, getting number of pages in result
	print("Grabbing first page")
	items = {}
	pages, task = await _api_call(session, '/v2/items?page=0&page_size=200', True)
	print(f"{pages} items")
	for val in task:
		items[val['id']] = val
	jobs = [asyncio.ensure_future(_api_call(session, f'/v2/items?page={page}&page_size=200')) for page in range(1, pages)]
	# get the rest of the recipes
	tasks = await asyncio.gather(*jobs)

	for p in tasks:
		for val in p:
			items[val['id']] = val

	return items


# get all available recipes
async def get_guild(session):
	# first request, getting number of pages in result
	print("Grabbing first page")
	guild_items = {}
	pages, task = await _api_call(session, '/v2/guild/upgrades?page=0&page_size=200', True)
	print(f"{pages} guild items")
	for val in task:
		guild_items[val['id']] = val
	jobs = [asyncio.ensure_future(_api_call(session, f'/v2/guild/upgrades?page={page}&page_size=200')) for page in range(1, pages)]
	# get the rest of the recipes
	tasks = await asyncio.gather(*jobs)

	for p in tasks:
		for val in p:
			guild_items[val['id']] = val

	return guild_items


# TODO: create recipe snippets for all items that includes min/max crafting xp levels
# Get the recipes we want and put them in recipe sheets while also gathering all the item_id we need
def parse_recipes(recipes):
	pass


# Allow list learned recipes, and make sure that recipes/etc only contain valid items
def validate_data(recipes, items, guild):
	clean_items(recipes, items)
	outputs = {recipes[x]['output_item_id'] for x in recipes}
	inputs = {x['item_id'] for y in recipes for x in recipes[y]['ingredients']}

	print(len(items))
	for item in list(items.keys()):
		if item not in outputs | inputs and not ('details' in items[item] and 'recipe_id' in items[item]['details'] and items[item]['details']['recipe_id'] in recipes):
			del items[item]
	for item in list(items.keys()):
		if 'details' in items[item] and 'recipe_id' in items[item]['details'] and items[item]['details']['recipe_id'] in recipes:
			print(items[item])
	print(len(items))


# removes invalid items and recipes based on rules and allow lists
def clean_items(recipes, items):
	removed = True
	# account bound ingredients that are considered "good".  Mostly used in cooking with renown hearts
	good_items = {
		# Master Chefs
		12245,  # Basil Leaf
		12235,  # Bell Pepper
		12137,  # Glass of Buttermilk
		12159,  # Cheese Wedge
		12328,  # Ginger Root
		12145,  # Rice Ball
		12325,  # Bowl of Sour Cream
		12141,  # Tomato
		12152,  # Packet of Yeast
		# Renown Heart NPCs
		12337,  # Almond
		12165,  # Apple
		12340,  # Avocado
		12251,  # Banana
		12237,  # Black Bean
		12240,  # Celery Stalk
		12338,  # Cherry
		12515,  # Chickpea
		12350,  # Coconut
		12256,  # Cumin
		12502,  # Eggplant
		12232,  # Green Bean
		12518,  # Horseradish Root
		12239,  # Kidney Bean
		12252,  # Lemon
		12339,  # Lime
		12249,  # Nutmeg Seed
		12503,  # Peach
		12514,  # Pear
		12516,  # Pinenut
		12517,  # Shallot
		# Karma Merchants
		12543,  # Mango
	}
	while removed:
		removed = False
		outputs = {recipes[x]['output_item_id'] for x in recipes}
		bound_items = set()
		for recipe in sorted(recipes):
			for x in recipes[recipe]['ingredients']:
				if x['item_id'] < 99999999 and 'AccountBound' in items[x['item_id']]['flags'] and x['item_id'] not in outputs | good_items:
					if recipes[recipe]['output_item_id'] < 99999999:
						bound_items.add(recipes[recipe]['output_item_id'])
					removed = True
					del recipes[recipe]
					break


# get more information on every item the recipes use
# Currently supported languages: en, fr, de, es, zh
async def itemlist(recipes, items, guild, session, lang="en"):
	print(f"Starting {lang} with {len(items)} items and {len(guild)} guild items")

	item_flags = {}
	item_sets = [','.join(items[i:i+200]) for i in range(0, len(items), 200)]
	jobs = [asyncio.ensure_future(_api_call(session, f'/v2/items?lang={lang}&ids={page}')) for page in item_sets]
	tasks = await asyncio.gather(*jobs)
	for p in tasks:
		for val in p:
			if any(x in val['game_types'] for x in ['Wvw', 'Dungeon', 'Pve']):
				item_flags[val['id']] = val

	clean_items(recipes, item_flags)

	guild_flags = {}
	guild_sets = [','.join(guild[i:i+200]) for i in range(0, len(guild), 200)]
	jobs = [asyncio.ensure_future(_api_call(session, f'/v2/guild/upgrades?lang={lang}&ids={page}')) for page in guild_sets]
	tasks = await asyncio.gather(*jobs)
	for p in tasks:
		for val in p:
			guild_flags[val['id']] = val
	for flag in guild_flags:
		item_flags[flag+99999999] = {'name': guild_flags[flag]["name"], "icon": guild_flags[flag]["icon"], 'rarity': "Basic", 'flags': ["NoSell"], "vendor_value": 0}

	page = f'# Created: {datetime.now().strftime("%Y-%m-%dT%H:%M")} PST\n'
	page += 'ilist = {\n'

	for i in sorted(item_flags):  # otherwise output is semi random order
		try:
			name = item_flags[i]['name'].replace('"', '\'').strip()
			page += f"\t{i}: \"{name}\",\n"
		except Exception as err:
			print('Error items: {}.\n'.format(str(err)))
	page += '}\n'
	with open(f"..\\auto_gen\\Items_{lang}.py", "w") as f:
		f.write(page)


# generate lists guild items (Scribe) and update item ids as appropriate
def get_guild_items(recipes):
	gulist = []
	for item in recipes:
		if 'Scribe' in recipes[item]['disciplines'] and recipes[item]['min_rating'] < 400:
			if "guild_ingredients" in recipes[item]:
				for i in recipes[item]['guild_ingredients']:
					if i['upgrade_id'] not in gulist:
						gulist.append(i['upgrade_id'])
					recipes[item]['ingredients'].append({"count": i['count'], "item_id": i['upgrade_id']+1000000})
			if 'output_upgrade_id' in recipes[item]:
				if recipes[item]['output_upgrade_id'] not in gulist:
					gulist.append(recipes[item]['output_upgrade_id'])
				recipes[item]['output_item_id'] = recipes[item]['output_upgrade_id'] + 1000000
	return gulist


# update recipe lists to have the name of their output item
def gen_multi_tracker():
	pass


async def main():
	api_root = "https://api.guildwars2.com"
	async with aiohttp.ClientSession(api_root) as session:
		#  load/dump code is temporary while validation code is finalized
#		recipes = await get_recipes(session)
#		items = await get_items(session)
#		guild = await get_guild(session)
#		with open('recipes.pickle', 'wb') as f:
#			pickle.dump(recipes, f)
#		with open('items.pickle', 'wb') as f:
#			pickle.dump(items, f)
#		with open('guild.pickle', 'wb') as f:
#			pickle.dump(guild, f)
		with open('recipes.pickle', 'rb') as f:
			recipes = pickle.load(f)
		with open('items.pickle', 'rb') as f:
			items = pickle.load(f)
		with open('guild.pickle', 'rb') as f:
			guild = pickle.load(f)
		validate_data(recipes, items, guild)

# If ran directly, call main
if __name__ == '__main__':
	asyncio.run(main())
