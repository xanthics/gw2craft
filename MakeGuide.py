#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Author: Jeremy Parks
Purpose: Generates a crafting guide based on current market prices
Note: Requires Python 3.7.x
'''

import math
from itertools import chain

import Globals
# Localized text
from translations import Localcz, Localde, Localen, Locales, Localfr, Localptbr, Localzh
from auto_gen import Items_de, Items_en, Items_es, Items, Items_fr, Items_zh
from collections import defaultdict
from MyPrint import printtofile


# scribe hack for single use recipes
badrecipe = []

# convert rarities to their xp multiplier
def rarityNum(num):
	if num == 'Rare':
		return 3.25
	elif num == 'Masterwork':
		return 2.0
	else:
		return 1.0


# compute the xp gain of a single craft
def xpgain(level, typ, minlvl):
	if '{},{},{}'.format(level, typ, minlvl) in Globals.table:
		return Globals.table['{},{},{}'.format(level, typ, minlvl)]
#	print(('Key miss with: {},{},{}'.format(level, typ, minlvl)))
	span = 0.0
	mult = 0.0
	if typ == 1: # refinement
		span = 25.0 
		mult = .3
	elif typ == 2: # part
		span = 25.0 
		mult = .6
	elif typ == 3: # item
		span = 40.0
		mult = 1.4
	elif typ == 4: # exotic weapon/armor
		span = 250.0
		mult = 1.85
	# xp_gain(N) = xp_req(N+1) * multiplier * (1.0 - (N - N_min) / span)
	gain = Globals.xpreq(level+1) * mult * (1.0 - (level - minlvl) / span)
	if gain < 0.0 or level - minlvl >= span:
		return 0.0
	return math.ceil(gain)


# compute what level would be after crafting items, assume order is refine > parts > discovery > items
def compute_level(_xp, craftlist, tlvl, xp_to_level):
	level = tlvl
	while xp_to_level[level+1] < _xp:
		level += 1
	for i,d in craftlist['ptitem']:
		_xp += int(i*xpgain(level,d,tlvl-25))
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
	# Non exotic weapon/armor crafts
	for i,d in (x for x in craftlist['discovery'] if not x[1] == 4):
		_xp += int((i+1)*xpgain(level,d,tlvl))
		while xp_to_level[level+1] < _xp:
			level += 1
	for i,d in (x for x in craftlist['item'] if not x[1] == 4):
		_xp += int(i*xpgain(level,d,tlvl))
		while xp_to_level[level+1] < _xp:
			level += 1
	# Exotic weapon/armor crafts
	for i,d in (x for x in craftlist['discovery'] if x[1] == 4):
		_xp += int((i+1)*xpgain(level,d,tlvl))
		while xp_to_level[level+1] < _xp:
			level += 1
	for i,d in (x for x in craftlist['item'] if x[1] == 4):
		_xp += int(i*xpgain(level,d,tlvl))
		while xp_to_level[level+1] < _xp:
			level += 1
	return _xp


# calculate the total xp 
def xp_calc(refines,parts,item,discoveries,mod,base_level,actu_level,typ):
	weight = 0.0
	weight += xpgain(actu_level,1,base_level)*refines
	weight += xpgain(actu_level,2,base_level)*parts
	weight += xpgain(actu_level,typ,base_level)*item*mod
	weight += xpgain(actu_level,typ,base_level)*discoveries*(1+mod)
	return weight


# Compute a guide
def costCraft(filename, c_recipes, fast, craftexo, mTiers, cList, mytime, xp_to_level, backupkey, free, modi=0.54):
	# TODO Hack, fix this
	# This is changing the recipe for Bronze Ingot to use 2 Copper Ore.
	if 19679 in c_recipes[0]:
		c_recipes[0][19679][19697] = 2

	rsps = dict([(38166, 38208), (38167, 38209), (38434, 38297), (38432, 38296), (38433, 38295), (38162, 38207)])
	craftcount = {} # Used to track current xp per tier
	make = {} # make list per tier
	pmake = {} # make list of "prior tier" items per tier
	buy = defaultdict(int) # buy list
	sell = defaultdict(int) # sell list
	tierbuy = None # buy list per tier, not used by cooking
	tiers = mTiers[::-1]
	non_item = ['Refinement', 'Insignia', 'Inscription', 'Component']

	# add recipes to cList
	for tier in c_recipes:
		for item in list(c_recipes[tier].keys()):
			if item in cList:# and item not in [1000190, 1000144, 1000277, 1000333]: # scribe recipes
				if not cList[item]['recipe']:
					cList[item]['recipe'] = []
				cList[item]['recipe'].append(c_recipes[tier][item])
				if "discover" in Items.ilist[item]:
					cList[item]['discover'].append(-1)
				else:
					cList[item]['discover'].append(0)
				if not 'tier' in cList[item]:
					cList[item]['tier'] = []
				cList[item]['tier'].append(tier) 

			else: 
				# gw2 api didn't have information about the item yet.
				# This should only happen when items are recently added to game
				print("Missing Item from itemlist: {}".format(item))
				del(c_recipes[tier][item])
				continue
#				exit(-1)

	# TODO Fix this, hack for scribe
	global mod
	mod = modi
	makeQueuecraft = makeQueuecraftnosub
	if "scribe" in filename:
		# something is broken with refinements in scribe guides, fix later
#		makeQueuecraft = makeQueuecraftwithsub
		mod = 0.45

	# Cooking guides don't use tierbuy, but they do care about karma items
	if "cook" in filename:
		if Globals.karmin: # this will be false the first time a cooking guide is called
			topl = []
			for top in sorted(Globals.karmin, key=lambda k: Globals.karmin[k], reverse=True)[:5]:
				topl.append(top)
			# "Almond","Apple","Avocado","Banana","Black Bean","Celery Stalk","Cherry","Chickpea","Coconut","Cumin","Eggplant","Green Bean","Horseradish Root","Kidney Bean","Lemon","Lime","Mango","Nutmeg Seed","Peach","Pear","Pinenut","Shallot"
			for i in [12337,  12165,  12340,  12251,  12237,  12240,  12338,  12515,  12350,  12256,  12502,  12232,  12518,  12239,  12252,  12339,  12543,  12249,  12503,  12514,  12516,  12517]:
				if not i in topl:
					cList[i]['cost'] = 99999999
	elif not craftexo: # 400+ doesn't care about tierbuy
		tierbuy = {0:defaultdict(int),75:defaultdict(int),150:defaultdict(int),225:defaultdict(int),300:defaultdict(int)}
		buy[19704] = 0.0 # Lump of Tin
		tierbuy[0][19704] = 0.0 # Lump of Tin

	for tier in range(0,500,25):#tiers:
		make[tier] = defaultdict(int)
		pmake[tier] = defaultdict(int)
		craftcount[tier] = {'refine':0.0,'part':[],'ptitem':[],'item':[],'discovery':[],'current_xp':xp_to_level[tier]}

	tcost = 0 # total cost
	treco = 0 # total recovery

	if craftexo:
		for i in range(0,400,25):
			craftcount[i]['current_xp'] = xp_to_level[i+25] + 1

		if 475 in tiers:
			if filename == "jewelcraft_400.html":
				tiers = [450,425,475,400]
			else:
				tiers = [425,450,475,400]

		for tier in tiers:
			bucket = {}
			bkey = []

			while craftcount[tier]['current_xp'] < xp_to_level[tier + 25]:
				bucket = makeQueuecraft(c_recipes[400], cList,craftcount,tier,xp_to_level,craftexo)
				bkey = sorted(bucket, reverse=True)
				
				tcost += bucket[bkey[0]]['cost']
				treco += cList[bucket[bkey[0]]['item_id']]['w'] * int(cList[bucket[bkey[0]]['item_id']]['output_item_count'])
				sell[bucket[bkey[0]]['item_id']] += int(cList[bucket[bkey[0]]['item_id']]['output_item_count'])
				sole = 0
				ttier = tier
				recalc = {tier:0} # always recalc the tier we are on
				for item in bucket[bkey[0]]['make']:
					val = 4 if cList[item]['rarity'] == 'Exotic' else 3
					if val == 3 and tier > 425 and 400 in cList[item]['tier']:
						ttier = 425
					elif val == 4 or 400 in cList[item]['tier']:
						ttier = tier
					else: 
						ttier = cList[item]['tier'][-1]
					index = 0
					if tier in cList[item]['tier']:
						index = cList[item]['tier'].index(tier)
					else:
						while len(cList[item]['tier']) > index+1 and int(cList[item]['tier'][index]) > tier:
							index += 1
					if not cList[item]['type'] in non_item and not cList[item]['discover'][index]:
						cList[item]['discover'][index] = 1
						craftcount[ttier]['discovery'].append((rarityNum(cList[item]['rarity']),val))
						make[ttier][item] += 1
					elif not cList[item]['type'] in non_item:
						craftcount[ttier]['item'].append((rarityNum(cList[item]['rarity']),val))
						make[ttier][item] += 1
					elif cList[item]['type'] == 'Refinement':
						if item == 19679: # Bronze Ingot
							craftcount[int(cList[item]['tier'][index])]['refine'] += 0.2
						else:
							craftcount[int(cList[item]['tier'][index])]['refine'] += 1.0
						make[int(cList[item]['tier'][index])][item] += 1
					else:
						if item in [13063,  13189,  13207,  13219,  13045,  13022,  13075,  13177,  13096,  13033] and not sole: # Sole IDs
							sole +=1
						else:
							craftcount[int(cList[item]['tier'][index])]['part'].append(rarityNum(cList[item]['rarity']))
						make[int(cList[item]['tier'][index])][item] += 1
					recalc[int(cList[item]['tier'][index])] = 0

				for ctier in recalc:
					craftcount[ctier]['current_xp'] = compute_level((xp_to_level[ctier] if ctier == 0 or xp_to_level[ctier] >= craftcount[ctier-25]['current_xp'] else craftcount[ctier-25]['current_xp']), craftcount[ctier],400,xp_to_level)

				for item in bucket[bkey[0]]['buy']:
					buy[item] += 1

				if set(rsps.keys()).intersection(set(bucket[bkey[0]]['make'])):
					cList[set(rsps.keys()).intersection(set(bucket[bkey[0]]['make'])).pop()]['RecipeLearned'] = True
	else: 
	# start at last bucket(375) and fill towards 0 bucket
		for tier in tiers:
			bucket = {}
			bkey = []
			# if this is a fast guide, choose our 1 item to craft
			if fast and (not tier == 375 or "cook" in filename):
				bucket = makeQueuecraft(c_recipes[tier], cList,craftcount,tier,xp_to_level,craftexo)
				bkey = sorted(bucket, reverse=True)
				# If we already made an "Item" this tier from another recipe, keep making that item
				if make[tier] and "cook" in filename: 
					bkey = []
					for item in bucket:
						if bucket[item]['item_id'] == list(make[tier].keys())[0]:
							bkey.append(item)
							break
				else:
					while cList[bucket[bkey[0]]['item_id']]['type'] in non_item:
						bkey.pop(0)

			while craftcount[tier]['current_xp'] < xp_to_level[tier + 25]:
				# We still want to compute every make on fast guides for the 375-400 range
				if fast and tier == 375 and "cook" not in filename:
					bucket = {}
					bucket = makeQueuecraft(c_recipes[tier], cList,craftcount,tier,xp_to_level,craftexo)
					bkey = sorted(bucket, reverse=True)
				elif not fast:
					if 0:#not tier == 0 and craftcount[tier][u'current_xp'] <= xp_to_level[tier+10]:
						bucket = makeQueuecraft(dict(chain(iter(c_recipes[tier].items()),iter(c_recipes[tier-25].items()))), cList,craftcount,tier,xp_to_level,craftexo)
					else:
						bucket = makeQueuecraft(c_recipes[tier], cList,craftcount,tier,xp_to_level,craftexo)
					bkey = sorted(bucket, reverse=True)

				tcost += bucket[bkey[0]]['cost']
				treco += cList[bucket[bkey[0]]['item_id']]['w'] * int(cList[bucket[bkey[0]]['item_id']]['output_item_count'])
				sell[bucket[bkey[0]]['item_id']] += int(cList[bucket[bkey[0]]['item_id']]['output_item_count'])
				sole = 0
				recalc = {tier:0} # always recalc the tier we are on
				for item in bucket[bkey[0]]['make']:
					index = 0
					if tier in cList[item]['tier']:
						index = cList[item]['tier'].index(tier)
					else:
						while len(cList[item]['tier']) > index+1 and int(cList[item]['tier'][index]) > tier:
							index += 1
					if item == bucket[bkey[0]]['item_id'] and int(cList[item]['tier'][index]) < tier:
						craftcount[tier]['ptitem'].append(rarityNum(cList[item]['rarity']),3)
						pmake[tier][item] += 1
					elif not cList[item]['type'] in non_item and not cList[item]['discover'][index]:
						cList[item]['discover'][index] = 1
						craftcount[int(cList[item]['tier'][index])]['discovery'].append((rarityNum(cList[item]['rarity']),3))
						make[int(cList[item]['tier'][index])][item] += 1
					elif not cList[item]['type'] in non_item:
						craftcount[int(cList[item]['tier'][index])]['item'].append((rarityNum(cList[item]['rarity']),3))
						make[int(cList[item]['tier'][index])][item] += 1
					elif cList[item]['type'] == 'Refinement':
						if item == 19679: # Bronze Ingot
							craftcount[int(cList[item]['tier'][index])]['refine'] += 0.2
						else:
							craftcount[int(cList[item]['tier'][index])]['refine'] += 1.0
						make[int(cList[item]['tier'][index])][item] += 1
					else:
						if item in [13063,  13189,  13207,  13219,  13045,  13022,  13075,  13177,  13096,  13033] and not sole: # Sole IDs
							sole +=1
						else:
							craftcount[int(cList[item]['tier'][index])]['part'].append(rarityNum(cList[item]['rarity']))
						make[int(cList[item]['tier'][index])][item] += 1
					recalc[int(cList[item]['tier'][index])] = 0
					if item in [78380, 78437, 78614, 78713]:
						global badrecipe
						badrecipe.append(item)

				for ctier in recalc:
					craftcount[ctier]['current_xp'] = compute_level((xp_to_level[ctier] if ctier == 0 or xp_to_level[ctier] >= craftcount[ctier-25]['current_xp'] else craftcount[ctier-25]['current_xp']), craftcount[ctier],ctier,xp_to_level)

				t = int(math.floor(tier/75.0)*75)
				if t == 375:
					t = 300

				if "cook" in filename or craftexo:
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
				if set(rsps.keys()).intersection(set(bucket[bkey[0]]['make'])):
					cList[set(rsps.keys()).intersection(set(bucket[bkey[0]]['make'])).pop()]['RecipeLearned'] = True

	# TODO add check for buying bronze ingot and reduce by amount we add, remove if <0
	if 19679 in make[0]:
		var = 5 - (make[0][19679] % 5)
		if var in [1, 2, 3, 4]:
			make[0][19679] += var
			tierbuy[0][19697] += 2 * var
			tierbuy[0][19704] += 0.2 * var
			buy[19697] += 2 * var
			buy[19704] += 0.2 * var
			tcost += cList[19697]['cost'] * var + 8.0 * (0.2 * var)
		make[0][19679] = make[0][19679] / 5

	if 19704 in buy and buy[19704] == 0.0:
		del (buy[19704])
		del (tierbuy[0][19704])

	printtofile(tcost, treco, sell, craftexo, mTiers, Globals.mydeepcopy(make), Globals.mydeepcopy(pmake), Globals.mydeepcopy(buy), Globals.mydeepcopy(tierbuy), Globals.mydeepcopy(cList), filename, mytime, Items_de.ilist, Localde, backupkey, free)
	printtofile(tcost, treco, sell, craftexo, mTiers, Globals.mydeepcopy(make), Globals.mydeepcopy(pmake), Globals.mydeepcopy(buy), Globals.mydeepcopy(tierbuy), Globals.mydeepcopy(cList), filename, mytime, Items_fr.ilist, Localfr, backupkey, free)
	printtofile(tcost, treco, sell, craftexo, mTiers, Globals.mydeepcopy(make), Globals.mydeepcopy(pmake), Globals.mydeepcopy(buy), Globals.mydeepcopy(tierbuy), Globals.mydeepcopy(cList), filename, mytime, Items_es.ilist, Locales, backupkey, free)
	printtofile(tcost, treco, sell, craftexo, mTiers, Globals.mydeepcopy(make), Globals.mydeepcopy(pmake), Globals.mydeepcopy(buy), Globals.mydeepcopy(tierbuy), Globals.mydeepcopy(cList), filename, mytime, Items_en.ilist, Localcz, backupkey, free)
	printtofile(tcost, treco, sell, craftexo, mTiers, Globals.mydeepcopy(make), Globals.mydeepcopy(pmake), Globals.mydeepcopy(buy), Globals.mydeepcopy(tierbuy), Globals.mydeepcopy(cList), filename, mytime, Items_en.ilist, Localptbr, backupkey, free)
	printtofile(tcost, treco, sell, craftexo, mTiers, Globals.mydeepcopy(make), Globals.mydeepcopy(pmake), Globals.mydeepcopy(buy), Globals.mydeepcopy(tierbuy), Globals.mydeepcopy(cList), filename, mytime, Items_zh.ilist, Localzh, backupkey, free)
	totals = {}
	totals.update(printtofile(tcost, treco, sell, craftexo, mTiers, Globals.mydeepcopy(make), pmake, buy, tierbuy, Globals.mydeepcopy(cList), filename, mytime, Items_en.ilist, Localen, backupkey, free))
	return totals


# given an item, determine if it is better to craft its sub items, or buy them.  return the recipe.
# include cost for current state, and xp generated.
def calcRecipecraft(recipe,items,craftcount,tier,itier,xp_to_level,craftexo):
	global badrecipe
	level = 0
	while xp_to_level[int(level)] < craftcount[int(tier)]['current_xp']:
		level += 1
	make = []
	buy = []
	cost = 0
	non_item = ['Refinement', 'Insignia', 'Inscription', 'Component']
	# Find the recipe we are looking for
	index = 0
	for i in range(len(items[recipe]['tier'])):
		if items[recipe]['tier'][i] == int(itier):
			index = i
			break

	# impossible to make item at this point.
	if int(items[recipe]['tier'][index]) > int(itier):
		return 9999999999, -99999999999, make, buy
	make.append(recipe)
	# TODO hack for scribe
	if recipe in badrecipe:
		xptotal = 0
	elif int(items[recipe]['tier'][index]) < int(tier) and not items[recipe]['type'] in non_item and not craftexo:
		xptotal = xp_calc(0,0,1,0,rarityNum(items[recipe]['rarity']),int(items[recipe]['tier'][index]),level,3)
	elif not items[recipe]['type'] in non_item and not items[recipe]['discover'][index]:
		xptotal = xp_calc(0,0,0,1,rarityNum(items[recipe]['rarity']),int(items[recipe]['tier'][index]),level,4 if craftexo and items[recipe]['rarity'] == 'Exotic' else 3)
	elif not items[recipe]['type'] in non_item:
		xptotal = xp_calc(0,0,1,0,rarityNum(items[recipe]['rarity']),int(items[recipe]['tier'][index]),level,4 if craftexo and items[recipe]['rarity'] == 'Exotic' else 3)
	elif items[recipe]['type'] == 'Refinement':
		if 19679 == recipe:
			xptotal = math.ceil(xp_calc(1,0,0,0,1.0,int(items[recipe]['tier'][index]),level,3)*0.2)
		else:
			xptotal = xp_calc(1,0,0,0,1.0,int(items[recipe]['tier'][index]),level,4 if craftexo and items[recipe]['rarity'] == 'Exotic' else 3)
	else:
		if recipe in [13063,  13189,  13207,  13219,  13045,  13022,  13075,  13177,  13096,  13033]: # Sole
			xptotal = xp_calc(0,1,0,0,1.0,int(items[recipe]['tier'][index]),level,4 if craftexo and items[recipe]['rarity'] == 'Exotic' else 3)*0.5
		else:
			xptotal = xp_calc(0,1,0,0,1.0,int(items[recipe]['tier'][index]),level,4 if craftexo and items[recipe]['rarity'] == 'Exotic' else 3)

	mycost = 0
	for item in items[recipe]['recipe'][index]:
		mycost += items[item]['cost']*items[recipe]['recipe'][index][item]
	if recipe in badrecipe:
		mycost += 9999999999

	for item in items[recipe]['recipe'][index]:
		if not items[item]['recipe'] == None:
			# if we have seen this item before, return its cached value
			if item in Globals.TLcache.hash:
				tcost = Globals.TLcache.hash[item]["cost"]
				txptotal = Globals.TLcache.hash[item]["xptotal"]
				tmake = Globals.TLcache.hash[item]["make"]
				tbuy = Globals.TLcache.hash[item]["buy"]
			else:
				tcost, txptotal, tmake, tbuy = calcRecipecraft(item,items,craftcount,items[item]['tier'][0],int(items[recipe]['tier'][index]),xp_to_level,craftexo)
				Globals.TLcache.hash[item] = {}
				Globals.TLcache.hash[item]["cost"] = tcost
				Globals.TLcache.hash[item]["xptotal"] = txptotal
				Globals.TLcache.hash[item]["make"] = tmake
				Globals.TLcache.hash[item]["buy"] = tbuy

			# Add the cost of the recipe to the inscription
			rsps = dict([(38166, 38208), (38167, 38209), (38434, 38297), (38432, 38296), (38433, 38295), (38162, 38207)])
			if item in list(rsps.keys()) and not 'RecipeLearned' in items[item]:
				tcost += items[rsps[item]]['cost']

			if tcost < items[item]['cost'] or float(xptotal+txptotal)/float(mycost+(tcost-items[item]['cost'])*items[recipe]['recipe'][index][item]) >= float(xptotal)/float(mycost):
				global mod
				xptotal += txptotal*items[recipe]['recipe'][index][item]*mod
				cost += tcost*items[recipe]['recipe'][index][item]
				buy += tbuy*items[recipe]['recipe'][index][item]
				make += tmake*items[recipe]['recipe'][index][item]
			else:
				buy += [item]*items[recipe]['recipe'][index][item]
				cost += items[item]['cost']*items[recipe]['recipe'][index][item]
		else:
			buy += [item]*items[recipe]['recipe'][index][item]
			cost += items[item]['cost']*items[recipe]['recipe'][index][item]
	return cost, xptotal, make, buy


def makeQueuecraftnosub(recipes,items,craftcount,tier,xp_to_level,craftexo):
	Globals.TLcache.hash = {}  # clear the item cache
	outdict = {}
	non_item = ['Refinement', 'Insignia', 'Inscription', 'Component']

	level = 0
	while xp_to_level[int(level)] < craftcount[int(tier)]['current_xp']:
		level += 1
	for recipe in list(recipes.keys()):
		index = 0
		for i in range(len(items[recipe]['tier'])):
			if items[recipe]['tier'][i] == int(tier):
				index = i
				break
		# swap which line is commented if you want guides that include "make 83 epaulets" for 25 copper savings
		if not items[recipe]['type'] in non_item and xp_calc(0,0,1,0,rarityNum(items[recipe]['rarity']),int(items[recipe]['tier'][index]),level,4 if items[recipe]['rarity'] == 'Exotic' else 3):
#		if int(items[recipe][u'tier']) > int(tier)-24:
			cost, xptotal, make, buy = calcRecipecraft(recipe,items,craftcount,tier,tier,xp_to_level,craftexo)
			# Uncomment these 3 lines and comment the 4th if you want guides that try to make the lowest total price after sellback
#			if items[recipe][u'w'] > cost:
#			   weight = float(items[recipe][u'w'] - cost)*100000.0
#			elif xptotal:
			if xptotal:
				weight = float(xptotal)/float(cost)
			else:
				weight = -1.0*float(cost)

			# don't want to collide keys
			while weight in outdict:
				weight -= 0.0001
			outdict[weight] = {'item_id':recipe,'w':xptotal,'make':make,'buy':buy,'cost':cost}

	return outdict


def makeQueuecraftwithsub(recipes,items,craftcount,tier,xp_to_level,craftexo):
	Globals.TLcache.hash = {}  # clear the item cache
	outdict = {}
	non_item = ['Refinement', 'Insignia', 'Inscription', 'Component']

	level = 0
	while xp_to_level[int(level)] < craftcount[int(tier)]['current_xp']:
		level += 1
	for recipe in list(recipes.keys()):
		cost, xptotal, make, buy = calcRecipecraft(recipe,items,craftcount,tier,tier,xp_to_level,craftexo)
		if xptotal:
			weight = float(xptotal)/float(cost)
		else:
			weight = -1.0*float(cost)

		# don't want to collide keys
		while weight in outdict:
			weight -= 0.0001
		outdict[weight] = {'item_id':recipe,'w':xptotal,'make':make,'buy':buy,'cost':cost}

	return outdict

