#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Author: Jeremy Parks
Purpose: Get current price data
Note: Requires Python 3.7.x
'''

import json
import os
import sys
import time

from auto_gen import Items
# so we can set custom headers
from multiprocessing import Pool
import requests
from random import randint, choice
import socket


def gw2apilistworker(input_url):
	baseURL = input_url[0]
	ids = input_url[1]
	version = input_url[2]
	outdict = {}
	getdata = True
	temp = []
	while getdata:
		try:
			request = baseURL + ",".join(str(i) for i in ids)
			header = {'User-agent': version}
			f = requests.get(request, headers=header, timeout=socket.getdefaulttimeout())
			temp = f.json()
			getdata = False
		except Exception as err:
			print('ERROR: %s.' % str(err))
			time.sleep(randint(1, 10))
	for sitem in temp:
		item = sitem["id"]
		# set value to greater of buy and vendor.  If 0 set to minimum sell value
		w = Items.ilist[item]['vendor_value']
		sellMethod = 0
		if sitem['buys']['unit_price'] * .85 > w:
			w = int(sitem['buys']['unit_price'] * .85)
			sellMethod = 1
		if w == 0:
			w = int(sitem['sells']['unit_price'] * .85)
			sellMethod = 2

		# Save all the information we care about
		outdict[item] = {'w': w, 'cost': sitem['sells']['unit_price'], 'recipe': None,
						 'rarity': Items.ilist[item]['rarity'], 'type': Items.ilist[item]['type'],
						 'icon': Items.ilist[item]['img_url'],
						 'output_item_count': Items.ilist[item]['output_item_count'], 'sellMethod': sellMethod,
						 "discover": [], 'whitelist': sitem[u'whitelisted']}

		if outdict[item]['type'] == 'UpgradeComponent' and outdict[item]['rarity'] == 'Exotic':
			outdict[item]['rarity'] = 'Exotic UpgradeComponent'

		# if the item has a low supply, ignore it
		if sitem['sells']['quantity'] <= 50:
			outdict[item]['cost'] = sys.maxsize

	return outdict


def gw2api():
	socket.setdefaulttimeout(5)
	listingURL = "https://api.guildwars2.com/v2/commerce/listings"
	user_agents = [
		'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
		'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36',
		'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1',
		'Mozilla/5.0 (Windows NT 6.3; rv:36.0) Gecko/20100101 Firefox/36.0'
	]
	version = choice(user_agents)
	header = {'User-agent': version}
	f = requests.get(listingURL, headers=header, timeout=socket.getdefaulttimeout())
	temp = f.json()
	valid = []
	invalid = []
	for item in list(Items.ilist.keys()):
		if item in temp:
			valid.append(item)
		else:
			invalid.append(item)

	baseURL = "https://api.guildwars2.com/v2/commerce/prices?ids="

	p = Pool()
	procs = [p.map(gw2apilistworker, [(baseURL, valid[i:i + 200], version) for i in range(0, len(valid), 200)])]

	resultdict = {}
	for p in procs:
		for i in p:
			resultdict.update(i)

	for item in invalid:
		resultdict[item] = {'w': 0, 'cost': sys.maxsize, 'recipe': None, 'rarity': Items.ilist[item]['rarity'],
							'type': Items.ilist[item]['type'], 'icon': Items.ilist[item]['img_url'],
							'output_item_count': Items.ilist[item]['output_item_count'], 'sellMethod': 0,
							"discover": [], 'whitelist': False}
		if resultdict[item]['type'] == 'UpgradeComponent' and resultdict[item]['rarity'] == 'Exotic':
			resultdict[item]['rarity'] = 'Exotic UpgradeComponent'

	return resultdict


# add some costs data to gcList
def appendCosts():
	cList = {}
	getprices = True  # loop variable to loop until we get a return

	count = 10  # loop variable to terminate loop after x attempts
	while getprices and count:
		try:
			cList = gw2api()
			getprices = False
		except Exception as err:
			print('ERROR: %s.' % str(err))
			time.sleep(randint(1, 10))
			count -= 1

	# if loop exited because of this variable we didn't get any data, terminate
	if not count:
		sys.exit(0)

	vendor_items = {
		19792: 8,  # Spool of Jute Thread
		19789: 16,  # Spool of Wool Thread
		19794: 24,  # Spool of Cotton Thread
		19793: 32,  # Spool of Linen Thread
		19791: 48,  # Spool of Silk Thread
		19790: 64,  # Spool of Gossamer Thread
		19704: 8,  # Lump of Tin
		19750: 16,  # Lump of Coal
		19924: 48,  # Lump of Primordium
		12157: 8,  # Jar of Vinegar
		12151: 8,  # Packet of Baking Powder
		12158: 8,  # Jar of Vegetable Oil
		12153: 8,  # Packet of Salt
		12155: 8,  # Bag of Sugar
		12156: 8,  # Jug of Water
		12324: 8,  # Bag of Starch
		12136: 8,  # Bag of Flour
		8576: 16,  # Bottle of Rice Wine
		12271: 8,  # Bottle of Soy Sauce
		13010: 496,  # "Minor Rune of Holding"
		13006: 1480,  # "Rune of Holding"
		13007: 5000,  # "Major Rune of Holding"
		13008: 20000,  # "Greater Rune of Holding"
		70647: 32,  # "Crystalline Bottle"
		75762: 104,  # "Bag of Mortar"
		1000352: 2400,  # Basic Flagpole Purchased from the commendation vendor.
		1000589: 2400,  # Basic Boulder Purchased from the basic decoration vendor.
		1000574: 2400,  # Basic Column Purchased from the basic decoration vendor.
		1000601: 2400,  # Basic Basket Purchased from the basic decoration vendor.
		1000403: 2400,  # White Balloon Purchased from the basic decoration vendor.
		1000223: 2400,  # Basic Planter Purchased from the basic decoration vendor.
		1000548: 2400,  # Basic Pedestal Purchased from the basic decoration vendor.
		1000209: 2400,  # Basic Shrub Purchased from the basic decoration vendor.
		1000516: 2400,  # Basic Crate Purchased from the basic decoration vendor.
		1000620: 2400,  # Basic Tree Purchased from the basic decoration vendor.
		1000202: 2400,  # Basic Table
		1000582: 2400,  # Basic Torch Purchased from the basic decoration vendor.
		1000437: 2400,  # Basic Candle Purchased from the basic decoration vendor.
		1000413: 2400,  # Basic Chair Purchased from the basic decoration vendor.
		1000224: 2400,  # Basic Bookshelf Purchased from the basic decoration vendor.
		46747: 150,  # Thermocatalytic Reagent.
		62942: 8,  # Crafter's Backpack Frame
	}

	for item in vendor_items:
		cList[item]['cost'] = vendor_items[item]
		cList[item]['whitelist'] = True

	# [u'Bell Pepper',u'Basil Leaf',u'Ginger Root',u'Tomato',u'Bowl of Sour Cream',u'Rice Ball',u'Packet of Yeast',u'Glass of Buttermilk',u'Cheese Wedge',u"Almond",u"Apple",u"Avocado",u"Banana",u"Black Bean",u"Celery Stalk",u"Cherry",u"Chickpea",u"Coconut",u"Cumin",u"Eggplant",u"Green Bean",u"Horseradish Root",u"Kidney Bean",u"Lemon",u"Lime",u"Mango",u"Nutmeg Seed",u"Peach",u"Pear",u"Pinenut",u"Shallot"]
	karma = [12235, 12245, 12328, 12141, 12325, 12145, 12152, 12137, 12159, 12337, 12165, 12340, 12251, 12237, 12240,
			 12338, 12515, 12350, 12256, 12502, 12232, 12518, 12239, 12252, 12339, 12543, 12249, 12503, 12514, 12516,
			 12517]
	for item in karma:
		cList[item]['cost'] = 0
		cList[item]['whitelist'] = True
	cList[12132]['cost'] = 99999999  # Loaf of Bread is soulbound, cheat to make it not purchased

	if os.isatty(sys.stdin.fileno()):
		print(len(list(cList.keys())))  # print number of items used by the guides

	return cList
