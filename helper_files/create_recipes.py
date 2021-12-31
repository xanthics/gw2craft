import asyncio
import sys
import aiohttp
import json
from datetime import datetime
from pyrate_limiter import *


# Special exception for windows.
if sys.version_info[0] == 3 and sys.version_info[1] >= 8 and sys.platform.startswith('win'):
	asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


# api request limit.  stored in a queue.Queue
limiter = Limiter(RequestRate(600, Duration.MINUTE))


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
	bad_karma_items = [
		19717,  # Sun Bead
		38014,  # Vial of Condensed Mists Essence
		38024,  # Shard of Crystallized Mists Essence
		43772,  # Charged Quartz Crystal
		46731,  # Pile of Bloodstone Dust
		46733,  # Dragonite Ore
		46735,  # Empyreal Fragment
		50025,  # Blade Shard
		66636,  # Ambrite Fossilized Centipede
		66640,  # Ambrite Fossilized Butterfly
		66642,  # Ambrite Fossilized Termite
		66644,  # Ambrite Fossilized Firefly
		66645,  # Ambrite Fossilized Millipede
		66646,  # Ambrite Fossilized Dragonfly
		66647,  # Ambrite Fossilized Grub
		66648,  # Ambrite Fossilized Hornet
		66649,  # Ambrite Fossilized Cricket
		66651,  # Ambrite Fossilized Spider
		66652,  # Ambrite Fossilized Cockroach
		66653,  # Ambrite Fossilized Beetle
		66654,  # Ambrite Fossilized Devourer
		66655,  # Ambrite Fossilized Bee
		66656,  # Ambrite Fossilized Mosquito
		66657,  # Ambrite Fossilized Mantis
		69392,  # Ley Line Spark
		69432,  # Pile of Auric Dust
		70447,  # Frog's Breath
		70493,  # Essence of Prey
		70537,  # Bauxite Ore
		70629,  # Uzolan's Notes
		70647,  # Crystalline Bottle
		70658,  # Essence of Natural Protection
		70718,  # Tenebrous Crystal
		70730,  # Essence of Ancient Knowledge
		70763,  # Spirit of the Chaos Gun Experiment
		70861,  # Jar of Wurmswort
		70940,  # Raw Honey
		70956,  # Nickel Ore
		71036,  # Essence of Fish
		71137,  # Infinitely Spiraled Device
		71201,  # Boar Bristle
		71203,  # Spirit of the Spark Experiment
		71287,  # Purple Potato
		71437,  # Essence of the Bonfire
		71446,  # Deadly Nightshade
		71671,  # Spirit of the Kudzu Experiment
		71720,  # Spirit of the Venom Experiment
		71723,  # Spirit of The Energizer Experiment
		71736,  # Vial of Manganese Dioxide
		71852,  # Essence of the End
		71873,  # Essence of Chickens and Eggs
		71908,  # Glob of Blue Ooze
		72126,  # Spirit of the Rodgort's Flame Experiment
		72154,  # Hylek Dart Poison Gland
		72337,  # Essence of Sharks
		72458,  # Spirit of Research
		72766,  # Essence of Hope
		72778,  # Spirit of The Lover Experiment
		72846,  # Essence of the Hunt
		73111,  # Essence of Villains
		73117,  # Spirit of The Bard Experiment
		73264,  # Golden Oxide Compound
		73332,  # Essence of Audacity
		73369,  # Energized Branded Crystal
		73503,  # Sabotaged Weapon Parts
		73524,  # Spirit of the Dusk Experiment
		73582,  # Mosquito Blood
		73615,  # Spirit of The Hunter Experiment
		73671,  # Essence of Dragons
		73683,  # Swift Egg
		73753,  # Essence of Blooms
		73764,  # Ley-Line Mercuric Compound
		73841,  # Spirit of the Zap Experiment
		73881,  # Michotl Tribe's Herbs
		73891,  # Spirit of the Storm Experiment
		74016,  # Nuhoch Saliva
		74032,  # Spirit of The Colossus Experiment
		74158,  # Spirit of The Device
		74237,  # Vial of Cobalt Salts
		74253,  # Fire Bug Larva
		74544,  # Essence of Industry
		74596,  # Bloomhunger Sap
		74643,  # Essence of the Colossal
		74662,  # Spirit of the Dawn Experiment
		75043,  # Essence of Tentacles
		75228,  # Essence of Love
		75232,  # Sun God's Vial
		75237,  # Spirit of the Rage Experiment
		75242,  # Egg of Darkness
		75246,  # Spirit of The Chosen Experiment
		75272,  # Black Powder
		75288,  # Glob of Yellow Ooze
		75414,  # Glob of Green Ooze
		75498,  # Pile of Beryl Dust
		75534,  # Spirit of the Tooth of Frostfang Experiment
		75535,  # Spirit of The Legend Experiment
		75555,  # Orrian Sea Urchin Roe
		75762,  # Bag of Mortar
		75769,  # Essence of Artistry
		75801,  # Essence of Meteorology
		75939,  # Essence of Technology
		75976,  # Charged Auric Particles
		75989,  # Experimental Reactor
		76006,  # Egg of Winds
		76038,  # Drop of Indigo Mushroom Milk
		76116,  # Spirit of the Ravenswood Branch
		76209,  # Zinc Ore
		76254,  # Shimmering Crystal
		76354,  # Spirit of the Carcharias Experiment
		76374,  # Glob of Red Ooze
		76523,  # Mamnoon Aloe
		76792,  # Undersea Wurm Filet
		76806,  # Essence of Concoctions
		76839,  # Milling Basin
		77026,  # Spirit of the Howl Experiment
		77190,  # Essence of Ancient Mysticism
		78324,  # Singed Griffon Feather
		78548,  # Spirit of the Hunt
		78685,  # Essence of the Hunt
		80181,  # Seraph Intricate Gossamer Insignia
		80454,  # Seraph Orichalcum Imbued Inscription
		82656,  # Elonian Matrix
		86798,  # Ascalonian Royal Iris
		86840,  # Koda's Blossom Petal
		86843,  # Shing Jea Orchid Petal
		86890,  # Krytan Spiderwort Bloom
		87153,  # Olmakhan Latigo Strap
		87289,  # Bottle of Coconut Milk
		87809,  # Plaguedoctor's Orichalcum-Imbued Inscription
		88011,  # Plaguedoctor's Intricate Gossamer Insignia
		91684,  # Rare Extract of Nourishment
		91697,  # Masterwork Extract of Nourishment
		91702,  # Pile of Powdered Gelatin Mix
		91726,  # Exotic Extract of Nourishment
		91838,  # Fine Extract of Nourishment
		92072,  # Hatched Chili
	]
	if not len(item['disciplines']) or item['type'] in ['Feast', 'Backpack'] or any(x['item_id'] in bad_karma_items for x in item['ingredients']) or (len(item['disciplines']) == 1 and item['disciplines'][0] == 'Scribe'):
		return False
	return True


# get all available recipes
async def get_recipes(session):
	# first request, getting number of pages in result
	print("Grabbing first page of recipes")
	recipes = {}
	pages, task = await _api_call(session, '/v2/recipes?page=0&page_size=200', True)
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

	items = set()
	guild = set()
	for item in recipes:
		del recipes[item]['time_to_craft_ms']
		del recipes[item]['chat_link']
		# we only care about items that can be crafted to produce xp
		if (any(x in recipes[item]['disciplines'] for x in ['Scribe', 'Jeweler']) and recipes[item]['min_rating'] < 400) or recipes[item]['min_rating'] < 500:
#			if 'LearnedFromItem' in recipes[item]['flags']:
#				print(recipes[item])
			items.add(str(item))
			items.add(str(recipes[item]['output_item_id']))
			for i in recipes[item]['ingredients']:
				items.add(str(i['item_id']))

			if 'Scribe' in recipes[item]['disciplines']:
				if "guild_ingredients" in recipes[item]:
					for i in recipes[item]['guild_ingredients']:
						guild.add(str(i['upgrade_id']))
						recipes[item]['ingredients'].append({"count": i['count'], "item_id": i['upgrade_id']+1000000})
				if 'output_upgrade_id' in recipes[item]:
					guild.add(str(recipes[item]['output_upgrade_id']))
					recipes[item]['output_item_id'] = recipes[item]['output_upgrade_id'] + 1000000
#	exit()
	return items, guild, recipes


# TODO: create recipe snippets for all items that includes min/max crafting xp levels
# Get the recipes we want and put them in recipe sheets while also gathering all the item_id we need
def parse_recipes(recipes):
	pass


# get more information on every item the recipes use
# Currently supported languages: en, fr, de, es, zh
async def itemlist(recipes, items, guild, session, lang="en"):
	print(f"Starting {lang} with {len(items)} items and {len(guild)} guild items")

	guild_flags = {}
	guild_sets = [','.join(guild[i:i+200]) for i in range(0, len(guild), 200)]
	jobs = [asyncio.ensure_future(_api_call(session, f'/v2/guild/upgrades?lang={lang}&ids={page}')) for page in guild_sets]
	tasks = await asyncio.gather(*jobs)
	for p in tasks:
		for val in p:
			guild_flags[val['id']] = val

	item_flags = {}
	item_sets = [','.join(items[i:i+200]) for i in range(0, len(items), 200)]
	jobs = [asyncio.ensure_future(_api_call(session, f'/v2/items?lang={lang}&ids={page}')) for page in item_sets]
	tasks = await asyncio.gather(*jobs)
	for p in tasks:
		for val in p:
			item_flags[val['id']] = val

	for flag in guild_flags:
		item_flags[flag+1000000] = {'name': guild_flags[flag]["name"], "icon": guild_flags[flag]["icon"], 'rarity': "Basic", 'flags': ["NoSell"], "vendor_value": 0}

	page = '# Created: {} PST\n'.format(datetime.now().strftime('%Y-%m-%dT%H:%M:%S'))
	page += 'ilist = {\n'
	# sorted is only so we can easily spot new items with diff
	good_items = [
		# good karma items
		12137,  # Glass of Buttermilk
		12141,  # Tomato
		12145,  # Rice Ball
		12152,  # Packet of Yeast
		12159,  # Cheese Wedge
		12165,  # Apple
		12232,  # Green Bean
		12235,  # Bell Pepper
		12237,  # Black Bean
		12239,  # Kidney Bean
		12240,  # Celery Stalk
		12245,  # Basil Leaf
		12249,  # Nutmeg Seed
		12251,  # Banana
		12252,  # Lemon
		12256,  # Cumin
		12325,  # Bowl of Sour Cream
		12328,  # Ginger Root
		12337,  # Almond
		12338,  # Cherry
		12339,  # Lime
		12340,  # Avocado
		12350,  # Coconut
		12502,  # Eggplant
		12503,  # Peach
		12514,  # Pear
		12515,  # Chickpea
		12516,  # Pinenut
		12517,  # Shallot
		12518,  # Horseradish Root
		12543,  # Mango
	]

	# Recipes learned from Master Craftsmen that we still want to consider
	# key is item_id
	good_recipes = [
		9819, 9820, 9825, 9826, 9827, 9831, 9832, 9834, 9835, 9839, 9840, 9843, 9847, 9848, 9849, 9851, 9853, 9854, 9855, 9856, 9857, 9858, 9863, 9864,
		9865, 9868, 9869, 9872, 9874, 9876, 9878, 9879, 9881, 9883, 9884, 9886, 9887, 9888, 9890, 9891, 9896, 9897, 9898, 9899, 9900, 9901, 9902, 9903,
		9905, 9909, 9912, 9916, 9921
	]

	outputs = [recipes[x]['output_item_id'] for x in recipes]
	inputs = [x['item_id'] for y in recipes for x in recipes[y]['ingredients']]
	for i in sorted(item_flags):  # otherwise output is semi random order
		# this section validates fetched items against patterns that are commonly "bad items"
		if i not in good_items and 'AccountBound' in item_flags[i]['flags'] and item_flags[i]['type'] in ['CraftingMaterial'] and i not in outputs:
			print(f'\t\t{i},  # {item_flags[i]["name"]}')
			continue
		if 'game_types' not in item_flags[i] or not any(x in item_flags[i]['game_types'] for x in ['Pve', 'Dungeon', 'Wvw']):
			continue
		if 'AccountBound' in item_flags[i]['flags'] and i not in outputs and i not in inputs and i not in good_recipes:
			continue
		try:
			page += "\t{}: \"{}\",\n".format(i, item_flags[i]['name'].replace('"', '\'').strip())
		except Exception as err:
			print('Error items: {}.\n'.format(str(err)))
	page += '}'
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


# TODO: rewrite to use json to store intermediary states
async def main():
	api_root = "https://api.guildwars2.com"
	async with aiohttp.ClientSession(api_root) as session:
		items, guild, recipes = await get_recipes(session)
		#parse_recipes()

		await itemlist(recipes, list(items), list(guild), session)
		#await itemlist(item_list, gulist, "fr")
		#await itemlist(item_list, gulist, "de")
		#await itemlist(item_list, gulist, "es")
		#await itemlist(item_list, gulist, "zh")
		#gen_multi_tracker()


# If ran directly, call main
if __name__ == '__main__':
	asyncio.run(main())
