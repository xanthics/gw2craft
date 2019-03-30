#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Author: Jeremy Parks
Purpose: Contains all functions for printing guides
Note: Requires Python 2.7.x
'''
import math
import Globals
from collections import defaultdict
import output


# Format copper values so they are easier to read
def mFormat(line):
	line = int(line)

	if abs(line) >= 10000:
		return '{}<span class=\"goldIcon\"></span>{:02d}<span class=\"silverIcon\"></span>{:02d}<span class=\"copperIcon\"></span>'.format(line//10000,(abs(line)%10000)//100,abs(line)%100)
	elif abs(line) >= 100:
		return '{}<span class=\"silverIcon\"></span>{:02d}<span class=\"copperIcon\"></span>'.format(str(line//100),abs(line)%100)
	else:
		return '{}<span class=\"copperIcon\"></span>'.format(line)

def printtofile(tcost, treco, sell, craftexo, mTiers, make, pmake, buy, tierbuy, cList, filename, mytime, cListName, localText):
	scribewarn = 'This is a beta guide, read all steps before attempting.'
	buttonList = []
	totals = {}
	if tierbuy:
		totals[filename.split('.')[0]] = {0:defaultdict(int),75:defaultdict(int),150:defaultdict(int),225:defaultdict(int),300:defaultdict(int),u'total':int(tcost)}
	else:
		totals[filename.split('.')[0]] = int(tcost)

	non_item = [u'Refinement', u'Insignia', u'Inscription', u'Component']

	karma_items = {12337:{u'note':u"{} <br />{}".format(localText.pickins,localText.disa),u'cost':77}, # Almond
					12165:{u'note':u"{} <br />{}".format(localText.milton,localText.jack),u'cost':35}, # Apple
					12340:{u'note':u"{}".format(localText.makayla),u'cost':77}, # Avocado
					12251:{u'note':u"{} <br />{} <br />{} <br />{}".format(localText.jenks,localText.sangdo,localText.goran,localText.vejj),u'cost':49}, # Banana
					12237:{u'note':u"{} <br />{}".format(localText.jenks,localText.leius),u'cost':49}, # Black Bean
					12240:{u'note':u"{} <br />{}".format(localText.bjarni,localText.milton),u'cost':35}, # Celery Stalk
					12338:{u'note':u"{} <br />{}".format(localText.summers,localText.disa),u'cost':77}, # Cherry
					12515:{u'note':u"{}".format(localText.naknar),u'cost':112}, # Chickpea
					12350:{u'note':u"{}".format(localText.tunnira),u'cost':112}, # Coconut
					12256:{u'note':u"{} <br />{}".format(localText.sagum,localText.milton),u'cost':35}, # Cumin
					12502:{u'note':u"{}".format(localText.jenrys),u'cost':154}, # Eggplant
					12232:{u'note':u"{}".format(localText.albin),u'cost':35}, # Green Bean
					12518:{u'note':u"{} <br />{}".format(localText.laudren,localText.wupwup),u'cost':112}, # Horseradish Root
					12239:{u'note':u"{} <br />{} <br />{}".format(localText.brian,localText.kastaz,localText.hune),u'cost':49}, # Kidney Bean
					12252:{u'note':u"{} <br />{} <br />{}".format(localText.yoal,localText.hrappa,localText.milton),u'cost':35}, # Lemon
					12339:{u'note':u"{}".format(localText.shelp),u'cost':77}, # Lime
					12543:{u'note':u"{}".format(localText.crandle),u'cost':203}, # Mango
					12249:{u'note':u"{} <br />{}".format(localText.jenks,localText.milton),u'cost':35}, # Nutmeg Seed
					12503:{u'note':u"{}".format(localText.nrocroc),u'cost':154}, # Peach
					12514:{u'note':u"{}".format(localText.braxa),u'cost':112}, # Pear
					12516:{u'note':u"{}".format(localText.tholin),u'cost':112}, # Pinenut
					12517:{u'note':u"{}".format(localText.ichtaca),u'cost':112}} # Shallot

	karma_chef = {12159:{u'note':localText.mcov,u'cost':35}, # Cheese Wedge
					12137:{u'note':localText.mcov,u'cost':35}, # Glass of Buttermilk
					12152:{u'note':localText.mcov,u'cost':35}, # Packet of Yeast
					12145:{u'note':localText.mcov,u'cost':49}, # Rice Ball
					12325:{u'note':localText.mcov,u'cost':77}, # Bowl of Sour Cream
					12141:{u'note':localText.mcov,u'cost':35}, # Tomato
					12328:{u'note':localText.mcov,u'cost':77}, # Ginger Root
					12245:{u'note':localText.mcov,u'cost':49}, # Basil Leaf
					12235:{u'note':localText.mcov,u'cost':49}} # Bell Pepper

	karma_recipe = {12131:{u'note':localText.elain,u'cost':35}, # Bowl of Watery Mushroom Soup
					12185:{u'note':localText.bjarni,u'cost':35}, # Handful of Bjarni's Rabbit Food
					12140:{u'note':localText.hrouda,u'cost':35}, # Bowl of Gelatinous Ooze Custard
					 8587:{u'note':localText.drottot,u'cost':35}, # Poached Egg
					12211:{u'note':localText.kevach,u'cost':35}, # Bowl of Cold Wurm Stew
					12198:{u'note':localText.vaastas,u'cost':35}, # Celebratory Steak
					12133:{u'note':localText.laewyn,u'cost':35}, # Warden Ration
					12149:{u'note':localText.krug,u'cost':35}, # Bowl of Ettin Stew
					12203:{u'note':localText.maxtar,u'cost':35}, # Bowl of Dolyak Stew
					12139:{u'note':localText.aidem,u'cost':35}, # Bowl of Front Line Stew
					12150:{u'note':localText.eda,u'cost':35}, # Eda's Apple Pie
					12343:{u'note':localText.kastaz,u'cost':35}, # Kastaz Roasted Poultry
					12160:{u'note':localText.auda,u'cost':35}, # Loaf of Walnut Sticky Bread
					12154:{u'note':localText.brian,u'cost':35}, # Bowl of Outrider Stew
					12292:{u'note':localText.glubb,u'cost':35}, # Bowl of Degun Shun Stew
					12233:{u'note':localText.tholin,u'cost':154}, # Handful of Trail Mix
					12739:{u'note':localText.triktiki,u'cost':35}, # Triktiki Omelet
					12352:{u'note':u"{} ({} {})".format(localText.pochtecatl,mFormat(368),localText.valuePer),u'cost':0}, # Griffon Egg Omelet
					12264:{u'note':localText.nrocroc,u'cost':35}, # Raspberry Pie
					12192:{u'note':localText.victor,u'cost':35}, # Beetletun Omelette
					19955:{u'note':localText.mcov,u'cost':350}, # Ravaging Intricate Wool Insignia
					19956:{u'note':localText.mcov,u'cost':350}, # Rejuvenating Intricate Wool Insignia
					19957:{u'note':localText.mcov,u'cost':350}, # Honed Intricate Wool Insignia
					19958:{u'note':localText.mcov,u'cost':350}, # Pillaging Intricate Wool Insignia
					19959:{u'note':localText.mcov,u'cost':350}, # Strong Intricate Wool Insignia
					19960:{u'note':localText.mcov,u'cost':350}, # Vigorous Intricate Wool Insignia
					19961:{u'note':localText.mcov,u'cost':350}, # Hearty Intricate Wool Insignia
					19962:{u'note':localText.mcov,u'cost':455}, # Ravaging Intricate Cotton Insignia
					19963:{u'note':localText.mcov,u'cost':455}, # Rejuvenating Intricate Cotton Insignia
					19964:{u'note':localText.mcov,u'cost':455}, # Honed Intricate Cotton Insignia
					19965:{u'note':localText.mcov,u'cost':455}, # Pillaging Intricate Cotton Insignia
					19966:{u'note':localText.mcov,u'cost':455}, # Strong Intricate Cotton Insignia
					19967:{u'note':localText.mcov,u'cost':455}, # Vigorous Intricate Cotton Insignia
					19968:{u'note':localText.mcov,u'cost':455}, # Hearty Intricate Cotton Insignia
					19969:{u'note':localText.mcov,u'cost':567}, # Carrion Intricate Linen Insignia
					19970:{u'note':localText.mcov,u'cost':567}, # Cleric's Intricate Linen Insignia
					19971:{u'note':localText.mcov,u'cost':567}, # Explorer's Intricate Linen Insignia
					19972:{u'note':localText.mcov,u'cost':567}, # Berserker's Intricate Linen Insignia
					19973:{u'note':localText.mcov,u'cost':567}, # Valkyrie Intricate Linen Insignia
					19974:{u'note':localText.mcov,u'cost':567}, # Rampager's Intricate Linen Insignia
					19975:{u'note':localText.mcov,u'cost':567}, # Knight's Intricate Linen Insignia
					19880:{u'note':localText.mcov,u'cost':672}, # Carrion Intricate Silk Insignia
					19881:{u'note':localText.mcov,u'cost':672}, # Cleric's Intricate Silk Insignia
					19882:{u'note':localText.mcov,u'cost':672}, # Explorer's Intricate Silk Insignia
					19883:{u'note':localText.mcov,u'cost':672}, # Berserker's Intricate Silk Insignia
					19886:{u'note':localText.mcov,u'cost':672}, # Valkyrie Intricate Silk Insignia
					19884:{u'note':localText.mcov,u'cost':672}, # Rampager's Intricate Silk Insignia
					19885:{u'note':localText.mcov,u'cost':672}, # Knight's Intricate Silk Insignia
					19934:{u'note':localText.mcov,u'cost':350}, # Ravaging Iron Imbued Inscription
					19935:{u'note':localText.mcov,u'cost':350}, # Rejuvenating Iron Imbued Inscription
					19936:{u'note':localText.mcov,u'cost':350}, # Honed Iron Imbued Inscription
					19937:{u'note':localText.mcov,u'cost':350}, # Pillaging Iron Imbued Inscription
					19938:{u'note':localText.mcov,u'cost':350}, # Strong Iron Imbued Inscription
					19939:{u'note':localText.mcov,u'cost':350}, # Vigorous Iron Imbued Inscription
					19940:{u'note':localText.mcov,u'cost':350}, # Hearty Iron Imbued Inscription
					19941:{u'note':localText.mcov,u'cost':455}, # Ravaging Steel Imbued Inscription
					19942:{u'note':localText.mcov,u'cost':455}, # Rejuvenating Steel Imbued Inscription
					19943:{u'note':localText.mcov,u'cost':455}, # Honed Steel Imbued Inscription
					19944:{u'note':localText.mcov,u'cost':455}, # Pillaging Steel Imbued Inscription
					19945:{u'note':localText.mcov,u'cost':455}, # Strong Steel Imbued Inscription
					19946:{u'note':localText.mcov,u'cost':455}, # Vigorous Steel Imbued Inscription
					19947:{u'note':localText.mcov,u'cost':455}, # Hearty Steel Imbued Inscription
					19948:{u'note':localText.mcov,u'cost':567}, # Carrion Darksteel Imbued Inscription
					19949:{u'note':localText.mcov,u'cost':567}, # Cleric's Darksteel Imbued Inscription
					19950:{u'note':localText.mcov,u'cost':567}, # Explorer's Darksteel Imbued Inscription
					19951:{u'note':localText.mcov,u'cost':567}, # Berserker's Darksteel Imbued Inscription
					19952:{u'note':localText.mcov,u'cost':567}, # Valkyrie Darksteel Imbued Inscription
					19953:{u'note':localText.mcov,u'cost':567}, # Rampager's Darksteel Imbued Inscription
					19954:{u'note':localText.mcov,u'cost':567}, # Knight's Darksteel Imbued Inscription
					19897:{u'note':localText.mcov,u'cost':672}, # Carrion Mithril Imbued Inscription
					19898:{u'note':localText.mcov,u'cost':672}, # Cleric's Mithril Imbued Inscription
					19899:{u'note':localText.mcov,u'cost':672}, # Explorer's Mithril Imbued Inscription
					19900:{u'note':localText.mcov,u'cost':672}, # Berserker's Mithril Imbued Inscription
					19903:{u'note':localText.mcov,u'cost':672}, # Valkyrie Mithril Imbued Inscription
					19901:{u'note':localText.mcov,u'cost':672}, # Rampager's Mithril Imbued Inscription
					19902:{u'note':localText.mcov,u'cost':672}, # Knight's Mithril Imbued Inscription
					19923:{u'note':localText.mcov,u'cost':896}, # inscr
					19920:{u'note':localText.mcov,u'cost':896},
					19917:{u'note':localText.mcov,u'cost':896},
					19918:{u'note':localText.mcov,u'cost':896},
					19919:{u'note':localText.mcov,u'cost':896},
					19922:{u'note':localText.mcov,u'cost':896},
					19921:{u'note':localText.mcov,u'cost':896},
					19912:{u'note':localText.mcov,u'cost':896}, # insig
					19913:{u'note':localText.mcov,u'cost':896},
					19910:{u'note':localText.mcov,u'cost':896},
					19911:{u'note':localText.mcov,u'cost':896},
					19915:{u'note':localText.mcov,u'cost':896},
					19914:{u'note':localText.mcov,u'cost':896},
					19916:{u'note':localText.mcov,u'cost':896},
					24543:{u'note':localText.mcov,u'cost':896}, # jewel
					24496:{u'note':localText.mcov,u'cost':896},
					24544:{u'note':localText.mcov,u'cost':896},
					24497:{u'note':localText.mcov,u'cost':896},
					24545:{u'note':localText.mcov,u'cost':896},
					24498:{u'note':localText.mcov,u'cost':896},
					24499:{u'note':localText.mcov,u'cost':896},
					24904:{u'note':localText.mcov,u'cost':231}, # Embellished Intricate Topaz Jewel
					24902:{u'note':localText.mcov,u'cost':231}, # Embellished Intricate Spinel Jewel
					24901:{u'note':localText.mcov,u'cost':231}, # Embellished Intricate Peridot Jewel
					24903:{u'note':localText.mcov,u'cost':231}, # Embellished Intricate Sunstone Jewel
					24899:{u'note':localText.mcov,u'cost':231}, # Embellished Intricate Carnelian Jewel
					24898:{u'note':localText.mcov,u'cost':231}, # Embellished Intricate Amethyst Jewel
					24900:{u'note':localText.mcov,u'cost':231}, # Embellished Intricate Lapis Jewel
					24911:{u'note':localText.mcov,u'cost':231}, # Embellished Gilded Topaz Jewel
					24905:{u'note':localText.mcov,u'cost':231}, # Embellished Gilded Amethyst Jewel
					24906:{u'note':localText.mcov,u'cost':231}, # Embellished Gilded Carnelian Jewel
					24907:{u'note':localText.mcov,u'cost':231}, # Embellished Gilded Lapis Jewel
					24908:{u'note':localText.mcov,u'cost':231}, # Embellished Gilded Peridot Jewel
					24909:{u'note':localText.mcov,u'cost':231}, # Embellished Gilded Spinel Jewel
					24910:{u'note':localText.mcov,u'cost':231}, # Embellished Gilded Sunstone Jewel
					24912:{u'note':localText.mcov,u'cost':231}, # Embellished Ornate Beryl Jewel
					24913:{u'note':localText.mcov,u'cost':231}, # Embellished Ornate Chrysocola Jewel
					24914:{u'note':localText.mcov,u'cost':231}, # Embellished Ornate Coral Jewel
					24915:{u'note':localText.mcov,u'cost':231}, # Embellished Ornate Emerald Jewel
					24916:{u'note':localText.mcov,u'cost':231}, # Embellished Ornate Opal Jewel
					24917:{u'note':localText.mcov,u'cost':231}, # Embellished Ornate Ruby Jewel
					24918:{u'note':localText.mcov,u'cost':231}, # Embellished Ornate Sapphire Jewel
					24919:{u'note':localText.mcov,u'cost':231}, # Embellished Brilliant Beryl Jewel
					24920:{u'note':localText.mcov,u'cost':231}, # Embellished Brilliant Chrysocola Jewel
					24921:{u'note':localText.mcov,u'cost':231}, # Embellished Brilliant Coral Jewel
					24922:{u'note':localText.mcov,u'cost':231}, # Embellished Brilliant Emerald Jewel
					24923:{u'note':localText.mcov,u'cost':231}, # Embellished Brilliant Opal Jewel
					24924:{u'note':localText.mcov,u'cost':231}, # Embellished Brilliant Ruby Jewel
					24925:{u'note':localText.mcov,u'cost':231}, # Embellished Brilliant Sapphire Jewel
					38162:{u'note':u"{} ({}: {} {})".format(localText.bRecipes,localText.rTP,mFormat(cList[38207][u'cost']),localText.valuePer),u'cost':0}, # Giver's Intricate Gossamer Insignia
					38166:{u'note':u"{} ({}: {} {})".format(localText.bRecipes,localText.rTP,mFormat(cList[38208][u'cost']),localText.valuePer),u'cost':0}, # Giver's Embroidered Silk Insignia
					38167:{u'note':u"{} ({}: {} {})".format(localText.bRecipes,localText.rTP,mFormat(cList[38209][u'cost']),localText.valuePer),u'cost':0}, # Giver's Embroidered Linen Insignia
					38434:{u'note':u"{} ({}: {} {})".format(localText.bRecipes,localText.rTP,mFormat(cList[38297][u'cost']),localText.valuePer),u'cost':0}, # Giver's Orichalcum-Imbued Inscription
					38432:{u'note':u"{} ({}: {} {})".format(localText.bRecipes,localText.rTP,mFormat(cList[38296][u'cost']),localText.valuePer),u'cost':0}, # Giver's Mithril-Imbued Inscription
					38433:{u'note':u"{} ({}: {} {})".format(localText.bRecipes,localText.rTP,mFormat(cList[38295][u'cost']),localText.valuePer),u'cost':0}, # Giver's Darksteel-Imbued Inscription
					}

	# Insignia -> Recipe Mapping.
	rsps = {38166:38208, # Giver's Embroidered Silk Insignia
		    38167:38209, # Giver's Embroidered Linen Insignia
			38434:38297, # Giver's Orichalcum-Imbued Inscription
			38432:38296, # Giver's Mithril-Imbued Inscription
			38433:38295, # Giver's Darksteel-Imbued Inscription
			38162:38207 # Giver's Intricate Gossamer Insignia
			}

	recipebuy = []
	for tier in range(0,500,25):
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
	basic_f = range(24272,24301) + [37897,24363] + range(24341,24359)

	# Rare Materials and Ectoplasm
	basic_r = range(24301,24341) + [19721]

	# Gems
	basic_g = range(24500,24536) + [37907,24889] + range(24464,24476) + range(24870,24877)

	# "Tiny Snowflake","Delicate Snowflake","Glittering Snowflake","Unique Snowflake","Pristine Snowflake","Piece of Candy Corn","Chattering Skull","Nougat Center","Plastic Fang"
	basic_h = range(38130,38136) + [36041,36060,36061,36059]

	# "Artichoke","Asparagus Spear","Basil Leaf","Bay Leaf","Beet","Black Peppercorn","Blackberry","Blueberry","Butternut Squash","Carrot","Cayenne Pepper","Chili Pepper","Chocolate Bar","Cinnamon Stick","Clam","Clove","Coriander Seed","Dill Sprig","Egg","Head of Cabbage","Head of Cauliflower","Head of Garlic","Head of Lettuce","Kale Leaf","Leek","Mint Leaf","Mushroom","Onion","Orange","Oregano Leaf","Parsley Leaf","Parsnip","Passion Fruit","Piece of Candy Corn","Portobello Mushroom","Potato","Raspberry","Rosemary Sprig","Rutabaga","Sage Leaf","Sesame Seed","Slab of Poultry Meat","Slab of Red Meat","Snow Truffle","Spinach Leaf","Stick of Butter","Strawberry","Sugar Pumpkin","Tarragon Leaves","Thyme Leaf","Turnip","Vanilla Bean","Walnut","Yam","Zucchini","Green Onion", Omnomberry, Lotus Root
	basic_fo = [12512,  12505,  12245,  12247,  12161,  12236,  12537,  12255,  12511,  12134,  12504,  12331,  12229,  12258,  12327,  12534,  12531,  12336,  12143,  12332,  12532,  12163,  12238,  12333,  12508,  12536,  12147,  12142,  12351,  12244,  12246,  12507,  36731,  36041,  12334,  12135,  12254,  12335,  12535,  12243,  12342,  24360,  24359,  12144,  12241,  12138,  12253,  12538,  12506,  12248,  12162,  12234,  12250,  12329,  12330,  12533,  12128, 12510]



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
					Globals.karmin[item] = buy[item] # used by cooking to make a top 5 list
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
	karma_str = u"<div class=\"s{0}\"><input type=\"checkbox\" /><span class=\"itemIcon\" style=\"background-image: url({1});\"></span><input type=\"number\" onkeypress=\"return event.charCode >= 48\" oninput=\"updateNeed(this, {2}, '{9}bv');\" id=\"{9}ih\" placeholder='0' min=\"0\" /><input type=\"number\" id=\"{9}bv\" value='{2}' raw_copper='0' readonly data-need = \"more\" min=\"0\" /> <button title=\""+localText.toggle+u"\" class=\"{3} arrow\" id=\"{4}\">{5}</button><div class=\"lsbutton\" id=\"1{6}\">{7} <span class=\"karmaIcon\"></span> "+localText.valuePer+u" 25 <br /> {8}</div></div>\n"
	collectable_str = u"<div class=\"s{0}\"><input type=\"checkbox\" /><span class=\"itemIcon\" style=\"background-image: url({1});\"></span><input type=\"number\" onkeypress=\"return event.charCode >= 48\" oninput=\"updateNeed(this, {2}, '{6}bv');\" id=\"{6}ih\" placeholder='0' min=\"0\" /><input type=\"number\" id=\"{6}bv\" value='{2}' raw_copper='{7}' class='vTotal' readonly data-need = \"more\" min=\"0\" /> <span class=\"{3}\">{4}</span> ({5} "+localText.valuePer+u")</div>\n"

	title = ""
	# Page Title Part 1
	if u"fast" in filename:
		title += localText.fGuides
	elif u"all" in filename:
		title += localText.tGuides
	else: # normal
		title += localText.nGuides
	# Page Title Part 2
	if filename in [u"cooking_fast.html",u"cooking.html"]:
		title += u': '+localText.cooking+u' - '+localText.nHearts
	elif filename in [u"cooking_karma_fast.html",u"cooking_karma.html"]:
		title += u': '+localText.cooking+u' - '+localText.aHearts
	elif filename in [u"cooking_karma_fast_light.html",u"cooking_karma_light.html"]:
		title += u': '+localText.cooking+u' - '+localText.tHearts
	elif filename in [u"leatherworking_fast.html", u"leatherworking.html", u"leatherworking_400.html"]:
		title += u': '+localText.lw
	elif filename in [u"tailor_fast.html", u"tailor.html", u"tailor_400.html"]:
		title += u': '+localText.tailor
	elif filename in [u"artificing_fast.html", u"artificing.html", u"artificing_400.html", u"artificing_450.html"]:
		title += u': '+localText.art
	elif filename in [u"jewelcraft_fast.html", u"jewelcraft.html", u"jewelcraft_400.html"]:
		title += u': '+localText.jc
	elif filename in [u"weaponcraft_fast.html", u"weaponcraft.html", u"weaponcraft_400.html", u"weaponcraft_450.html"]:
		title += u': '+localText.wc
	elif filename in [u"huntsman_fast.html", u"huntsman.html", u"huntsman_400.html", u"huntsman_450.html"]:
		title += u': '+localText.hunt
	elif filename in [u"armorcraft_fast.html", u"armorcraft.html", u"armorcraft_400.html"]:
		title += u': '+localText.ac

	t = 0 # used to control div background color
	kt = 0 # karma total
	page = [u'<!DOCTYPE html>\n']
	page.append(u'<html>\n')
	page.append(u'<head>\n')
	# Ezoic adwords
	page.append(u'''<!-- Ezoic Code -->
<script>var ezoicId = 39853;</script>
<script type="text/javascript" src="//go.ezoic.net/ezoic/ezoic.js"></script>
<!-- Ezoic Code -->
<!-- Ezoic Ad Testing Code-->
<script src="//g.ezoic.net/ezoic/ezoiclitedata.go?did=39853"></script>
<!-- Ezoic Ad Testing Code-->''')
	# Title Part 1
	page.append(u'	<title>'+title+u' - Guild War 2 Crafting Guide</title>\n')
	page.append(u'	<meta name="description" content="Guild Wars 2 always current crafting guide for '+filename.split('.')[0].replace("_"," ").title()+u'">\n')
	page.append(u'	<meta name="keywords" content="best videogames, free mmos, free mmorpg, best free mmorpg, best mmorpg, free to play, mmos, mmorpg, free game, online games, fantasy games, PC games, PC gaming, crafting guide, crafting guides, Guild Wars 2, Trading Post"/>\n')
	page.append(u'	<meta http-equiv="content-type" content="text/html;charset=UTF-8">\n')
	page.append(u'	<link href="/css/layout.css" rel="stylesheet" type="text/css" />')
	page.append(u'	<link rel="icon" type="image/png" href="/fi.gif">\n')
	page.append(u'	<script src="//ajax.googleapis.com/ajax/libs/jquery/1.9.0/jquery.min.js"></script>\n')
	page.append(u'	<script>(window.jQuery || document.write(\'<script src="http://ajax.aspnetcdn.com/ajax/jquery/jquery-1.9.0.min.js"><\/script>\'));</script>\n')
	page.append(u'	<script src="/js/menu.js" type="text/javascript"></script>\n')
	page.append(u'</head>\n')
	page.append(u'<body>\n%s\n'%(localText.header%(filename,filename,filename,filename,filename,filename)))
	page.append(u"""<script> 
  (function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
  (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
  m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
  })(window,document,'script','//www.google-analytics.com/analytics.js','ga');

  ga('create', 'UA-38972433-1', 'auto');
  ga('send', 'pageview');

</script>""")
	page.append(u'<section class=\"main\">')
	page.append(u'<div style="width: 100%; border: 2px #fffaaa solid; border-left: 0px; border-right: 0px; background: #fffddd; height: 24px;">\n')
	page.append(u'<span class=\"warning\"></span><span style="position: relative; top: 4px;"><span style="color: red">%s</span>	%s: %s</span>\n'%(localText.warning1,localText.warning2,mytime))
	page.append(u'</div><br />\n')
	if u'scribe' in filename:
		page.append(u'<div>\n')
		page.append(u'<button title=\"{}\" class =\"arrow\" id=\"scribehint\">{}</button><div class=\"lsbutton\" id=\"1scribehint\">\n'.format(localText.toggle, localText.scribetease))
		page.append(u'{}</div><br /></div><br />\n'.format(localText.scribeinfo))
		buttonList.append(u'scribehint')

#	page.append(u"<div class=\"s{}\">{}: <button class=\"arrow {}\" title=\"{}\" id=\"{}{}\">{}</button> {}\n</div>\n".format(
#		t, localText.discover, cList[item][u'rarity'], localText.toggle, item, tier, cListName[item], tstr))
	page.append(u"<strong>%s</strong><br />\n"%(localText.region))
#	# adword
	page.append(u'<div style="float:right;position:absolute;right:-320px;">\n')
	page.append(u'<!-- Ezoic - Large sidebar - sidebar -->\n<div id="ezoic-pub-ad-placeholder-103"></div>\n\<!-- End Ezoic - Large sidebar - sidebar -->\n\n</div>\n')
	page.append(localText.moreInfo%(u"<img src=\"/img/arrow.png\" alt=ARROW>"))
	page.append(u'<!-- Ezoic - page_title - under_page_title -->\n<div id="ezoic-pub-ad-placeholder-105">\n</div><!-- End Ezoic - page_title - under_page_title -->')
	# Page Title Part 1
	page.append(u'<h1>'+title+u'</h1>')
	page.append(u'<dl>\n')
	page.append(u'	<dt>%s</dt>\n'%localText.iCost)
	page.append(u'	<dd>'+mFormat(tcost)+u'</dd>\n')
	page.append(u'	<dt>%s</dt>\n'%localText.eRecovery)
	page.append(u'	<dd><span style="position: relative; left: -9px;">- '+mFormat(treco)+u'</span></dd>\n')
	page.append(u'	<dt>%s</dt>\n'%localText.fCost)
	page.append(u'	<dd style="border-top: 1px #666 solid;">'+mFormat(tcost-treco)+u'</dd>\n')
	page.append(u'</dl>')
	page.append(u'<div class="clear"></div>')

	remaining = u'<dl>\n	<dt>{}</dt>\n	<dd><span class="mygold">{}</span><span class=\"goldIcon\"></span><span class="mysilver">{}</span><span class=\"silverIcon\"></span><span class="mycopper">{}</span><span class=\"copperIcon\"></span></dd>\n</dl><div class="clear"></div>'.format(localText.remCost,tcost//10000,(tcost//100)%100,tcost%100)


	page.append(u'<br /><button title=\"%s\" class=\"arrow\" id=\"tcost\">%s:</button><div class=\"lsbutton\" id=\"1tcost\">'%(localText.toggle,localText.sList))
	for line in sorted(sell):
		if cList[line][u'w'] > 0:
			t = (t + 1) % 2
			page.append(u'<div class=\"s%i\">%3i <span class=\"%s\">%s</span> - %s %s</div>\n'%(t,sell[line],cList[line][u'rarity'],cListName[line],(localText.soldVia%mFormat(cList[line][u'w'])),localText.method[cList[line][u'sellMethod']]))

	page.append(u"</div><script type=\"text/javascript\">$('#1tcost').hide();</script><br />")
	buttonList.append(u'tcost')
	page.append(u'<!-- Ezoic - page_title_2 - under_page_title -->\n<div id="ezoic-pub-ad-placeholder-106"></div>\n<!-- End Ezoic - page_title_2 - under_page_title -->')
	page.append(u'<br /><br /><input type="text" id="api_key" name="api key" placeholder="Enter API key here" style=\'text-align: center;\'><br />')
	page.append(u'<button type="button" onclick="updateBank(document.getElementById(\'api_key\').value.trim());" style=\'text-align: center;\'>Get Bank Content</button>\n')
	page.append(u'<br /> The API key you enter needs \'inventories\' permission to work.  <a href="https://account.arena.net/applications/create">You can generate a key here</a>. <br /><br />')
	page.append(u'Clicking the button will update the quantities of all items in your bank and material storage that are used in this guide.')
	page.append(u"<br /><br /><div class=\"s1\"><input type=\"checkbox\" /><span class=\"itemIcon\" style=\"background-image: url(/apple-touch-icon-144x144-precomposed.png);\"></span><input type=\"text\" value='Have' readonly style=\"width: 4em;\" /><input type=\"text\" value='Need' readonly style=\"width: 4em;\" /> Name of an item and its per unit cost.</div>\n")

	if b_vendor or b_karma_c or b_karma_w:
		page.append(remaining)
		page.append(u"<h2>%s</h2>\n"%localText.buyVendor)
		if b_karma_c or b_karma_w:
			page.append(u"<span class=\"karmaIcon\"></span>{}<br /><br />\n".format(localText.kNote))

		for item in sorted(b_karma_w):
			t = (t + 1) % 2
			page.append(karma_str.format(t, cList[item][u'icon'], buy[item], cList[item][u'rarity'], item, cListName[item], item, karma_items[item][u'cost'], karma_items[item][u'note'], item))
			buttonList.append(item)
			kt += int(math.ceil(buy[item]/25.0)*karma_items[item][u'cost'])

		for item in sorted(b_karma_c):
			t = (t + 1) % 2
			page.append(karma_str.format(t, cList[item][u'icon'], buy[item], cList[item][u'rarity'], item, cListName[item], item, karma_chef[item][u'cost'], karma_chef[item][u'note'], item))
			buttonList.append(item)
			kt += int(math.ceil(buy[item]/25.0)*karma_chef[item][u'cost'])

		for item in sorted(b_vendor):
			t = (t + 1) % 2
			page.append(u"<div class=\"s{0}\"><input type=\"checkbox\" /><span class=\"itemIcon\" style=\"background-image: url({1});\"></span><input type=\"number\" onkeypress=\"return event.charCode >= 48\" oninput=\"updateNeed(this, {2}, '{8}bv');\" id=\"{8}ih\" placeholder='0' min=\"0\" /><input type=\"number\" id=\"{8}bv\" value='{2}' raw_copper='{9}' class='vTotal' readonly data-need = \"more\" min=\"0\" /> <span class=\"{3}\">{4}</span> ({5} {6} from {7})</div>\n".format(t, cList[item][u'icon'], buy[item], cList[item][u'rarity'], cListName[item], mFormat(cList[item][u'cost']), localText.valuePer, localText.method[0], item, cList[item][u'cost']))

	page.append(u'<!-- Ezoic - first_paragraph - under_first_paragraph -->\n<div id="ezoic-pub-ad-placeholder-107"></div>\n<!-- End Ezoic - first_paragraph - under_first_paragraph -->')
	if recipebuy:
		page.append(u"<h2>%s</h2>\n"%localText.bRecipes)
		for item in recipebuy:
			t = (t + 1) % 2
			if karma_recipe[item][u'cost']:
				page.append((u"<div class=\"s%d\"><input type=\"checkbox\" /><span class=\"itemIcon\" style=\"background-image: url(%s);\"></span><button title=\""+localText.toggle+u"\" class=\"arrow %s\" id=\"%d\">%s</button><div class=\"lsbutton\" id=\"1%d\">%i <span class=\"karmaIcon\"></span>, %s</div></div>\n")%(t,cList[item][u'icon'],cList[item][u'rarity'],item,cListName[item],item,karma_recipe[item][u'cost'],karma_recipe[item][u'note']))
			else:
				if item in rsps:
					page.append((u"<div class=\"s%d\"><input type=\"checkbox\" /><span class=\"itemIcon\" style=\"background-image: url(%s);\"></span><button title=\""+localText.toggle+u"\" class=\"arrow %s\" id=\"%d\">%s</button><div class=\"lsbutton\" id=\"1%d\">%s</div></div>\n")%(t,cList[item]['icon'],cList[item][u'rarity'],item,cListName[rsps[item]],item,karma_recipe[item][u'note']))
				else:
					page.append((u"<div class=\"s%d\"><input type=\"checkbox\" /><span class=\"itemIcon\" style=\"background-image: url(%s);\"></span><button title=\""+localText.toggle+u"\" class=\"arrow %s\" id=\"%d\">%s</button><div class=\"lsbutton\" id=\"1%d\">%s</div></div>\n")%(t,cList[item]['icon'],cList[item][u'rarity'],item,cListName[item],item,karma_recipe[item][u'note']))
			buttonList.append(item)
			kt += int(karma_recipe[item][u'cost'])
	if kt:
		page.append(u'<br />\nTotal <span class=\"karmaIcon\"></span>: '+str(kt)+u'<br />\n')
	if b_common or b_fine or b_rare or b_gem or b_holiday or b_food:
		page.append(remaining)
		page.append(u'<h2>%s</h2>\n'%localText.collectibles)
		for item in sorted(b_common):
			t = (t + 1) % 2
			page.append(collectable_str.format(t, cList[item][u'icon'], buy[item], cList[item][u'rarity'], cListName[item], mFormat(cList[item][u'cost']), item, cList[item][u'cost']))
		for item in sorted(b_fine):
			t = (t + 1) % 2
			page.append(collectable_str.format(t, cList[item][u'icon'], buy[item], cList[item][u'rarity'], cListName[item], mFormat(cList[item][u'cost']), item, cList[item][u'cost']))
		for item in sorted(b_rare):
			t = (t + 1) % 2
			page.append(collectable_str.format(t, cList[item][u'icon'], buy[item], cList[item][u'rarity'], cListName[item], mFormat(cList[item][u'cost']), item, cList[item][u'cost']))
		for item in sorted(b_gem):
			t = (t + 1) % 2
			page.append(collectable_str.format(t, cList[item][u'icon'], buy[item], cList[item][u'rarity'], cListName[item], mFormat(cList[item][u'cost']), item, cList[item][u'cost']))
		for item in sorted(b_holiday):
			t = (t + 1) % 2
			page.append(collectable_str.format(t, cList[item][u'icon'], buy[item], cList[item][u'rarity'], cListName[item], mFormat(cList[item][u'cost']), item, cList[item][u'cost']))
		for item in sorted(b_food):
			t = (t + 1) % 2
			page.append(collectable_str.format(t, cList[item][u'icon'], buy[item], cList[item][u'rarity'], cListName[item], mFormat(cList[item][u'cost']), item, cList[item][u'cost']))
	page.append(u'<!-- Ezoic - second_paragraph - under_second_paragraph -->\n<div id="ezoic-pub-ad-placeholder-108"></div>\n<!-- End Ezoic - second_paragraph - under_second_paragraph -->')
	if b_mix:
		page.append(remaining)
		page.append(u'<h2>%s</h2>\n'%localText.mixedTP)
		for item in sorted(b_mix):
			t = (t + 1) % 2
			page.append(collectable_str.format(t, cList[item][u'icon'], buy[item], cList[item][u'rarity'], cListName[item], mFormat(cList[item][u'cost']), item, cList[item][u'cost']))
	page.append(u'<!-- Ezoic - mid_content - mid_content -->\n<div id="ezoic-pub-ad-placeholder-109"></div>\n<!-- End Ezoic - mid_content - mid_content -->')

	page.append(u"<br />\n<br />\n<h2>%s</h2>\n"%localText.make)
	# adword adaptive
	page.append(u'<br /><div style="width: 100%;display:block;">\n')
	page.append(u'<!-- Ezoic - first banner - mid_content -->\n<div id="ezoic-pub-ad-placeholder-104"></div>\n<!-- End Ezoic - first banner - mid_content -->\n')
	page.append(u'</div>\n')

	page.append(u"<button title=\""+localText.toggle+u"\" class =\"info\" id=\"show_all\">%s</button><br />"%localText.expand)
	page.append(u"<button title=\""+localText.toggle+u"\" class =\"info\" id=\"hide_all\">%s</button>"%localText.collapse)
	rt = 0
	for tier in mTiers:

		if tier in [75, 425]:  # long content
			page.append(u'<!-- Ezoic - long_1 - long_content -->\n<div id="ezoic-pub-ad-placeholder-110"></div>\n<!-- End Ezoic - long_1 - long_content -->')
		elif tier in [100]:  # long content
			page.append(u'<!-- Ezoic - long_2 - long_content -->\n<div id="ezoic-pub-ad-placeholder-111"></div>\n<!-- End Ezoic - long_2 - long_content -->')
		elif tier in [150, 450]:  # longer
			page.append(u'<!-- Ezoic - longer_1 - longer_content -->\n<div id="ezoic-pub-ad-placeholder-112"></div>\n<!-- End Ezoic - longer_1 - longer_content -->')
		elif tier in [175]:  # longer
			page.append(u'<!-- Ezoic - longer_2 - longer_content -->\n<div id="ezoic-pub-ad-placeholder-113"></div>\n<!-- End Ezoic - longer_2 - longer_content -->')
		elif tier in [225, 475]:  # longest
			page.append(u'<!-- Ezoic - longest_1 - longest_content -->\n<div id="ezoic-pub-ad-placeholder-114"></div>\n<!-- End Ezoic - longest_1 - longest_content -->')
		elif tier in [250]:  # longest
			page.append(u'<!-- Ezoic - longest_2 - longest_content -->\n<div id="ezoic-pub-ad-placeholder-115"></div>\n<!-- End Ezoic - longest_2 - longest_content -->')
		elif tier in [300]:  # bottom
			page.append(u'<!-- Ezoic - bottom_1 - bottom_of_page -->\n<div id="ezoic-pub-ad-placeholder-116"></div>\n<!-- End Ezoic - bottom_1 - bottom_of_page -->')
		elif tier in [325]:  # bottom
			page.append(u'<!-- Ezoic - bottom_2 - bottom_of_page -->\n<div id="ezoic-pub-ad-placeholder-117"></div>\n<!-- End Ezoic - bottom_2 - bottom_of_page -->')

		if tier == 400:
			precraft = sorted([i for i in make if make[i] and i < 400])
			if precraft:
				page.append((u"<br />\n<h3>%s:<400</h3>\n")%(localText.level))
				for lvl in precraft:
					for item in make[lvl]:
						t = (t + 1) % 2
						page.append(u"<div class=\"s"+str(t)+u"\">"+localText.make+u":%3i <span class=\"%s\">%s</span></div>\n"%(make[lvl][item],cList[item][u'rarity'],cListName[item]))

		if tierbuy and tier in [0,75,150,225,300]:
			tt = 0
			tc = tier+75
			if tier == 300:
				tc += 25
			page.append((u"<br /><br /><h4>%s:<button title=\""+localText.toggle+u"\" class =\"info\" id=\""+str(tier)+u"tier\">%s</button></h4>\n<div class=\"lsbutton\" id=\"1"+str(tier)+u"tier\">")%((localText.tier%(tier/75+1,tier,tc)),localText.buyList%(tier/75+1)))
			page.append(u"<h5>%s</h5>"%localText.blNotice)
			for item in sorted(tierbuy[tier]):
				t = (t + 1) % 2
				page.append((u"<div class=\"s"+str(t)+u"\"><input type=\"checkbox\" /><span class=\"itemIcon\" style=\"background-image: url("+cList[item][u'icon']+u");\"></span><span class=\"quantity\">%i</span> <span class=\"%s\">%s</span> (%4s "+localText.valuePer+u")</div>\n")%(tierbuy[tier][item],cList[item][u'rarity'],cListName[item],mFormat(cList[item][u'cost'])))
				tt += tierbuy[tier][item]*cList[item][u'cost']
			buttonList.append(str(tier)+u'tier')
			rt += tt
			totals[filename.split('.')[0]][tier] = tt
			page.append(u"</div><h4>%s</h4>\n"%(localText.costRT%(mFormat(tt),mFormat(rt))))
		page.append((u"<br />\n<h3>%s:%3i</h3>\n")%(localText.level,tier))
		if pmake[tier]:
			for item in sorted(pmake[tier]):
				t = (t + 1) % 2
				page.append(u"<div class=\"s"+str(t)+u"\"><input type=\"checkbox\" />"+localText.make+u":%3i <span class=\"%s\">%s</span> (From %i tier) </div>\n"%(pmake[tier][item],cList[item][u'rarity'],cListName[item],tier-25))
		for item in sorted(make[tier], key=make[tier].get, reverse=True):
			if cList[item][u'type'] == u'Refinement':
				t = (t + 1) % 2
				if item == 19679: # Bronze Ingot
					page.append((u"<div class=\"s"+str(t)+u"\"><input type=\"checkbox\" />"+localText.make+u":%3i <span class=\"%s\">%s</span> (%s)</div>\n")%(make[tier][item],cList[item][u'rarity'],cListName[item],localText.bNote))
				else:
					page.append(u"<div class=\"s"+str(t)+u"\"><input type=\"checkbox\" />"+localText.make+u":%3i <span class=\"%s\">%s</span></div>\n"%(make[tier][item],cList[item][u'rarity'],cListName[item]))
		for item in sorted(make[tier], key=make[tier].get, reverse=True):
			if cList[item][u'type'] in non_item and not cList[item][u'type'] == u'Refinement':
				t = (t + 1) % 2
				if item in [13063,  13189,  13207,  13219,  13045,  13022,  13075,  13177,  13096,  13033, 13201, 13231]: # Sole
					page.append((u"<div class=\"s"+str(t)+u"\"><input type=\"checkbox\" />"+localText.make+u":%3i <span class=\"%s\">%s</span> (%s)</div>\n")%(make[tier][item]/2,cList[item][u'rarity'],cListName[item],localText.sNote))
				else:
					page.append(u"<div class=\"s"+str(t)+u"\"><input type=\"checkbox\" />"+localText.make+u":%3i <span class=\"%s\">%s</span></div>\n"%(make[tier][item],cList[item][u'rarity'],cListName[item]))

		index = 0
		if tier == 425:
			for item in sorted(make[tier]):
				try:
					index = cList[item][u'tier'].index(400)
				except:
					index = 0
				if cList[item][u'discover'][index] == 1 and not cList[item][u'rarity'] == u'Exotic':
					cList[item][u'discover'][index] = 0
					if make[tier][item] > 1:
						make[tier][item] -= 1
					else:
						del(make[tier][item])
					t = (t + 1) % 2
					tstr = u"<div class=\"sbutton\" id=\"1"+str(item)+str(tier)+u"\">"
					for s in cList[item][u'recipe'][index]:
						tstr += u"\n<br />\t<span class=\"itemIcon\" style=\"background-image: url("+cList[s][u'icon']+u");\"></span> <span class=\""+cList[s][u'rarity']+u'\">'+cListName[s]+u"</span> ("+str(cList[item][u'recipe'][index][s])+u")"
					tstr += u"</div><br />"
					page.append(u"<div class=\"s"+str(t)+u"\"><input type=\"checkbox\" />"+localText.discover+u": <button class=\"arrow "+cList[item][u'rarity']+u'\" title=\"'+localText.toggle+u'\" id=\"'+str(item)+str(tier)+u'\">'+cListName[item]+u"</button> "+tstr+u"\n</div>\n")
					buttonList.append(str(item)+str(tier))
			for item in sorted(make[tier]):
				if not cList[item][u'type'] in non_item and not cList[item][u'rarity'] == u'Exotic':
					t = (t + 1) % 2
					page.append(u"<div class=\"s"+str(t)+u"\"><input type=\"checkbox\" />"+localText.make+u":%3i <span class=\"%s\">%s</span></div>\n"%(make[tier][item],cList[item][u'rarity'],cListName[item]))
			for item in sorted(make[tier]):
				try:
					index = cList[item][u'tier'].index(400)
				except:
					index = 0
				if cList[item][u'discover'][index] == 1 and cList[item][u'rarity'] == u'Exotic':
					cList[item][u'discover'][index] = 0
					if make[tier][item] > 1:
						make[tier][item] -= 1
					else:
						del(make[tier][item])
					t = (t + 1) % 2
					tstr = u"<div class=\"sbutton\" id=\"1"+str(item)+str(tier)+u"\">"
					if craftexo:
						inde = 400
					else:
						inde = tier
					for s in cList[item][u'recipe'][index]:
						tstr += u"\n<br />\t<span class=\"itemIcon\" style=\"background-image: url("+cList[s][u'icon']+u");\"></span> <span class=\""+cList[s][u'rarity']+u'\">'+cListName[s]+u"</span> ("+str(cList[item][u'recipe'][index][s])+u")"
					tstr += u"</div><br />"
					page.append(u"<div class=\"s"+str(t)+u"\"><input type=\"checkbox\" />"+localText.discover+u": <button class=\"arrow "+cList[item][u'rarity']+u'\" title=\"'+localText.toggle+u'\" id=\"'+str(item)+str(tier)+u'\">'+cListName[item]+u"</button> "+tstr+u"\n</div>\n")
					buttonList.append(str(item)+str(tier))
			for item in sorted(make[tier]):
				if not cList[item][u'type'] in non_item and cList[item][u'rarity'] == u'Exotic':
					t = (t + 1) % 2
					page.append(u"<div class=\"s"+str(t)+u"\"><input type=\"checkbox\" />"+localText.make+u":%3i <span class=\"%s\">%s</span></div>\n"%(make[tier][item],cList[item][u'rarity'],cListName[item]))
		else:
			for item in sorted(make[tier]):
				if craftexo:
					try:
						index = cList[item][u'tier'].index(400)
					except:
						index = 0
				else:
					index = cList[item][u'tier'].index(tier)
				if cList[item][u'discover'][index] == 1:
					cList[item][u'discover'][index] = 0
					if make[tier][item] > 1:
						make[tier][item] -= 1
					else:
						del(make[tier][item])
					t = (t + 1) % 2
					tstr = u"<div class=\"sbutton\" id=\"1"+str(item)+str(tier)+u"\">"
					for s in cList[item][u'recipe'][index]:
						tstr += u"\n<br />\t<span class=\"itemIcon\" style=\"background-image: url("+cList[s][u'icon']+u");\"></span> <span class=\""+cList[s][u'rarity']+u'\">'+cListName[s]+u"</span> ("+str(cList[item][u'recipe'][index][s])+u")"
					tstr += u"</div><br />"
					page.append(u"<div class=\"s"+str(t)+u"\"><input type=\"checkbox\" />"+localText.discover+u": <button class=\"arrow "+cList[item][u'rarity']+u'\" title=\"'+localText.toggle+u'\" id=\"'+str(item)+str(tier)+u'\">'+cListName[item]+u"</button> "+tstr+u"\n</div>\n")
					buttonList.append(str(item)+str(tier))
			for item in sorted(make[tier]):
				if not cList[item][u'type'] in non_item:
					t = (t + 1) % 2
					page.append(u"<div class=\"s"+str(t)+u"\"><input type=\"checkbox\" />"+localText.make+u":%3i <span class=\"%s\">%s</span></div>\n"%(make[tier][item],cList[item][u'rarity'],cListName[item]))
	page.append(u'<br />\n<h3>%s:%i</h3>\n'%(localText.level,tier+25))
	t = (t + 1) % 2
	page.append(u"<div class=\"s"+str(t)+u"\">%s</div>\n"%localText.finish)
	# adword adaptive
	page.append(u'<br /><div style="width: 100%;display:block;">\n')
	page.append(u'<!-- Ezoic - Tail - bottom_of_page -->\n<div id="ezoic-pub-ad-placeholder-102"></div>\n<!-- End Ezoic - Tail - bottom_of_page -->')
	page.append(u'</div>\n')
	page.append(u'</section>\n')
	page.append(u'%s\n<script type="text/javascript">\n'%localText.cright)
	for item in buttonList:
		page.append(u"$(\"#"+str(item)+u"\").click(function () {\n\t$(\"#1"+str(item)+u"\").toggle();});\n")
	page.append(u"$(\".sbutton\").hide();\n")
	page.append(u"$(\".lsbutton\").hide();\n")
	page.append(u"$(\"#show_all\").click(function () {$(\".sbutton\").show();")
	page.append(u"});\n$(\"#hide_all\").click(function () {$(\".sbutton\").hide();")
	page.append(u'});\n</script>\n')
	page.append(u'</body>\n')
	page.append(u'</html>\n')

	output.write_file(localText.path,filename,''.join(page))
	return totals

def maketotals(totals, mytime, localText):
	tpage1 = u""
	tpage2 = u""
	tpage3 = u""

	page = u'''
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

	<link href="/css/layout.css" rel="stylesheet" type="text/css" />
	<link rel="icon" type="image/png" href="/fi.gif" />

	<script src="//ajax.googleapis.com/ajax/libs/jquery/1.9.0/jquery.min.js"></script>
	<script src="/js/menu.js" type="text/javascript"></script>
</head>
<body>'''
	page += u"""<script> 
  (function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
  (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
  m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
  })(window,document,'script','//www.google-analytics.com/analytics.js','ga');

  ga('create', 'UA-38972433-1', 'auto');
  ga('send', 'pageview');

</script>"""
	page += localText.header%(u'total.html',u'total.html',u'total.html',u'total.html',u'total.html',u'total.html')
	page += u"<section class=\"main\">\n<strong>%s</strong><br />\n"%(localText.region)
	page += u"<h5 style=\"text-align:center;\">"+localText.updated+u": " + mytime + u"</h5>"
	# adword
	page += u'<div style="float:right;position:absolute;right:-320px;">\n \
<!-- Ezoic - Large sidebar - sidebar -->\n\
<div id="ezoic-pub-ad-placeholder-103"></div>\n\
<!-- End Ezoic - Large sidebar - sidebar -->\n\
</div>\n'
	page += localText.note
	page += u'	<table>'
	page += u'<tr><th>'+localText.craft+u'</th><th>'+localText.nGuides+u'</th><th>'+localText.fGuides+u'</th><th>1-200</th></tr>\n'
	page += u'<tr><td>'+localText.nHearts+u'</td><td>'+mFormat(totals[u'cooking'])+u'</td><td>'+mFormat(totals[u'cooking_fast'])+u'</td><td>'+mFormat(totals[u'cooking_fast_200'])+u'</td></tr>\n'
	page += u'<tr><td>'+localText.tHearts+u'</td><td>'+mFormat(totals[u'cooking_karma_light'])+u'</td><td>'+mFormat(totals[u'cooking_karma_fast_light'])+u'</td></tr>\n'
	page += u'<tr><td>'+localText.aHearts+u'</td><td>'+mFormat(totals[u'cooking_karma'])+u'</td><td>'+mFormat(totals[u'cooking_karma_fast'])+u'</td><td>'+mFormat(totals[u'cooking_karma_fast_200'])+u'</td></tr>\n'

	page += u"</table>\n<br />\n<table>\n<tr><th>"+localText.craft+u"</th><th>"+localText.nGuides+u"</th><th>"+localText.fGuides+u"</th><th>400-450</th><th>400-500</th></tr>\n"


	tpage1 += u"</table>\n<br />\n<table>\n<tr><th>"+localText.nGuides+u"</th><th>"+localText.tiers+u" 1</th><th>"+localText.tiers+u" 2</th><th>"+localText.tiers+u" 3</th><th>"+localText.tiers+u" 4</th><th>"+localText.tiers+u" 5</th></tr>\n"
	tpage2 += u"</table>\n<br />\n<table>\n<tr><th>"+localText.fGuides+u"</th><th>"+localText.tiers+u" 1</th><th>"+localText.tiers+u" 2</th><th>"+localText.tiers+u" 3</th><th>"+localText.tiers+u" 4</th><th>"+localText.tiers+u" 5</th></tr>\n"

	ctnc = 0
	ctfc = 0
	cttc = 0
	ct4c = 0
	ct45c = 0
	for i in [(u'jewelcraft',u'jewelcraft_fast',localText.jc),
			  (u'artificing',u'artificing_fast',u'artificing_450',u'artificing_400',localText.art),
			  (u'huntsman',u'huntsman_fast',u'huntsman_450',u'huntsman_400',localText.hunt),
			  (u'weaponcraft',u'weaponcraft_fast',u'weaponcraft_450',u'weaponcraft_400',localText.wc),
			  (u'armorcraft',u'armorcraft_fast',u'armorcraft_450',u'armorcraft_400',localText.ac),
			  (u'leatherworking',u'leatherworking_fast',u'leatherworking_450',u'leatherworking_400',localText.lw),
			  (u'tailor', u'tailor_fast', u'tailor_450', u'tailor_400', localText.tailor)]:

		ind = 2
		if len(i) == 3:
			page += u'<tr><td>'+i[ind]+u'</td><td>'+mFormat(totals[i[0]][u'total'])+u'</td><td>'+mFormat(totals[i[1]][u'total'])+u'</td></tr>\n'
		else:
			ind = 4
			page += u'<tr><td>'+i[ind]+u'</td><td>'+mFormat(totals[i[0]][u'total'])+u'</td><td>'+mFormat(totals[i[1]][u'total'])+u'</td><td>'+mFormat(totals[i[2]])+u'</td><td>'+mFormat(totals[i[3]])+u'</td></tr>\n'
			ct45c += totals[i[2]]
			ct4c += totals[i[3]]

		tpage1 += u'<tr><td>'+i[ind]+u'</td><td>'+mFormat(totals[i[0]][0])+u'</td><td>'+mFormat(totals[i[0]][75])+u'</td><td>'+mFormat(totals[i[0]][150])+u'</td><td>'+mFormat(totals[i[0]][225])+u'</td><td>'+mFormat(totals[i[0]][300])+u'</td></tr>\n'
		tpage2 += u'<tr><td>'+i[ind]+u'</td><td>'+mFormat(totals[i[1]][0])+u'</td><td>'+mFormat(totals[i[1]][75])+u'</td><td>'+mFormat(totals[i[1]][150])+u'</td><td>'+mFormat(totals[i[1]][225])+u'</td><td>'+mFormat(totals[i[1]][300])+u'</td></tr>\n'

		ctnc += totals[i[0]][u'total']
		ctfc += totals[i[1]][u'total']

	page += u'<tr><td><strong>'+localText.totals+u'</strong></td><td><strong>'+ mFormat(ctnc)+u'</strong></td><td><strong>'+ mFormat(ctfc)+u'</strong></td><td><strong>'+ mFormat(ct45c)+u'</strong></td><td><strong>'+ mFormat(ct4c)+u'</strong></td></tr>\n<br />\n'
	page += u'<tr><td>'+localText.scribe+u'</td><td>'+mFormat(totals[u'scribe'][u'total'])+u'</td></tr></table>\n'
	tpage1 += u'<tr><td>' + localText.scribe + u'</td><td>' + mFormat(totals[u'scribe'][0]) + u'</td><td>' + mFormat(totals[u'scribe'][75]) + u'</td><td>' + mFormat(totals[u'scribe'][150]) + u'</td><td>' + mFormat(totals[u'scribe'][225]) + u'</td><td>' + mFormat(totals[u'scribe'][300]) + u'</td></tr>\n'

	tpage1 += u' </table>\n<br />'
	tpage2 += u' </table>\n<br />'
	tpage3 += u' </table>'

	page += tpage1 + tpage2

	# adword adaptive
	page += u'<br /><div style="width: 100%;display:block;">\n \
	<!-- Ezoic - Tail - bottom_of_page -->\n \
<div id="ezoic-pub-ad-placeholder-102"></div>\n\
<!-- End Ezoic - Tail - bottom_of_page --></div>\n'

	page += u'\n</section>\n' + localText.cright
	page += u'</body>\n'
	page += u'</html>\n'

	output.write_file(localText.path,u'total.html',page)
	return
