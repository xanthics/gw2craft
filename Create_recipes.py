#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
* Copyright (c) 2013-2016 Jeremy Parks. All rights reserved.
*
* Permission is hereby granted, free of charge, to any person obtaining a
* copy of this software and associated documentation files (the "Software"),
* to deal in the Software without restriction, including without limitation
* the rights to use, copy, modify, merge, publish, distribute, sublicense,
* and/or sell copies of the Software, and to permit persons to whom the
* Software is furnished to do so, subject to the following conditions:
*
* The above copyright notice and this permission notice shall be included in
* all copies or substantial portions of the Software.
*
* THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
* IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
* FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
* AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
* LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
* FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
* DEALINGS IN THE SOFTWARE.

Author: Jeremy Parks
Purpose: Generates(or updates) all the recipes and the item list used by Crafting.py
Note: Requires Python 3.7.x
'''
import codecs
import json
import os
import socket
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime
from multiprocessing import Pool

API_ROOT = "https://api.guildwars2.com/v2/"


# Helper Function
def recipelistWorker(items):
	outdict = {}
	items = _api_call('recipes.json?ids={}'.format(",".join(map(str, items))))
	for i in items:
		outdict[i['id']] = i

	return outdict


# Get and return all available recipes from the API
def get_recipes():
	lister = _api_call('recipes.json')
	p = Pool()
	procs = [p.map(recipelistWorker, [lister[i:i + 200] for i in range(0, len(lister), 200)])]

	flags = {}
	for p in procs:
		for i in p:
			flags.update(i)

	return flags


# Get the recipes we want and put them in recipe sheets while also gathering
# all the item_id we need
def parse_recipes(recipes):
	# Karma items so cooking lists are built properly
	# key is item_id
	karma = [12165, 12232, 12237, 12239, 12240, 12249, 12251, 12252, 12256,
			 12337, 12338, 12339, 12340, 12350, 12502, 12503, 12514, 12515,
			 12516, 12517, 12518, 12543]

	# These recipes have to be purchased from AH, therefore we don't want them
	# Glazed Peach Tart[s], Glazed Pear Tart[s], Piece[s] of Candy Corn Almond
	# Brittle, Strawberry Ghost[s], Bowl[s] of Candy Corn Custard
	# key is item_id
	bad_recipes = [36081, 36080, 36077, 36076, 36074]

	# Recipes learned from Master Craftsmen that we still want to consider
	# key is item_id
	# 38162, 38166, 38167, 38434, 38432, 38433 are giver recipes
	good_recipes = [19880, 19881, 19882, 19883, 19884, 19885, 19886, 19897,
					19898, 19899, 19900, 19901, 19902, 19903, 19934, 19935,
					19936, 19937, 19938, 19939, 19940, 19941, 19942, 19943,
					19944, 19945, 19946, 19947, 19948, 19949, 19950, 19951,
					19952, 19953, 19954, 19955, 19956, 19957, 19958, 19959,
					19960, 19961, 19962, 19963, 19964, 19965, 19966, 19967,
					19968, 19969, 19970, 19971, 19972, 19973, 19974, 19975,
					24899, 24900, 24901, 24902, 24903, 24904, 24905, 24906,
					24907, 24908, 24909, 24910, 24911, 24912, 24913, 24914,
					24915, 24916, 24917, 24919, 24920, 24921, 24922, 24923,
					24924, 24898, 24918, 24925, 19923, 19920, 19917, 19918,
					19922, 19921, 19919, 38162, 38166, 38167, 38434, 38432,
					38433, 19912, 19913, 19910, 19911, 19915, 19914, 19916,
					24543, 24496, 24544, 24497, 24545, 24498, 24499]

	# Karma and account bound items that we don't want to save the recipe of items that use
	# Sun Beads, Obsidian Shard, Essence of Luck, Essence of Luck, Essence of Luck, Essence of Luck, Essence of Luck
	bad_karma = [19717, 19925, 45175, 45176, 45177, 45178, 1000721] + list(range(49424, 49441))

	crafts = {'Weaponsmith': {}, 'Chef': {}, 'Chef_karma': {}, 'Huntsman': {},
			  'Armorsmith': {}, 'Jeweler': {}, 'Artificer': {}, 'Tailor': {},
			  'Leatherworker': {}, 'Scribe': {}}
	item_ids = {}

	new_recipes = {r[0]: r[1] for r in list(recipes.items())
				   if not int(r[1]['output_item_id']) in bad_recipes
				   and not r[1]['type'] in ['Feast', 'Backpack']
				   or (r[1]['type'] == 'Backpack' and 'Scribe' in r[1]['disciplines'])}
	nc = {}
	for _recipe, data in list(new_recipes.items()):
		min_rating = data['min_rating']
		item_id = data['output_item_id']
		item_count = data['output_item_count']
		ingredient_set = set(int(i['item_id']) for i in data['ingredients'])

		# We don't want cap level recipes or recipes that use items the player can't buy off the tp or make
		# 24838 at lvl 375 is a bugged recipe(Major Rune of Water, Tailoring)
		if min_rating == 500 or (min_rating == 400 and ('Scribe' in data['disciplines'] or 'Jeweler' in data['disciplines'])) or set(bad_karma).intersection(set(ingredient_set)):  # or (item_id == 24838 and min_rating == 375):
			continue

		for it in data['disciplines']:
			key = it
			# We don't want recipe items.  Except for karma cooking and known good recipes
			if 'LearnedFromItem' in data['flags'] and not (it == 'Chef' or int(item_id) in good_recipes):
				continue
			if it == 'Chef' and (set(karma) & ingredient_set or 'LearnedFromItem' in data['flags']):
				key = 'Chef_karma'

			crafts[key].setdefault(min_rating, {})
			crafts[key][min_rating][item_id] = data['ingredients']
			item_ids[item_id] = {'output_item_count': item_count,
								 'type': data['type'],
								 'flags': data['flags']}
			if it in nc:
				nc[it] += 1
			else:
				nc[it] = 1
	import auto_gen.Items_en as ige
	for craft in crafts:
		page = '# -*- coding: utf-8 -*-\n'
		page += '# Created: {} PST\n'.format(datetime.now().strftime('%Y-%m-%dT%H:%M:%S'))
		page += 'recipes = {\n'
		for lvl in sorted(crafts[craft]):
			page += "\t{}: {{\n".format(lvl)
			for obj in sorted(crafts[craft][lvl]):
				mystr = ""
				for part in sorted(crafts[craft][lvl][obj], key=lambda k: k['item_id']):
					if not part['item_id'] in item_ids:
						item_ids[part['item_id']] = {'type': 'Other', 'output_item_count': 0, 'flags': []}
					mystr += "{}: {}, ".format(part['item_id'], part['count'])
				page += "\t\t{}: {{{}}},  # {}\n".format(obj, mystr[:-2], ige.ilist[obj])
			page += "\t},\n"
		page += "}"
		with codecs.open("auto_gen\\" + craft + ".py", "wb", encoding='utf-8') as f:
			f.write(page)

	for item in [38207, 38208, 38209, 38295, 38296, 38297]:
		item_ids[item] = {'type': 'Recipe', 'output_item_count': 1, 'flags': []}

	return item_ids


# helper function
def guilditemlistWorker(vals):
	ids = vals[0]
	lang = vals[1]
	outdict = {}
	items = _api_call('guild/upgrades.json?ids={}&lang={}'.format(",".join(map(str, ids)), lang))
	for i in items:
		outdict[i['id']] = i
	return outdict


# helper function
def itemlistWorker(vals):
	ids = vals[0]
	lang = vals[1]
	outdict = {}
	items = _api_call('items.json?ids={}&lang={}'.format(",".join(map(str, ids)), lang))
	for i in items:
		outdict[i['id']] = i
	return outdict


# get more information on every item the recipes use
# Currently supported languages: en, fr, de, es
def itemlist(item_list, gulist, lang="en"):
	print("Starting {}".format(lang))
	lister = gulist
	p = Pool()
	procs = [p.map(guilditemlistWorker, [(lister[i:i + 200], lang) for i in range(0, len(lister), 200)])]

	guild_flags = {}
	for p in procs:
		for i in p:
			guild_flags.update(i)

	lister = list(item_list.keys())
	p = Pool()
	procs = [p.map(itemlistWorker, [(lister[i:i + 200], lang) for i in range(0, len(lister), 200)])]

	flags = {}
	for p in procs:
		for i in p:
			flags.update(i)

	for item in list(guild_flags.keys()):
		flags[item+1000000] = {'name': guild_flags[item]["name"], "icon": guild_flags[item]["icon"],
							   'rarity': "Basic", 'flags': ["NoSell"], "vendor_value": 0}

	if lang == "en":
		page = '# -*- coding: utf-8 -*-\n'
		page += '# Created: {} PST\n'.format(datetime.now().strftime('%Y-%m-%dT%H:%M:%S'))
		page += 'ilist = {\n'
		# sorted is only so we can easily spot new items with diff
		for i in sorted(flags):  # otherwise output is semi random order
			try:
				item_list[i]['rarity'] = flags[i]['rarity']
				if "NoSell" in flags[i]["flags"]:
					item_list[i]['vendor_value'] = 0
				else:
					item_list[i]['vendor_value'] = int(flags[i]['vendor_value'])
				if item_list[i]['flags']:
					item_list[i]['discover'] = 0
				item_list[i]['img_url'] = flags[i]['icon']
				del (item_list[i]['flags'])
				page += "\t{}: {},\n".format(i, item_list[i])
			except Exception as err:
				print('Error ilist: {}.'.format(str(err)))
				#exit()
		page += '}'
		with codecs.open("auto_gen\\Items.py", "wb", encoding='utf-8') as f:
			f.write(page.replace(": ", ":"))

	page = '# -*- coding: utf-8 -*-\n'
	page += '# Created: {} PST\n'.format(datetime.now().strftime('%Y-%m-%dT%H:%M:%S'))
	page += 'ilist = {\n'
	# sorted is only so we can easily spot new items with diff
	for i in sorted(flags):  # otherwise output is semi random order
		try:
			page += "\t{}: \"{}\",\n".format(i, flags[i]['name'].replace('"', '\'').strip())
		except Exception as err:
			print('Error items: {}.\n'.format(str(err)))
	page += '}'
	with codecs.open("auto_gen\\Items_%s.py" % lang, "wb", encoding='utf-8') as f:
		f.write(page)


def _api_call(endpoint):
	while (1):
		try:
			f = urllib.request.urlopen(API_ROOT + endpoint)
			item = json.load(f)
			return item
		except Exception as err:
			print('Error api: {}. at {}\n'.format(str(err), API_ROOT + endpoint))


# add guild_ingredient item_id to each item
def guild_recipes(recipes):
	gulist = []
	for item in list(recipes.keys()):
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
	return gulist, recipes


def gen_multi_tracker():
	# importing now (local) as they are created with earlier code and not needed until now
	from auto_gen import Items, Armorsmith, Artificer, Chef, Chef_karma, Huntsman, Jeweler, Leatherworker, Scribe, Tailor, Weaponsmith

	# Generate a set of recipes with multiple outputs that are used by other recipes
	multi_items = {}
	for craft in [Armorsmith, Artificer, Chef, Chef_karma, Huntsman, Jeweler, Leatherworker, Scribe, Tailor, Weaponsmith]:
		for tier in craft.recipes:
			for item in craft.recipes[tier]:
				for mat in craft.recipes[tier][item]:
					if Items.ilist[mat]['output_item_count'] > 1:
						multi_items[mat] = Items.ilist[mat]['output_item_count']
						craft.recipes[tier][item][mat] /= Items.ilist[mat]['output_item_count']

	page = ['# -*- coding: utf-8 -*-', '# Created: {} PST\n'.format(datetime.now().strftime('%Y-%m-%dT%H:%M:%S')), 'ilist = {']
	# sorted is only so we can easily spot new items with diff
	for item in sorted(multi_items):
		page.append(f'\t{item}: {multi_items[item]},')
	page.append('}\n')
	with codecs.open("auto_gen\\mod_recipes.py", "wb", encoding='utf-8') as f:
		f.write('\n'.join(page))


def main():
	os.environ['NO_PROXY'] = 'api.guildwars2.com'
	socket.setdefaulttimeout(15)
	recipes = get_recipes()
	gulist, recipes = guild_recipes(recipes)
	item_list = parse_recipes(recipes)

	itemlist(item_list, gulist)
	itemlist(item_list, gulist, "fr")
	itemlist(item_list, gulist, "de")
	itemlist(item_list, gulist, "es")
	itemlist(item_list, gulist, "zh")
	gen_multi_tracker()


# If ran directly, call main
if __name__ == '__main__':
	main()
