#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
* Copyright (c) 2013 Jeremy Parks. All rights reserved.
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
Note: Requires Python 2.7.x
'''
import urllib, json, math, codecs, socket
from multiprocessing import Process, Queue, cpu_count

API_ROOT = u"https://api.guildwars2.com/v2/"

# Helper Function
def recipelistWorker(items, out_q):
	outdict = {}

	items = _api_call(u'recipes.json?ids={}'.format(",".join(map(str,items))))
	for i in items:
		outdict[i[u'id']] = i

	out_q.put(outdict)

# Get and return all available recipes from the API
def get_recipes():
	lister = _api_call(u'recipes.json')	
	out_q = Queue()
	chunksize = 200
	nprocs = int(math.ceil(len(lister)/chunksize))+1
	procs = []

	for i in range(nprocs):
		p = Process(target=recipelistWorker,
					args=(lister[chunksize * i:chunksize * (i + 1)],out_q))
		procs.append(p)
		p.start()

	flags = {}
	for i in range(nprocs):
		flags.update(out_q.get())

	for p in procs:
		p.join()

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
	bad_karma = [19717, 19925, 45175, 45176, 45177, 45178]

	crafts = {u'Weaponsmith':{}, u'Chef':{}, u'Chef_karma':{}, u'Huntsman':{},
			  u'Armorsmith':{}, u'Jeweler':{}, u'Artificer':{}, u'Tailor':{},
			  u'Leatherworker':{}}
	item_ids = {}

	new_recipes = {r[0]:r[1] for r in recipes.items()
				   if not int(r[1][u'output_item_id']) in bad_recipes
				   and not r[1][u'type'] in [u'Feast',u'Backpack']}

	for _recipe, data in new_recipes.items():
		min_rating = data[u'min_rating']
		item_id = data[u'output_item_id']
		item_count = data[u'output_item_count']
		ingredient_set = set(int(i[u'item_id']) for i in data[u'ingredients'])

		# We don't want cap level recipes or recipes that use items the player can't buy off the tp or make
		if min_rating == 500 or (min_rating == 400 and u'Chef' in data[u'disciplines']) or set(bad_karma).intersection(set(ingredient_set)):
			continue
			
		for it in data[u'disciplines']:
			key = it
			# We don't want recipe items.  Except for karma cooking and known good recipes
			if u'LearnedFromItem' in data[u'flags'] and not (it == u'Chef' or int(item_id) in good_recipes):
				continue
			if it == u'Chef' and (set(karma) & ingredient_set or u'LearnedFromItem' in data[u'flags']):
				key = u'Chef_karma'

			crafts[key].setdefault(min_rating, {})
			crafts[key][min_rating][item_id] = data[u'ingredients']
			item_ids[item_id] = {u'output_item_count': item_count,
								 u'type': data[u'type'],
								 u'flags': data[u'flags']}


	for craft in crafts:
		page = u'# -*- coding: utf-8 -*-\nrecipes = {\n'
		for lvl in sorted(crafts[craft]):
			page += u"\t{}:{{\n".format(lvl)
			for obj in sorted(crafts[craft][lvl]):
				mystr = u""
				for part in sorted(crafts[craft][lvl][obj]):
					if not part[u'item_id'] in item_ids:
						item_ids[part[u'item_id']] = {u'type':u'Other',u'output_item_count':u'0',u'flags':[]}
					mystr += u"{}:{},".format(part[u'item_id'],part[u'count'])
				page += u"\t\t{}:{{{}}},\n".format(obj,mystr[:-1])
			page += u"\t},\n"
		page += u"}"
		with codecs.open(craft+".py", "wb", encoding='utf-8') as f:
			f.write(page)

	for item in [38207, 38208, 38209, 38295, 38296, 38297]:
		item_ids[item] = {u'type':u'Recipe',u'output_item_count':u'1',u'flags':[]}

	return item_ids

# helper function
def itemlistWorker(ids, lang, out_q):
	outdict = {}
	items = _api_call(u'items.json?ids={}&lang={}'.format(",".join(map(str,ids)), lang))
	for i in items:
		outdict[i[u'id']] = i
	out_q.put(outdict)

# get more information on every item the recipes use
# Currently supported languages: en, fr, de, es
def itemlist(item_list, lang=u"en"):
	print "Starting {}".format(lang)
	out_q = Queue()
	lister = item_list.keys()
	chunksize = 200
	nprocs = int(math.ceil(len(lister)/chunksize))+1
	procs = []
	for i in range(nprocs):
		p = Process(target=itemlistWorker,
					args=(lister[chunksize * i:chunksize * (i + 1)], lang, out_q))
		procs.append(p)
		p.start()

	flags = {}
	for i in range(nprocs):
		flags.update(out_q.get())

	for p in procs:
		p.join()

	if lang == u"en":
		page = u'# -*- coding: utf-8 -*-\nilist = {\n'
		# sorted is only so we can easily spot new items with diff
		for i in sorted(flags): # otherwise output is semi random order
			try:
				item_list[i][u'rarity'] = flags[i][u'rarity']
				if u"NoSell" in flags[i][u"flags"]:
					item_list[i][u'vendor_value'] = 0
				else:
					item_list[i][u'vendor_value'] = int(flags[i][u'vendor_value'])
				if item_list[i][u'flags']:
					item_list[i][u'discover'] = 0
				item_list[i][u'img_url'] = flags[i][u'icon']
				del(item_list[i][u'flags'])
				page += u"\t{}:{},\n".format(i, item_list[i])
			except Exception, err:
				print 'Error: {}.\n'.format(str(err))
		page += u'}'
		with codecs.open("Items.py","wb", encoding='utf-8') as f:
			f.write(page.replace(u": ", ":"))

	page = u'# -*- coding: utf-8 -*-\nilist = {\n'
	# sorted is only so we can easily spot new items with diff
	for i in sorted(flags): # otherwise output is semi random order
		try:
			page += u"\t{}:u\"{}\",\n".format(i, flags[i][u'name'].replace('"','\''))
		except Exception, err:
			print 'Error: {}.\n'.format(str(err))
	page += u'}'
	with codecs.open("Items_%s.py" % lang,"wb", encoding='utf-8') as f:
		f.write(page)

def _api_call(endpoint):
	while(1):
		try:
			f = urllib.urlopen(API_ROOT + endpoint)
			item = json.load(f)
			return item
		except Exception, err:
			print 'Error: {}.\n'.format(str(err))

	
def main():
	socket.setdefaulttimeout(15)
	recipes = get_recipes()
	item_list = parse_recipes(recipes)
	itemlist(item_list)
	itemlist(item_list, u"fr")
	itemlist(item_list, u"de")
	itemlist(item_list, u"es")

# If ran directly, call main
if __name__ == '__main__':
	main()
