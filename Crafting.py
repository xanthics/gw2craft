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
Purpose: Generates a crafting guide for all crafts in Guild Wars 2 based on current market prices
Note: Requires Python 2.7.x
'''

import urllib, json, datetime, math, os, codecs
# recipe and item lists
import Armorsmith, Artificer, Chef, Chef_karma, Huntsman, Jeweler, Leatherworker, Tailor, Weaponsmith, items
# Localized text
import Items_en, Items_de, Items_fr, Items_es, localen, localde, localfr, locales
from multiprocessing import Process, Queue
from copy import deepcopy
from collections import defaultdict
from itertools import chain
from ftplib import FTP
# FTP Login
from ftp_info import ftp_url, ftp_user, ftp_pass

# helper function to get data via item_id
def search(item_id, itemlist):
    return next( (element for element in itemlist if item_id == int(element[u'data_id'])), None)

def itemlistworker(_itemList, temp, out_q):

    outdict = {}
    for item in _itemList:
        # Get our item from the gw2spidy list
        val = search(item, temp)

        # set value to greater of buy and vendor.  If 0 set to minimum sell value
        w = items.ilist[item][u'vendor_value']
        sellMethod = "Vendor"
        if val[u'max_offer_unit_price']*.85 > w:
            w = int(val[u'max_offer_unit_price']*.85)
            sellMethod = "Max Buyout"
        if w == 0:
            w = int(val[u'min_sale_unit_price']*.85)
            sellMethod = "Minimum Sale Price"

        # Save all the information we care about
        outdict[item] = {u'w':w,u'cost':val[u'min_sale_unit_price'],u'recipe':None,u'rarity':items.ilist[item][u'rarity'],u'type':items.ilist[item][u'type'],u'icon':val[u'img'],u'output_item_count':items.ilist[item][u'output_item_count'],u'sellMethod':sellMethod} 

        if u"discover" in items.ilist[item]:
            outdict[item][u'discover'] = 0

        # if the item has a low supply, ignore it
        if val[u'sale_availability'] <= 50:
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

    print len(temp[u'results']) # print total items returned from gw2spidy

    cList = {}
    cList = cItemlist(items.ilist.keys(),temp[u'results'])

    cList[19792][u'cost'] = 8 # Spool of Jute Thread
    cList[19789][u'cost'] = 16 # Spool of Wool Thread
    cList[19794][u'cost'] = 24 # Spool of Cotton Thread
    cList[19793][u'cost'] = 32 # Spool of Linen Thread
    cList[19791][u'cost'] = 48 # Spool of Silk Thread
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
    #[u'Bell Pepper',u'Basil Leaf',u'Ginger Root',u'Tomato',u'Bowl of Sour Cream',u'Rice Ball',u'Packet of Yeast',u'Glass of Buttermilk',u'Cheese Wedge',u"Almond",u"Apple",u"Avocado",u"Banana",u"Black Bean",u"Celery Stalk",u"Cherry",u"Chickpea",u"Coconut",u"Cumin",u"Eggplant",u"Green Bean",u"Horseradish Root",u"Kidney Bean",u"Lemon",u"Lime",u"Mango",u"Nutmeg Seed",u"Peach",u"Pear",u"Pinenut",u"Shallot"]
    karma = [12235,  12245,  12328,  12141,  12325,  12145,  12152,  12137,  12159,  12337,  12165,  12340,  12251,  12237,  12240,  12338,  12515,  12350,  12256,  12502,  12232,  12518,  12239,  12252,  12339,  12543,  12249,  12503,  12514,  12516,  12517]
    for item in karma:
        cList[item][u'cost'] = 0
    cList[12132][u'cost'] = 99999999 # Loaf of Bread is soulbound, cheat to make it not purchased

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
    for i in craftlist[u'ptitem']:
        _xp += int(i*xpgain(level,3,tlvl-25))
        while xp_to_level[level+1] < _xp:
            level += 1
    for i in range(0,int(math.ceil(craftlist[u'refine']))):
        _xp += int(xpgain(level,1,tlvl))
        while xp_to_level[level+1] < _xp:
            level += 1
    for i in craftlist[u'part']:
        _xp += int(i*xpgain(level,2,tlvl))
        while xp_to_level[level+1] < _xp:
            level += 1
    for i in craftlist[u'discovery']:
        _xp += int((i+1)*xpgain(level,3,tlvl))
        while xp_to_level[level+1] < _xp:
            level += 1
    for i in craftlist[u'item']:
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

# Compute a guide
def costCraft(filename,c_recipes,fast,ignoreMixed,cList,mytime,xp_to_level):
    print "Start", filename
    # TODO Hack, fix this
    # This is changing the recipe for Bronze Ingot to use 2 Copper Ore.
    if 19679 in c_recipes[0]:
        c_recipes[0][19679][19697] = 2

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
                    cList[i][u'cost'] = 99999999
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
            bucket = makeQueuecraft(c_recipes[tier], cList,craftcount,tier,ignoreMixed,xp_to_level)
            bkey = sorted(bucket, reverse=True)
            # If we already made an "Item" this tier from another recipe, keep making that item
            if make[tier] and "cook" in filename: 
                bkey = []
                for item in bucket:
                    if bucket[item][u'item_id'] == make[tier].keys()[0]:
                        bkey.append(item)
                        break
            else:
                while cList[bucket[bkey[0]][u'item_id']][u'type'] in non_item:
                    bkey.pop(0)

        while craftcount[tier][u'current_xp'] < xp_to_level[tier + 25]:

            # We still want to compute every make on fast guides for the 375-400 range
            if fast and tier == 375 and not "cook" in filename:
                bucket = {}
                bucket = makeQueuecraft(c_recipes[tier], cList,craftcount,tier,ignoreMixed,xp_to_level)
                bkey = sorted(bucket, reverse=True)
            elif not fast:
                if not tier == 0 and craftcount[tier][u'current_xp'] <= xp_to_level[tier+10]:
                    bucket = makeQueuecraft(dict(chain(c_recipes[tier].iteritems(),c_recipes[tier-25].iteritems())), cList,craftcount,tier,ignoreMixed,xp_to_level)
                else:
                    bucket = makeQueuecraft(c_recipes[tier], cList,craftcount,tier,ignoreMixed,xp_to_level)
                bkey = sorted(bucket, reverse=True)
                
            tcost += bucket[bkey[0]][u'cost']
            treco += cList[bucket[bkey[0]][u'item_id']][u'w'] * int(cList[bucket[bkey[0]][u'item_id']][u'output_item_count'])
            sell[bucket[bkey[0]][u'item_id']] += int(cList[bucket[bkey[0]][u'item_id']][u'output_item_count'])
            sole = 0
            recalc = {tier:0} # always recalc the tier we are on
            for item in bucket[bkey[0]][u'make']:
                if item == bucket[bkey[0]][u'item_id'] and int(cList[item][u'tier']) < tier:
                    craftcount[tier][u'ptitem'].append(rarityNum(cList[item][u'rarity']))
                    pmake[tier][item] += 1
                elif not cList[item][u'type'] in non_item and not 'discover' in cList[item]:
                    cList[item][u'discover'] = 1
                    craftcount[int(cList[item][u'tier'])][u'discovery'].append(rarityNum(cList[item][u'rarity']))
                    make[int(cList[item][u'tier'])][item] += 1
                elif not cList[item][u'type'] in non_item:
                    craftcount[int(cList[item][u'tier'])][u'item'].append(rarityNum(cList[item][u'rarity']))
                    make[int(cList[item][u'tier'])][item] += 1
                elif cList[item][u'type'] == u'Refinement':
                    if item == 19679: # Bronze Ingot
                        craftcount[int(cList[item][u'tier'])][u'refine'] += 0.2
                    else:
                        craftcount[int(cList[item][u'tier'])][u'refine'] += 1.0
                    make[int(cList[item][u'tier'])][item] += 1
                else:
                    if item in [13063,  13189,  13207,  13219,  13045,  13022,  13075,  13177,  13096,  13033] and not sole: # Sole IDs
                        sole +=1
                    else:
                        craftcount[int(cList[item][u'tier'])][u'part'].append(rarityNum(cList[item][u'rarity']))
                    make[int(cList[item][u'tier'])][item] += 1
                recalc[int(cList[item][u'tier'])] = 0

            for ctier in recalc:
                craftcount[ctier][u'current_xp'] = compute_level((xp_to_level[ctier] if ctier == 0 or xp_to_level[ctier] >= craftcount[ctier-25][u'current_xp'] else craftcount[ctier-25][u'current_xp']), craftcount[ctier],ctier,xp_to_level)

            t = int(math.floor(tier/75.0)*75)
            if t == 375:
                t = 300
            if "cook" in filename:
                for item in bucket[bkey[0]][u'buy']:
                    buy[item] += 1
            else:
                for item in bucket[bkey[0]][u'buy']:
                    # Lump of Tin and Bronze Ingot
                    if t == 0 and item == 19704 and 19679 in bucket[bkey[0]][u'make']:
                        tierbuy[t][item] += .2
                        buy[item] += .2
                    else:
                        tierbuy[t][item] += 1
                        buy[item] += 1

    printtofile(tcost, treco, sell, deepcopy(make), deepcopy(pmake), deepcopy(buy), deepcopy(tierbuy), deepcopy(cList), filename, mytime, Items_de.ilist, localde, "de/")
    printtofile(tcost, treco, sell, deepcopy(make), deepcopy(pmake), deepcopy(buy), deepcopy(tierbuy), deepcopy(cList), filename, mytime, Items_fr.ilist, localfr, "fr/")
    printtofile(tcost, treco, sell, deepcopy(make), deepcopy(pmake), deepcopy(buy), deepcopy(tierbuy), deepcopy(cList), filename, mytime, Items_es.ilist, locales, "es/")
    totals = {}
    totals.update(printtofile(tcost, treco, sell, deepcopy(make), deepcopy(pmake), deepcopy(buy), deepcopy(tierbuy), deepcopy(cList), filename, mytime, Items_en.ilist, localen))
    return totals    

# given an item, determine if it is better to craft its sub items, or buy them.  return the recipe.
# include cost for current state, and xp generated.
def calcRecipecraft(recipe,items,craftcount,tier,count,itier,ignoreMixed,xp_to_level):
    level = 0
    while xp_to_level[int(level)] < craftcount[int(tier)][u'current_xp']:
        level += 1
    xptotal = 0
    make = []
    buy = []
    cost = 0
    non_item = [u'Refinement', u'Insignia', u'Inscription', u'Component']
    # For our traditional style guides, we still want to consider buying gems even though you can refine.    This is a list of those gems
    # "Amber Pebble","Garnet Pebble","Malachite Pebble","Pearl","Tiger's Eye Pebble","Turquoise Pebble","Amethyst Nugget","Carnelian Nugget","Lapis Nugget","Peridot Nugget","Spinel Nugget","Sunstone Nugget","Topaz Nugget","Amethyst Lump","Carnelian Lump","Lapis Lump","Peridot Lump","Spinel Lump","Sunstone Lump","Topaz Lump","Beryl Shard","Chrysocola Shard","Coral Chunk","Emerald Shard","Opal Shard","Ruby Shard","Sapphire Shard","Beryl Crystal","Chrysocola Crystal","Coral Tentacle","Emerald Crystal","Opal Crystal","Ruby Crystal","Sapphire Crystal","Passion Flower"
    gemss = [24534,  24464,  24466,  24500,  24467,  24465,  24501,  24469,  24470,  24468,  24889,  24471,  24535,  24527,  24472,  24507,  24504,  24526,  24503,  24506,  24872,  24870,  24874,  24871,  24875,  24873,  24876,  24519,  24511,  24509,  24473,  24521,  24474,  24475,  37907]
    # impossible to make item at this point.
    if int(items[recipe][u'tier']) > int(itier):
#        print recipe
        return 9999999999, -99999999999, make, buy
    for i in range(0,count):
        make.append(recipe)
    if int(items[recipe][u'tier']) < int(tier) and not items[recipe][u'type'] in non_item:
        xptotal = xp_calc(0,0,count,0,rarityNum(items[recipe][u'rarity']),int(items[recipe][u'tier']),level)*.85
    elif not items[recipe][u'type'] in non_item and not 'discover' in items[recipe]:
        xptotal = xp_calc(0,0,count-1,1,rarityNum(items[recipe][u'rarity']),int(items[recipe][u'tier']),level)
    elif not items[recipe][u'type'] in non_item:
        xptotal = xp_calc(0,0,count,0,rarityNum(items[recipe][u'rarity']),int(items[recipe][u'tier']),level)
    elif items[recipe][u'type'] == u'Refinement':
        if 19679 == recipe:
            xptotal = math.ceil(xp_calc(count,0,0,0,1.0,int(items[recipe][u'tier']),level)*0.2)
        else:
            xptotal = xp_calc(count,0,0,0,1.0,int(items[recipe][u'tier']),level)
    else:
        if recipe in [13063,  13189,  13207,  13219,  13045,  13022,  13075,  13177,  13096,  13033]: # Sole
            xptotal = xp_calc(0,count,0,0,1.0,int(items[recipe][u'tier']),level)*0.5
        else:
            xptotal = xp_calc(0,count,0,0,1.0,int(items[recipe][u'tier']),level)

    mycost = 0
    for item in items[recipe][u'recipe']:
        mycost += items[item][u'cost']*items[recipe][u'recipe'][item]

    mycost *= count
    for item in items[recipe][u'recipe']:
        if not items[item][u'recipe'] == None:
            tcost, txptotal, tmake, tbuy = calcRecipecraft(item,items,craftcount,items[item][u'tier'],items[recipe][u'recipe'][item]*count,int(items[recipe][u'tier']),ignoreMixed,xp_to_level)
            if (ignoreMixed and item not in gemss) or tcost < items[item][u'cost']*items[recipe][u'recipe'][item]*count or float(xptotal+txptotal)/float(mycost-items[item][u'cost']*items[recipe][u'recipe'][item]*count+tcost) >= float(xptotal)/float(mycost):
                xptotal += txptotal*.85
                cost += tcost
                buy += tbuy
                make += tmake
            else:
                for i in range(0,int(math.ceil(count*items[recipe][u'recipe'][item]))):
                    buy.append(item)
                cost += items[item][u'cost']*count*items[recipe][u'recipe'][item]
        else:
            for i in range(0,int(math.ceil(count*items[recipe][u'recipe'][item]))):
                buy.append(item)
            cost += items[item][u'cost']*count*items[recipe][u'recipe'][item]
    return cost, xptotal, make, buy

def makeQueuecraft(recipes,items,craftcount,tier,ignoreMixed,xp_to_level):
    outdict = {}
    cost = 0
    xptotal = 0
    make = []
    buy = []
    non_item = [u'Refinement', u'Insignia', u'Inscription', u'Component']

    for recipe in recipes.keys():
        # swap which line is commented if you want guides that include "make 83 epaulets" for 25 copper savings
        if not items[recipe][u'type'] in non_item:
#        if int(items[recipe][u'tier']) > int(tier)-24:
            cost, xptotal, make, buy = calcRecipecraft(recipe,items,craftcount,tier,1,tier,ignoreMixed,xp_to_level)
            # Uncomment these 3 lines and comment the 4th if you want guides that try to make the lowest total price after sellback
#            if items[recipe][u'w'] > cost:
#               weight = float(items[recipe][u'w'] - cost)*100000.0
#            elif xptotal:
            if xptotal:
                weight = float(xptotal)/float(cost)
            else:
                weight = -1.0*float(cost)

            # don't want to collide keys
            while weight in outdict:
                weight -= 0.0001
            outdict[weight] = {'item_id':recipe,'w':xptotal,'make':make,'buy':buy,'cost':cost}

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

# TODO localize text strings for supported languages. -- modify to take a file with all the language sensitive strings
def printtofile(tcost, treco, sell, make, pmake, buy, tierbuy, cList, filename, mytime, cListName, localText, path=""):
    buttonList = []
    totals = {}
    if tierbuy:
        totals[filename.split('.')[0]] = {0:defaultdict(int),75:defaultdict(int),150:defaultdict(int),225:defaultdict(int),300:defaultdict(int),'total':int(tcost)}
    else:
        totals[filename.split('.')[0]] = int(tcost)

    non_item = [u'Refinement', u'Insignia', u'Inscription', u'Component']

    recipebuy = []
    for tier in [0,25,50,75,100,125,150,175,200,225,250,275,300,325,350,375]:
        for item in make[tier]:
            if item in localText.karma_recipe:
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
            tcost += cList[19697][u'cost']*var+8.0*(0.2*var)
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
            if item in localText.karma_chef:
                b_karma_c[item] = buy[item]
            elif item in localText.karma_items:
                if path == "":
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

    karma_str = u"<div class=\"s%d\"><input type=\"checkbox\" /><span class=\"itemIcon\" style=\"background-image: url(%s);\"></span><span class=\"quantity\">%d</span> <button title=\"Click To Toggle\" class=\"%s arrow\" id=\"%d\">%s</button><div class=\"lsbutton\" id=\"1%d\">%d <span class=\"karmaIcon\"></span> per 25 <br /> %s</div></div>\n"
    collectable_str = u"<div class=\"s%d\"><input type=\"checkbox\" /><span class=\"itemIcon\" style=\"background-image: url(%s);\"></span><span class=\"quantity\">%d</span> <span class=\"%s\">%s</span> (%4s per)</div>\n"


    t = 0 # used to control div background color
    kt = 0 # karma total
    with codecs.open(path+filename, 'wb', encoding='utf-8') as f:
        f.write(u'<!DOCTYPE html>\n')
        f.write(u'<html>\n')
        f.write(u'<head>\n')
        f.write(u'    <title>'+filename.split('.')[0].replace("_"," ").title()+'</title>\n')
        f.write(u'    <meta name="description" content="Guild Wars 2 always current crafting guide for '+filename.split('.')[0].replace("_"," ").title()+'">\n')
        f.write(u'    <meta http-equiv="content-type" content="text/html;charset=UTF-8">\n')
        f.write(u'    <link href="/css/layout.css" rel="stylesheet" type="text/css" />') 
        f.write(u'    <link rel="icon" type="image/png" href="/fi.gif">')
        f.write(u'    <script src="//ajax.googleapis.com/ajax/libs/jquery/1.9.0/jquery.min.js"></script>\n')
        f.write(u'    <script>(window.jQuery || document.write(\'<script src="http://ajax.aspnetcdn.com/ajax/jquery/jquery-1.9.0.min.js"><\/script>\'));</script>\n')
        f.write(u'    <script src="/js/menu.js" type="text/javascript"></script>\n')
        f.write(u'</head>\n')
        f.write(u'<body>\n'+localText.header%(filename,filename,filename)+'\n<section>')
        f.write(u'<div style="width: 100%; border: 2px #fffaaa solid; border-left: 0px; border-right: 0px; background: #fffddd; height: 24px;">\n')
        f.write(u'<img src="/css/warning-icon.png" width="24px" height="24px" style="padding: 0 8px 0 8px; float: left;"><span style="position: relative; top: 4px;"><span style="color: red">Do not refresh this page.</span>    It may change. Updated: '+mytime+'</b></span>\n')
        f.write(u'</div><br />\n')
        f.write(u'Wherever you see this  <img src=\"/img/arrow.png\"></img> you can click for more information <br />')
        f.write(u'<h1>'+filename.split('.')[0].replace("_"," ").title()+'</h1>')
        # adword
        f.write(u'<div style="display:block;float:Right;"> \
                \n<script type="text/javascript"><!-- \
                \ngoogle_ad_client = "ca-pub-6865907345688710"; \
                \n/* half page banner 2 */ \
                \ngoogle_ad_slot = "9379048580"; \
                \ngoogle_ad_width = 234; \
                \ngoogle_ad_height = 60; \
                \n//--> \
                \n</script> \
                \n<script type="text/javascript" \
                \nsrc="http://pagead2.googlesyndication.com/pagead/show_ads.js"> \
                \n</script> \
                \n</div>\n')
        f.write(u'<dl>\n')
        f.write(u'    <dt>'+localText.iCost+'</dt>\n')
        f.write(u'    <dd>'+mFormat(tcost)+'</dd>\n')
        f.write(u'    <dt>'+localText.eRecovery+'</dt>\n')
        f.write(u'    <dd><span style="position: relative; left: -9px;">- '+mFormat(treco)+'</span></dd>\n')
        f.write(u'    <dt>'+localText.fCost+'</dt>\n')
        f.write(u'    <dd style="border-top: 1px #666 solid;">'+mFormat(tcost-treco)+'</dd>\n')
        f.write(u'</dl>')
        f.write(u'<div class="clear"></div>')
        f.write(u'<br /><button title=\"Click To Toggle\" class=\"arrow\" id=\"tcost\">'+localText.sList+':</button><div class=\"lsbutton\" id=\"1tcost\">')
        for line in sorted(sell):
            if cList[line][u'w'] > 0:
                t = (t+1)%2
                f.write(u'<div class=\"s%i\">%3i <span class=\"%s\">%s</span> - Sold for %s per via %s</div>\n'%(t,sell[line],cList[line][u'rarity'],cListName[line],mFormat(cList[line][u'w']),cList[line][u'sellMethod']))

        f.write(u"</div><script type=\"text/javascript\">$('#1tcost').hide();</script><br />")
        buttonList.append('tcost')

        if b_vendor or b_karma_c or b_karma_w:
            f.write(u"<h2>BUY VENDOR</h2>\n")
            if b_karma_c or b_karma_w:
                f.write(u"<span class=\"karmaIcon\"></span> Note: 11 Basil Leaf(e.g.) means buy 1 bulk Basil Leaf and you will have 14 left over<br /><br />\n")

            for item in sorted(b_karma_w):
                t = (t+1)%2
                f.write(karma_str%(t,cList[item][u'icon'],buy[item],cList[item][u'rarity'],item,cListName[item],item,localText.karma_items[item][u'cost'],localText.karma_items[item][u'note']))
                buttonList.append(item)
                kt += int(math.ceil(buy[item]/25.0)*localText.karma_items[item][u'cost'])

            for item in sorted(b_karma_c):
                t = (t+1)%2
                f.write(karma_str%(t,cList[item][u'icon'],buy[item],cList[item][u'rarity'],item,cListName[item],item,localText.karma_chef[item][u'cost'],localText.karma_chef[item][u'note']))
                buttonList.append(item)
                kt += int(math.ceil(buy[item]/25.0)*localText.karma_chef[item][u'cost'])

            for item in sorted(b_vendor):
                t = (t+1)%2
                f.write(u"<div class=\"s%i\"><input type=\"checkbox\" /><span class=\"itemIcon\" style=\"background-image: url(%s);\"></span><span class=\"quantity\">%i</span> <span class=\"%s\">%s</span> (%4s per from Vendor)</div>\n"%(t,cList[item][u'icon'],buy[item],cList[item][u'rarity'],cListName[item],mFormat(cList[item][u'cost'])))

        if recipebuy:
            f.write(u"<h2>"+localText.bRecipes+"</h2>\n")
            for item in recipebuy:
                t = (t+1)%2
                f.write((u"<div class=\"s%d\"><input type=\"checkbox\" /><span class=\"itemIcon\" style=\"background-image: url(%s);\"></span><button title=\"Click To Toggle\" class=\"arrow %s\" id=\"%d\">%s</button><div class=\"lsbutton\" id=\"1%d\">%i <span class=\"karmaIcon\"></span>, %s</div></div>\n")%(t,cList[item]['icon'],cList[item]['rarity'],item,cListName[item],item,localText.karma_recipe[item]['cost'],localText.karma_recipe[item]['note']))
                buttonList.append(item)
                kt += int(localText.karma_recipe[item][u'cost'])
        if kt:
            f.write(u'<br />\nTotal <span class=\"karmaIcon\"></span>: '+str(kt)+'<br />\n')
        if b_common or b_fine or b_rare or b_gem or b_holiday or b_food:
            f.write(u'<h2>'+localText.collectibles+'</h2>\n')
            for item in sorted(b_common):
                t = (t+1)%2
                f.write(collectable_str%(t,cList[item][u'icon'],buy[item],cList[item][u'rarity'],cListName[item],mFormat(cList[item][u'cost'])))
            for item in sorted(b_fine):
                t = (t+1)%2
                f.write(collectable_str%(t,cList[item][u'icon'],buy[item],cList[item][u'rarity'],cListName[item],mFormat(cList[item][u'cost'])))
            for item in sorted(b_rare):
                t = (t+1)%2
                f.write(collectable_str%(t,cList[item][u'icon'],buy[item],cList[item][u'rarity'],cListName[item],mFormat(cList[item][u'cost'])))
            for item in sorted(b_gem):
                t = (t+1)%2
                f.write(collectable_str%(t,cList[item][u'icon'],buy[item],cList[item][u'rarity'],cListName[item],mFormat(cList[item][u'cost'])))
            for item in sorted(b_holiday):
                t = (t+1)%2
                f.write(collectable_str%(t,cList[item][u'icon'],buy[item],cList[item][u'rarity'],cListName[item],mFormat(cList[item][u'cost'])))
            for item in sorted(b_food):
                t = (t+1)%2
                f.write(collectable_str%(t,cList[item][u'icon'],buy[item],cList[item][u'rarity'],cListName[item],mFormat(cList[item][u'cost'])))

        if b_mix:
            f.write(u'<h2>MIXED(Buy on TP)</h2>\n')
            for item in sorted(b_mix):
                t = (t+1)%2
                f.write(collectable_str%(t,cList[item][u'icon'],buy[item],cList[item][u'rarity'],cListName[item],mFormat(cList[item][u'cost'])))

        f.write(u"<br />\n<br />\n<h2>MAKE</h2>\n")
        f.write(u"<button title=\"Click To Show All Discovery Recipes\" class =\"info\" id=\"show_all\">Expand All Discovery Recipes</button><br />")
        f.write(u"<button title=\"Click To Hide All Discovery Recipes\" class =\"info\" id=\"hide_all\">Collapse All Discovery Recipes</button>")
        rt = 0
        for tier in [0,25,50,75,100,125,150,175,200,225,250,275,300,325,350,375]:
            if tierbuy and tier in [0,75,150,225,300]:
                tt = 0
                tc = tier+75
                if tier == 300:
                    tc += 25
                f.write((u"<br /><br /><h4>Tier %i, Levels %i-%i:<button title=\"Click To Toggle\" class =\"info\" id=\""+str(tier)+"tier\">Buy List(Only Tier %i)</button></h4>\n<div class=\"lsbutton\" id=\"1"+str(tier)+"tier\">")%(tier/75+1,tier,tc,tier/75+1))
                f.write(u"<h5>Notice: If you are following the full guide then you already purchased these materials.</h5>")
                for item in sorted(tierbuy[tier]):
                    t = (t+1)%2
                    f.write(u"<div class=\"s"+str(t)+"\"><input type=\"checkbox\" /><span class=\"itemIcon\" style=\"background-image: url("+cList[item][u'icon']+");\"></span><span class=\"quantity\">%i</span> <span class=\"%s\">%s</span> (%4s per)</div>\n"%(tierbuy[tier][item],cList[item][u'rarity'],cListName[item],mFormat(cList[item][u'cost'])))
                    tt += tierbuy[tier][item]*cList[item][u'cost']
                buttonList.append(str(tier)+'tier')
                rt += tt
                totals[filename.split('.')[0]][tier] = tt
                f.write(u"</div><h4>Cost: %s ( Rolling Total: %s)</h4>\n"% (mFormat(tt),mFormat(rt)))        
            f.write((u"<br />\n<h3>Level:%3i</h3>\n")%(tier))
            if pmake[tier]:
                for item in sorted(pmake[tier]):
                    t = (t+1)%2
                    f.write(u"<div class=\"s"+str(t)+"\">Make:%3i <span class=\"%s\">%s</span> (From %i tier) </div>\n"%(pmake[tier][item],cList[item][u'rarity'],cListName[item],tier-25))
            for item in sorted(make[tier], key=make[tier].get,reverse=True):
                if cList[item][u'type'] == u'Refinement':
                    t = (t+1)%2
                    if item == 19679: # Bronze Ingot
                        f.write(u"<div class=\"s"+str(t)+"\">Make:%3i <span class=\"%s\">%s</span> (Produces 5 Ingot per make)</div>\n"%(make[tier][item],cList[item][u'rarity'],cListName[item]))
                    else:
                        f.write(u"<div class=\"s"+str(t)+"\">Make:%3i <span class=\"%s\">%s</span></div>\n"%(make[tier][item],cList[item][u'rarity'],cListName[item]))
            for item in sorted(make[tier], key=make[tier].get,reverse=True):
                if cList[item][u'type'] in non_item and not cList[item][u'type'] == u'Refinement':
                    t = (t+1)%2
                    if item in [13063,  13189,  13207,  13219,  13045,  13022,  13075,  13177,  13096,  13033]: # Sole
                        f.write(u"<div class=\"s"+str(t)+"\">Make:%3i <span class=\"%s\">%s</span> (Produces 2 Soles per make)</div>\n"%(make[tier][item]/2,cList[item][u'rarity'],cListName[item]))
                    else:
                        f.write(u"<div class=\"s"+str(t)+"\">Make:%3i <span class=\"%s\">%s</span></div>\n"%(make[tier][item],cList[item][u'rarity'],cListName[item]))
            for item in sorted(make[tier]):

                if 'discover' in cList[item] and cList[item][u'discover'] == 1:
                    if make[tier][item] > 1:
                        make[tier][item] -= 1
                    else:
                        del(make[tier][item])
                    t = (t+1)%2
                    tstr = "<div class=\"sbutton\" id=\"1"+str(item)+"\">"
                    for s in cList[item][u'recipe']:
                        tstr += "\n<br />\t<span class=\"itemIcon\" style=\"background-image: url("+cList[s][u'icon']+");\"></span> <span class=\""+cList[s][u'rarity']+'\">'+cListName[s]+"</span> ("+str(cList[item][u'recipe'][s])+")"
                    tstr += "</div><br />"
                    f.write(u"<div class=\"s"+str(t)+"\">Discover: <button class=\"arrow "+cList[item][u'rarity']+'\" title=\"Click To Toggle\" id=\"'+str(item)+'\">'+cListName[item]+"</button> "+tstr+"\n</div>\n")
                    buttonList.append(item)
            for item in sorted(make[tier]):
                if not cList[item][u'type'] in non_item:
                    t = (t+1)%2
                    f.write(u"<div class=\"s"+str(t)+"\">Make:%3i <span class=\"%s\">%s</span></div>\n"%(make[tier][item],cList[item][u'rarity'],cListName[item]))
        f.write(u'<br />\n<h3>Level:400</h3>\n')
        t = (t+1)%2
        f.write(u"<div class=\"s"+str(t)+"\">Nothing.    You are done!</div>\n")
        # adword
        f.write(u'<br /><div style="display:block;text-align:Right;"> \
                \n<script type="text/javascript"><!-- \
                \ngoogle_ad_client = "ca-pub-6865907345688710"; \
                \n/* Tail ad */ \
                \ngoogle_ad_slot = "9889445788"; \
                \ngoogle_ad_width = 336; \
                \ngoogle_ad_height = 280; \
                \n//--> \
                \n</script> \
                \n<script type="text/javascript" \
                \nsrc="http://pagead2.googlesyndication.com/pagead/show_ads.js"> \
                \n</script> \
                \n</div>\n')
        f.write(u'</section>\n'+localText.cright+'\n<script type="text/javascript">\n')
        for item in buttonList:
            f.write(u"$(\"#"+str(item)+"\").click(function () {\n\t$(\"#1"+str(item)+"\").toggle();});\n")
        f.write(u"$(\".sbutton\").hide();\n")
        f.write(u"$(\".lsbutton\").hide();\n")
        f.write(u"$(\"#show_all\").click(function () {$(\".sbutton\").show();")
        f.write(u"});\n$(\"#hide_all\").click(function () {$(\".sbutton\").hide();")
        f.write(u'});\n</script>\n')
        f.write(u'</body>\n')
        f.write(u'</html>\n')
    return totals

def maketotals(totals, mytime, localText, path=""):

    page = '''
<!DOCTYPE html>
<html>
<head>
    <title>Totals</title>
    <meta name="description" content="Guild Wars 2 always current crafting guide price totals">
    <meta http-equiv="content-type" content="text/html;charset=UTF-8">

    <link href="/css/layout.css" rel="stylesheet" type="text/css" />
    <link rel="icon" type="image/png" href="/fi.gif" />

    <script src="//ajax.googleapis.com/ajax/libs/jquery/1.9.0/jquery.min.js"></script>
    <script src="/js/menu.js" type="text/javascript"></script>
</head>
<body>'''
    page += localText.header%('total.html','total.html','total.html')

    page += "<section>\n<h5 style=\"text-align:center;\">Updated: " + mytime + "</h5>"
    page += '''
<strong>Note:</strong> The prices show here are initial costs and do not take sellback into account.
    <table>
    <tr><th>Craft</th><th>Total - Normal</th><th>Total - Fast</th></tr>\n'''
    page += '<tr><td>cooking_karma</td><td>'+mFormat(totals[u'cooking_karma'])+'</td><td>'+mFormat(totals[u'cooking_karma_fast'])+'</td></tr>\n'
    page += '<tr><td>cooking_karma_light</td><td>'+mFormat(totals[u'cooking_karma_light'])+'</td><td>'+mFormat(totals[u'cooking_karma_fast_light'])+'</td></tr>\n'
    page += '<tr><td>cooking</td><td>'+mFormat(totals[u'cooking'])+'</td><td>'+mFormat(totals[u'cooking_fast'])+'</td></tr>\n'
    
    page += "</table>\n<br />\n<table>\n<tr><th>Craft</th><th>Total Cost</th><th>Tier 0-75</th><th>Tier 75-150</th><th>Tier 150-225</th><th>Tier 225-300</th><th>Tier 300-400</th></tr>\n"
    cttl = 0
    for i in [u'armorcraft','artificing','huntsman','jewelcraft','leatherworking','tailor','weaponcraft']:
        page += '<tr><td>'+i+'</td><td>'+mFormat(totals[i][u'total'])+'</td><td>'+mFormat(totals[i][0])+'</td><td>'+mFormat(totals[i][75])+'</td><td>'+mFormat(totals[i][150])+'</td><td>'+mFormat(totals[i][225])+'</td><td>'+mFormat(totals[i][300])+'</td></tr>\n'
        cttl += totals[i][u'total']

    page += ' </table>\n<br /><strong>Total for non-cooking normal: </strong>' + mFormat(cttl)

    page += "<br /><br /></table>\n<br />\n<table>\n<tr><th>Craft</th><th>Total Cost</th><th>Tier 0-75</th><th>Tier 75-150</th><th>Tier 150-225</th><th>Tier 225-300</th><th>Tier 300-400</th></tr>\n"
    cttl = 0
    for i in [u'armorcraft_fast','artificing_fast','huntsman_fast','jewelcraft_fast','leatherworking_fast','tailor_fast','weaponcraft_fast']:
        page += '<tr><td>'+i+'</td><td>'+mFormat(totals[i][u'total'])+'</td><td>'+mFormat(totals[i][0])+'</td><td>'+mFormat(totals[i][75])+'</td><td>'+mFormat(totals[i][150])+'</td><td>'+mFormat(totals[i][225])+'</td><td>'+mFormat(totals[i][300])+'</td></tr>\n'
        cttl += totals[i][u'total']

    page += ' </table>\n<br /><strong>Total for non-cooking fast: </strong>' + mFormat(cttl)

    page += "<br /><br /></table>\n<br />\n<table>\n<tr><th>Craft</th><th>Total Cost</th><th>Tier 0-75</th><th>Tier 75-150</th><th>Tier 150-225</th><th>Tier 225-300</th><th>Tier 300-400</th></tr>\n"
    cttl = 0
    for i in [u'armorcraft_craft_all','artificing_craft_all','huntsman_craft_all','jewelcraft_craft_all','leatherworking_craft_all','tailor_craft_all','weaponcraft_craft_all']:
        page += '<tr><td>'+i+'</td><td>'+mFormat(totals[i][u'total'])+'</td><td>'+mFormat(totals[i][0])+'</td><td>'+mFormat(totals[i][75])+'</td><td>'+mFormat(totals[i][150])+'</td><td>'+mFormat(totals[i][225])+'</td><td>'+mFormat(totals[i][300])+'</td></tr>\n'
        cttl += totals[i][u'total']

    page += ' </table>\n<br /><strong>Total for non-cooking traditional: </strong>' + mFormat(cttl)

    page += '\n</section>\n' + localText.cright + '\n</body>\n</html>'

    with codecs.open(path+'total.html', 'wb', encoding='utf-8') as f:
        f.write(page)

# Join 2 recipe dicts
def join(A, B):
        if not isinstance(A, dict) or not isinstance(B, dict):
                return A or B
        return dict([(a, join(A.get(a), B.get(a))) for a in set(A.keys()) | set(B.keys())])

def recipeworker(cmds, cList, mytime, xp_to_level, out_q):
    totals = {}
    for cmd in cmds:
        totals.update(costCraft(cmd[0],cmd[1],cmd[2],cmd[3],deepcopy(cList),mytime,xp_to_level))
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
    rList.append([("cooking_karma_fast.html",cooking_karma,True,False),
                  ("cooking_karma_fast_light.html",cooking_karma,True,False),
                  ("cooking_fast.html",Chef.recipes,True,False)])
    rList.append([("cooking_karma.html",cooking_karma,False,False),
                  ("cooking_karma_light.html",cooking_karma,False,False),
                  ("cooking.html",Chef.recipes,False,False)])
    rList.append([("jewelcraft_fast.html",Jeweler.recipes,True,False),
                  ("jewelcraft.html",Jeweler.recipes,False,False),
                  ("jewelcraft_craft_all.html",Jeweler.recipes,False,True)])
    rList.append([("artificing_fast.html",Artificer.recipes,True,False),
                  ("artificing.html",Artificer.recipes,False,False),
                  ("artificing_craft_all.html",Artificer.recipes,False,True)])
    rList.append([("weaponcraft_fast.html",Weaponsmith.recipes,True,False),
                  ("weaponcraft.html",Weaponsmith.recipes,False,False),
                  ("weaponcraft_craft_all.html",Weaponsmith.recipes,False,True)])
    rList.append([("huntsman_fast.html",Huntsman.recipes,True,False),
                  ("huntsman.html",Huntsman.recipes,False,False),
                  ("huntsman_craft_all.html",Huntsman.recipes,False,True)])
    rList.append([("armorcraft_fast.html",Armorsmith.recipes,True,False),
                  ("armorcraft.html",Armorsmith.recipes,False,False),
                  ("armorcraft_craft_all.html",Armorsmith.recipes,False,True)])
    rList.append([("tailor_fast.html",Tailor.recipes,True,False),
                  ("tailor.html",Tailor.recipes,False,False),
                  ("tailor_craft_all.html",Tailor.recipes,False,True)])
    rList.append([("leatherworking_fast.html",Leatherworker.recipes,True,False),
                  ("leatherworking.html",Leatherworker.recipes,False,False),
                  ("leatherworking_craft_all.html",Leatherworker.recipes,False,True)])

    nprocs = len(rList)

    procs = []
    global header
    global cright

    for i in range(nprocs):
        p = Process(target=recipeworker,args=(rList[i],cList,mytime,xp_to_level,out_q))
        procs.append(p)
        p.start()

    totals = {}
    for i in range(nprocs):
        totals.update(out_q.get())

    for p in procs:
        p.join()

    maketotals(totals,mytime,localen)
    maketotals(totals,mytime,localde,'de/')
    maketotals(totals,mytime,localfr,'fr/')
    maketotals(totals,mytime,locales,'es/')

    print datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
    print "Starting upload"
    myFtp = FTP(ftp_url)
    myFtp.login(ftp_user,ftp_pass)
    for lang in ['','de/','fr/','es/']:
        for item in [u"cooking_fast.html", "cooking_karma_fast.html", "cooking_karma_fast_light.html",
                     "cooking.html", "cooking_karma.html", "cooking_karma_light.html",
                     "leatherworking_fast.html", "leatherworking.html", "leatherworking_craft_all.html",
                     "tailor_fast.html", "tailor.html", "tailor_craft_all.html",
                     "artificing_fast.html", "artificing.html", "artificing_craft_all.html",
                     "jewelcraft_fast.html", "jewelcraft.html", "jewelcraft_craft_all.html",
                     "weaponcraft_fast.html", "weaponcraft.html", "weaponcraft_craft_all.html",
                     "huntsman_fast.html", "huntsman.html", "huntsman_craft_all.html",
                     "armorcraft_fast.html", "armorcraft.html", "armorcraft_craft_all.html",
                     "total.html"]:
            with codecs.open(lang+item,'rb') as f:
                myFtp.storbinary(u'STOR /gw2crafts.net/'+lang+item,f)
            os.remove(lang+item)
    myFtp.close()


# If ran directly, call main
if __name__ == '__main__':
    main()
