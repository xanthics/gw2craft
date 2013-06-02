#!/usr/bin/env python
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
Purpose: Generates a crafting guide for all crafts in Guild Wars 2 based on current market prices
Note: Requires Python 2.7.x
'''

import urllib, json, time, datetime, math, os
# recipe and item lists
import Armorsmith, Artificer, Chef, Chef_karma, Huntsman, Jeweler, Leatherworker, Tailor, Weaponsmith, items
from multiprocessing import Process, Queue
from copy import deepcopy
from collections import defaultdict
from itertools import chain
from ftplib import FTP
from random import random
# FTP Login
from ftp_info import ftp_url, ftp_user, ftp_pass

#Navigation bar for each guide and totals page
header = u"""<nav>
	<ul>
		<li><a href="http://gw2crafts.net/">Home</a></li>
		<li><a href="http://gw2crafts.net/nav.html">Normal Guides</a>
		<ul>
			<li><a href="#">Cooking</a>
			<ul>
				<li><a href="http://gw2crafts.net/cooking.html">No Hearts</a></li>
				<li><a href="http://gw2crafts.net/cooking_karma_light.html">Top 5 Hearts</a></li>
				<li><a href="http://gw2crafts.net/cooking_karma.html">All Hearts</a></li>
			</ul>
			</li>
			<li><a href="http://gw2crafts.net/jewelcraft.html">Jewelcrafting</a></li>
			<li><a href="http://gw2crafts.net/artificing.html">Artificing</a></li>
			<li><a href="http://gw2crafts.net/huntsman.html">Huntsman</a></li>
			<li><a href="http://gw2crafts.net/weaponcraft.html">Weaponcrafting</a></li>
			<li><a href="http://gw2crafts.net/armorcraft.html">Armorcrafting</a></li>
			<li><a href="http://gw2crafts.net/leatherworking.html">Leatherworking</a></li>
			<li><a href="http://gw2crafts.net/tailor.html">Tailoring</a></li>
		</ul>
		</li>
		<li><a href="http://gw2crafts.net/nav.html">Fast Guides</a>
		<ul>
			<li><a href="#">Cooking</a>
			<ul>
				<li><a href="http://gw2crafts.net/cooking_fast.html">No Hearts</a></li>
				<li><a href="http://gw2crafts.net/cooking_karma_fast_light.html">Top 5 Hearts</a></li>
				<li><a href="http://gw2crafts.net/cooking_karma_fast.html">All Hearts</a></li>
			</ul>
			</li>
			<li><a href="http://gw2crafts.net/jewelcraft_fast.html">Jewelcrafting</a></li>
			<li><a href="http://gw2crafts.net/artificing_fast.html">Artificing</a></li>
			<li><a href="http://gw2crafts.net/huntsman_fast.html">Huntsman</a></li>
			<li><a href="http://gw2crafts.net/weaponcraft_fast.html">Weaponcrafting</a></li>
			<li><a href="http://gw2crafts.net/armorcraft_fast.html">Armorcrafting</a></li>
			<li><a href="http://gw2crafts.net/leatherworking_fast.html">Leatherworking</a></li>
			<li><a href="http://gw2crafts.net/tailor_fast.html">Tailoring</a></li>
		</ul>
		</li>
		<li><a href="http://gw2crafts.net/nav.html">Traditional Guides</a>
		<ul>
			<li><a href="http://gw2crafts.net/jewelcraft_craft_all.html">Jewelcrafting</a></li>
			<li><a href="http://gw2crafts.net/artificing_craft_all.html">Artificing</a></li>
			<li><a href="http://gw2crafts.net/huntsman_craft_all.html">Huntsman</a></li>
			<li><a href="http://gw2crafts.net/weaponcraft_craft_all.html">Weaponcrafting</a></li>
			<li><a href="http://gw2crafts.net/armorcraft_craft_all.html">Armorcrafting</a></li>
			<li><a href="http://gw2crafts.net/leatherworking_craft_all.html">Leatherworking</a></li>
			<li><a href="http://gw2crafts.net/tailor_craft_all.html">Tailoring</a></li>
		</ul>
		</li>
		<li><a href="http://gw2crafts.net/total.html">Totals</a></li>
		<li><a href="http://gw2crafts.net/faq.html">About</a></li>
	</ul>
</nav>
"""

# Copyright notice for GW2 IP
cright = u'''<footer>
	Guild Wars 2 &#0169; 2012 ArenaNet, Inc. All rights reserved. NCsoft, the interlocking NC logo, ArenaNet, Guild Wars, Guild Wars Factions, Guild Wars Nightfall, Guild Wars: Eye of the North, Guild Wars 2, and all associated logos and designs are trademarks or registered trademarks of NCsoft Corporation. All other trademarks are the property of their respective owners.
</footer>'''

# helper function to get data via item_id
def search(name, people):
	return [element for element in people if name == int(element['data_id'])]

def itemlistworker(_itemList, temp, out_q):

	outdict = {}
	for item in _itemList:
		val = search(item, temp)[0]
		w = items.ilist[item][u'vendor_value']
		if val['max_offer_unit_price'] > w:
			w = val['max_offer_unit_price']
		if w == 0:
			w = val['min_sale_unit_price']
		outdict[item] = {u'w':w,u'cost':val['min_sale_unit_price'],u'recipe':None,u'rarity':items.ilist[item][u'rarity'],u'type':items.ilist[item][u'type'],u'icon':val['img'], u'name':items.ilist[item][u'name']} 
		# if the item has a low supply, ignore it
		if val['sale_availability'] <= 50:
			outdict[item][u'cost'] = 99999999
	out_q.put(outdict)

# helper function to parse out only the items we care about from gw2spidy
def cItemlist(itemList,temp):
	out_q = Queue()
	nprocs = 8

	chunksize = int(math.ceil(len(itemList) / float(nprocs)))
	procs = []

	for i in range(nprocs):
		p = Process(target=itemlistworker,args=(itemList[chunksize * i:chunksize * (i + 1)],temp,out_q))
		procs.append(p)
		p.start()

	resultdict = {}
	for i in range(nprocs):
		resultdict.update(out_q.get())

	for p in procs:
		p.join()

	return resultdict


# add some costs data to gcList
def appendCosts():
	temp = []
	# This could be in a while loop and keep trying until success, but unnecessary
	try:
		baseURL = "http://gw2spidy.com/api/v0.9/json/all-items/all"
		f = urllib.urlopen(baseURL)
		temp = json.load(f)
	except Exception, err:
		print u'ERROR: %s.\n' % str(err)
		exit(-1)

	print len(temp['results']) # print total items returned from gw2spidy

	cList = {}
	cList = cItemlist(items.ilist.keys(),temp['results'])

	cList[19792]['cost'] = 8 # Spool of Jute Thread
	cList[19789]['cost'] = 16 # Spool of Wool Thread
	cList[19794]['cost'] = 24 # Spool of Cotton Thread
	cList[19793]['cost'] = 32 # Spool of Linen Thread
	cList[19791]['cost'] = 48 # Spool of Silk Thread
	cList[19704]['cost'] = 8 # Lump of Tin
	cList[19750]['cost'] = 16 # Lump of Coal
	cList[19924]['cost'] = 48 # Lump of Primordium
	cList[12157]['cost'] = 8 # Jar of Vinegar
	cList[12151]['cost'] = 8 # Packet of Baking Powder
	cList[12158]['cost'] = 8 # Jar of Vegetable Oil
	cList[12153]['cost'] = 8 # Packet of Salt
	cList[12155]['cost'] = 8 # Bag of Sugar
	cList[12156]['cost'] = 8 # Jug of Water
	cList[12324]['cost'] = 8 # Bag of Starch
	cList[12136]['cost'] = 8 # Bag of Flour
	cList[8576]['cost'] = 16 # Bottle of Rice Wine
	cList[12271]['cost'] = 8 # Bottle of Soy Sauce
	cList[13010]['cost'] = 496 # "Minor Rune of Holding"
	cList[13006]['cost'] = 1480 # "Rune of Holding"
	cList[13007]['cost'] = 5000 # "Major Rune of Holding"
	cList[13008]['cost'] = 20000 # "Greater Rune of Holding"
	#[u'Bell Pepper',u'Basil Leaf',u'Ginger Root',u'Tomato',u'Bowl of Sour Cream',u'Rice Ball',u'Packet of Yeast',u'Glass of Buttermilk',u'Cheese Wedge',u"Almond",u"Apple",u"Avocado",u"Banana",u"Black Bean",u"Celery Stalk",u"Cherry",u"Chickpea",u"Coconut",u"Cumin",u"Eggplant",u"Green Bean",u"Horseradish Root",u"Kidney Bean",u"Lemon",u"Lime",u"Mango",u"Nutmeg Seed",u"Peach",u"Pear",u"Pinenut",u"Shallot"]
	karma = [12235,  12245,  12328,  12141,  12325,  12145,  12152,  12137,  12159,  12337,  12165,  12340,  12251,  12237,  12240,  12338,  12515,  12350,  12256,  12502,  12232,  12518,  12239,  12252,  12339,  12543,  12249,  12503,  12514,  12516,  12517]
	for item in karma:
		cList[item]['cost'] = 0
	cList[12132]['cost'] = 99999999 # Loaf of Bread is soulbound, cheat to make it not purchased

	print len(cList.keys()) # print number of items used by the guides

	return cList

# convert rarities to their xp multiplier
def rarityNum(num):
	if num == u'Rare':
		return 3.25
	elif num == u'Masterwork':
		return 2.0
	else:
		return 1.0

def xpreq(level):
	tmp = 500
	for i in range(1,level):
		tmp = math.floor(tmp * 1.01)
	return tmp

# compute the xp gain of a single craft
def xpgain(level,typ,minlvl):
	span = 0.0
	gain = 0.0
	if typ == 1: # refinement
		span = 25.0 
		mult = .3
	if typ == 2: # part
		span = 25.0 
		mult = .6
	if typ == 3: # item
		span = 40.0
		mult = 1.4
	# xp_gain(N) = xp_req(N+1) * multiplier * (1.0 - (N - N_min) / span)
	gain = xpreq(level+1) * mult * (1.0 - (level - minlvl) / span)
	if gain < 0.0 or level - minlvl == span:
		return 0.0
	return math.ceil(gain)

# compute what level would be after crafting items, assume order is refine > parts > discovery > items
def compute_level(_xp, craftlist, tlvl, xp_to_level):
	level = tlvl
	while xp_to_level[level+1] < _xp:
		level += 1
	for i in craftlist['ptitem']:
		_xp += int(i*xpgain(level,3,tlvl-25))
		while xp_to_level[level+1] < _xp:
			level += 1
	for i in range(0,int(math.ceil(craftlist['refine']))):
		_xp += int(xpgain(level,1,tlvl))
		while xp_to_level[level+1] < _xp:
			level += 1
	for i in craftlist['part']:
		_xp += int(i*xpgain(level,2,tlvl))
		while xp_to_level[level+1] < _xp:
			level += 1
	for i in craftlist['discovery']:
		_xp += int((i+1)*xpgain(level,3,tlvl))
		while xp_to_level[level+1] < _xp:
			level += 1
	for i in craftlist['item']:
		_xp += int(i*xpgain(level,3,tlvl))
		while xp_to_level[level+1] < _xp:
			level += 1
	return _xp

# calculate the total xp 
def xp_calc(refines,parts,item,discoveries,mod,base_level,actu_level):
	weight = 0.0
	weight += xpgain(actu_level,1,base_level)*refines
	weight += xpgain(actu_level,2,base_level)*parts
	weight += xpgain(actu_level,3,base_level)*item*mod
	weight += xpgain(actu_level,3,base_level)*discoveries*(1+mod)
	return weight

# Hold our 5 most popular renown heart karma items for cooking
karmin = {}

# Compute a non-cooking guide
def costCraft(filename,c_recipes,fast,ignore_mixed,cList,mytime,header,cright,xp_to_level):
	print "Start", filename
	# TODO Hack, fix this
	if 19679 in c_recipes[0]:
		c_recipes[0][19679][19697] = 2

	buttonList = [] # Buttons for discovery
	craftcount = {} # Used to track current xp per tier
	make = {} # make list per tier
	pmake = {} # make list of "prior tier" items per tier
	buy = defaultdict(int) # buy list
	sell = defaultdict(int) # sell list
	tierbuy = None # buy list per tier, not used by cooking
	tiers = [375,350,325,300,275,250,225,200,175,150,125,100,75,50,25,0]
	non_item = [u'Refinement', u'Insignia', u'Inscription', u'Component']

	# add recipes to cList
	for tier in c_recipes:
		for item in c_recipes[tier]:
			if item in cList:
				cList[item][u'recipe'] = c_recipes[tier][item]
			else: 
				print u"Missing Item from itemlist: " + item
				exit(-1)
			cList[item][u'tier'] = tier
			if u"discover" in items.ilist[item]:
				cList[item][u'discover'] = 0

	# Cooking guides don't use tierbuy, but they do care about karma items
	if "cook" in filename:
		global karmin
		if karmin: # this will be false the first time a cooking guide is called
			topl = []
			for top in sorted(karmin, key=lambda k: karmin[k], reverse=True)[:5]:
				topl.append(top)
			# "Almond","Apple","Avocado","Banana","Black Bean","Celery Stalk","Cherry","Chickpea","Coconut","Cumin","Eggplant","Green Bean","Horseradish Root","Kidney Bean","Lemon","Lime","Mango","Nutmeg Seed","Peach","Pear","Pinenut","Shallot"
			for i in [12337,  12165,  12340,  12251,  12237,  12240,  12338,  12515,  12350,  12256,  12502,  12232,  12518,  12239,  12252,  12339,  12543,  12249,  12503,  12514,  12516,  12517]:
				if not i in topl:
					cList[i]['cost'] = 99999999
	else:
		tierbuy = {0:defaultdict(int),75:defaultdict(int),150:defaultdict(int),225:defaultdict(int),300:defaultdict(int)}
		buy[19704] = 0.0 # Lump of Tin
		tierbuy[0][19704] = 0.0 # Lump of Tin

	for tier in tiers:
		make[tier] = defaultdict(int)
		pmake[tier] = defaultdict(int)
		craftcount[tier] = {'refine':0.0,'part':[],'ptitem':[],'item':[],'discovery':[],'current_xp':xp_to_level[tier]}

	tcost = 0 # total cost
	treco = 0 # total recovery
	# start at last bucket(375) and fill towards 0 bucket
	for tier in tiers:
		bucket = {}
		bkey = []
		# if this is a fast guide, choose our 1 item to craft
		if fast and (not tier == 375 or "cook" in filename):
			bucket = makeQueuecraft(c_recipes[tier], cList,craftcount,tier,ignore_mixed,xp_to_level)
			bkey = sorted(bucket, reverse=True)
			# If we already made something for cooking at this tier from another recipe, keep making that item
			if make[tier] and "cook" in filename: 
				bkey = []
				for item in bucket:
					if bucket[item][u'item_id'] == make[tier].keys()[0]:
						bkey.append(item)
						break
			else:
				while cList[bucket[bkey[0]][u'item_id']][u'type'] in non_item:
					bkey.pop(0)

		while compute_level(xp_to_level[tier], craftcount[tier],tier,xp_to_level) < xp_to_level[tier + 25]:
			if not tier == 0:
				if not compute_level(craftcount[tier-25]['current_xp'], craftcount[tier],tier,xp_to_level) < xp_to_level[tier + 25]:
					break
			if fast and tier == 375 and not "cook" in filename:
				bucket = {}
				bucket = makeQueuecraft(c_recipes[tier], cList,craftcount,tier,ignore_mixed,xp_to_level)
				bkey = sorted(bucket, reverse=True)
			elif not fast:
				if not tier == 0 and craftcount[tier]['current_xp'] <= xp_to_level[tier+10]:
					bucket = makeQueuecraft(dict(chain(c_recipes[tier].iteritems(),c_recipes[tier-25].iteritems())), cList,craftcount,tier,ignore_mixed,xp_to_level)
				else:
					bucket = makeQueuecraft(c_recipes[tier], cList,craftcount,tier,ignore_mixed,xp_to_level)
				bkey = sorted(bucket, reverse=True)
				
			tcost += bucket[bkey[0]]['cost']
			treco += cList[bucket[bkey[0]]['item_id']]['w']
			# TODO fix this, all text formatting needs to be in printtofile
			sell["<span class=\"%s\">%s</span> - Sold for %s per"%(cList[bucket[bkey[0]]['item_id']]['rarity'],cList[bucket[bkey[0]]['item_id']]['name'],mFormat(cList[bucket[bkey[0]]['item_id']]['w']))] += 1
			sole = 0
			for item in bucket[bkey[0]]['make']:
				if item == bucket[bkey[0]]['item_id'] and int(cList[item]['tier']) < tier:
					craftcount[tier]['ptitem'].append(rarityNum(cList[item]['rarity']))
					craftcount[tier]['current_xp'] = compute_level(xp_to_level[tier], craftcount[tier],tier,xp_to_level)
					pmake[tier][item] += 1
				elif not cList[item]['type'] in non_item and not 'discover' in cList[item]:
					cList[item]['discover'] = 1
					craftcount[int(cList[item]['tier'])]['discovery'].append(rarityNum(cList[item]['rarity']))
					make[int(cList[item]['tier'])][item] += 1
				elif not cList[item]['type'] in non_item:
					craftcount[int(cList[item]['tier'])]['item'].append(rarityNum(cList[item]['rarity']))
					make[int(cList[item]['tier'])][item] += 1
				elif cList[item]['type'] == u'Refinement':
					if item == 19679: # Bronze Ingot
						craftcount[int(cList[item]['tier'])]['refine'] += 0.2
					else:
						craftcount[int(cList[item]['tier'])]['refine'] += 1.0
					make[int(cList[item]['tier'])][item] += 1
				else:
					if item in [13063,  13189,  13207,  13219,  13045,  13022,  13075,  13177,  13096,  13033] and not sole: # Sole IDs
						sole +=1
					else:
						craftcount[int(cList[item]['tier'])]['part'].append(rarityNum(cList[item]['rarity']))
					make[int(cList[item]['tier'])][item] += 1
				ctier = int(cList[item]['tier'])
				craftcount[ctier]['current_xp'] = compute_level(xp_to_level[ctier], craftcount[ctier],ctier,xp_to_level)
			t = int(math.floor(tier/75.0)*75)
			if t == 375:
				t = 300
			if "cook" in filename:
				for item in bucket[bkey[0]]['buy']:
					buy[item] += 1
			else:
				for item in bucket[bkey[0]]['buy']:
					# Lump of Tin and Bronze Ingot
					if t == 0 and item == 19704 and 19679 in bucket[bkey[0]]['make']:
						tierbuy[t][item] += .2
						buy[item] += .2
					else:
						tierbuy[t][item] += 1
						buy[item] += 1
	totals = {}
	totals.update(printtofile(tcost, treco, sell, make, pmake, buy, tierbuy, cList, buttonList, filename, mytime, header, cright))
	return totals	

# given an item, determine if it is better to craft its sub items, or buy them.	return the recipe.
# include cost for current state, and xp generated.
def calcRecipecraft(recipe,items,craftcount,tier,count,itier,ignore_mixed,xp_to_level):
	level = 0
	while xp_to_level[int(level)] < craftcount[int(tier)]['current_xp']:
		level += 1
	xptotal = 0
	make = []
	buy = []
	cost = 0
	non_item = [u'Refinement', u'Insignia', u'Inscription', u'Component']
	# For our traditional style guides, we still want to consider buying gems even though you can refine.	This is a list of those gems
	# "Amber Pebble","Garnet Pebble","Malachite Pebble","Pearl","Tiger's Eye Pebble","Turquoise Pebble","Amethyst Nugget","Carnelian Nugget","Lapis Nugget","Peridot Nugget","Spinel Nugget","Sunstone Nugget","Topaz Nugget","Amethyst Lump","Carnelian Lump","Lapis Lump","Peridot Lump","Spinel Lump","Sunstone Lump","Topaz Lump","Beryl Shard","Chrysocola Shard","Coral Chunk","Emerald Shard","Opal Shard","Ruby Shard","Sapphire Shard","Beryl Crystal","Chrysocola Crystal","Coral Tentacle","Emerald Crystal","Opal Crystal","Ruby Crystal","Sapphire Crystal","Passion Flower"
	gemss = [24534,  24464,  24466,  24500,  24467,  24465,  24501,  24469,  24470,  24468,  24889,  24471,  24535,  24527,  24472,  24507,  24504,  24526,  24503,  24506,  24872,  24870,  24874,  24871,  24875,  24873,  24876,  24519,  24511,  24509,  24473,  24521,  24474,  24475,  37907]
	# impossible to make item at this point.
	if int(items[recipe]['tier']) > int(itier):
#		print recipe
		return 9999999999, -99999999999, make, buy
	for i in range(0,count):
		make.append(recipe)
	if int(items[recipe]['tier']) < int(tier) and not items[recipe]['type'] in non_item:
		xptotal = xp_calc(0,0,count,0,rarityNum(items[recipe]['rarity']),int(items[recipe]['tier']),level)*.85
	elif not items[recipe]['type'] in non_item and not 'discover' in items[recipe]:
		xptotal = xp_calc(0,0,count-1,1,rarityNum(items[recipe]['rarity']),int(items[recipe]['tier']),level)
	elif not items[recipe]['type'] in non_item:
		xptotal = xp_calc(0,0,count,0,rarityNum(items[recipe]['rarity']),int(items[recipe]['tier']),level)
	elif items[recipe]['type'] == u'Refinement':
		if 19679 == recipe:
			xptotal = math.ceil(xp_calc(count,0,0,0,1.0,int(items[recipe]['tier']),level)*0.2)
		else:
			xptotal = xp_calc(count,0,0,0,1.0,int(items[recipe]['tier']),level)
	else:
		if recipe in [13063,  13189,  13207,  13219,  13045,  13022,  13075,  13177,  13096,  13033]: # Sole
			xptotal = xp_calc(0,count,0,0,1.0,int(items[recipe]['tier']),level)*0.5
		else:
			xptotal = xp_calc(0,count,0,0,1.0,int(items[recipe]['tier']),level)

	mycost = 0
	for item in items[recipe]['recipe']:
		mycost += items[item]['cost']*items[recipe]['recipe'][item]

	mycost *= count
	for item in items[recipe]['recipe']:
		if not items[item]['recipe'] == None:
			tcost, txptotal, tmake, tbuy = calcRecipecraft(item,items,craftcount,items[item]['tier'],items[recipe]['recipe'][item]*count,int(items[recipe]['tier']),ignore_mixed,xp_to_level)
			if (ignore_mixed and item not in gemss) or tcost < items[item]['cost']*items[recipe]['recipe'][item]*count or float(xptotal+txptotal)/float(mycost-items[item]['cost']*items[recipe]['recipe'][item]*count+tcost) >= float(xptotal)/float(mycost):
				xptotal += txptotal*.85
				cost += tcost
				buy += tbuy
				make += tmake
			else:
				for i in range(0,int(math.ceil(count*items[recipe]['recipe'][item]))):
					buy.append(item)
				cost += items[item]['cost']*count*items[recipe]['recipe'][item]
		else:
			for i in range(0,int(math.ceil(count*items[recipe]['recipe'][item]))):
				buy.append(item)
			cost += items[item]['cost']*count*items[recipe]['recipe'][item]
	return cost, xptotal, make, buy

def makeQueuecraft(recipes,items,craftcount,tier,ignore_mixed,xp_to_level):
	outdict = {}
	cost = 0
	xptotal = 0
	make = []
	buy = []
	non_item = [u'Refinement', u'Insignia', u'Inscription', u'Component']

	for recipe in recipes.keys():
		if not items[recipe]['type'] in non_item:# or int(items[i]['tier']) > int(tier)-25:
			cost, xptotal, make, buy = calcRecipecraft(recipe,items,craftcount,tier,1,tier,ignore_mixed,xp_to_level)
			if xptotal:
				outdict[float(xptotal)/float(cost)+0.00001*random()] = {'item_id':recipe,'w':xptotal,'make':make,'buy':buy,'cost':cost}
			else:
				outdict[-1.0*float(cost)-random()] = {'item_id':recipe,'w':xptotal,'make':make,'buy':buy,'cost':cost}

	return outdict

# Format copper values so they are easier to read
def mFormat(line):
	line = int(line)
	tmp = ''
	rStr = ''

	if line < 0:
		tmp = '-'
		line *= -1

	mStr = str(line)
	mLen = len(mStr)

	if mLen > 4:
		rStr += "%2d<span class=\"goldIcon\"></span>" % int(mStr[0:mLen-4])
	if mLen > 3:
		rStr += '%2d<span class=\"silverIcon\"></span>' % int(mStr[mLen-4:mLen-2])
	elif mLen == 3:
		rStr += '%2d<span class=\"silverIcon\"></span>' % int(mStr[mLen-3:mLen-2])

	if mLen == 1:
		rStr += '%2d<span class=\"copperIcon\"></span>' % int(mStr)
	else:
		rStr += '%2d<span class=\"copperIcon\"></span>' % int(mStr[mLen-2:])

	return tmp + rStr

# TODO Replace all "duplicate" f.write statements with function calls for easier reading
def printtofile(tcost, treco, sell, make, pmake, buy, tierbuy, cList, buttonList, filename, mytime, header, cright):
	discbutton = buttonList[:]
	totals = {}
	if tierbuy:
		totals[filename.split('.')[0]] = {0:defaultdict(int),75:defaultdict(int),150:defaultdict(int),225:defaultdict(int),300:defaultdict(int),'total':int(tcost)}
	else:
		totals[filename.split('.')[0]] = int(tcost)

	non_item = [u'Refinement', u'Insignia', u'Inscription', u'Component']

	karma_items  = {12337:{'note':"Lieutenant Pickins - Greystone Rise(Harathi Hinterlands 35-45) <br /> Disa - Snowslide Ravine(Dredgehaunt Cliffs 40-50)",'cost':77}, # Almond
					12165:{'note':"Farmer Eda - Shaemoor Fields(Queensdale 1-15) <br /> Apple Jack(16c per) - Cornucopian Fields(Gendarran Fields 25-35)",'cost':35}, # Apple
					12340:{'note':"Fallen Angel Makayla - Stronghold of Ebonhawke(Fields of Ruin 30-40)",'cost':77}, # Avocado
					12251:{'note':"Deputy Jenks - Giant's Passage (Kessex Hills 15-25) <br /> Sangdo Swiftwing - Cereboth Canyon(Kessex Hills 15-25) <br /> Seraph Soldier Goran - The Wendon Steps(Brisban Wildlands 15-25) <br /> Security Captain Vejj - Almuten Estates(Gendarran Fields 25-35)",'cost':49}, # Banana
					12237:{'note':"Deputy Jenks - Overlake Haven(Kessex Hills 15-25) <br /> Field Medic Leius - Nebo Terrace(Gendarran Fields 25-35)",'cost':49}, # Black Bean
					12240:{'note':"Bjarni - Hangrammr Climb(Wayfayer Foothills 1-15) <br /> Milton Book - Cornucopian Fields(Gendarran Fields 25-35)",'cost':35}, # Celery Stalk
					12338:{'note':"Lieutenant Summers - Nightguard Beach(Harathi Hinterlands 35-45) <br /> Disa - Snowslide Ravine(Dredgehaunt Cliffs 35-45)",'cost':77}, # Cherry
					12515:{'note':"Naknar - Ebbing Heart Run(Iron Marches 50-60)",'cost':112}, # Chickpea
					12350:{'note':"Lionscout Tunnira - Archen Foreland(Bloodtide Coast 45-55)",'cost':112}, # Coconut
					12256:{'note':"Sagum Relicseeker - Agnos Gorge(Plains of Ashford 1-15) <br /> Milton Book - Cornucopian Fields(Gendarran Fields 25-35)",'cost':35}, # Cumin
					12502:{'note':"Environmental Activist Jenrys - Judgement Rock(Mount Maelstrom 60-70)",'cost':154}, # Eggplant
					12232:{'note':"Albin Chronicler - The Icesteppes(Wayfarer Foothills 1-15)",'cost':35}, # Green Bean
					12518:{'note':"Laudren - Thundertroll Swamp(Sparkfly Fen 55-65) <br /> Wupwup Chief - Apostate Wastes(Fireheart Rise 60-70)",'cost':112}, # Horseradish Root
					12239:{'note':"Seraph Archer Brian - Ossencrest Climb(Snowden Drifts 15-25) <br /> Kastaz Strongpaw - Noxin Dells(Diessa Plateau 15-25) <br /> Hune - The Thunderhorns(Lornar's Pass 25-40)",'cost':49}, # Kidney Bean
					12252:{'note':"Eona - Mabon Market(Caledon Forest 1-15) <br /> Researcher Hrappa - Voloxian Passage(Metrica Province 1-15) <br /> Milton Book - Cornucopian Fields(Gendarran Fields 25-35)",'cost':35}, # Lemon
					12339:{'note':"Shelp - Degun Shun(Blazeridge Steppes 40-50)",'cost':77}, # Lime
					12543:{'note':"Agent Crandle - Fort Trinity(Straits of Devastation 70-75)",'cost':203}, # Mango
					12249:{'note':"Farmer Eda - Shaemoor Fields(Queensdale 1-15) <br /> Deputy Jenks - Overlake Haven(Kessex Hills 15-25) <br /> Milton Book - Cornucopian Fields(Gendarran Fields 25-35)",'cost':35}, # Nutmeg Seed
					12503:{'note':"Nrocroc Chief - Apostate Wastes(Fireheart Rise 60-70)",'cost':154}, # Peach
					12514:{'note':"Braxa Scalehunter - Champion's Shield(Iron Marches 50-60)",'cost':112}, # Pear
					12516:{'note':"Scholar Tholin - Krongar Pass(Timberline Falls 50-60)",'cost':112}, # Pinenut
					12517:{'note':"Ichtaca - Hunting Banks(Timberline Falls 50-60)",'cost':112}} # Shallot

	karma_chef = {12159:{'note':"Master Chef or vendor near cooking area",'cost':35}, # Cheese Wedge
					12137:{'note':"Master Chef or vendor near cooking area",'cost':35}, # Glass of Buttermilk
					12152:{'note':"Master Chef or vendor near cooking area",'cost':35}, # Packet of Yeast
					12145:{'note':"Master Chef or vendor near cooking area",'cost':49}, # Rice Ball
					12325:{'note':"Master Chef or vendor near cooking area",'cost':77}, # Bowl of Sour Cream
					12141:{'note':"Master Chef or vendor near cooking area",'cost':35}, # Tomato
					12328:{'note':"Master Chef or vendor near cooking area",'cost':77}, # Ginger Root
					12245:{'note':"Master Chef or vendor near cooking area",'cost':49}, # Basil Leaf
					12235:{'note':"Master Chef or vendor near cooking area",'cost':49}} # Bell Pepper

	karma_recipe = {12131:{'note':"Elain - Grenbrack Delves(Caledon Forest 1-15)",'cost':35}, # Bowl of Watery Mushroom Soup
					12185:{'note':"Bjarni - Breakneck Pass(Wayfarer Foothills 1-15)",'cost':35}, # Handful of Bjarni's Rabbit Food
					12140:{'note':"PR&T Senior Investigator Hrouda - Akk Wilds(Metrica Province 1-15)",'cost':35}, # Bowl of Gelatinous Ooze Custard
					8587:{'note':"Drottot Lashtail - Devourer's Mouth(Plains of Ashford 1-15)",'cost':35}, # Poached Egg
					12211:{'note':"Lodge Keeper Kevach - Dolyak Pass(Wayfarer Foothills 1-15)",'cost':35}, # Bowl of Cold Wurm Stew
					12198:{'note':"Vaastas Meatslayer - Village of Butcher's Block(Diessa Plateau 15-25)",'cost':35}, # Celebratory Steak
					12133:{'note':"Laewyn - Wychmire Swamp(Caledon Forest 1-15)",'cost':35}, # Warden Ration
					12149:{'note':"Veteran Krug - Taminn Foothills(Queensdale 1-15)",'cost':35}, # Bowl of Ettin Stew
					12203:{'note':"Maxtar Rapidstep - Dolyak Pass(Wayfarer Foothills 1-15)",'cost':35}, # Bowl of Dolyak Stew
					12139:{'note':"Aidem Finlay - Hidden Lake(Brisban Wildlands 15-25)",'cost':35}, # Bowl of Front Line Stew
					12150:{'note':"Farmer Eda - Shaemoor Fields(Queensdale 1-15)",'cost':35}, # Eda's Apple Pie
					12343:{'note':"Kastaz Strongpaw - Noxin Dells(Diessa Plateau 15-25)",'cost':35}, # Kastaz Roasted Poultry
					12160:{'note':"Lionguard Auda - Dragon's Rising(Silverpeak Mountains 15-25)",'cost':35}, # Loaf of Walnut Sticky Bread
					12154:{'note':"Seraph Archer Brian - Ossencrest Climb(Snowden Drifts 15-25)",'cost':35}, # Bowl of Outrider Stew
					12292:{'note':"Glubb - Degun Shun(Blazeridge Steppes 40-50)",'cost':35}, # Bowl of Degun Shun Stew
					12233:{'note':"Scholar Tholin - Krongar Pass(Timberline Falls 50-60)",'cost':35}, # Handful of Trail Mix
					12739:{'note':"Sentry Triktiki - Arcallion Digs(Harathi Hinterlands 35-45)",'cost':35}, # Triktiki Omelet
					12352:{'note':"Pochtecatl - Jelako Cliffrise(Bloodtide Coast 45-55)",'cost':35}, # Griffon Egg Omelet
					12264:{'note':"Nrocroc Chief - Apostate Wastes(Fireheart Rise 60-70)",'cost':35}, # Raspberry Pie
					12192:{'note':"Assistant Chef Victor- Scaver Plateau(Queensdale 1-15)",'cost':35}, # Beetletun Omelette
					19955:{'note':"Master Craftsman or Vendor",'cost':350}, # Ravaging Intricate Wool Insignia
					19956:{'note':"Master Craftsman or Vendor",'cost':350}, # Rejuvenating Intricate Wool Insignia
					19957:{'note':"Master Craftsman or Vendor",'cost':350}, # Honed Intricate Wool Insignia
					19958:{'note':"Master Craftsman or Vendor",'cost':350}, # Pillaging Intricate Wool Insignia
					19959:{'note':"Master Craftsman or Vendor",'cost':350}, # Strong Intricate Wool Insignia
					19960:{'note':"Master Craftsman or Vendor",'cost':350}, # Vigorous Intricate Wool Insignia
					19961:{'note':"Master Craftsman or Vendor",'cost':350}, # Hearty Intricate Wool Insignia
					19962:{'note':"Master Craftsman or Vendor",'cost':455}, # Ravaging Intricate Cotton Insignia
					19963:{'note':"Master Craftsman or Vendor",'cost':455}, # Rejuvenating Intricate Cotton Insignia
					19964:{'note':"Master Craftsman or Vendor",'cost':455}, # Honed Intricate Cotton Insignia
					19965:{'note':"Master Craftsman or Vendor",'cost':455}, # Pillaging Intricate Cotton Insignia
					19966:{'note':"Master Craftsman or Vendor",'cost':455}, # Strong Intricate Cotton Insignia
					19967:{'note':"Master Craftsman or Vendor",'cost':455}, # Vigorous Intricate Cotton Insignia
					19968:{'note':"Master Craftsman or Vendor",'cost':455}, # Hearty Intricate Cotton Insignia
					19969:{'note':"Master Craftsman or Vendor",'cost':567}, # Carrion Intricate Linen Insignia
					19970:{'note':"Master Craftsman or Vendor",'cost':567}, # Cleric's Intricate Linen Insignia
					19971:{'note':"Master Craftsman or Vendor",'cost':567}, # Explorer's Intricate Linen Insignia
					19972:{'note':"Master Craftsman or Vendor",'cost':567}, # Berserker's Intricate Linen Insignia
					19973:{'note':"Master Craftsman or Vendor",'cost':567}, # Valkyrie Intricate Linen Insignia
					19974:{'note':"Master Craftsman or Vendor",'cost':567}, # Rampager's Intricate Linen Insignia
					19975:{'note':"Master Craftsman or Vendor",'cost':567}, # Knight's Intricate Linen Insignia
					19880:{'note':"Master Craftsman or Vendor",'cost':672}, # Carrion Intricate Silk Insignia
					19881:{'note':"Master Craftsman or Vendor",'cost':672}, # Cleric's Intricate Silk Insignia
					19882:{'note':"Master Craftsman or Vendor",'cost':672}, # Explorer's Intricate Silk Insignia
					19883:{'note':"Master Craftsman or Vendor",'cost':672}, # Berserker's Intricate Silk Insignia
					19886:{'note':"Master Craftsman or Vendor",'cost':672}, # Valkyrie Intricate Silk Insignia
					19884:{'note':"Master Craftsman or Vendor",'cost':672}, # Rampager's Intricate Silk Insignia
					19885:{'note':"Master Craftsman or Vendor",'cost':672}, # Knight's Intricate Silk Insignia
					19934:{'note':"Master Craftsman or Vendor",'cost':350}, # Ravaging Iron Imbued Inscription
					19935:{'note':"Master Craftsman or Vendor",'cost':350}, # Rejuvenating Iron Imbued Inscription
					19936:{'note':"Master Craftsman or Vendor",'cost':350}, # Honed Iron Imbued Inscription
					19937:{'note':"Master Craftsman or Vendor",'cost':350}, # Pillaging Iron Imbued Inscription
					19938:{'note':"Master Craftsman or Vendor",'cost':350}, # Strong Iron Imbued Inscription
					19939:{'note':"Master Craftsman or Vendor",'cost':350}, # Vigorous Iron Imbued Inscription
					19940:{'note':"Master Craftsman or Vendor",'cost':350}, # Hearty Iron Imbued Inscription
					19941:{'note':"Master Craftsman or Vendor",'cost':455}, # Ravaging Steel Imbued Inscription
					19942:{'note':"Master Craftsman or Vendor",'cost':455}, # Rejuvenating Steel Imbued Inscription
					19943:{'note':"Master Craftsman or Vendor",'cost':455}, # Honed Steel Imbued Inscription
					19944:{'note':"Master Craftsman or Vendor",'cost':455}, # Pillaging Steel Imbued Inscription
					19945:{'note':"Master Craftsman or Vendor",'cost':455}, # Strong Steel Imbued Inscription
					19946:{'note':"Master Craftsman or Vendor",'cost':455}, # Vigorous Steel Imbued Inscription
					19947:{'note':"Master Craftsman or Vendor",'cost':455}, # Hearty Steel Imbued Inscription
					19948:{'note':"Master Craftsman or Vendor",'cost':567}, # Carrion Darksteel Imbued Inscription
					19949:{'note':"Master Craftsman or Vendor",'cost':567}, # Cleric's Darksteel Imbued Inscription
					19950:{'note':"Master Craftsman or Vendor",'cost':567}, # Explorer's Darksteel Imbued Inscription
					19951:{'note':"Master Craftsman or Vendor",'cost':567}, # Berserker's Darksteel Imbued Inscription
					19952:{'note':"Master Craftsman or Vendor",'cost':567}, # Valkyrie Darksteel Imbued Inscription
					19953:{'note':"Master Craftsman or Vendor",'cost':567}, # Rampager's Darksteel Imbued Inscription
					19954:{'note':"Master Craftsman or Vendor",'cost':567}, # Knight's Darksteel Imbued Inscription
					19897:{'note':"Master Craftsman or Vendor",'cost':672}, # Carrion Mithril Imbued Inscription
					19898:{'note':"Master Craftsman or Vendor",'cost':672}, # Cleric's Mithril Imbued Inscription
					19899:{'note':"Master Craftsman or Vendor",'cost':672}, # Explorer's Mithril Imbued Inscription
					19900:{'note':"Master Craftsman or Vendor",'cost':672}, # Berserker's Mithril Imbued Inscription
					19903:{'note':"Master Craftsman or Vendor",'cost':672}, # Valkyrie Mithril Imbued Inscription
					19901:{'note':"Master Craftsman or Vendor",'cost':672}, # Rampager's Mithril Imbued Inscription
					19902:{'note':"Master Craftsman or Vendor",'cost':672}, # Knight's Mithril Imbued Inscription
					24904:{'note':"Master Craftsman or Vendor",'cost':231}, # Embellished Intricate Topaz Jewel
					24902:{'note':"Master Craftsman or Vendor",'cost':231}, # Embellished Intricate Spinel Jewel
					24901:{'note':"Master Craftsman or Vendor",'cost':231}, # Embellished Intricate Peridot Jewel
					24903:{'note':"Master Craftsman or Vendor",'cost':231}, # Embellished Intricate Sunstone Jewel
					24899:{'note':"Master Craftsman or Vendor",'cost':231}, # Embellished Intricate Carnelian Jewel
					24898:{'note':"Master Craftsman or Vendor",'cost':231}, # Embellished Intricate Amethyst Jewel
					24900:{'note':"Master Craftsman or Vendor",'cost':231}, # Embellished Intricate Lapis Jewel
					24911:{'note':"Master Craftsman or Vendor",'cost':231}, # Embellished Gilded Topaz Jewel
					24905:{'note':"Master Craftsman or Vendor",'cost':231}, # Embellished Gilded Amethyst Jewel
					24906:{'note':"Master Craftsman or Vendor",'cost':231}, # Embellished Gilded Carnelian Jewel
					24907:{'note':"Master Craftsman or Vendor",'cost':231}, # Embellished Gilded Lapis Jewel
					24908:{'note':"Master Craftsman or Vendor",'cost':231}, # Embellished Gilded Peridot Jewel
					24909:{'note':"Master Craftsman or Vendor",'cost':231}, # Embellished Gilded Spinel Jewel
					24910:{'note':"Master Craftsman or Vendor",'cost':231}, # Embellished Gilded Sunstone Jewel
					24912:{'note':"Master Craftsman or Vendor",'cost':231}, # Embellished Ornate Beryl Jewel
					24913:{'note':"Master Craftsman or Vendor",'cost':231}, # Embellished Ornate Chrysocola Jewel
					24914:{'note':"Master Craftsman or Vendor",'cost':231}, # Embellished Ornate Coral Jewel
					24915:{'note':"Master Craftsman or Vendor",'cost':231}, # Embellished Ornate Emerald Jewel
					24916:{'note':"Master Craftsman or Vendor",'cost':231}, # Embellished Ornate Opal Jewel
					24917:{'note':"Master Craftsman or Vendor",'cost':231}, # Embellished Ornate Ruby Jewel
					24918:{'note':"Master Craftsman or Vendor",'cost':231}, # Embellished Ornate Sapphire Jewel
					24919:{'note':"Master Craftsman or Vendor",'cost':231}, # Embellished Brilliant Beryl Jewel
					24920:{'note':"Master Craftsman or Vendor",'cost':231}, # Embellished Brilliant Chrysocola Jewel
					24921:{'note':"Master Craftsman or Vendor",'cost':231}, # Embellished Brilliant Coral Jewel
					24922:{'note':"Master Craftsman or Vendor",'cost':231}, # Embellished Brilliant Emerald Jewel
					24923:{'note':"Master Craftsman or Vendor",'cost':231}, # Embellished Brilliant Opal Jewel
					24924:{'note':"Master Craftsman or Vendor",'cost':231}, # Embellished Brilliant Ruby Jewel
					24925:{'note':"Master Craftsman or Vendor",'cost':231}} # Embellished Brilliant Sapphire Jewel

	recipebuy = []
	for tier in [0,25,50,75,100,125,150,175,200,225,250,275,300,325,350,375]:
		for item in make[tier]:
			if item in karma_recipe:
				recipebuy.append(item)

	# 'Spool of Jute Thread','Spool of Wool Thread','Spool of Cotton Thread','Spool of Linen Thread','Spool of Silk Thread','Lump of Tin','Lump of Coal','Lump of Primordium','Jar of Vinegar','Packet of Baking Powder','Jar of Vegetable Oil','Packet of Salt','Bag of Sugar','Jug of Water','Bag of Starch','Bag of Flour','Bottle of Soy Sauce',"Bottle of Rice Wine", "Minor Rune of Holding", "Rune of Holding", "Major Rune of Holding", "Greater Rune of Holding"
	vendor = [19792,  19789,  19794,  19793,  19791,  19704,  19750,  19924,  12157,  12151,  12158,  12153,  12155,  12156,  12324,  12136,  12271,  8576,  13010,  13006,  13007,  13008]

	# "Jute Scrap","Bolt of Jute","Copper Ore","Copper Ingot","Bronze Ingot","Rawhide Leather Section","Stretched Rawhide Leather Square","Green Wood Log","Green Wood Plank","Wool Scrap","Bolt of Wool","Iron Ore","Silver Ore","Iron Ingot","Silver Ingot","Thin Leather Section","Cured Thin Leather Square","Soft Wood Log","Soft Wood Plank","Cotton Scrap","Bolt of Cotton","Spool of Cotton Thread","Iron Ore","Gold Ore","Gold Ingot","Steel Ingot","Coarse Leather Section","Cured Coarse Leather Square","Seasoned Wood Log","Seasoned Wood Plank","Linen Scrap","Bolt of Linen","Platinum Ore","Platinum Ingot","Darksteel Ingot","Rugged Leather Section","Cured Rugged Leather Square","Hard Wood Log","Hard Wood Plank","Silk Scrap","Bolt of Silk","Mithril Ore","Mithril Ingot","Thick Leather Section","Cured Thick Leather Square","Elder Wood Log","Elder Wood Plank"
	basic = [19718,  19720,  19697,  19680,  19679,  19719,  19738,  19723,  19710,  19739,  19740,  19699,  19703,  19683,  19687,  19728,  19733,  19726,  19713,  19741,  19742,  19794,  19699,  19698,  19682,  19688,  19730,  19734,  19727,  19714,  19743,  19744,  19702,  19686,  19681,  19731,  19736,  19724,  19711,  19748,  19747,  19700,  19684,  19729,  19735,  19722,  19709]

	# "Bone Chip","Tiny Claw","Pile of Glittering Dust","Tiny Fang","Tiny Scale","Tiny Totem","Tiny Venom Sac","Vial of Weak Blood","Bone Shard","Small Claw","Pile of Shimmering Dust","Small Fang","Small Scale","Small Totem","Small Venom Sac","Vial of Thin Blood","Bone","Claw","Pile of Radiant Dust","Fang","Scale","Totem","Venom Sac","Vial of Blood","Heavy Bone","Sharp Claw","Pile of Luminous Dust","Sharp Fang","Smooth Scale","Engraved Totem","Full Venom Sac","Vial of Thick Blood","Large Bone","Large Claw","Pile of Incandescent Dust","Large Fang","Large Scale","Intricate Totem","Potent Venom Sac","Vial of Potent Blood","Karka Shell"
	basic_f = [24342,  24346,  24272,  24352,  24284,  24296,  24278,  24290,  24343,  24347,  24273,  24353,  24285,  24297,  24279,  24291,  24344,  24348,  24274,  24354,  24286,  24298,  24280,  24292,  24345,  24349,  24275,  24355,  24287,  24363,  24281,  24293,  24341,  24350,  24276,  24356,  24288,  24299,  24282,  24294,  37897]

	# "Pile of Soiled Essence","Onyx Sliver","Molten Sliver","Glacial Sliver","Destroyer Sliver","Crystal Sliver","Corrupted Sliver","Charged Sliver","Pile of Foul Essence","Onyx Fragment","Molten Fragment","Glacial Fragment","Destroyer Fragment","Crystal Fragment","Corrupted Fragment","Charged Fragment","Pile of Filthy Essence","Onyx Shard","Molten Shard","Glacial Shard","Destroyer Shard","Crystal Shard","Corrupted Shard","Charged Shard","Pile of Vile Essence","Onyx Core","Molten Core","Glacial Core","Destroyer Core","Crystal Core","Corrupted Core","Charged Core","Glob of Ectoplasm"
	basic_r = [24331,  24306,  24311,  24316,  24321,  24326,  24336,  24301,  24332,  24307,  24312,  24317,  24322,  24327,  24337,  24302,  24333,  24308,  24313,  24318,  24323,  24328,  24338,  24303,  24334,  24309,  24314,  24319,  24324,  24329,  24339,  24304,  19721]

	# "Amber Pebble","Garnet Pebble","Malachite Pebble","Pearl","Tiger's Eye Pebble","Turquoise Pebble","Amethyst Nugget","Carnelian Nugget","Lapis Nugget","Peridot Nugget","Spinel Nugget","Sunstone Nugget","Topaz Nugget","Amethyst Lump","Carnelian Lump","Lapis Lump","Peridot Lump","Spinel Lump","Sunstone Lump","Topaz Lump","Beryl Shard","Chrysocola Shard","Coral Chunk","Emerald Shard","Opal Shard","Ruby Shard","Sapphire Shard","Beryl Crystal","Chrysocola Crystal","Coral Tentacle","Emerald Crystal","Opal Crystal","Ruby Crystal","Sapphire Crystal","Passion Flower"
	basic_g = [24534,  24464,  24466,  24500,  24467,  24465,  24501,  24469,  24470,  24468,  24889,  24471,  24535,  24527,  24472,  24507,  24504,  24526,  24503,  24506,  24872,  24870,  24874,  24871,  24875,  24873,  24876,  24519,  24511,  24509,  24473,  24521,  24474,  24475,  37907]

	# "Tiny Snowflake","Delicate Snowflake","Glittering Snowflake","Unique Snowflake","Pristine Snowflake","Piece of Candy Corn","Chattering Skull","Nougat Center","Plastic Fang"
	basic_h = [38130,  38131,  38132,  38133,  38134,  36041,  36060,  36061,  36059]

	# "Artichoke","Asparagus Spear","Basil Leaf","Bay Leaf","Beet","Black Peppercorn","Blackberry","Blueberry","Butternut Squash","Carrot","Cayenne Pepper","Chili Pepper","Chocolate Bar","Cinnamon Stick","Clam","Clove","Coriander Seed","Dill Sprig","Egg","Head of Cabbage","Head of Cauliflower","Head of Garlic","Head of Lettuce","Kale Leaf","Leek","Mint Leaf","Mushroom","Onion","Orange","Oregano Leaf","Parsley Leaf","Parsnip","Passion Fruit","Piece of Candy Corn","Portobello Mushroom","Potato","Raspberry","Rosemary Sprig","Rutabaga","Sage Leaf","Sesame Seed","Slab of Poultry Meat","Slab of Red Meat","Snow Truffle","Spinach Leaf","Stick of Butter","Strawberry","Sugar Pumpkin","Tarragon Leaves","Thyme Leaf","Turnip","Vanilla Bean","Walnut","Yam","Zucchini","Green Onion"
	basic_fo = [12512,  12505,  12245,  12247,  12161,  12236,  12537,  12255,  12511,  12134,  12504,  12331,  12229,  12258,  12327,  12534,  12531,  12336,  12143,  12332,  12532,  12163,  12238,  12333,  12508,  12536,  12147,  12142,  12351,  12244,  12246,  12507,  36731,  36041,  12334,  12135,  12254,  12335,  12535,  12243,  12342,  24360,  24359,  12144,  12241,  12138,  12253,  12538,  12506,  12248,  12162,  12234,  12250,  12329,  12330,  12533]

	# TODO add check for buying bronze ingot and reduce by amount we add, remove if <0
	if 19679 in make[0]:
		var = 5 - (make[0][19679] % 5)
		if var in [1,2,3,4]:
			make[0][19679] += var
			tierbuy[0][19697] += 2*var
			tierbuy[0][19704] += 0.2*var
			buy[19697] += 2*var
			buy[19704] += 0.2*var
			tcost += cList[19697]['cost']*var+8.0*(0.2*var)
		make[0][19679] = make[0][19679]/5

	if 19704 in buy and buy[19704] == 0.0:
		del(buy[19704])
		del(tierbuy[0][19704])

	b_karma_w = defaultdict(int)
	b_karma_c = defaultdict(int)
	b_vendor = defaultdict(int)
	b_common = defaultdict(int)
	b_fine = defaultdict(int)
	b_rare = defaultdict(int)
	b_gem = defaultdict(int)
	b_holiday = defaultdict(int)
	b_food = defaultdict(int)
	b_mix = defaultdict(int)

	for item in buy:	
			if item in karma_chef:
				b_karma_c[item] = buy[item]
			elif item in karma_items:
				karmin[item] = buy[item] # used by cooking to make a top 5 list
				b_karma_w[item] = buy[item]
			elif item in vendor:
				b_vendor[item] = buy[item]
			elif item in basic:
				b_common[item] = buy[item]
			elif item in basic_f:
				b_fine[item] = buy[item]
			elif item in basic_r:
				b_rare[item] = buy[item]
			elif item in basic_g:
				b_gem[item] = buy[item]
			elif item in basic_h:
				b_holiday[item] = buy[item]
			elif item in basic_fo:
				b_food[item] = buy[item]
			else:
				b_mix[item] = buy[item]

	t = 0 # used to control div background color
	kt = 0 # karma total
	with open(filename,'wb') as f:
		f.write('<!DOCTYPE html>\n')
		f.write('<html>\n')
		f.write('<head>\n')
		f.write('	<title>'+filename.split('.')[0].replace("_"," ").title()+'</title>\n')
		f.write('	<meta name="description" content="Guild Wars 2 always current crafting guide for '+filename.split('.')[0].replace("_"," ").title()+'">\n')
		f.write('	<meta http-equiv="content-type" content="text/html;charset=UTF-8">\n')
		f.write('	<script src="//ajax.googleapis.com/ajax/libs/jquery/1.9.0/jquery.min.js"></script>\n')
		f.write('	<script>(window.jQuery || document.write(\'<script src="http://ajax.aspnetcdn.com/ajax/jquery/jquery-1.9.0.min.js"><\/script>\'));</script>\n')
		f.write('	<script src="js/menu.js" type="text/javascript"></script>\n')
		f.write('	<link href="css/layout.css" rel="stylesheet" type="text/css" />') 
		f.write('	<link rel="icon" type="image/png" href="/fi.gif">')
		f.write('</head>\n')
		f.write('<body>\n'+header+'\n<section>')
		f.write('<div style="width: 100%; border: 2px #fffaaa solid; border-left: 0px; border-right: 0px; background: #fffddd; height: 24px;">\n')
		f.write('<img src="css/warning-icon.png" width="24px" height="24px" style="padding: 0 8px 0 8px; float: left;"><span style="position: relative; top: 4px;"><span style="color: red">Do not refresh this page.</span>	It may change. Updated: '+mytime+'</b></span>\n')
		f.write('</div>\n')
		f.write("<br />Wherever you see this  <img src=\"/img/arrow.png\"></img> you can click for more information <br />")
		f.write("<button title=\"Click To Show All Discovery Recipes\" class =\"info\" id=\"show_all\">Show All Discovery</button><br />")
		f.write("<button title=\"Click To Hide All Discovery Recipes\" class =\"info\" id=\"hide_all\">Hide All Discovery</button><br />")
		f.write('<h1>'+filename.split('.')[0].replace("_"," ").title()+'</h1>')
		f.write('<dl>\n')
		f.write('	<dt>Initial Cost</dt>\n')
		f.write('	<dd>'+mFormat(tcost)+'</dd>\n')
		f.write('	<dt>Expected Recovery</dt>\n')
		f.write('	<dd><span style="position: relative; left: -9px;">- '+mFormat(treco)+'</span></dd>\n')
		f.write('	<dt>Expected Final Cost</dt>\n')
		f.write('	<dd style="border-top: 1px #666 solid;">'+mFormat(tcost-treco)+'</dd>\n')
		f.write('</dl>')
		f.write('<div class="clear"></div>')
		f.write('<br /><button title=\"Click To Toggle\" class=\"arrow\" id=\"tcost\">Sell List:</button><div class=\"lsbutton\" id=\"1tcost\">')
		for line in sorted(sell):
			t = (t+1)%2
			f.write("<div class=\"s"+str(t)+"\">%3i %s</div>\n"%(sell[line],line))
		f.write("</div><script type=\"text/javascript\">$('#1tcost').hide();</script><br />")
		buttonList.append('tcost')

		if b_vendor or b_karma_c or b_karma_w:
			f.write("<h2>BUY VENDOR</h2>\n")
			if b_karma_c or b_karma_w:
				f.write("<span class=\"karmaIcon\"></span> Note: 11 Basil Leaf(e.g.) means buy 1 bulk Basil Leaf and you will have 14 left over<br /><br />\n")

			for item in sorted(b_karma_w):
				t = (t+1)%2
				f.write(("<div class=\"s"+str(t)+"\"><input type=\"checkbox\" /><span class=\"itemIcon\" style=\"background-image: url("+cList[item]['icon']+");\"></span><span class=\"quantity\">%i</span> <button title=\"Click To Toggle\" class=\"%s arrow\" id=\""+str(item)+"\">%s</button><div class=\"lsbutton\" id=\"1"+str(item)+"\">%i <span class=\"karmaIcon\"></span> per 25 <br /> %s</div></div>\n")%(buy[item],cList[item]['rarity'],cList[item][u'name'],karma_items[item]['cost'],karma_items[item]['note']))
				buttonList.append(item)
				kt += int(math.ceil(buy[item]/25.0)*karma_items[item]['cost'])

			for item in sorted(b_karma_c):
				t = (t+1)%2
				f.write(("<div class=\"s"+str(t)+"\"><input type=\"checkbox\" /><span class=\"itemIcon\" style=\"background-image: url("+cList[item]['icon']+");\"></span><span class=\"quantity\">%i</span> <span class=\"%s\">%s</span> (%i <span class=\"karmaIcon\"></span> per 25, %s)</div>\n")%(buy[item],cList[item]['rarity'],cList[item][u'name'],karma_chef[item]['cost'],karma_chef[item]['note']))
				kt += int(math.ceil(buy[item]/25.0)*karma_chef[item]['cost'])

			for item in sorted(b_vendor):
				t = (t+1)%2

				f.write("<div class=\"s"+str(t)+"\"><input type=\"checkbox\" /><span class=\"itemIcon\" style=\"background-image: url("+cList[item]['icon']+");\"></span><span class=\"quantity\">%i</span> <span class=\"%s\">%s</span> (%4s per from Vendor)</div>\n"%(buy[item],cList[item]['rarity'],cList[item][u'name'],mFormat(cList[item]['cost'])))

		if recipebuy:
			f.write("<h2>BUY RECIPES</h2>\n")
			for item in recipebuy:
				t = (t+1)%2
				f.write(("<div class=\"s"+str(t)+"\"><input type=\"checkbox\" /><span class=\"itemIcon\" style=\"background-image: url("+cList[item]['icon']+");\"></span><button title=\"Click To Toggle\" class=\"arrow %s\" id=\""+str(item)+"\">%s</button><div class=\"lsbutton\" id=\"1"+str(item)+"\">%i <span class=\"karmaIcon\"></span>, %s</div></div>\n")%(cList[item]['rarity'],cList[item][u'name'],karma_recipe[item]['cost'],karma_recipe[item]['note']))
				buttonList.append(item)
				kt += int(karma_recipe[item]['cost'])
		if kt:
			f.write('<br />\nTotal <span class=\"karmaIcon\"></span>: '+str(kt)+'<br />\n')
		if b_common or b_fine or b_rare or b_gem or b_holiday or b_food:
			f.write('<h2>COLLECTIBLES(Check Bank First or Buy on TP)</h2>\n')
			for item in sorted(b_common):
				t = (t+1)%2
				f.write("<div class=\"s"+str(t)+"\"><input type=\"checkbox\" /><span class=\"itemIcon\" style=\"background-image: url("+cList[item]['icon']+");\"></span><span class=\"quantity\">%i</span> <span class=\"%s\">%s</span> (%4s per)</div>\n"%(buy[item],cList[item]['rarity'],cList[item][u'name'],mFormat(cList[item]['cost'])))
			for item in sorted(b_fine):
				t = (t+1)%2
				f.write("<div class=\"s"+str(t)+"\"><input type=\"checkbox\" /><span class=\"itemIcon\" style=\"background-image: url("+cList[item]['icon']+");\"></span><span class=\"quantity\">%i</span> <span class=\"%s\">%s</span> (%4s per)</div>\n"%(buy[item],cList[item]['rarity'],cList[item][u'name'],mFormat(cList[item]['cost'])))
			for item in sorted(b_rare):
				t = (t+1)%2
				f.write("<div class=\"s"+str(t)+"\"><input type=\"checkbox\" /><span class=\"itemIcon\" style=\"background-image: url("+cList[item]['icon']+");\"></span><span class=\"quantity\">%i</span> <span class=\"%s\">%s</span> (%4s per)</div>\n"%(buy[item],cList[item]['rarity'],cList[item][u'name'],mFormat(cList[item]['cost'])))
			for item in sorted(b_gem):
				t = (t+1)%2
				f.write("<div class=\"s"+str(t)+"\"><input type=\"checkbox\" /><span class=\"itemIcon\" style=\"background-image: url("+cList[item]['icon']+");\"></span><span class=\"quantity\">%i</span> <span class=\"%s\">%s</span> (%4s per)</div>\n"%(buy[item],cList[item]['rarity'],cList[item][u'name'],mFormat(cList[item]['cost'])))
			for item in sorted(b_holiday):
				t = (t+1)%2
				f.write("<div class=\"s"+str(t)+"\"><input type=\"checkbox\" /><span class=\"itemIcon\" style=\"background-image: url("+cList[item]['icon']+");\"></span><span class=\"quantity\">%i</span> <span class=\"%s\">%s</span> (%4s per)</div>\n"%(buy[item],cList[item]['rarity'],cList[item][u'name'],mFormat(cList[item]['cost'])))
			for item in sorted(b_food):
				t = (t+1)%2
				f.write("<div class=\"s"+str(t)+"\"><input type=\"checkbox\" /><span class=\"itemIcon\" style=\"background-image: url("+cList[item]['icon']+");\"></span><span class=\"quantity\">%i</span> <span class=\"%s\">%s</span> (%4s per)</div>\n"%(buy[item],cList[item]['rarity'],cList[item][u'name'],mFormat(cList[item]['cost'])))

		if b_mix:
			f.write('<h2>MIXED(Buy on TP)</h2>\n')
			for item in sorted(b_mix):
				t = (t+1)%2
				f.write("<div class=\"s"+str(t)+"\"><input type=\"checkbox\" /><span class=\"itemIcon\" style=\"background-image: url("+cList[item]['icon']+");\"></span><span class=\"quantity\">%i</span> <span class=\"%s\">%s</span> (%4s per)</div>\n"%(buy[item],cList[item]['rarity'],cList[item][u'name'],mFormat(cList[item]['cost'])))

		f.write("<br />\n<br />\n<h2>MAKE</h2>\n")
		rt = 0
		for tier in [0,25,50,75,100,125,150,175,200,225,250,275,300,325,350,375]:
			if tierbuy and tier in [0,75,150,225,300]:
				tt = 0
				tc = tier+75
				if tier == 300:
					tc += 25
				f.write(("<br /><br /><h4>Tier %i, Levels %i-%i:<button title=\"Click To Toggle\" class =\"info\" id=\""+str(tier)+"tier\">Buy List(Only Tier %i)</button></h4>\n<div class=\"lsbutton\" id=\"1"+str(tier)+"tier\">")%(tier/75+1,tier,tc,tier/75+1))
				f.write("<h5>Notice: If you are following the full guide then you already purchased these materials.</h5>")
				for item in sorted(tierbuy[tier]):
					t = (t+1)%2
					f.write("<div class=\"s"+str(t)+"\"><input type=\"checkbox\" /><span class=\"itemIcon\" style=\"background-image: url("+cList[item]['icon']+");\"></span><span class=\"quantity\">%i</span> <span class=\"%s\">%s</span> (%4s per)</div>\n"%(tierbuy[tier][item],cList[item]['rarity'],cList[item][u'name'],mFormat(cList[item]['cost'])))
					tt += tierbuy[tier][item]*cList[item]['cost']
				buttonList.append(str(tier)+'tier')
				rt += tt
				totals[filename.split('.')[0]][tier] = tt
				f.write("</div><h4>Cost: %s ( Rolling Total: %s)</h4>\n"% (mFormat(tt),mFormat(rt)))		
			f.write(("<br />\n<h3>Level:%3i</h3>\n")%(tier))
			if pmake[tier]:
				for item in sorted(pmake[tier]):
					t = (t+1)%2
					f.write("<div class=\"s"+str(t)+"\">Make:%3i <span class=\"%s\">%s</span> (From %i tier) </div>\n"%(pmake[tier][item],cList[item]['rarity'],cList[item][u'name'],tier-25))
			for item in sorted(make[tier], key=make[tier].get,reverse=True):
				if cList[item][u'type'] == u'Refinement':
					t = (t+1)%2
					if item == 19679: # Bronze Ingot
						f.write("<div class=\"s"+str(t)+"\">Make:%3i <span class=\"%s\">%s</span> (Produces 5 Ingot per make)</div>\n"%(make[tier][item],cList[item]['rarity'],cList[item][u'name']))
					else:
						f.write("<div class=\"s"+str(t)+"\">Make:%3i <span class=\"%s\">%s</span></div>\n"%(make[tier][item],cList[item]['rarity'],cList[item][u'name']))
			for item in sorted(make[tier], key=make[tier].get,reverse=True):
				if cList[item]['type'] in non_item and not cList[item]['type'] == u'Refinement':
					t = (t+1)%2
					if item in [13063,  13189,  13207,  13219,  13045,  13022,  13075,  13177,  13096,  13033]: # Sole
						f.write("<div class=\"s"+str(t)+"\">Make:%3i <span class=\"%s\">%s</span> (Produces 2 Soles per make)</div>\n"%(make[tier][item]/2,cList[item]['rarity'],cList[item][u'name']))
					else:
						f.write("<div class=\"s"+str(t)+"\">Make:%3i <span class=\"%s\">%s</span></div>\n"%(make[tier][item],cList[item]['rarity'],cList[item][u'name']))
			for item in sorted(make[tier]):

				if 'discover' in cList[item] and cList[item]['discover'] == 1:
					if make[tier][item] > 1:
						make[tier][item] -= 1
					else:
						del(make[tier][item])
					t = (t+1)%2
					tstr = "<div class=\"sbutton\" id=\"1"+str(item)+"\">"
					for s in cList[item]['recipe']:
						tstr += "\n<br />\t<span class=\"itemIcon\" style=\"background-image: url("+cList[s]['icon']+");\"></span> <span class=\""+cList[s]['rarity']+'\">'+cList[s]['name']+"</span> ("+str(cList[item]['recipe'][s])+")"
					tstr += "</div><br />"
					f.write("<div class=\"s"+str(t)+"\">Discover: <button class=\"arrow "+cList[item]['rarity']+'\" title=\"Click To Toggle\" id=\"'+str(item)+'\">'+cList[item]['name']+"</button> "+tstr+"\n</div>\n")
					buttonList.append(item)
			for item in sorted(make[tier]):
				if not cList[item][u'type'] in non_item:
					t = (t+1)%2
					f.write("<div class=\"s"+str(t)+"\">Make:%3i <span class=\"%s\">%s</span></div>\n"%(make[tier][item],cList[item]['rarity'],cList[item][u'name']))
		f.write('<br />\n<h3>Level:400</h3>\n')
		t = (t+1)%2
		f.write("<div class=\"s"+str(t)+"\">Nothing.	You are done!</div>\n"+'</section>\n'+cright)
		f.write('\n<script type="text/javascript">\n')
		for item in buttonList:
			f.write("$(\"#"+str(item)+"\").click(function () {\n\t$(\"#1"+str(item)+"\").toggle();});\n")
		f.write("$(\".sbutton\").hide();\n")
		f.write("$(\".lsbutton\").hide();\n")
		f.write("$(\"#show_all\").click(function () {$(\".sbutton\").show();")
		f.write("});\n$(\"#hide_all\").click(function () {$(\".sbutton\").hide();")
		f.write('});\n</script>\n')
		f.write('</body>\n')
		f.write('</html>\n')
	return totals

def maketotals(totals, mytime):
	global header
	global cright

	page = '''
<!DOCTYPE html>
<html>
<head>
	<title>Totals</title>
	<meta name="description" content="Guild Wars 2 always current crafting guide price totals">
	<meta http-equiv="content-type" content="text/html;charset=UTF-8">

	<script src="//ajax.googleapis.com/ajax/libs/jquery/1.9.0/jquery.min.js"></script>
	<script src="js/menu.js" type="text/javascript"></script>
	<link href="css/layout.css" rel="stylesheet" type="text/css" />

	<link rel="icon" type="image/png" href="/fi.gif">
</head>
<body>'''
	page += header

	page += "<section>\n<h5 style=\"text-align:center;\">Updated: " + mytime + "</h5>"
	page += '''
<strong>Note:</strong> The prices show here are initial costs and do not take sellback into account.
	<table>
	<tr><th>Craft</th><th>Total - Normal</th><th>Total - Fast</th></tr>\n'''
	page += '<tr><td>cooking_karma</td><td>'+mFormat(totals['cooking_karma'])+'</td><td>'+mFormat(totals['cooking_karma_fast'])+'</td></tr>\n'
	page += '<tr><td>cooking_karma_light</td><td>'+mFormat(totals['cooking_karma_light'])+'</td><td>'+mFormat(totals['cooking_karma_fast_light'])+'</td></tr>\n'
	page += '<tr><td>cooking</td><td>'+mFormat(totals['cooking'])+'</td><td>'+mFormat(totals['cooking_fast'])+'</td></tr>\n'
	
	page += "</table>\n<br />\n<table>\n<tr><th>Craft</th><th>Total Cost</th><th>Tier 0-75</th><th>Tier 75-150</th><th>Tier 150-225</th><th>Tier 225-300</th><th>Tier 300-400</th></tr>\n"
	cttl = 0
	for i in ['armorcraft','artificing','huntsman','jewelcraft','leatherworking','tailor','weaponcraft']:
		page += '<tr><td>'+i+'</td><td>'+mFormat(totals[i]['total'])+'</td><td>'+mFormat(totals[i][0])+'</td><td>'+mFormat(totals[i][75])+'</td><td>'+mFormat(totals[i][150])+'</td><td>'+mFormat(totals[i][225])+'</td><td>'+mFormat(totals[i][300])+'</td></tr>\n'
		cttl += totals[i]['total']

	page += ' </table>\n<br /><strong>Total for non-cooking normal: </strong>' + mFormat(cttl)

	page += "<br /><br /></table>\n<br />\n<table>\n<tr><th>Craft</th><th>Total Cost</th><th>Tier 0-75</th><th>Tier 75-150</th><th>Tier 150-225</th><th>Tier 225-300</th><th>Tier 300-400</th></tr>\n"
	cttl = 0
	for i in ['armorcraft_fast','artificing_fast','huntsman_fast','jewelcraft_fast','leatherworking_fast','tailor_fast','weaponcraft_fast']:
		page += '<tr><td>'+i+'</td><td>'+mFormat(totals[i]['total'])+'</td><td>'+mFormat(totals[i][0])+'</td><td>'+mFormat(totals[i][75])+'</td><td>'+mFormat(totals[i][150])+'</td><td>'+mFormat(totals[i][225])+'</td><td>'+mFormat(totals[i][300])+'</td></tr>\n'
		cttl += totals[i]['total']

	page += ' </table>\n<br /><strong>Total for non-cooking fast: </strong>' + mFormat(cttl)

	page += "<br /><br /></table>\n<br />\n<table>\n<tr><th>Craft</th><th>Total Cost</th><th>Tier 0-75</th><th>Tier 75-150</th><th>Tier 150-225</th><th>Tier 225-300</th><th>Tier 300-400</th></tr>\n"
	cttl = 0
	for i in ['armorcraft_craft_all','artificing_craft_all','huntsman_craft_all','jewelcraft_craft_all','leatherworking_craft_all','tailor_craft_all','weaponcraft_craft_all']:
		page += '<tr><td>'+i+'</td><td>'+mFormat(totals[i]['total'])+'</td><td>'+mFormat(totals[i][0])+'</td><td>'+mFormat(totals[i][75])+'</td><td>'+mFormat(totals[i][150])+'</td><td>'+mFormat(totals[i][225])+'</td><td>'+mFormat(totals[i][300])+'</td></tr>\n'
		cttl += totals[i]['total']

	page += ' </table>\n<br /><strong>Total for non-cooking traditional: </strong>' + mFormat(cttl)

	page += '\n</section>\n' + cright + '\n</body>\n</html>'

	with open('total.html','wb') as f:
		f.write(page)

# Join 2 recipe dicts
def join(A, B):
		if not isinstance(A, dict) or not isinstance(B, dict):
				return A or B
		return dict([(a, join(A.get(a), B.get(a))) for a in set(A.keys()) | set(B.keys())])

def recipeworker(cmds, cList, mytime, header, cright, xp_to_level, out_q):
	totals = {}
	for cmd in cmds:
		totals.update(costCraft(cmd[0],cmd[1],cmd[2],cmd[3],deepcopy(cList),mytime,header,cright,xp_to_level))
	out_q.put(totals)

def main():
	mytime = "<span class=\"localtime\">" + datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S')+'+00:00</span>'
	print datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
	# Will hold level:total xp pairs (array)
	xp_to_level = [0]
	# populate the xp chart
	for i in range(1,410):
		xp_to_level.append(xpreq(i)+xp_to_level[i-1])

	cList = {}
	cList = appendCosts()

	out_q = Queue()
	rList = []
	#TODO change the way flags are passed so it is easier to understand

	cooking_karma = join(Chef.recipes, Chef_karma.recipes)
	rList.append([("cooking_karma_fast.html",cooking_karma,True,False),("cooking_karma_fast_light.html",cooking_karma,True,False)])
	rList.append([("cooking_karma.html",cooking_karma,False,False),("cooking_karma_light.html",cooking_karma,False,False)])
	rList.append([("cooking_fast.html",Chef.recipes,True,False),("cooking.html",Chef.recipes,False,False)])

	rList.append([("jewelcraft_fast.html",Jeweler.recipes,True,False),("jewelcraft.html",Jeweler.recipes,False,False),("jewelcraft_craft_all.html",Jeweler.recipes,False,True)])

	rList.append([("artificing_fast.html",Artificer.recipes,True,False),("artificing.html",Artificer.recipes,False,False),("artificing_craft_all.html",Artificer.recipes,False,True)])

	rList.append([("weaponcraft_fast.html",Weaponsmith.recipes,True,False),("weaponcraft.html",Weaponsmith.recipes,False,False),("weaponcraft_craft_all.html",Weaponsmith.recipes,False,True)])

	rList.append([("huntsman_fast.html",Huntsman.recipes,True,False),("huntsman.html",Huntsman.recipes,False,False),("huntsman_craft_all.html",Huntsman.recipes,False,True)])

	rList.append([("armorcraft_fast.html",Armorsmith.recipes,True,False),("armorcraft.html",Armorsmith.recipes,False,False),("armorcraft_craft_all.html",Armorsmith.recipes,False,True)])

	rList.append([("tailor_fast.html",Tailor.recipes,True,False),("tailor.html",Tailor.recipes,False,False),("tailor_craft_all.html",Tailor.recipes,False,True)])

	rList.append([("leatherworking_fast.html",Leatherworker.recipes,True,False),("leatherworking.html",Leatherworker.recipes,False,False),("leatherworking_craft_all.html",Leatherworker.recipes,False,True)])

	nprocs = len(rList)

	procs = []
	global header
	global cright

	for i in range(nprocs):
		p = Process(target=recipeworker,args=(rList[i],cList,mytime,header,cright,xp_to_level,out_q))
		procs.append(p)
		p.start()

	totals = {}
	for i in range(nprocs):
		totals.update(out_q.get())

	for p in procs:
		p.join()

	maketotals(totals,mytime)
	print datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
	print "Starting upload"
	myFtp = FTP(ftp_url)
	myFtp.login(ftp_user,ftp_pass)
	for item in ["cooking_fast.html", "cooking_karma_fast.html", "cooking_karma_fast_light.html", "leatherworking_fast.html", "tailor_fast.html", "artificing_fast.html", "jewelcraft_fast.html", "weaponcraft_fast.html", "huntsman_fast.html", "armorcraft_fast.html", "cooking.html", "cooking_karma.html", "cooking_karma_light.html", "leatherworking.html", "tailor.html", "artificing.html", "jewelcraft.html", "weaponcraft.html", "huntsman.html", "armorcraft.html", "leatherworking_craft_all.html", "tailor_craft_all.html", "artificing_craft_all.html", "jewelcraft_craft_all.html", "weaponcraft_craft_all.html", "huntsman_craft_all.html", "armorcraft_craft_all.html", "total.html"]:
		with open(item,'rb') as f:
			myFtp.storbinary('STOR /gw2crafts.net/'+item,f)
		os.remove(item)
	myFtp.close()


# If ran directly, call main
if __name__ == '__main__':
	main()
