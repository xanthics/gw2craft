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
Purpose: Get current price data
Note: Requires Python 2.7.x
'''

import time
import json
import os
import sys
import math
import Items
# so we can set custom headers
from multiprocessing import Process, Queue, cpu_count
from urllib import FancyURLopener
from random import choice, randint

# helper function to get data via item_id
def searchGWT(item_id, itemlist, idIndex):
	return next( (element for element in itemlist if item_id == int(element[idIndex])), None)

def itemlistworkerGWT(_itemList, temp, idIndex, buyIndex, sellIndex, supplyIndex, out_q):

	outdict = {}
	for item in _itemList:
		# Get our item from the gw2spidy list
		val = searchGWT(item, temp, idIndex)

		try:
			# set value to greater of buy and vendor.  If 0 set to minimum sell value
			w = Items.ilist[item][u'vendor_value']
			sellMethod = 0
			if val[buyIndex]*.85 > w:
				w = int(val[buyIndex]*.85)
				sellMethod = 1
			if w == 0:
				w = int(val[sellIndex]*.85)
				sellMethod = 2

			# Save all the information we care about
			outdict[item] = {u'w':w,u'cost':val[sellIndex],u'recipe':None,u'rarity':Items.ilist[item][u'rarity'],u'type':Items.ilist[item][u'type'],u'icon':Items.ilist[item][u'img_url'],u'output_item_count':Items.ilist[item][u'output_item_count'],u'sellMethod':sellMethod,u"discover":[]} 
			# if the item has a low supply, ignore it
			if val[supplyIndex] <= 50:
				outdict[item][u'cost'] = 99999999

		# gw2spidy doesn't have the item indexed yet
		except Exception, err:
#			print u'ERROR: %s. %i, %s' % (str(err),item,Items_en.ilist[item])
			# Save all the information we care about
			outdict[item] = {u'w':0,u'cost':99999999,u'recipe':None,u'rarity':Items.ilist[item][u'rarity'],u'type':Items.ilist[item][u'type'],u'icon':Items.ilist[item][u'img_url'],u'output_item_count':Items.ilist[item][u'output_item_count'],u'sellMethod':sellMethod,u"discover":[]} 

		if outdict[item][u'type'] == u'UpgradeComponent' and outdict[item][u'rarity'] == u'Exotic':
			outdict[item][u'rarity'] = u'Exotic UpgradeComponent'

	out_q.put(outdict)

# helper function to parse out only the items we care about from gw2spidy
def cItemlistGWT(itemList,temp,key):
	out_q = Queue()
	nprocs = cpu_count() * 2

	chunksize = int(math.ceil(len(itemList) / float(nprocs)))
	procs = []

	for i in range(nprocs):
		p = Process(target=itemlistworkerGWT,args=(itemList[chunksize * i:chunksize * (i + 1)],temp,key.index(u'id'),key.index(u'buy'),key.index(u'sell'),key.index(u'supply'),out_q))
		procs.append(p)
		p.start()

	resultdict = {}
	for i in range(nprocs):
		resultdict.update(out_q.get())

	for p in procs:
		p.join()

	return resultdict

# helper function to get data via item_id
def search(item_id, itemlist):
	return next( (element for element in itemlist if item_id == int(element[u'data_id'])), None)

def itemlistworker(_itemList, temp, out_q):

	outdict = {}
	for item in _itemList:
		# Get our item from the gw2spidy list
		val = search(item, temp)

		try:
			# set value to greater of buy and vendor.  If 0 set to minimum sell value
			w = Items.ilist[item][u'vendor_value']
			sellMethod = 0
			if val[u'max_offer_unit_price']*.85 > w:
				w = int(val[u'max_offer_unit_price']*.85)
				sellMethod = 1
			if w == 0:
				w = int(val[u'min_sale_unit_price']*.85)
				sellMethod = 2

			# Save all the information we care about
			outdict[item] = {u'w':w,u'cost':val[u'min_sale_unit_price'],u'recipe':None,u'rarity':Items.ilist[item][u'rarity'],u'type':Items.ilist[item][u'type'],u'icon':Items.ilist[item][u'img_url'],u'output_item_count':Items.ilist[item][u'output_item_count'],u'sellMethod':sellMethod,u"discover":[]} 
			# if the item has a low supply, ignore it
			if val[u'sale_availability'] <= 50:
				outdict[item][u'cost'] = 99999999

		# gw2spidy doesn't have the item indexed yet
		except Exception, err:
#			print u'ERROR: %s. %i, %s' % (str(err),item,Items_en.ilist[item])
			# Save all the information we care about
			outdict[item] = {u'w':0,u'cost':99999999,u'recipe':None,u'rarity':Items.ilist[item][u'rarity'],u'type':Items.ilist[item][u'type'],u'icon':Items.ilist[item][u'img_url'],u'output_item_count':Items.ilist[item][u'output_item_count'],u'sellMethod':sellMethod,u"discover":[]} 

		if outdict[item][u'type'] == u'UpgradeComponent' and outdict[item][u'rarity'] == u'Exotic':
			outdict[item][u'rarity'] = u'Exotic UpgradeComponent'

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

# pretend we are a browser
class MyOpener(FancyURLopener):
	user_agents = [
	'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:25.0) Gecko/20100101 Firefox/25.0',
	'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:25.0) Gecko/20100101 Firefox/25.0',
	'Mozilla/5.0 (compatible; MSIE 10.6; Windows NT 6.1; Trident/5.0; InfoPath.2; SLCC1; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET CLR 2.0.50727) 3gpp-gba UNTRUSTED/1.0',
	'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.17 Safari/537.36'
]
	version = choice(user_agents)

def gw2apilistworker(baseURL, ids, out_q,myopener):
	outdict = {}
	getdata = True
	temp = []
	while getdata:
		try:
			f = myopener.open(baseURL+",".join(str(i) for i in ids))
			temp = json.load(f)
			getdata = False
		except Exception, err:
			print u'ERROR: %s.' % str(err)
			time.sleep(randint(1,10))
	for sitem in temp:
		item = sitem["id"]
		# set value to greater of buy and vendor.  If 0 set to minimum sell value
		w = Items.ilist[item][u'vendor_value']
		sellMethod = 0
		if sitem[u'buys'][u'unit_price']*.85 > w:
			w = int(sitem[u'buys'][u'unit_price']*.85)
			sellMethod = 1
		if w == 0:
			w = int(sitem[u'sells'][u'unit_price']*.85)
			sellMethod = 2

		# Save all the information we care about
		outdict[item] = {u'w':w,u'cost':sitem[u'sells'][u'unit_price'],u'recipe':None,u'rarity':Items.ilist[item][u'rarity'],u'type':Items.ilist[item][u'type'],u'icon':Items.ilist[item][u'img_url'],u'output_item_count':Items.ilist[item][u'output_item_count'],u'sellMethod':sellMethod,u"discover":[]} 

		if outdict[item][u'type'] == u'UpgradeComponent' and outdict[item][u'rarity'] == u'Exotic':
			outdict[item][u'rarity'] = u'Exotic UpgradeComponent'

		# if the item has a low supply, ignore it
		if sitem[u'sells'][u'quantity'] <= 50:
			outdict[item][u'cost'] = sys.maxint

	out_q.put(outdict)

def gw2api():
	
	listingURL = "https://api.guildwars2.com/v2/commerce/listings"
	myopener = MyOpener()
	f = myopener.open(listingURL)
	temp = json.load(f)
	valid = []
	invalid = []
	for item in Items.ilist.keys():
		if item in temp:
			valid.append(item)
		else:
			invalid.append(item)


	baseURL = "https://api.guildwars2.com/v2/commerce/prices?ids="

	out_q = Queue()
	procs = []
	chunksize = 200

	for i in range(int(len(valid)/chunksize)):
		p = Process(target=gw2apilistworker,args=(baseURL,valid[chunksize * i:chunksize * (i + 1)],out_q,myopener))
		procs.append(p)
		p.start()

	p = Process(target=gw2apilistworker,args=(baseURL,valid[chunksize * (i + 1):],out_q,myopener))
	procs.append(p)
	p.start()

	resultdict = {}
	for i in range(int(len(valid)/chunksize)+1):
		resultdict.update(out_q.get())

	for p in procs:
		p.join()

	for item in invalid:
		resultdict[item] = {u'w':0,u'cost':sys.maxint,u'recipe':None,u'rarity':Items.ilist[item][u'rarity'],u'type':Items.ilist[item][u'type'],u'icon':Items.ilist[item][u'img_url'],u'output_item_count':Items.ilist[item][u'output_item_count'],u'sellMethod':0,u"discover":[]}
		if resultdict[item][u'type'] == u'UpgradeComponent' and resultdict[item][u'rarity'] == u'Exotic':
			resultdict[item][u'rarity'] = u'Exotic UpgradeComponent'

	return resultdict

# add some costs data to gcList
def appendCosts():
	temp = []
	cList = {}
	myopener = MyOpener()
	getprices = True # loop variable to loop until we get a return

	count = 10 # loop variable to terminate loop after x attempts
	while getprices and count:
		try:
			cList = gw2api()
			getprices = False
		except Exception, err:
			print u'ERROR: %s.' % str(err)
			time.sleep(randint(1,10))
			count -= 1

#	count = 10 # loop variable to terminate loop after x attempts
	# This could be in a while loop and keep trying until success, but unnecessary
#	while getprices and count:
#		try:
#			baseURL = "http://api.guildwarstrade.com/1/bulk/items.json"
#			f = myopener.open(baseURL)
#			temp = json.load(f)
#			if os.isatty(sys.stdin.fileno()):
#				print len(temp[u'items']) # print total items returned from GWT
#			cList = cItemlistGWT(Items.ilist.keys(),temp[u'items'],temp[u'columns'])
#			getprices = False
#		except Exception, err:
#			print u'ERROR: %s.' % str(err)
#			try:
#				baseURL = "http://gw2spidy.com/api/v0.9/json/all-items/all"
#				f = myopener.open(baseURL)
#				temp = json.load(f)
#				if os.isatty(sys.stdin.fileno()):
#					print len(temp[u'results']) # print total items returned from gw2spidy
#				cList = cItemlist(Items.ilist.keys(),temp[u'results'])
#				getprices = False
#			except Exception, err:
#				print u'ERROR: %s.' % str(err)
#				time.sleep(randint(1,10))
#				count -= 1

	# if loop exited because of this variable we didn't get any data, terminate
	if not count:
		sys.exit(0)

	cList[19792][u'cost'] = 8 # Spool of Jute Thread
	cList[19789][u'cost'] = 16 # Spool of Wool Thread
	cList[19794][u'cost'] = 24 # Spool of Cotton Thread
	cList[19793][u'cost'] = 32 # Spool of Linen Thread
	cList[19791][u'cost'] = 48 # Spool of Silk Thread
	cList[19790][u'cost'] = 64 # Spool of Gossamer Thread
	cList[19704][u'cost'] = 8 # Lump of Tin
	cList[19750][u'cost'] = 16 # Lump of Coal
	cList[19924][u'cost'] = 48 # Lump of Primordium
	cList[12157][u'cost'] = 8 # Jar of Vinegar
	cList[12151][u'cost'] = 8 # Packet of Baking Powder
	cList[12158][u'cost'] = 8 # Jar of Vegetable Oil
	cList[12153][u'cost'] = 8 # Packet of Salt
	cList[12155][u'cost'] = 8 # Bag of Sugar
	cList[12156][u'cost'] = 8 # Jug of Water
	cList[12324][u'cost'] = 8 # Bag of Starch
	cList[12136][u'cost'] = 8 # Bag of Flour
	cList[8576][u'cost'] = 16 # Bottle of Rice Wine
	cList[12271][u'cost'] = 8 # Bottle of Soy Sauce
	cList[13010][u'cost'] = 496 # "Minor Rune of Holding"
	cList[13006][u'cost'] = 1480 # "Rune of Holding"
	cList[13007][u'cost'] = 5000 # "Major Rune of Holding"
	cList[13008][u'cost'] = 20000 # "Greater Rune of Holding"
	if 62942 in cList:
		cList[62942][u'cost'] = 8 # Crafter's Backpack Frame
	#[u'Bell Pepper',u'Basil Leaf',u'Ginger Root',u'Tomato',u'Bowl of Sour Cream',u'Rice Ball',u'Packet of Yeast',u'Glass of Buttermilk',u'Cheese Wedge',u"Almond",u"Apple",u"Avocado",u"Banana",u"Black Bean",u"Celery Stalk",u"Cherry",u"Chickpea",u"Coconut",u"Cumin",u"Eggplant",u"Green Bean",u"Horseradish Root",u"Kidney Bean",u"Lemon",u"Lime",u"Mango",u"Nutmeg Seed",u"Peach",u"Pear",u"Pinenut",u"Shallot"]
	karma = [12235,  12245,  12328,  12141,  12325,  12145,  12152,  12137,  12159,  12337,  12165,  12340,  12251,  12237,  12240,  12338,  12515,  12350,  12256,  12502,  12232,  12518,  12239,  12252,  12339,  12543,  12249,  12503,  12514,  12516,  12517]
	for item in karma:
		cList[item][u'cost'] = 0
	cList[12132][u'cost'] = 99999999 # Loaf of Bread is soulbound, cheat to make it not purchased

	if os.isatty(sys.stdin.fileno()):
		print len(cList.keys()) # print number of items used by the guides

	return cList
