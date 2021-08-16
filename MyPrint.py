#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Author: Jeremy Parks
Purpose: Contains all functions for printing guides
Note: Requires Python 3.7.x
'''
import math
import Globals
from collections import defaultdict
import output


# Format copper values so they are easier to read
from auto_gen import mod_recipes


def mFormat(line):
	line = int(line)

	if abs(line) >= 10000:
		return '{}<span class=\"goldIcon\"></span>{:02d}<span class=\"silverIcon\"></span>{:02d}<span class=\"copperIcon\"></span>'.format(line // 10000, (abs(line) % 10000) // 100, abs(line) % 100)
	elif abs(line) >= 100:
		return '{}<span class=\"silverIcon\"></span>{:02d}<span class=\"copperIcon\"></span>'.format(str(line // 100), abs(line) % 100)
	else:
		return '{}<span class=\"copperIcon\"></span>'.format(line)


def printtofile(tcost, treco, sell, craftexo, mTiers, make, pmake, buy, tierbuy, cList, filename, mytime, cListName, localText, backupkey, free):
	buttonList = []
	totals = {'free': free}
	if tierbuy:
		totals[filename.split('.')[0]] = {0: defaultdict(int), 75: defaultdict(int), 150: defaultdict(int), 225: defaultdict(int), 300: defaultdict(int), 'total': int(tcost)}
	else:
		totals[filename.split('.')[0]] = int(tcost)

	non_item = ['Refinement', 'Insignia', 'Inscription', 'Component']

	karma_items = {12337: {'note': "{} <br />{}".format(localText.pickins, localText.disa), 'cost': 77},  # Almond
				   12165: {'note': "{} <br />{}".format(localText.milton, localText.jack), 'cost': 35},  # Apple
				   12340: {'note': "{}".format(localText.makayla), 'cost': 77},  # Avocado
				   12251: {'note': "{} <br />{} <br />{} <br />{}".format(localText.jenks, localText.sangdo, localText.goran, localText.vejj), 'cost': 49},  # Banana
				   12237: {'note': "{} <br />{}".format(localText.jenks, localText.leius), 'cost': 49},  # Black Bean
				   12240: {'note': "{} <br />{}".format(localText.bjarni, localText.milton), 'cost': 35},  # Celery Stalk
				   12338: {'note': "{} <br />{}".format(localText.summers, localText.disa), 'cost': 77},  # Cherry
				   12515: {'note': "{}".format(localText.naknar), 'cost': 112},  # Chickpea
				   12350: {'note': "{}".format(localText.tunnira), 'cost': 112},  # Coconut
				   12256: {'note': "{} <br />{}".format(localText.sagum, localText.milton), 'cost': 35},  # Cumin
				   12502: {'note': "{}".format(localText.jenrys), 'cost': 154},  # Eggplant
				   12232: {'note': "{}".format(localText.albin), 'cost': 35},  # Green Bean
				   12518: {'note': "{} <br />{}".format(localText.laudren, localText.wupwup), 'cost': 112},  # Horseradish Root
				   12239: {'note': "{} <br />{} <br />{}".format(localText.brian, localText.kastaz, localText.hune), 'cost': 49},  # Kidney Bean
				   12252: {'note': "{} <br />{} <br />{}".format(localText.yoal, localText.hrappa, localText.milton), 'cost': 35},  # Lemon
				   12339: {'note': "{}".format(localText.shelp), 'cost': 77},  # Lime
				   12543: {'note': "{}".format(localText.crandle), 'cost': 203},  # Mango
				   12249: {'note': "{} <br />{}".format(localText.jenks, localText.milton), 'cost': 35},  # Nutmeg Seed
				   12503: {'note': "{}".format(localText.nrocroc), 'cost': 154},  # Peach
				   12514: {'note': "{}".format(localText.braxa), 'cost': 112},  # Pear
				   12516: {'note': "{}".format(localText.tholin), 'cost': 112},  # Pinenut
				   12517: {'note': "{}".format(localText.ichtaca), 'cost': 112}}  # Shallot

	karma_chef = {12159: {'note': localText.mcov, 'cost': 35},  # Cheese Wedge
				  12137: {'note': localText.mcov, 'cost': 35},  # Glass of Buttermilk
				  12152: {'note': localText.mcov, 'cost': 35},  # Packet of Yeast
				  12145: {'note': localText.mcov, 'cost': 49},  # Rice Ball
				  12325: {'note': localText.mcov, 'cost': 77},  # Bowl of Sour Cream
				  12141: {'note': localText.mcov, 'cost': 35},  # Tomato
				  12328: {'note': localText.mcov, 'cost': 77},  # Ginger Root
				  12245: {'note': localText.mcov, 'cost': 49},  # Basil Leaf
				  12235: {'note': localText.mcov, 'cost': 49}}  # Bell Pepper

	karma_recipe = {12131: {'note': localText.elain, 'cost': 35},  # Bowl of Watery Mushroom Soup
					12185: {'note': localText.bjarni, 'cost': 35},  # Handful of Bjarni's Rabbit Food
					12140: {'note': localText.hrouda, 'cost': 35},  # Bowl of Gelatinous Ooze Custard
					8587: {'note': localText.drottot, 'cost': 35},  # Poached Egg
					12211: {'note': localText.kevach, 'cost': 35},  # Bowl of Cold Wurm Stew
					12198: {'note': localText.vaastas, 'cost': 35},  # Celebratory Steak
					12133: {'note': localText.laewyn, 'cost': 35},  # Warden Ration
					12149: {'note': localText.krug, 'cost': 35},  # Bowl of Ettin Stew
					12203: {'note': localText.maxtar, 'cost': 35},  # Bowl of Dolyak Stew
					12139: {'note': localText.aidem, 'cost': 35},  # Bowl of Front Line Stew
					12150: {'note': localText.eda, 'cost': 35},  # Eda's Apple Pie
					12343: {'note': localText.kastaz, 'cost': 35},  # Kastaz Roasted Poultry
					12160: {'note': localText.auda, 'cost': 35},  # Loaf of Walnut Sticky Bread
					12154: {'note': localText.brian, 'cost': 35},  # Bowl of Outrider Stew
					12292: {'note': localText.glubb, 'cost': 35},  # Bowl of Degun Shun Stew
					12233: {'note': localText.tholin, 'cost': 154},  # Handful of Trail Mix
					12739: {'note': localText.triktiki, 'cost': 35},  # Triktiki Omelet
					12352: {'note': "{} ({} {})".format(localText.pochtecatl, mFormat(368), localText.valuePer), 'cost': 0},  # Griffon Egg Omelet
					12264: {'note': localText.nrocroc, 'cost': 35},  # Raspberry Pie
					12192: {'note': localText.victor, 'cost': 35},  # Beetletun Omelette
					19955: {'note': localText.mcov, 'cost': 350},  # Ravaging Intricate Wool Insignia
					19956: {'note': localText.mcov, 'cost': 350},  # Rejuvenating Intricate Wool Insignia
					19957: {'note': localText.mcov, 'cost': 350},  # Honed Intricate Wool Insignia
					19958: {'note': localText.mcov, 'cost': 350},  # Pillaging Intricate Wool Insignia
					19959: {'note': localText.mcov, 'cost': 350},  # Strong Intricate Wool Insignia
					19960: {'note': localText.mcov, 'cost': 350},  # Vigorous Intricate Wool Insignia
					19961: {'note': localText.mcov, 'cost': 350},  # Hearty Intricate Wool Insignia
					19962: {'note': localText.mcov, 'cost': 455},  # Ravaging Intricate Cotton Insignia
					19963: {'note': localText.mcov, 'cost': 455},  # Rejuvenating Intricate Cotton Insignia
					19964: {'note': localText.mcov, 'cost': 455},  # Honed Intricate Cotton Insignia
					19965: {'note': localText.mcov, 'cost': 455},  # Pillaging Intricate Cotton Insignia
					19966: {'note': localText.mcov, 'cost': 455},  # Strong Intricate Cotton Insignia
					19967: {'note': localText.mcov, 'cost': 455},  # Vigorous Intricate Cotton Insignia
					19968: {'note': localText.mcov, 'cost': 455},  # Hearty Intricate Cotton Insignia
					19969: {'note': localText.mcov, 'cost': 567},  # Carrion Intricate Linen Insignia
					19970: {'note': localText.mcov, 'cost': 567},  # Cleric's Intricate Linen Insignia
					19971: {'note': localText.mcov, 'cost': 567},  # Explorer's Intricate Linen Insignia
					19972: {'note': localText.mcov, 'cost': 567},  # Berserker's Intricate Linen Insignia
					19973: {'note': localText.mcov, 'cost': 567},  # Valkyrie Intricate Linen Insignia
					19974: {'note': localText.mcov, 'cost': 567},  # Rampager's Intricate Linen Insignia
					19975: {'note': localText.mcov, 'cost': 567},  # Knight's Intricate Linen Insignia
					19880: {'note': localText.mcov, 'cost': 672},  # Carrion Intricate Silk Insignia
					19881: {'note': localText.mcov, 'cost': 672},  # Cleric's Intricate Silk Insignia
					19882: {'note': localText.mcov, 'cost': 672},  # Explorer's Intricate Silk Insignia
					19883: {'note': localText.mcov, 'cost': 672},  # Berserker's Intricate Silk Insignia
					19886: {'note': localText.mcov, 'cost': 672},  # Valkyrie Intricate Silk Insignia
					19884: {'note': localText.mcov, 'cost': 672},  # Rampager's Intricate Silk Insignia
					19885: {'note': localText.mcov, 'cost': 672},  # Knight's Intricate Silk Insignia
					19934: {'note': localText.mcov, 'cost': 350},  # Ravaging Iron Imbued Inscription
					19935: {'note': localText.mcov, 'cost': 350},  # Rejuvenating Iron Imbued Inscription
					19936: {'note': localText.mcov, 'cost': 350},  # Honed Iron Imbued Inscription
					19937: {'note': localText.mcov, 'cost': 350},  # Pillaging Iron Imbued Inscription
					19938: {'note': localText.mcov, 'cost': 350},  # Strong Iron Imbued Inscription
					19939: {'note': localText.mcov, 'cost': 350},  # Vigorous Iron Imbued Inscription
					19940: {'note': localText.mcov, 'cost': 350},  # Hearty Iron Imbued Inscription
					19941: {'note': localText.mcov, 'cost': 455},  # Ravaging Steel Imbued Inscription
					19942: {'note': localText.mcov, 'cost': 455},  # Rejuvenating Steel Imbued Inscription
					19943: {'note': localText.mcov, 'cost': 455},  # Honed Steel Imbued Inscription
					19944: {'note': localText.mcov, 'cost': 455},  # Pillaging Steel Imbued Inscription
					19945: {'note': localText.mcov, 'cost': 455},  # Strong Steel Imbued Inscription
					19946: {'note': localText.mcov, 'cost': 455},  # Vigorous Steel Imbued Inscription
					19947: {'note': localText.mcov, 'cost': 455},  # Hearty Steel Imbued Inscription
					19948: {'note': localText.mcov, 'cost': 567},  # Carrion Darksteel Imbued Inscription
					19949: {'note': localText.mcov, 'cost': 567},  # Cleric's Darksteel Imbued Inscription
					19950: {'note': localText.mcov, 'cost': 567},  # Explorer's Darksteel Imbued Inscription
					19951: {'note': localText.mcov, 'cost': 567},  # Berserker's Darksteel Imbued Inscription
					19952: {'note': localText.mcov, 'cost': 567},  # Valkyrie Darksteel Imbued Inscription
					19953: {'note': localText.mcov, 'cost': 567},  # Rampager's Darksteel Imbued Inscription
					19954: {'note': localText.mcov, 'cost': 567},  # Knight's Darksteel Imbued Inscription
					19897: {'note': localText.mcov, 'cost': 672},  # Carrion Mithril Imbued Inscription
					19898: {'note': localText.mcov, 'cost': 672},  # Cleric's Mithril Imbued Inscription
					19899: {'note': localText.mcov, 'cost': 672},  # Explorer's Mithril Imbued Inscription
					19900: {'note': localText.mcov, 'cost': 672},  # Berserker's Mithril Imbued Inscription
					19903: {'note': localText.mcov, 'cost': 672},  # Valkyrie Mithril Imbued Inscription
					19901: {'note': localText.mcov, 'cost': 672},  # Rampager's Mithril Imbued Inscription
					19902: {'note': localText.mcov, 'cost': 672},  # Knight's Mithril Imbued Inscription
					19923: {'note': localText.mcov, 'cost': 896},  # inscr
					19920: {'note': localText.mcov, 'cost': 896},
					19917: {'note': localText.mcov, 'cost': 896},
					19918: {'note': localText.mcov, 'cost': 896},
					19919: {'note': localText.mcov, 'cost': 896},
					19922: {'note': localText.mcov, 'cost': 896},
					19921: {'note': localText.mcov, 'cost': 896},
					19912: {'note': localText.mcov, 'cost': 896},  # insig
					19913: {'note': localText.mcov, 'cost': 896},
					19910: {'note': localText.mcov, 'cost': 896},
					19911: {'note': localText.mcov, 'cost': 896},
					19915: {'note': localText.mcov, 'cost': 896},
					19914: {'note': localText.mcov, 'cost': 896},
					19916: {'note': localText.mcov, 'cost': 896},
					24543: {'note': localText.mcov, 'cost': 896},  # jewel
					24496: {'note': localText.mcov, 'cost': 896},
					24544: {'note': localText.mcov, 'cost': 896},
					24497: {'note': localText.mcov, 'cost': 896},
					24545: {'note': localText.mcov, 'cost': 896},
					24498: {'note': localText.mcov, 'cost': 896},
					24499: {'note': localText.mcov, 'cost': 896},
					24904: {'note': localText.mcov, 'cost': 231},  # Embellished Intricate Topaz Jewel
					24902: {'note': localText.mcov, 'cost': 231},  # Embellished Intricate Spinel Jewel
					24901: {'note': localText.mcov, 'cost': 231},  # Embellished Intricate Peridot Jewel
					24903: {'note': localText.mcov, 'cost': 231},  # Embellished Intricate Sunstone Jewel
					24899: {'note': localText.mcov, 'cost': 231},  # Embellished Intricate Carnelian Jewel
					24898: {'note': localText.mcov, 'cost': 231},  # Embellished Intricate Amethyst Jewel
					24900: {'note': localText.mcov, 'cost': 231},  # Embellished Intricate Lapis Jewel
					24911: {'note': localText.mcov, 'cost': 231},  # Embellished Gilded Topaz Jewel
					24905: {'note': localText.mcov, 'cost': 231},  # Embellished Gilded Amethyst Jewel
					24906: {'note': localText.mcov, 'cost': 231},  # Embellished Gilded Carnelian Jewel
					24907: {'note': localText.mcov, 'cost': 231},  # Embellished Gilded Lapis Jewel
					24908: {'note': localText.mcov, 'cost': 231},  # Embellished Gilded Peridot Jewel
					24909: {'note': localText.mcov, 'cost': 231},  # Embellished Gilded Spinel Jewel
					24910: {'note': localText.mcov, 'cost': 231},  # Embellished Gilded Sunstone Jewel
					24912: {'note': localText.mcov, 'cost': 231},  # Embellished Ornate Beryl Jewel
					24913: {'note': localText.mcov, 'cost': 231},  # Embellished Ornate Chrysocola Jewel
					24914: {'note': localText.mcov, 'cost': 231},  # Embellished Ornate Coral Jewel
					24915: {'note': localText.mcov, 'cost': 231},  # Embellished Ornate Emerald Jewel
					24916: {'note': localText.mcov, 'cost': 231},  # Embellished Ornate Opal Jewel
					24917: {'note': localText.mcov, 'cost': 231},  # Embellished Ornate Ruby Jewel
					24918: {'note': localText.mcov, 'cost': 231},  # Embellished Ornate Sapphire Jewel
					24919: {'note': localText.mcov, 'cost': 231},  # Embellished Brilliant Beryl Jewel
					24920: {'note': localText.mcov, 'cost': 231},  # Embellished Brilliant Chrysocola Jewel
					24921: {'note': localText.mcov, 'cost': 231},  # Embellished Brilliant Coral Jewel
					24922: {'note': localText.mcov, 'cost': 231},  # Embellished Brilliant Emerald Jewel
					24923: {'note': localText.mcov, 'cost': 231},  # Embellished Brilliant Opal Jewel
					24924: {'note': localText.mcov, 'cost': 231},  # Embellished Brilliant Ruby Jewel
					24925: {'note': localText.mcov, 'cost': 231},  # Embellished Brilliant Sapphire Jewel
					38162: {'note': "{} ({}: {} {})".format(localText.bRecipes, localText.rTP, mFormat(cList[38207]['cost']), localText.valuePer), 'cost': 0},  # Giver's Intricate Gossamer Insignia
					38166: {'note': "{} ({}: {} {})".format(localText.bRecipes, localText.rTP, mFormat(cList[38208]['cost']), localText.valuePer), 'cost': 0},  # Giver's Embroidered Silk Insignia
					38167: {'note': "{} ({}: {} {})".format(localText.bRecipes, localText.rTP, mFormat(cList[38209]['cost']), localText.valuePer), 'cost': 0},  # Giver's Embroidered Linen Insignia
					38434: {'note': "{} ({}: {} {})".format(localText.bRecipes, localText.rTP, mFormat(cList[38297]['cost']), localText.valuePer), 'cost': 0},  # Giver's Orichalcum-Imbued Inscription
					38432: {'note': "{} ({}: {} {})".format(localText.bRecipes, localText.rTP, mFormat(cList[38296]['cost']), localText.valuePer), 'cost': 0},  # Giver's Mithril-Imbued Inscription
					38433: {'note': "{} ({}: {} {})".format(localText.bRecipes, localText.rTP, mFormat(cList[38295]['cost']), localText.valuePer), 'cost': 0},  # Giver's Darksteel-Imbued Inscription
					}

	# Insignia -> Recipe Mapping.
	rsps = {38166: 38208,  # Giver's Embroidered Silk Insignia
			38167: 38209,  # Giver's Embroidered Linen Insignia
			38434: 38297,  # Giver's Orichalcum-Imbued Inscription
			38432: 38296,  # Giver's Mithril-Imbued Inscription
			38433: 38295,  # Giver's Darksteel-Imbued Inscription
			38162: 38207  # Giver's Intricate Gossamer Insignia
			}

	recipebuy = []
	for tier in range(0, 500, 25):
		for item in make[tier]:
			if item in karma_recipe:
				recipebuy.append(item)

	vendor = [19792, 19789, 19794, 19793, 19791, 19704, 19750, 19924, 12157, 12151, 12158, 12153, 12155,
			  12156, 12324, 12136, 12271, 8576, 13010, 13006, 13007, 13008, 19790, 62942, 70647, 75762,
			  1000352, 1000589, 1000574, 1000601, 1000403, 1000376, 1000223, 1000548, 1000209, 1000516,
			  1000620, 1000202, 1000582, 1000437, 1000413, 1000224, 46747]

	# "Jute Scrap","Bolt of Jute","Copper Ore","Copper Ingot","Bronze Ingot","Rawhide Leather Section","Stretched Rawhide Leather Square","Green Wood Log","Green Wood Plank","Wool Scrap","Bolt of Wool","Iron Ore","Silver Ore","Iron Ingot","Silver Ingot","Thin Leather Section","Cured Thin Leather Square","Soft Wood Log","Soft Wood Plank","Cotton Scrap","Bolt of Cotton","Spool of Cotton Thread","Iron Ore","Gold Ore","Gold Ingot","Steel Ingot","Coarse Leather Section","Cured Coarse Leather Square","Seasoned Wood Log","Seasoned Wood Plank","Linen Scrap","Bolt of Linen","Platinum Ore","Platinum Ingot","Darksteel Ingot","Rugged Leather Section","Cured Rugged Leather Square","Hard Wood Log","Hard Wood Plank","Silk Scrap","Bolt of Silk","Mithril Ore","Mithril Ingot","Thick Leather Section","Cured Thick Leather Square","Elder Wood Log","Elder Wood Plank", Orichalcum Ore, Ancient Wood Log
	basic = [19718, 19720, 19697, 19680, 19679, 19719, 19738, 19723, 19710, 19739, 19740, 19699, 19703, 19683, 19687,
			 19728, 19733, 19726, 19713, 19741, 19742, 19794, 19699, 19698, 19682, 19688, 19730, 19734, 19727, 19714,
			 19743, 19744, 19702, 19686, 19681, 19731, 19736, 19724, 19711, 19748, 19747, 19700, 19684, 19729, 19735,
			 19722, 19709, 19701, 19725, 19685, 19712, 19732, 19737, 19745, 19746]

	# Fine Materials
	basic_f = list(range(24272, 24301)) + [37897, 24363] + list(range(24341, 24359))

	# Rare Materials and Ectoplasm
	basic_r = list(range(24301, 24341)) + [19721]

	# Gems
	basic_g = list(range(24500, 24536)) + [37907, 24889] + list(range(24464, 24476)) + list(range(24870, 24877))

	# "Tiny Snowflake","Delicate Snowflake","Glittering Snowflake","Unique Snowflake","Pristine Snowflake","Piece of Candy Corn","Chattering Skull","Nougat Center","Plastic Fang"
	basic_h = list(range(38130, 38136)) + [36041, 36060, 36061, 36059]

	# "Artichoke","Asparagus Spear","Basil Leaf","Bay Leaf","Beet","Black Peppercorn","Blackberry","Blueberry","Butternut Squash","Carrot","Cayenne Pepper","Chili Pepper","Chocolate Bar","Cinnamon Stick","Clam","Clove","Coriander Seed","Dill Sprig","Egg","Head of Cabbage","Head of Cauliflower","Head of Garlic","Head of Lettuce","Kale Leaf","Leek","Mint Leaf","Mushroom","Onion","Orange","Oregano Leaf","Parsley Leaf","Parsnip","Passion Fruit","Piece of Candy Corn","Portobello Mushroom","Potato","Raspberry","Rosemary Sprig","Rutabaga","Sage Leaf","Sesame Seed","Slab of Poultry Meat","Slab of Red Meat","Snow Truffle","Spinach Leaf","Stick of Butter","Strawberry","Sugar Pumpkin","Tarragon Leaves","Thyme Leaf","Turnip","Vanilla Bean","Walnut","Yam","Zucchini","Green Onion", Omnomberry, Lotus Root
	basic_fo = [12512, 12505, 12245, 12247, 12161, 12236, 12537, 12255, 12511, 12134, 12504, 12331, 12229, 12258, 12327, 12534, 12531, 12336, 12143, 12332, 12532, 12163, 12238, 12333, 12508, 12536, 12147, 12142, 12351, 12244, 12246, 12507, 36731, 36041, 12334, 12135, 12254, 12335, 12535, 12243, 12342, 24360, 24359, 12144, 12241, 12138, 12253, 12538, 12506,
				12248, 12162, 12234, 12250, 12329, 12330, 12533, 12128, 12510]

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
			if localText.path == "":
				Globals.karmin[item] = buy[item]  # used by cooking to make a top 5 list
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
	karma_str = "<div class=\"s{0}\"><input type=\"checkbox\" /><span class=\"itemIcon\" style=\"background-image: url({1});\"></span><input type=\"number\" onkeypress=\"return event.charCode >= 48\" oninput=\"updateNeed(this, {2}, '{9}bv');\" id=\"{9}ih\" placeholder='0' min=\"0\" value=\"0\" /><input type=\"number\" id=\"{9}bv\" value='{2}' raw_copper='0' readonly data-need = \"more\" min=\"0\" /> <button title=\"" + localText.toggle + "\" class=\"{3} arrow\" id=\"{4}\">{5}</button><div class=\"lsbutton\" id=\"1{6}\">{7} <span class=\"karmaIcon\"></span> " + localText.valuePer + " 25 <br /> {8}</div></div>\n"
	collectable_str = "<div class=\"s{0}\"><input type=\"checkbox\" /><span class=\"itemIcon\" style=\"background-image: url({1});\"></span><input type=\"number\" onkeypress=\"return event.charCode >= 48\" oninput=\"updateNeed(this, {2}, '{6}bv');\" id=\"{6}ih\" placeholder='0' min=\"0\" value=\"0\" /><input type=\"number\" id=\"{6}bv\" value='{2}' raw_copper='{7}' class='vTotal' readonly data-need = \"more\" min=\"0\" /> <span class=\"{3} select_text\">{4}</span> ({5} " + localText.valuePer + ")</div>\n"

	title = ""
	# Page Title Part 1
	if "fast" in filename:
		title += localText.fGuides
	elif "all" in filename:
		title += localText.tGuides
	else:  # normal
		title += localText.nGuides
	# Page Title Part 2
	if filename in ["cooking_fast.html", "cooking.html"]:
		title += ': ' + localText.cooking + ' - ' + localText.nHearts
	elif filename in ["cooking_karma_fast.html", "cooking_karma.html"]:
		title += ': ' + localText.cooking + ' - ' + localText.aHearts
	elif filename in ["cooking_karma_fast_light.html", "cooking_karma_light.html"]:
		title += ': ' + localText.cooking + ' - ' + localText.tHearts
	elif filename in ["leatherworking_fast.html", "leatherworking.html", "leatherworking_400.html"]:
		title += ': ' + localText.lw
	elif filename in ["tailor_fast.html", "tailor.html", "tailor_400.html"]:
		title += ': ' + localText.tailor
	elif filename in ["artificing_fast.html", "artificing.html", "artificing_400.html", "artificing_450.html"]:
		title += ': ' + localText.art
	elif filename in ["jewelcraft_fast.html", "jewelcraft.html", "jewelcraft_400.html"]:
		title += ': ' + localText.jc
	elif filename in ["weaponcraft_fast.html", "weaponcraft.html", "weaponcraft_400.html", "weaponcraft_450.html"]:
		title += ': ' + localText.wc
	elif filename in ["huntsman_fast.html", "huntsman.html", "huntsman_400.html", "huntsman_450.html"]:
		title += ': ' + localText.hunt
	elif filename in ["armorcraft_fast.html", "armorcraft.html", "armorcraft_400.html"]:
		title += ': ' + localText.ac

	t = 0  # used to control div background color
	kt = 0  # karma total
	page = ['<!DOCTYPE html>\n']
	page.append('<html>\n')
	page.append('<head>\n')
	# Ezoic adwords
	page.append('''<!-- Ezoic Code -->
<script>var ezoicId = 39853;</script>
<script type="text/javascript" src="//go.ezoic.net/ezoic/ezoic.js"></script>
<!-- Ezoic Code -->
<!-- Ezoic Ad Testing Code-->
<script src="//g.ezoic.net/ezoic/ezoiclitedata.go?did=39853"></script>
<!-- Ezoic Ad Testing Code-->''')
	# Title Part 1
	page.append('	<title>' + title + ' - Guild Wars 2 Crafting Guide</title>\n')
	page.append('	<meta name="description" content="Guild Wars 2 always current crafting guide for ' + filename.split('.')[0].replace("_", " ").title() + '">\n')
	page.append('	<meta name="keywords" content="best videogames, free mmos, free mmorpg, best free mmorpg, best mmorpg, free to play, mmos, mmorpg, free game, online games, fantasy games, PC games, PC gaming, crafting guide, crafting guides, Guild Wars 2, Trading Post"/>\n')
	page.append('	<meta http-equiv="content-type" content="text/html;charset=UTF-8">\n')
	page.append('	<meta http-equiv="Cache-Control" content="public, max-age=1260">\n')
	page.append('	<link href="/css/layout.css" rel="stylesheet" type="text/css" />')
	page.append('	<link rel="icon" type="image/png" href="/fi.gif">\n')
	page.append('	<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.9.0/jquery.min.js"></script>\n')
#	page.append('	<script>(window.jQuery || document.write(\'<script src="http://ajax.aspnetcdn.com/ajax/jquery/jquery-1.9.0.min.js"></script>\'));</script>\n')
	page.append('	<script src="/js/menu.js" type="text/javascript"></script>\n')
	page.append('</head>\n')
	page.append('<body>\n%s\n' % (
		Globals.header.format(localText.path, localText.home, localText.nGuides, localText.fGuides, localText.special, localText.cooking, localText.nHearts, localText.tHearts, localText.aHearts, localText.jc, localText.art, localText.hunt, localText.wc, localText.ac, localText.lw, localText.tailor, localText.scribe, localText.totals, localText.about,
							  localText.lang, localText.lang_code, filename, 'f2p/' if free else '')))
	page.append("""<script> 
  (function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
  (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
  m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
  })(window,document,'script','//www.google-analytics.com/analytics.js','ga');

  ga('create', 'UA-38972433-1', 'auto');
  ga('send', 'pageview');

</script>""")
	page.append('<section class=\"main\">')
	page.append('<div style="width: 100%; border: 2px #fffaaa solid; border-left: 0px; border-right: 0px; background: #fffddd; height: 24px;">\n')
	page.append('<span class=\"warning\"></span><span style="position: relative; top: 4px;"><span style="color: red">%s</span>	%s: %s</span> <a href="/%s/%s%s" style="position: relative; top: 4px;">3 month link</a>\n' % (localText.warning1, localText.warning2, mytime, backupkey, localText.path, f'f2p/{filename}' if free else filename))
	page.append('</div><br />\n')
	if 'scribe' in filename:
		page.append('<div>\n')
		page.append("<p>Please email me at <a href=\"mailto:gw2crafts@live.com\">gw2crafts@live.com</a> if you would like your guild listed here.  The following guild(s) have the necessary crafting recipes unlocked and are accepting guests:</p>")
		page.append("<hr>")
		page.append("<p>Hearth of Owl [HoO] is grateful to share our scribing station with all scribes-in-training.  We are an NA guild, but still totally open to accepting EU members for scribing.</p>")
		page.append("<p>We are an experienced PvE guild that shares knowledge and resources to help new and returning players get acclimated to the vast, ever-changing world of Tyria.  We strive for a friendly and spoiler-free environment.</p>")
		page.append("<p>You can join our discord for more information and a faster guild invite.<br /><a href=\"https://discord.gg/BavHsUP\">https://discord.gg/BavHsUP</a></p>")
		page.append("<p>Otherwise, whisper or send an in-game mail to receive an invite.<br />ecstaseed.2109<br />archangel.4027</p>")
		page.append("<hr>")
		page.append('<button title=\"{}\" class =\"arrow\" id=\"scribehint\">{}</button><div class=\"lsbutton\" id=\"1scribehint\">\n'.format(localText.toggle, localText.scribetease))
		page.append('{}</div><br /></div><br />\n'.format(localText.scribeinfo))
		buttonList.append('scribehint')

	#	page.append(u"<div class=\"s{}\">{}: <button class=\"arrow {}\" title=\"{}\" id=\"{}{}\">{}</button> {}\n</div>\n".format(
	#		t, localText.discover, cList[item][u'rarity'], localText.toggle, item, tier, cListName[item], tstr))
	page.append("<strong>%s</strong><br />\n" % (localText.region))
	page.append(f"<strong>Notice:</strong> you are following a {'F2P' if free else 'Core'} guide.  <a href=\"{'/' if free else '/f2p/'}{localText.path}{filename}\">Click here for a {'Core' if free else 'F2P'} account guide</a>.<br />")
	#	# adword
	page.append('<div style="float:right;position:absolute;right:-320px;">\n')
	page.append('<!-- Ezoic - Large sidebar - sidebar -->\n<div id="ezoic-pub-ad-placeholder-103"></div>\n<!-- End Ezoic - Large sidebar - sidebar -->\n\n</div>\n')
	page.append(localText.moreInfo % ("<img src=\"/img/arrow.png\" alt=ARROW>"))
	page.append('<!-- Ezoic - page_title - under_page_title -->\n<div id="ezoic-pub-ad-placeholder-105">\n</div><!-- End Ezoic - page_title - under_page_title -->')
	# Page Title Part 1
	page.append('<h1>' + title + '</h1>')
	page.append('<dl>\n')
	page.append('	<dt>%s</dt>\n' % localText.iCost)
	page.append('	<dd>' + mFormat(tcost) + '</dd>\n')
	page.append('	<dt>%s</dt>\n' % localText.eRecovery)
	page.append('	<dd><span style="position: relative; left: -9px;">- ' + mFormat(treco) + '</span></dd>\n')
	page.append('	<dt>%s</dt>\n' % localText.fCost)
	page.append('	<dd style="border-top: 1px #666 solid;">' + mFormat(tcost - treco) + '</dd>\n')
	page.append('</dl>')
	page.append('<div class="clear"></div>')

	remaining = '<dl>\n	<dt>{}</dt>\n	<dd><span class="mygold">{}</span><span class=\"goldIcon\"></span><span class="mysilver">{}</span><span class=\"silverIcon\"></span><span class="mycopper">{}</span><span class=\"copperIcon\"></span></dd>\n</dl><div class="clear"></div>'.format(localText.remCost, int(tcost // 10000), int((tcost // 100) % 100), int(tcost % 100))

	page.append('<br /><button title=\"%s\" class=\"arrow\" id=\"tcost\">%s:</button><div class=\"lsbutton\" id=\"1tcost\">' % (localText.toggle, localText.sList))
	for line in sorted(sell):
		if cList[line]['w'] > 0:
			t = (t + 1) % 2
			page.append('<div class=\"s%i\">%3i <span class=\"%s select_text\">%s</span> - %s %s</div>\n' % (t, sell[line], cList[line]['rarity'], cListName[line], (localText.soldVia % mFormat(cList[line]['w'])), localText.method[cList[line]['sellMethod']]))

	page.append("</div><script type=\"text/javascript\">$('#1tcost').hide();</script><br />")
	buttonList.append('tcost')
	page.append('<!-- Ezoic - page_title_2 - under_page_title -->\n<div id="ezoic-pub-ad-placeholder-106"></div>\n<!-- End Ezoic - page_title_2 - under_page_title -->')
	page.append('<br /><br /><input type="text" id="api_key" name="api key" placeholder="Enter API key here" style=\'text-align: center;\'><br />')
	page.append('<button type="button" onclick="updateBank(document.getElementById(\'api_key\').value.trim());" style=\'text-align: center;\'>Get Bank Content</button>\n')
	page.append('<br /> The API key you enter needs \'inventories\' permission to work.  <a href="https://account.arena.net/applications/create">You can generate a key here</a>. <br /><br />')
	page.append('Clicking the button will update the quantities of all items in your bank and material storage that are used in this guide.')
	page.append(
		"<br /><br /><div class=\"s1\"><input type=\"checkbox\" /><span class=\"itemIcon\" style=\"background-image: url(/apple-touch-icon-144x144-precomposed.png);\"></span><input type=\"text\" value='Have' readonly style=\"width: 4em;\" /><input type=\"text\" value='Need' readonly style=\"width: 4em;\" /> Name of an item and its per unit cost.</div>\n")

	if b_vendor or b_karma_c or b_karma_w:
		page.append(remaining)
		page.append("<h2>%s</h2>\n" % localText.buyVendor)
		if b_karma_c or b_karma_w:
			page.append("<span class=\"karmaIcon\"></span>{}<br /><br />\n".format(localText.kNote))

		for item in sorted(b_karma_w):
			t = (t + 1) % 2
			page.append(karma_str.format(t, cList[item]['icon'], buy[item], cList[item]['rarity'], item, cListName[item], item, karma_items[item]['cost'], karma_items[item]['note'], item))
			buttonList.append(item)
			kt += int(math.ceil(buy[item] / 25.0) * karma_items[item]['cost'])

		for item in sorted(b_karma_c):
			t = (t + 1) % 2
			page.append(karma_str.format(t, cList[item]['icon'], buy[item], cList[item]['rarity'], item, cListName[item], item, karma_chef[item]['cost'], karma_chef[item]['note'], item))
			buttonList.append(item)
			kt += int(math.ceil(buy[item] / 25.0) * karma_chef[item]['cost'])

		for item in sorted(b_vendor):
			t = (t + 1) % 2
			page.append(
				"<div class=\"s{0}\"><input type=\"checkbox\" /><span class=\"itemIcon\" style=\"background-image: url({1});\"></span><input type=\"number\" onkeypress=\"return event.charCode >= 48\" oninput=\"updateNeed(this, {2}, '{8}bv');\" id=\"{8}ih\" placeholder='0' min=\"0\" value=\"0\" /><input type=\"number\" id=\"{8}bv\" value='{2}' raw_copper='{9}' class='vTotal' readonly data-need = \"more\" min=\"0\" /> <span class=\"{3} select_text\">{4}</span> ({5} {6} from {7})</div>\n".format(
					t, cList[item]['icon'], buy[item], cList[item]['rarity'], cListName[item], mFormat(cList[item]['cost']), localText.valuePer, localText.method[0], item, cList[item]['cost']))

	page.append('<!-- Ezoic - first_paragraph - under_first_paragraph -->\n<div id="ezoic-pub-ad-placeholder-107"></div>\n<!-- End Ezoic - first_paragraph - under_first_paragraph -->')
	if recipebuy:
		page.append("<h2>%s</h2>\n" % localText.bRecipes)
		for item in recipebuy:
			t = (t + 1) % 2
			if karma_recipe[item]['cost']:
				page.append(("<div class=\"s%d\"><input type=\"checkbox\" /><span class=\"itemIcon\" style=\"background-image: url(%s);\"></span><button title=\"" + localText.toggle + "\" class=\"arrow %s\" id=\"%d\">%s</button><div class=\"lsbutton\" id=\"1%d\">%i <span class=\"karmaIcon\"></span>, %s</div></div>\n") % (
				t, cList[item]['icon'], cList[item]['rarity'], item, cListName[item], item, karma_recipe[item]['cost'], karma_recipe[item]['note']))
			else:
				if item in rsps:
					page.append(("<div class=\"s%d\"><input type=\"checkbox\" /><span class=\"itemIcon\" style=\"background-image: url(%s);\"></span><button title=\"" + localText.toggle + "\" class=\"arrow %s\" id=\"%d\">%s</button><div class=\"lsbutton\" id=\"1%d\">%s</div></div>\n") % (
					t, cList[item]['icon'], cList[item]['rarity'], item, cListName[rsps[item]], item, karma_recipe[item]['note']))
				else:
					page.append(("<div class=\"s%d\"><input type=\"checkbox\" /><span class=\"itemIcon\" style=\"background-image: url(%s);\"></span><button title=\"" + localText.toggle + "\" class=\"arrow %s\" id=\"%d\">%s</button><div class=\"lsbutton\" id=\"1%d\">%s</div></div>\n") % (
					t, cList[item]['icon'], cList[item]['rarity'], item, cListName[item], item, karma_recipe[item]['note']))
			buttonList.append(item)
			kt += int(karma_recipe[item]['cost'])
	if kt:
		page.append('<br />\nTotal <span class=\"karmaIcon\"></span>: ' + str(kt) + '<br />\n')
	if b_common or b_fine or b_rare or b_gem or b_holiday or b_food:
		page.append(remaining)
		page.append('<h2>%s</h2>\n' % localText.collectibles)
		for item in sorted(b_common):
			t = (t + 1) % 2
			page.append(collectable_str.format(t, cList[item]['icon'], buy[item], cList[item]['rarity'], cListName[item], mFormat(cList[item]['cost']), item, cList[item]['cost']))
		for item in sorted(b_fine):
			t = (t + 1) % 2
			page.append(collectable_str.format(t, cList[item]['icon'], buy[item], cList[item]['rarity'], cListName[item], mFormat(cList[item]['cost']), item, cList[item]['cost']))
		for item in sorted(b_rare):
			t = (t + 1) % 2
			page.append(collectable_str.format(t, cList[item]['icon'], buy[item], cList[item]['rarity'], cListName[item], mFormat(cList[item]['cost']), item, cList[item]['cost']))
		for item in sorted(b_gem):
			t = (t + 1) % 2
			page.append(collectable_str.format(t, cList[item]['icon'], buy[item], cList[item]['rarity'], cListName[item], mFormat(cList[item]['cost']), item, cList[item]['cost']))
		for item in sorted(b_holiday):
			t = (t + 1) % 2
			page.append(collectable_str.format(t, cList[item]['icon'], buy[item], cList[item]['rarity'], cListName[item], mFormat(cList[item]['cost']), item, cList[item]['cost']))
		for item in sorted(b_food):
			t = (t + 1) % 2
			page.append(collectable_str.format(t, cList[item]['icon'], buy[item], cList[item]['rarity'], cListName[item], mFormat(cList[item]['cost']), item, cList[item]['cost']))
	page.append('<!-- Ezoic - second_paragraph - under_second_paragraph -->\n<div id="ezoic-pub-ad-placeholder-108"></div>\n<!-- End Ezoic - second_paragraph - under_second_paragraph -->')
	if b_mix:
		page.append(remaining)
		page.append('<h2>%s</h2>\n' % localText.mixedTP)
		for item in sorted(b_mix):
			t = (t + 1) % 2
			page.append(collectable_str.format(t, cList[item]['icon'], buy[item], cList[item]['rarity'], cListName[item], mFormat(cList[item]['cost']), item, cList[item]['cost']))
	page.append('<!-- Ezoic - mid_content - mid_content -->\n<div id="ezoic-pub-ad-placeholder-109"></div>\n<!-- End Ezoic - mid_content - mid_content -->')

	page.append("<br />\n<br />\n<h2>%s</h2>\n" % localText.make)
	# adword adaptive
	page.append('<br /><div style="width: 100%;display:block;">\n')
	page.append('<!-- Ezoic - first banner - mid_content -->\n<div id="ezoic-pub-ad-placeholder-104"></div>\n<!-- End Ezoic - first banner - mid_content -->\n')
	page.append('</div>\n')

	page.append("<button title=\"" + localText.toggle + "\" class =\"info\" id=\"show_all\">%s</button><br />" % localText.expand)
	page.append("<button title=\"" + localText.toggle + "\" class =\"info\" id=\"hide_all\">%s</button>" % localText.collapse)
	rt = 0
	for tier in mTiers:

		if tier in [75, 425]:  # long content
			page.append('<!-- Ezoic - long_1 - long_content -->\n<div id="ezoic-pub-ad-placeholder-110"></div>\n<!-- End Ezoic - long_1 - long_content -->')
		elif tier in [100]:  # long content
			page.append('<!-- Ezoic - long_2 - long_content -->\n<div id="ezoic-pub-ad-placeholder-111"></div>\n<!-- End Ezoic - long_2 - long_content -->')
		elif tier in [150, 450]:  # longer
			page.append('<!-- Ezoic - longer_1 - longer_content -->\n<div id="ezoic-pub-ad-placeholder-112"></div>\n<!-- End Ezoic - longer_1 - longer_content -->')
		elif tier in [175]:  # longer
			page.append('<!-- Ezoic - longer_2 - longer_content -->\n<div id="ezoic-pub-ad-placeholder-113"></div>\n<!-- End Ezoic - longer_2 - longer_content -->')
		elif tier in [225, 475]:  # longest
			page.append('<!-- Ezoic - longest_1 - longest_content -->\n<div id="ezoic-pub-ad-placeholder-114"></div>\n<!-- End Ezoic - longest_1 - longest_content -->')
		elif tier in [250]:  # longest
			page.append('<!-- Ezoic - longest_2 - longest_content -->\n<div id="ezoic-pub-ad-placeholder-115"></div>\n<!-- End Ezoic - longest_2 - longest_content -->')
		elif tier in [300]:  # bottom
			page.append('<!-- Ezoic - bottom_1 - bottom_of_page -->\n<div id="ezoic-pub-ad-placeholder-116"></div>\n<!-- End Ezoic - bottom_1 - bottom_of_page -->')
		elif tier in [325]:  # bottom
			page.append('<!-- Ezoic - bottom_2 - bottom_of_page -->\n<div id="ezoic-pub-ad-placeholder-117"></div>\n<!-- End Ezoic - bottom_2 - bottom_of_page -->')

		if tier == 400:
			precraft = sorted([i for i in make if make[i] and i < 400])
			if precraft:
				page.append(("<br />\n<h3>%s:<400</h3>\n") % (localText.level))
				for lvl in precraft:
					for item in make[lvl]:
						t = (t + 1) % 2
						page.append("<div class=\"s" + str(t) + "\">" + localText.make + ":%3i <span class=\"%s select_text\">%s</span></div>\n" % (make[lvl][item], cList[item]['rarity'], cListName[item]))

		if tierbuy and tier in [0, 75, 150, 225, 300]:
			tt = 0
			tc = tier + 75
			if tier == 300:
				tc += 25
			page.append(("<br /><br /><h4>%s:<button title=\"" + localText.toggle + "\" class =\"info\" id=\"" + str(tier) + "tier\">%s</button></h4>\n<div class=\"lsbutton\" id=\"1" + str(tier) + "tier\">") % ((localText.tier % (tier / 75 + 1, tier, tc)), localText.buyList % (tier / 75 + 1)))
			page.append("<h5>%s</h5>" % localText.blNotice)
			for item in sorted(tierbuy[tier]):
				t = (t + 1) % 2
				page.append(("<div class=\"s" + str(t) + "\"><input type=\"checkbox\" /><span class=\"itemIcon\" style=\"background-image: url(" + cList[item]['icon'] + ");\"></span><span class=\"quantity\">%i</span> <span class=\"%s select_text\">%s</span> (%4s " + localText.valuePer + ")</div>\n") % (
				tierbuy[tier][item], cList[item]['rarity'], cListName[item], mFormat(cList[item]['cost'])))
				tt += tierbuy[tier][item] * cList[item]['cost']
			buttonList.append(str(tier) + 'tier')
			rt += tt
			totals[filename.split('.')[0]][tier] = tt
			page.append("</div><h4>%s</h4>\n" % (localText.costRT % (mFormat(tt), mFormat(rt))))
		page.append(("<br />\n<h3>%s:%3i</h3>\n") % (localText.level, tier))
		if pmake[tier]:
			for item in sorted(pmake[tier]):
				t = (t + 1) % 2
				page.append("<div class=\"s" + str(t) + "\"><input type=\"checkbox\" />" + localText.make + ":%3i <span class=\"%s select_text\">%s</span> (From %i tier) </div>\n" % (pmake[tier][item], cList[item]['rarity'], cListName[item], tier - 25))
		for item in sorted(make[tier], key=make[tier].get, reverse=True):
			if cList[item]['type'] == 'Refinement':
				t = (t + 1) % 2
				if item in mod_recipes.ilist:  # multi output recipe
					page.append(("<div class=\"s" + str(t) + "\"><input type=\"checkbox\" />" + localText.make + ":%3i <span class=\"%s select_text\">%s</span> (%s)</div>\n") % (make[tier][item], cList[item]['rarity'], cListName[item], localText.bNote.format(mod_recipes.ilist[item])))
				else:
					page.append("<div class=\"s" + str(t) + "\"><input type=\"checkbox\" />" + localText.make + ":%3i <span class=\"%s select_text\">%s</span></div>\n" % (make[tier][item], cList[item]['rarity'], cListName[item]))
		for item in sorted(make[tier], key=make[tier].get, reverse=True):
			if cList[item]['type'] in non_item and not cList[item]['type'] == 'Refinement':
				t = (t + 1) % 2
				if item in mod_recipes.ilist:  # multi output recipe
					page.append(("<div class=\"s" + str(t) + "\"><input type=\"checkbox\" />" + localText.make + ":%3i <span class=\"%s select_text\">%s</span> (%s)</div>\n") % (make[tier][item], cList[item]['rarity'], cListName[item], localText.bNote.format(mod_recipes.ilist[item])))
				else:
					page.append("<div class=\"s" + str(t) + "\"><input type=\"checkbox\" />" + localText.make + ":%3i <span class=\"%s select_text\">%s</span></div>\n" % (make[tier][item], cList[item]['rarity'], cListName[item]))

		if tier == 425:
			for item in sorted(make[tier]):
				try:
					index = cList[item]['tier'].index(400)
				except:
					index = 0
				if cList[item]['discover'][index] == 1 and not cList[item]['rarity'] == 'Exotic':
					cList[item]['discover'][index] = 0
					if make[tier][item] > 1:
						make[tier][item] -= 1
					else:
						del (make[tier][item])
					t = (t + 1) % 2
					tstr = "<div class=\"sbutton\" id=\"1" + str(item) + str(tier) + "\">"
					for s in cList[item]['recipe'][index]:
						tstr += "\n<br />\t<span class=\"itemIcon\" style=\"background-image: url(" + cList[s]['icon'] + ");\"></span> <span class=\"" + cList[s]['rarity'] + ' select_text\">' + cListName[s] + "</span> (" + str(cList[item]['recipe'][index][s]) + ")"
					tstr += "</div><br />"
					page.append("<div class=\"s" + str(t) + "\"><input type=\"checkbox\" />" + localText.discover + ": <button class=\"arrow " + cList[item]['rarity'] + '\" title=\"' + localText.toggle + '\" id=\"' + str(item) + str(tier) + '\">' + cListName[item] + "</button> " + tstr + "\n</div>\n")
					buttonList.append(str(item) + str(tier))
			for item in sorted(make[tier]):
				if not cList[item]['type'] in non_item and not cList[item]['rarity'] == 'Exotic':
					t = (t + 1) % 2
					page.append("<div class=\"s" + str(t) + "\"><input type=\"checkbox\" />" + localText.make + ":%3i <span class=\"%s select_text\">%s</span></div>\n" % (make[tier][item], cList[item]['rarity'], cListName[item]))
			for item in sorted(make[tier]):
				try:
					index = cList[item]['tier'].index(400)
				except:
					index = 0
				if cList[item]['discover'][index] == 1 and cList[item]['rarity'] == 'Exotic':
					cList[item]['discover'][index] = 0
					if make[tier][item] > 1:
						make[tier][item] -= 1
					else:
						del (make[tier][item])
					t = (t + 1) % 2
					tstr = "<div class=\"sbutton\" id=\"1" + str(item) + str(tier) + "\">"
					if craftexo:
						inde = 400
					else:
						inde = tier
					for s in cList[item]['recipe'][index]:
						tstr += "\n<br />\t<span class=\"itemIcon\" style=\"background-image: url(" + cList[s]['icon'] + ");\"></span> <span class=\"" + cList[s]['rarity'] + ' select_text\">' + cListName[s] + "</span> (" + str(cList[item]['recipe'][index][s]) + ")"
					tstr += "</div><br />"
					page.append("<div class=\"s" + str(t) + "\"><input type=\"checkbox\" />" + localText.discover + ": <button class=\"arrow " + cList[item]['rarity'] + '\" title=\"' + localText.toggle + '\" id=\"' + str(item) + str(tier) + '\">' + cListName[item] + "</button> " + tstr + "\n</div>\n")
					buttonList.append(str(item) + str(tier))
			for item in sorted(make[tier]):
				if not cList[item]['type'] in non_item and cList[item]['rarity'] == 'Exotic':
					t = (t + 1) % 2
					page.append("<div class=\"s" + str(t) + "\"><input type=\"checkbox\" />" + localText.make + ":%3i <span class=\"%s select_text\">%s</span></div>\n" % (make[tier][item], cList[item]['rarity'], cListName[item]))
		else:
			for item in sorted(make[tier]):
				if craftexo:
					try:
						index = cList[item]['tier'].index(400)
					except:
						index = 0
				else:
					index = cList[item]['tier'].index(tier)
				if cList[item]['discover'][index] == 1:
					cList[item]['discover'][index] = 0
					if make[tier][item] > 1:
						make[tier][item] -= 1
					else:
						del (make[tier][item])
					t = (t + 1) % 2
					tstr = "<div class=\"sbutton\" id=\"1" + str(item) + str(tier) + "\">"
					for s in cList[item]['recipe'][index]:
						tstr += "\n<br />\t<span class=\"itemIcon\" style=\"background-image: url(" + cList[s]['icon'] + ");\"></span> <span class=\"" + cList[s]['rarity'] + ' select_text\">' + cListName[s] + "</span> (" + str(cList[item]['recipe'][index][s]) + ")"
					tstr += "</div><br />"
					page.append("<div class=\"s" + str(t) + "\"><input type=\"checkbox\" />" + localText.discover + ": <button class=\"arrow " + cList[item]['rarity'] + '\" title=\"' + localText.toggle + '\" id=\"' + str(item) + str(tier) + '\">' + cListName[item] + "</button> " + tstr + "\n</div>\n")
					buttonList.append(str(item) + str(tier))
			for item in sorted(make[tier]):
				if not cList[item]['type'] in non_item:
					t = (t + 1) % 2
					page.append("<div class=\"s" + str(t) + "\"><input type=\"checkbox\" />" + localText.make + ":%3i <span class=\"%s select_text\">%s</span></div>\n" % (make[tier][item], cList[item]['rarity'], cListName[item]))
	page.append('<br />\n<h3>%s:%i</h3>\n' % (localText.level, tier + 25))
	t = (t + 1) % 2
	page.append("<div class=\"s" + str(t) + "\">%s</div>\n" % localText.finish)
	# adword adaptive
	page.append('<br /><div style="width: 100%;display:block;">\n')
	page.append('<div id="sponsor"><div id="github_image"><a href="https://github.com/sponsors/xanthics"><img alt="Sponsor me on Github!" src="img/github_sponsor.png" class="sponsor_img"></a></div><div id="patreon_image"><a href="https://www.patreon.com/xanthics"><img alt="Become a Patron!" src="img/become_a_patron_button@2x.png" class="sponsor_img"></a></div></div>')
	page.append('<br/ ><hr><br />\n<!-- Ezoic - Tail - bottom_of_page -->\n<div id="ezoic-pub-ad-placeholder-102"></div>\n<!-- End Ezoic - Tail - bottom_of_page --></div>\n')
	page.append('</section>\n')
	page.append('%s\n<script type="text/javascript">\n' % localText.cright)
	for item in buttonList:
		page.append("$(\"#" + str(item) + "\").click(function () {\n\t$(\"#1" + str(item) + "\").toggle();});\n")
	page.append("$(\".sbutton\").hide();\n")
	page.append("$(\".lsbutton\").hide();\n")
	page.append("$(\"#show_all\").click(function () {$(\".sbutton\").show();")
	page.append("});\n$(\"#hide_all\").click(function () {$(\".sbutton\").hide();")
	page.append('});\n</script>\n')
	page.append('</body>\n')
	page.append('</html>\n')

	output.write_file(f"{'f2p/' if free else ''}{localText.path}", filename, ''.join(page), backupkey)
	return totals


def maketotals(totals, mytime, localText, free):
	tpage1 = ""
	tpage2 = ""
	tpage3 = ""

	page = '''
<!DOCTYPE html>
<html>
<head>
	<!-- Ezoic Code -->
	<script>var ezoicId = 39853;</script>
	<script type="text/javascript" src="//go.ezoic.net/ezoic/ezoic.js"></script>
	<!-- Ezoic Code -->
	<!-- Ezoic Ad Testing Code-->
	<script src="//g.ezoic.net/ezoic/ezoiclitedata.go?did=39853"></script>
	<!-- Ezoic Ad Testing Code-->
	<title>Totals</title>
	<meta name="description" content="Guild Wars 2 always current crafting guide price totals">
	<meta name="keywords" content="best videogames, free mmos, free mmorpg, best free mmorpg, best mmorpg, free to play, mmos, mmorpg, free game, online games, fantasy games, PC games, PC gaming, crafting guide, crafting guides, Guild Wars 2, Trading Post"/>
	<meta http-equiv="content-type" content="text/html;charset=UTF-8">
	<meta http-equiv="Cache-Control" content="public, max-age=1260">

	<link href="/css/layout.css" rel="stylesheet" type="text/css" />
	<link rel="icon" type="image/png" href="/fi.gif" />

	<script src="//ajax.googleapis.com/ajax/libs/jquery/1.9.0/jquery.min.js"></script>
	<script src="/js/menu.js" type="text/javascript"></script>
</head>
<body>'''
	page += """<script> 
  (function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
  (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
  m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
  })(window,document,'script','//www.google-analytics.com/analytics.js','ga');

  ga('create', 'UA-38972433-1', 'auto');
  ga('send', 'pageview');

</script>"""
	page += Globals.header.format(localText.path, localText.home, localText.nGuides, localText.fGuides, localText.special, localText.cooking, localText.nHearts, localText.tHearts, localText.aHearts, localText.jc, localText.art, localText.hunt, localText.wc, localText.ac, localText.lw, localText.tailor, localText.scribe, localText.totals, localText.about,
								  localText.lang, localText.lang_code, 'total.html', 'f2p/' if free else '')
	page += "<section class=\"main\">\n<strong>%s</strong><br />\n" % (localText.region)
	page += f"<strong>Notice:</strong> you are following a {'F2P' if free else 'Core'} guide.  <a href=\"{'/' if free else '/f2p/'}{localText.path}total.html\">Click here for a {'Core' if free else 'F2P'} account guide</a>.<br />"
	page += "<h5 style=\"text-align:center;\">" + localText.updated + ": " + mytime + "</h5>"
	# adword
	page += '<div style="float:right;position:absolute;right:-320px;">\n \
<!-- Ezoic - Large sidebar - sidebar -->\n\
<div id="ezoic-pub-ad-placeholder-103"></div>\n\
<!-- End Ezoic - Large sidebar - sidebar -->\n\
</div>\n'
	page += localText.note
	page += '	<table>'
	page += '<tr><th>' + localText.craft + '</th><th>' + localText.nGuides + '</th><th>' + localText.fGuides + '</th><th>1-200</th></tr>\n'
	page += '<tr><td>' + localText.nHearts + '</td><td>' + mFormat(totals['cooking']) + '</td><td>' + mFormat(totals['cooking_fast']) + '</td><td>' + mFormat(totals['cooking_fast_200']) + '</td></tr>\n'
	page += '<tr><td>' + localText.tHearts + '</td><td>' + mFormat(totals['cooking_karma_light']) + '</td><td>' + mFormat(totals['cooking_karma_fast_light']) + '</td></tr>\n'
	page += '<tr><td>' + localText.aHearts + '</td><td>' + mFormat(totals['cooking_karma']) + '</td><td>' + mFormat(totals['cooking_karma_fast']) + '</td><td>' + mFormat(totals['cooking_karma_fast_200']) + '</td></tr>\n'

	page += "</table>\n<br />\n<table>\n<tr><th>" + localText.craft + "</th><th>" + localText.nGuides + "</th><th>" + localText.fGuides + "</th><th>400-450</th><th>400-500</th></tr>\n"

	tpage1 += "</table>\n<br />\n<table>\n<tr><th>" + localText.nGuides + "</th><th>" + localText.tiers + " 1</th><th>" + localText.tiers + " 2</th><th>" + localText.tiers + " 3</th><th>" + localText.tiers + " 4</th><th>" + localText.tiers + " 5</th></tr>\n"
	tpage2 += "</table>\n<br />\n<table>\n<tr><th>" + localText.fGuides + "</th><th>" + localText.tiers + " 1</th><th>" + localText.tiers + " 2</th><th>" + localText.tiers + " 3</th><th>" + localText.tiers + " 4</th><th>" + localText.tiers + " 5</th></tr>\n"

	ctnc = 0
	ctfc = 0
	cttc = 0
	ct4c = 0
	ct45c = 0
	for i in [('jewelcraft', 'jewelcraft_fast', localText.jc),
			  ('artificing', 'artificing_fast', 'artificing_450', 'artificing_400', localText.art),
			  ('huntsman', 'huntsman_fast', 'huntsman_450', 'huntsman_400', localText.hunt),
			  ('weaponcraft', 'weaponcraft_fast', 'weaponcraft_450', 'weaponcraft_400', localText.wc),
			  ('armorcraft', 'armorcraft_fast', 'armorcraft_450', 'armorcraft_400', localText.ac),
			  ('leatherworking', 'leatherworking_fast', 'leatherworking_450', 'leatherworking_400', localText.lw),
			  ('tailor', 'tailor_fast', 'tailor_450', 'tailor_400', localText.tailor)]:

		ind = 2
		if len(i) == 3:
			page += '<tr><td>' + i[ind] + '</td><td>' + mFormat(totals[i[0]]['total']) + '</td><td>' + mFormat(totals[i[1]]['total']) + '</td></tr>\n'
		else:
			ind = 4
			page += '<tr><td>' + i[ind] + '</td><td>' + mFormat(totals[i[0]]['total']) + '</td><td>' + mFormat(totals[i[1]]['total']) + '</td><td>' + mFormat(totals[i[2]]) + '</td><td>' + mFormat(totals[i[3]]) + '</td></tr>\n'
			ct45c += totals[i[2]]
			ct4c += totals[i[3]]

		tpage1 += '<tr><td>' + i[ind] + '</td><td>' + mFormat(totals[i[0]][0]) + '</td><td>' + mFormat(totals[i[0]][75]) + '</td><td>' + mFormat(totals[i[0]][150]) + '</td><td>' + mFormat(totals[i[0]][225]) + '</td><td>' + mFormat(totals[i[0]][300]) + '</td></tr>\n'
		tpage2 += '<tr><td>' + i[ind] + '</td><td>' + mFormat(totals[i[1]][0]) + '</td><td>' + mFormat(totals[i[1]][75]) + '</td><td>' + mFormat(totals[i[1]][150]) + '</td><td>' + mFormat(totals[i[1]][225]) + '</td><td>' + mFormat(totals[i[1]][300]) + '</td></tr>\n'

		ctnc += totals[i[0]]['total']
		ctfc += totals[i[1]]['total']

	page += '<tr><td><strong>' + localText.totals + '</strong></td><td><strong>' + mFormat(ctnc) + '</strong></td><td><strong>' + mFormat(ctfc) + '</strong></td><td><strong>' + mFormat(ct45c) + '</strong></td><td><strong>' + mFormat(ct4c) + '</strong></td></tr>\n<br />\n'
	page += '<tr><td>' + localText.scribe + '</td><td>' + mFormat(totals['scribe']['total']) + '</td></tr></table>\n'
	tpage1 += '<tr><td>' + localText.scribe + '</td><td>' + mFormat(totals['scribe'][0]) + '</td><td>' + mFormat(totals['scribe'][75]) + '</td><td>' + mFormat(totals['scribe'][150]) + '</td><td>' + mFormat(totals['scribe'][225]) + '</td><td>' + mFormat(totals['scribe'][300]) + '</td></tr>\n'

	tpage1 += ' </table>\n<br />'
	tpage2 += ' </table>\n<br />'
	tpage3 += ' </table>'

	page += tpage1 + tpage2

	# adword adaptive
	page += '<div id="sponsor"><div id="github_image"><a href="https://github.com/sponsors/xanthics"><img alt="Sponsor me on Github!" src="img/github_sponsor.png" class="sponsor_img"></a></div><div id="patreon_image"><a href="https://www.patreon.com/xanthics"><img alt="Become a Patron!" src="img/become_a_patron_button@2x.png" class="sponsor_img"></a></div></div>'
	page += '<br/ ><hr><br /><div style="width: 100%;display:block;">\n \
	<!-- Ezoic - Tail - bottom_of_page -->\n \
<div id="ezoic-pub-ad-placeholder-102"></div>\n\
<!-- End Ezoic - Tail - bottom_of_page --></div>\n'
	page += '\n</section>\n' + localText.cright
	page += '</body>\n'
	page += '</html>\n'

	output.write_file(f"{'f2p/' if free else ''}{localText.path}", 'total.html', page)
	return
