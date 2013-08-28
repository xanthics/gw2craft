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
        sellMethod = 0
        if val[u'max_offer_unit_price']*.85 > w:
            w = int(val[u'max_offer_unit_price']*.85)
            sellMethod = 1
        if w == 0:
            w = int(val[u'min_sale_unit_price']*.85)
            sellMethod = 2

        # Save all the information we care about
        outdict[item] = {u'w':w,u'cost':val[u'min_sale_unit_price'],u'recipe':None,u'rarity':items.ilist[item][u'rarity'],u'type':items.ilist[item][u'type'],u'icon':items.ilist[item][u'img_url'],u'output_item_count':items.ilist[item][u'output_item_count'],u'sellMethod':sellMethod} 

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
    for _i in range(1,level):
        tmp = math.floor(tmp * 1.01)
    return tmp

# compute the xp gain of a single craft
def xpgain(level,typ,minlvl):
    span = 0.0
    mult = 0.0
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
                if not cList[item][u'recipe']:
                    cList[item][u'recipe'] = []
                cList[item][u'recipe'].append(c_recipes[tier][item])
            else: 
                print u"Missing Item from itemlist: " + item
                exit(-1)
            if not u'tier' in cList[item]:
                cList[item][u'tier'] = []
            cList[item][u'tier'].append(tier)

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
        craftcount[tier] = {u'refine':0.0,u'part':[],u'ptitem':[],u'item':[],u'discovery':[],u'current_xp':xp_to_level[tier]}

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
                if 0:#not tier == 0 and craftcount[tier][u'current_xp'] <= xp_to_level[tier+10]:
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
                index = 0
                if tier in cList[item][u'tier']:
                    index = cList[item][u'tier'].index(tier)
                else:
                    while len(cList[item][u'tier']) > index+1 and int(cList[item][u'tier'][index]) > tier:
                        index += 1
                if item == bucket[bkey[0]][u'item_id'] and int(cList[item][u'tier'][index]) < tier:
                    craftcount[tier][u'ptitem'].append(rarityNum(cList[item][u'rarity']))
                    pmake[tier][item] += 1
                elif not cList[item][u'type'] in non_item and not 'discover' in cList[item]:
                    cList[item][u'discover'] = 1
                    craftcount[int(cList[item][u'tier'][index])][u'discovery'].append(rarityNum(cList[item][u'rarity']))
                    make[int(cList[item][u'tier'][index])][item] += 1
                elif not cList[item][u'type'] in non_item:
                    craftcount[int(cList[item][u'tier'][index])][u'item'].append(rarityNum(cList[item][u'rarity']))
                    make[int(cList[item][u'tier'][index])][item] += 1
                elif cList[item][u'type'] == u'Refinement':
                    if item == 19679: # Bronze Ingot
                        craftcount[int(cList[item][u'tier'][index])][u'refine'] += 0.2
                    else:
                        craftcount[int(cList[item][u'tier'][index])][u'refine'] += 1.0
                    make[int(cList[item][u'tier'][index])][item] += 1
                else:
                    if item in [13063,  13189,  13207,  13219,  13045,  13022,  13075,  13177,  13096,  13033] and not sole: # Sole IDs
                        sole +=1
                    else:
                        craftcount[int(cList[item][u'tier'][index])][u'part'].append(rarityNum(cList[item][u'rarity']))
                    make[int(cList[item][u'tier'][index])][item] += 1
                recalc[int(cList[item][u'tier'][index])] = 0

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

    printtofile(tcost, treco, sell, deepcopy(make), deepcopy(pmake), deepcopy(buy), deepcopy(tierbuy), deepcopy(cList), filename, mytime, Items_de.ilist, localde)
    printtofile(tcost, treco, sell, deepcopy(make), deepcopy(pmake), deepcopy(buy), deepcopy(tierbuy), deepcopy(cList), filename, mytime, Items_fr.ilist, localfr)
    printtofile(tcost, treco, sell, deepcopy(make), deepcopy(pmake), deepcopy(buy), deepcopy(tierbuy), deepcopy(cList), filename, mytime, Items_es.ilist, locales)
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
    # Find the recipe we are looking for
    index = 0
    for i in range(len(items[recipe][u'tier'])):
        if items[recipe][u'tier'][i] == int(itier):
            index = i
            break
    # For our traditional style guides, we still want to consider buying gems even though you can refine.    This is a list of those gems
    # "Amber Pebble","Garnet Pebble","Malachite Pebble","Pearl","Tiger's Eye Pebble","Turquoise Pebble","Amethyst Nugget","Carnelian Nugget","Lapis Nugget","Peridot Nugget","Spinel Nugget","Sunstone Nugget","Topaz Nugget","Amethyst Lump","Carnelian Lump","Lapis Lump","Peridot Lump","Spinel Lump","Sunstone Lump","Topaz Lump","Beryl Shard","Chrysocola Shard","Coral Chunk","Emerald Shard","Opal Shard","Ruby Shard","Sapphire Shard","Beryl Crystal","Chrysocola Crystal","Coral Tentacle","Emerald Crystal","Opal Crystal","Ruby Crystal","Sapphire Crystal","Passion Flower"
    gemss = [24534,  24464,  24466,  24500,  24467,  24465,  24501,  24469,  24470,  24468,  24889,  24471,  24535,  24527,  24472,  24507,  24504,  24526,  24503,  24506,  24872,  24870,  24874,  24871,  24875,  24873,  24876,  24519,  24511,  24509,  24473,  24521,  24474,  24475,  37907]
    # impossible to make item at this point.
    if int(items[recipe][u'tier'][index]) > int(itier):
#        print recipe
        return 9999999999, -99999999999, make, buy
    for _i in range(0,count):
        make.append(recipe)
    if int(items[recipe][u'tier'][index]) < int(tier) and not items[recipe][u'type'] in non_item:
        xptotal = xp_calc(0,0,count,0,rarityNum(items[recipe][u'rarity']),int(items[recipe][u'tier'][index]),level)
    elif not items[recipe][u'type'] in non_item and not 'discover' in items[recipe]:
        xptotal = xp_calc(0,0,count-1,1,rarityNum(items[recipe][u'rarity']),int(items[recipe][u'tier'][index]),level)
    elif not items[recipe][u'type'] in non_item:
        xptotal = xp_calc(0,0,count,0,rarityNum(items[recipe][u'rarity']),int(items[recipe][u'tier'][index]),level)
    elif items[recipe][u'type'] == u'Refinement':
        if 19679 == recipe:
            xptotal = math.ceil(xp_calc(count,0,0,0,1.0,int(items[recipe][u'tier'][index]),level)*0.2)
        else:
            xptotal = xp_calc(count,0,0,0,1.0,int(items[recipe][u'tier'][index]),level)
    else:
        if recipe in [13063,  13189,  13207,  13219,  13045,  13022,  13075,  13177,  13096,  13033]: # Sole
            xptotal = xp_calc(0,count,0,0,1.0,int(items[recipe][u'tier'][index]),level)*0.5
        else:
            xptotal = xp_calc(0,count,0,0,1.0,int(items[recipe][u'tier'][index]),level)

    mycost = 0
    for item in items[recipe][u'recipe'][index]:
        mycost += items[item][u'cost']*items[recipe][u'recipe'][index][item]

    mycost *= count
    for item in items[recipe][u'recipe'][index]:
        if not items[item][u'recipe'] == None:
            tcost, txptotal, tmake, tbuy = calcRecipecraft(item,items,craftcount,items[item][u'tier'][0],items[recipe][u'recipe'][index][item]*count,int(items[recipe][u'tier'][index]),ignoreMixed,xp_to_level)
            if (ignoreMixed and item not in gemss) or tcost < items[item][u'cost']*items[recipe][u'recipe'][index][item]*count or float(xptotal+txptotal)/float(mycost-items[item][u'cost']*items[recipe][u'recipe'][index][item]*count+tcost) >= float(xptotal)/float(mycost):
                xptotal += txptotal
                cost += tcost
                buy += tbuy
                make += tmake
            else:
                for _i in range(0,int(math.ceil(count*items[recipe][u'recipe'][index][item]))):
                    buy.append(item)
                cost += items[item][u'cost']*count*items[recipe][u'recipe'][index][item]
        else:
            for _i in range(0,int(math.ceil(count*items[recipe][u'recipe'][index][item]))):
                buy.append(item)
            cost += items[item][u'cost']*count*items[recipe][u'recipe'][index][item]
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
            outdict[weight] = {u'item_id':recipe,u'w':xptotal,u'make':make,u'buy':buy,u'cost':cost}

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

def printtofile(tcost, treco, sell, make, pmake, buy, tierbuy, cList, filename, mytime, cListName, localText):
    buttonList = []
    totals = {}
    if tierbuy:
        totals[filename.split('.')[0]] = {0:defaultdict(int),75:defaultdict(int),150:defaultdict(int),225:defaultdict(int),300:defaultdict(int),u'total':int(tcost)}
    else:
        totals[filename.split('.')[0]] = int(tcost)

    non_item = [u'Refinement', u'Insignia', u'Inscription', u'Component']

    karma_items  = {12337:{u'note':u"%s <br /> %s"%(localText.pickins,localText.disa),u'cost':77}, # Almond
                    12165:{u'note':u"%s <br /> %s"%(localText.eda,localText.jack),u'cost':35}, # Apple
                    12340:{u'note':u"%s"%(localText.makayla),u'cost':77}, # Avocado
                    12251:{u'note':u"%s <br /> %s <br /> %s <br /> %s"%(localText.jenks,localText.sangdo,localText.goran,localText.vejj),u'cost':49}, # Banana
                    12237:{u'note':u"%s <br /> %s"%(localText.jenks,localText.leius),u'cost':49}, # Black Bean
                    12240:{u'note':u"%s <br /> %s"%(localText.bjarni,localText.milton),u'cost':35}, # Celery Stalk
                    12338:{u'note':u"%s <br /> %s"%(localText.summers,localText.disa),u'cost':77}, # Cherry
                    12515:{u'note':u"%s"%(localText.naknar),u'cost':112}, # Chickpea
                    12350:{u'note':u"%s"%(localText.tunnira),u'cost':112}, # Coconut
                    12256:{u'note':u"%s <br /> %s"%(localText.sagum,localText.milton),u'cost':35}, # Cumin
                    12502:{u'note':u"%s"%(localText.jenrys),u'cost':154}, # Eggplant
                    12232:{u'note':u"%s"%(localText.albin),u'cost':35}, # Green Bean
                    12518:{u'note':u"%s <br /> %s"%(localText.laudren,localText.wupwup),u'cost':112}, # Horseradish Root
                    12239:{u'note':u"%s <br /> %s <br /> %s"%(localText.brian,localText.kastaz,localText.hune),u'cost':49}, # Kidney Bean
                    12252:{u'note':u"%s <br /> %s <br /> %s"%(localText.eona,localText.hrappa,localText.milton),u'cost':35}, # Lemon
                    12339:{u'note':u"%s"%(localText.shelp),u'cost':77}, # Lime
                    12543:{u'note':u"%s"%(localText.crandle),u'cost':203}, # Mango
                    12249:{u'note':u"%s <br /> %s <br /> %s"%(localText.eda,localText.jenks,localText.milton),u'cost':35}, # Nutmeg Seed
                    12503:{u'note':u"%s"%(localText.nrocroc),u'cost':154}, # Peach
                    12514:{u'note':u"%s"%(localText.braxa),u'cost':112}, # Pear
                    12516:{u'note':u"%s"%(localText.tholin),u'cost':112}, # Pinenut
                    12517:{u'note':u"%s"%(localText.ichtaca),u'cost':112}} # Shallot

    karma_chef   = {12159:{u'note':localText.mcov,u'cost':35}, # Cheese Wedge
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
                    12233:{u'note':localText.tholin,u'cost':35}, # Handful of Trail Mix
                    12739:{u'note':localText.triktiki,u'cost':35}, # Triktiki Omelet
                    12352:{u'note':"%s (%s %s)"%(localText.pochtecatl,mFormat(368),localText.valuePer),u'cost':0}, # Griffon Egg Omelet
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
                    24925:{u'note':localText.mcov,u'cost':231}} # Embellished Brilliant Sapphire Jewel

    recipebuy = []
    for tier in [0,25,50,75,100,125,150,175,200,225,250,275,300,325,350,375]:
        for item in make[tier]:
            if item in karma_recipe:
                recipebuy.append(item)

    # 'Spool of Jute Thread',u'Spool of Wool Thread',u'Spool of Cotton Thread',u'Spool of Linen Thread',u'Spool of Silk Thread',u'Lump of Tin',u'Lump of Coal',u'Lump of Primordium',u'Jar of Vinegar',u'Packet of Baking Powder',u'Jar of Vegetable Oil',u'Packet of Salt',u'Bag of Sugar',u'Jug of Water',u'Bag of Starch',u'Bag of Flour',u'Bottle of Soy Sauce',"Bottle of Rice Wine", "Minor Rune of Holding", "Rune of Holding", "Major Rune of Holding", "Greater Rune of Holding"
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
            if item in karma_chef:
                b_karma_c[item] = buy[item]
            elif item in karma_items:
                if localText.path == "":
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

    karma_str = u"<div class=\"s%d\"><input type=\"checkbox\" /><span class=\"itemIcon\" style=\"background-image: url(%s);\"></span><span class=\"quantity\">%d</span> <button title=\""+localText.toggle+u"\" class=\"%s arrow\" id=\"%d\">%s</button><div class=\"lsbutton\" id=\"1%d\">%d <span class=\"karmaIcon\"></span> "+localText.valuePer+u" 25 <br /> %s</div></div>\n"
    collectable_str = u"<div class=\"s%d\"><input type=\"checkbox\" /><span class=\"itemIcon\" style=\"background-image: url(%s);\"></span><span class=\"quantity\">%d</span> <span class=\"%s\">%s</span> (%4s "+localText.valuePer+u")</div>\n"


    t = 0 # used to control div background color
    kt = 0 # karma total
    with codecs.open(localText.path+filename, 'wb', encoding='utf-8') as f:
        f.write(u'<!DOCTYPE html>\n')
        f.write(u'<html>\n')
        f.write(u'<head>\n')
        # Title Part 1
        if u"fast" in filename:
            f.write(u'    <title>'+localText.fGuides)
        elif u"all" in filename:
            f.write(u'    <title>'+localText.tGuides)
        else: # normal
            f.write(u'    <title>'+localText.nGuides)
        # Title Part 2
        if filename in [u"cooking_fast.html",u"cooking.html"]:
            f.write(u': '+localText.cooking+u' - '+localText.nHearts+u'</title>\n')
        elif filename in [u"cooking_karma_fast.html",u"cooking_karma.html"]:
            f.write(u': '+localText.cooking+u' - '+localText.aHearts+u'</title>\n')
        elif filename in [u"cooking_karma_fast_light.html",u"cooking_karma_light.html"]:
            f.write(u': '+localText.cooking+u' - '+localText.tHearts+u'</title>\n')
        elif filename in [u"leatherworking_fast.html", u"leatherworking.html", u"leatherworking_craft_all.html"]:
            f.write(u': '+localText.lw+u'</title>\n')
        elif filename in [u"tailor_fast.html", u"tailor.html", u"tailor_craft_all.html"]:
            f.write(u': '+localText.tailor+u'</title>\n')
        elif filename in [u"artificing_fast.html", u"artificing.html", u"artificing_craft_all.html"]:
            f.write(u': '+localText.art+u'</title>\n>')
        elif filename in [u"jewelcraft_fast.html", u"jewelcraft.html", u"jewelcraft_craft_all.html"]:
            f.write(u': '+localText.jc+u'</title>\n')
        elif filename in [u"weaponcraft_fast.html", u"weaponcraft.html", u"weaponcraft_craft_all.html"]:
            f.write(u': '+localText.wc+u'</title>\n')
        elif filename in [u"huntsman_fast.html", u"huntsman.html", u"huntsman_craft_all.html"]:
            f.write(u': '+localText.hunt+u'</title>\n>')
        elif filename in [u"armorcraft_fast.html", u"armorcraft.html", u"armorcraft_craft_all.html"]:
            f.write(u': '+localText.ac+u'</title>\n')
        f.write(u'    <meta name="description" content="Guild Wars 2 always current crafting guide for '+filename.split('.')[0].replace("_"," ").title()+u'">\n')
        f.write(u'    <meta http-equiv="content-type" content="text/html;charset=UTF-8">\n')
        f.write(u'    <link href="/css/layout.css" rel="stylesheet" type="text/css" />') 
        f.write(u'    <link rel="icon" type="image/png" href="/fi.gif">')
        f.write(u'    <script src="//ajax.googleapis.com/ajax/libs/jquery/1.9.0/jquery.min.js"></script>\n')
        f.write(u'    <script>(window.jQuery || document.write(\'<script src="http://ajax.aspnetcdn.com/ajax/jquery/jquery-1.9.0.min.js"><\/script>\'));</script>\n')
        f.write(u'    <script src="/js/menu.js" type="text/javascript"></script>\n')
        f.write(u'</head>\n')
        f.write(u'<body>\n%s\n'%(localText.header%(filename,filename,filename)))
        f.write(u'<section class=\"main\">')
        f.write(u'<div style="width: 100%; border: 2px #fffaaa solid; border-left: 0px; border-right: 0px; background: #fffddd; height: 24px;">\n')
        f.write(u'<img src="/css/warning-icon.png" width="24" height="24" style="padding: 0 8px 0 8px; float: left;" alt="WARNING"><span style="position: relative; top: 4px;"><span style="color: red">%s</span>    %s: %s</span>\n'%(localText.warning1,localText.warning2,mytime))
        f.write(u'</div><br />\n')
        # adword
        f.write(u'<div style="float:right;position:absolute;right:-320px;"> \
                \n<script type="text/javascript"><!-- \
                \ngoogle_ad_client = "ca-pub-6865907345688710"; \
                \n/* large sidebar */ \
                \ngoogle_ad_slot = "9285292589"; \
                \ngoogle_ad_width = 300; \
                \ngoogle_ad_height = 600; \
                \n//--> \
                \n</script> \
                \n<script type="text/javascript" \
                \nsrc="http://pagead2.googlesyndication.com/pagead/show_ads.js"> \
                \n</script> \
                \n</div>\n')
        f.write(localText.moreInfo%(u"<img src=\"/img/arrow.png\" alt=ARROW>"))
        # Page Title Part 1
        if u"fast" in filename:
            f.write(u'<h1>'+localText.fGuides)
        elif u"all" in filename:
            f.write(u'<h1>'+localText.tGuides)
        else: # normal
            f.write(u'<h1>'+localText.nGuides)
        # Page Title Part 2
        if filename in [u"cooking_fast.html",u"cooking.html"]:
            f.write(u': '+localText.cooking+u' - '+localText.nHearts+u'</h1>')
        elif filename in [u"cooking_karma_fast.html",u"cooking_karma.html"]:
            f.write(u': '+localText.cooking+u' - '+localText.aHearts+u'</h1>')
        elif filename in [u"cooking_karma_fast_light.html",u"cooking_karma_light.html"]:
            f.write(u': '+localText.cooking+u' - '+localText.tHearts+u'</h1>')
        elif filename in [u"leatherworking_fast.html", u"leatherworking.html", u"leatherworking_craft_all.html"]:
            f.write(u': '+localText.lw+u'</h1>')
        elif filename in [u"tailor_fast.html", u"tailor.html", u"tailor_craft_all.html"]:
            f.write(u': '+localText.tailor+u'</h1>')
        elif filename in [u"artificing_fast.html", u"artificing.html", u"artificing_craft_all.html"]:
            f.write(u': '+localText.art+u'</h1>')
        elif filename in [u"jewelcraft_fast.html", u"jewelcraft.html", u"jewelcraft_craft_all.html"]:
            f.write(u': '+localText.jc+u'</h1>')
        elif filename in [u"weaponcraft_fast.html", u"weaponcraft.html", u"weaponcraft_craft_all.html"]:
            f.write(u': '+localText.wc+u'</h1>')
        elif filename in [u"huntsman_fast.html", u"huntsman.html", u"huntsman_craft_all.html"]:
            f.write(u': '+localText.hunt+u'</h1>')
        elif filename in [u"armorcraft_fast.html", u"armorcraft.html", u"armorcraft_craft_all.html"]:
            f.write(u': '+localText.ac+u'</h1>')
        f.write(u'<dl>\n')
        f.write(u'    <dt>%s</dt>\n'%localText.iCost)
        f.write(u'    <dd>'+mFormat(tcost)+u'</dd>\n')
        f.write(u'    <dt>%s</dt>\n'%localText.eRecovery)
        f.write(u'    <dd><span style="position: relative; left: -9px;">- '+mFormat(treco)+u'</span></dd>\n')
        f.write(u'    <dt>%s</dt>\n'%localText.fCost)
        f.write(u'    <dd style="border-top: 1px #666 solid;">'+mFormat(tcost-treco)+u'</dd>\n')
        f.write(u'</dl>')
        f.write(u'<div class="clear"></div>')
        f.write(u'<br /><button title=\"%s\" class=\"arrow\" id=\"tcost\">%s:</button><div class=\"lsbutton\" id=\"1tcost\">'%(localText.toggle,localText.sList))
        for line in sorted(sell):
            if cList[line][u'w'] > 0:
                t = (t+1)%2
                f.write(u'<div class=\"s%i\">%3i <span class=\"%s\">%s</span> - %s %s</div>\n'%(t,sell[line],cList[line][u'rarity'],cListName[line],(localText.soldVia%mFormat(cList[line][u'w'])),localText.method[cList[line][u'sellMethod']]))

        f.write(u"</div><script type=\"text/javascript\">$('#1tcost').hide();</script><br />")
        buttonList.append('tcost')

        if b_vendor or b_karma_c or b_karma_w:
            f.write(u"<h2>%s</h2>\n"%localText.buyVendor)
            if b_karma_c or b_karma_w:
                f.write(u"<span class=\"karmaIcon\"></span> %s<br /><br />\n"%(localText.kNote))

            for item in sorted(b_karma_w):
                t = (t+1)%2
                f.write(karma_str%(t,cList[item][u'icon'],buy[item],cList[item][u'rarity'],item,cListName[item],item,karma_items[item][u'cost'],karma_items[item][u'note']))
                buttonList.append(item)
                kt += int(math.ceil(buy[item]/25.0)*karma_items[item][u'cost'])

            for item in sorted(b_karma_c):
                t = (t+1)%2
                f.write(karma_str%(t,cList[item][u'icon'],buy[item],cList[item][u'rarity'],item,cListName[item],item,karma_chef[item][u'cost'],karma_chef[item][u'note']))
                buttonList.append(item)
                kt += int(math.ceil(buy[item]/25.0)*karma_chef[item][u'cost'])

            for item in sorted(b_vendor):
                t = (t+1)%2
                f.write((u"<div class=\"s%i\"><input type=\"checkbox\" /><span class=\"itemIcon\" style=\"background-image: url(%s);\"></span><span class=\"quantity\">%i</span> <span class=\"%s\">%s</span> (%4s %s from %s)</div>\n")%(t,cList[item][u'icon'],buy[item],cList[item][u'rarity'],cListName[item],mFormat(cList[item][u'cost']),localText.valuePer,localText.method[0]))

        if recipebuy:
            f.write(u"<h2>%s</h2>\n"%localText.bRecipes)
            for item in recipebuy:
                t = (t+1)%2
                f.write((u"<div class=\"s%d\"><input type=\"checkbox\" /><span class=\"itemIcon\" style=\"background-image: url(%s);\"></span><button title=\""+localText.toggle+u"\" class=\"arrow %s\" id=\"%d\">%s</button><div class=\"lsbutton\" id=\"1%d\">%i <span class=\"karmaIcon\"></span>, %s</div></div>\n")%(t,cList[item]['icon'],cList[item]['rarity'],item,cListName[item],item,karma_recipe[item]['cost'],karma_recipe[item]['note']))
                buttonList.append(item)
                kt += int(karma_recipe[item][u'cost'])
        if kt:
            f.write(u'<br />\nTotal <span class=\"karmaIcon\"></span>: '+str(kt)+u'<br />\n')
        if b_common or b_fine or b_rare or b_gem or b_holiday or b_food:
            f.write(u'<h2>%s</h2>\n'%localText.collectibles)
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
            f.write(u'<h2>%s</h2>\n'%localText.mixedTP)
            for item in sorted(b_mix):
                t = (t+1)%2
                f.write(collectable_str%(t,cList[item][u'icon'],buy[item],cList[item][u'rarity'],cListName[item],mFormat(cList[item][u'cost'])))

        f.write(u"<br />\n<br />\n<h2>%s</h2>\n"%localText.make)
        f.write(u"<button title=\""+localText.toggle+u"\" class =\"info\" id=\"show_all\">%s</button><br />"%localText.expand)
        f.write(u"<button title=\""+localText.toggle+u"\" class =\"info\" id=\"hide_all\">%s</button>"%localText.collapse)
        rt = 0
        for tier in [0,25,50,75,100,125,150,175,200,225,250,275,300,325,350,375]:
            if tierbuy and tier in [0,75,150,225,300]:
                tt = 0
                tc = tier+75
                if tier == 300:
                    tc += 25
                f.write((u"<br /><br /><h4>%s:<button title=\""+localText.toggle+u"\" class =\"info\" id=\""+str(tier)+u"tier\">%s</button></h4>\n<div class=\"lsbutton\" id=\"1"+str(tier)+u"tier\">")%((localText.tier%(tier/75+1,tier,tc)),localText.buyList%(tier/75+1)))
                f.write(u"<h5>%s</h5>"%localText.blNotice)
                for item in sorted(tierbuy[tier]):
                    t = (t+1)%2
                    f.write((u"<div class=\"s"+str(t)+u"\"><input type=\"checkbox\" /><span class=\"itemIcon\" style=\"background-image: url("+cList[item][u'icon']+u");\"></span><span class=\"quantity\">%i</span> <span class=\"%s\">%s</span> (%4s "+localText.valuePer+u")</div>\n")%(tierbuy[tier][item],cList[item][u'rarity'],cListName[item],mFormat(cList[item][u'cost'])))
                    tt += tierbuy[tier][item]*cList[item][u'cost']
                buttonList.append(str(tier)+u'tier')
                rt += tt
                totals[filename.split('.')[0]][tier] = tt
                f.write(u"</div><h4>%s</h4>\n"%(localText.costRT%(mFormat(tt),mFormat(rt))))        
            f.write((u"<br />\n<h3>%s:%3i</h3>\n")%(localText.level,tier))
            if pmake[tier]:
                for item in sorted(pmake[tier]):
                    t = (t+1)%2
                    f.write(u"<div class=\"s"+str(t)+u"\">"+localText.make+u":%3i <span class=\"%s\">%s</span> (From %i tier) </div>\n"%(pmake[tier][item],cList[item][u'rarity'],cListName[item],tier-25))
            for item in sorted(make[tier], key=make[tier].get,reverse=True):
                if cList[item][u'type'] == u'Refinement':
                    t = (t+1)%2
                    if item == 19679: # Bronze Ingot
                        f.write((u"<div class=\"s"+str(t)+u"\">"+localText.make+u":%3i <span class=\"%s\">%s</span> (%s)</div>\n")%(make[tier][item],cList[item][u'rarity'],cListName[item],localText.bNote))
                    else:
                        f.write(u"<div class=\"s"+str(t)+u"\">"+localText.make+u":%3i <span class=\"%s\">%s</span></div>\n"%(make[tier][item],cList[item][u'rarity'],cListName[item]))
            for item in sorted(make[tier], key=make[tier].get,reverse=True):
                if cList[item][u'type'] in non_item and not cList[item][u'type'] == u'Refinement':
                    t = (t+1)%2
                    if item in [13063,  13189,  13207,  13219,  13045,  13022,  13075,  13177,  13096,  13033]: # Sole
                        f.write((u"<div class=\"s"+str(t)+u"\">"+localText.make+u":%3i <span class=\"%s\">%s</span> (%s)</div>\n")%(make[tier][item]/2,cList[item][u'rarity'],cListName[item],localText.sNote))
                    else:
                        f.write(u"<div class=\"s"+str(t)+u"\">"+localText.make+u":%3i <span class=\"%s\">%s</span></div>\n"%(make[tier][item],cList[item][u'rarity'],cListName[item]))
            for item in sorted(make[tier]):

                if 'discover' in cList[item] and cList[item][u'discover'] == 1:
                    if make[tier][item] > 1:
                        make[tier][item] -= 1
                    else:
                        del(make[tier][item])
                    t = (t+1)%2
                    tstr = "<div class=\"sbutton\" id=\"1"+str(item)+str(tier)+u"\">"
                    for s in cList[item][u'recipe'][cList[item][u'tier'].index(tier)]:
                        tstr += "\n<br />\t<span class=\"itemIcon\" style=\"background-image: url("+cList[s][u'icon']+u");\"></span> <span class=\""+cList[s][u'rarity']+u'\">'+cListName[s]+u"</span> ("+str(cList[item][u'recipe'][cList[item][u'tier'].index(tier)][s])+u")"
                    tstr += "</div><br />"
                    f.write(u"<div class=\"s"+str(t)+u"\">"+localText.discover+u": <button class=\"arrow "+cList[item][u'rarity']+u'\" title=\"'+localText.toggle+u'\" id=\"'+str(item)+str(tier)+u'\">'+cListName[item]+u"</button> "+tstr+u"\n</div>\n")
                    buttonList.append(str(item)+str(tier))
            for item in sorted(make[tier]):
                if not cList[item][u'type'] in non_item:
                    t = (t+1)%2
                    f.write(u"<div class=\"s"+str(t)+u"\">"+localText.make+u":%3i <span class=\"%s\">%s</span></div>\n"%(make[tier][item],cList[item][u'rarity'],cListName[item]))
        f.write(u'<br />\n<h3>%s:400</h3>\n'%localText.level)
        t = (t+1)%2
        f.write(u"<div class=\"s"+str(t)+u"\">%s</div>\n"%localText.finish)
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
        f.write(u'</section>\n')
        f.write('%s\n<script type="text/javascript">\n'%localText.cright)
        for item in buttonList:
            f.write(u"$(\"#"+str(item)+u"\").click(function () {\n\t$(\"#1"+str(item)+u"\").toggle();});\n")
        f.write(u"$(\".sbutton\").hide();\n")
        f.write(u"$(\".lsbutton\").hide();\n")
        f.write(u"$(\"#show_all\").click(function () {$(\".sbutton\").show();")
        f.write(u"});\n$(\"#hide_all\").click(function () {$(\".sbutton\").hide();")
        f.write(u'});\n</script>\n')
        f.write(u'</body>\n')
        f.write(u'</html>\n')
    return totals

def maketotals(totals, mytime, localText):
    tpage1 = u""
    tpage2 = u""
    tpage3 = u""

    page = u'''
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
    page += localText.header%('total.html',u'total.html',u'total.html')

    page += u"<section class=\"main\">\n<h5 style=\"text-align:center;\">"+localText.updated+u": " + mytime + u"</h5>"
    page += localText.note
    page += u'    <table>'
    page += u'<tr><th>'+localText.craft+u'</th><th>'+localText.nGuides+u'</th><th>'+localText.fGuides+u'</th></tr>\n'
    page += u'<tr><td>'+localText.nHearts+u'</td><td>'+mFormat(totals[u'cooking'])+u'</td><td>'+mFormat(totals[u'cooking_fast'])+u'</td></tr>\n'
    page += u'<tr><td>'+localText.tHearts+u'</td><td>'+mFormat(totals[u'cooking_karma_light'])+u'</td><td>'+mFormat(totals[u'cooking_karma_fast_light'])+u'</td></tr>\n'
    page += u'<tr><td>'+localText.aHearts+u'</td><td>'+mFormat(totals[u'cooking_karma'])+u'</td><td>'+mFormat(totals[u'cooking_karma_fast'])+u'</td></tr>\n'
     
    page += u"</table>\n<br />\n<table>\n<tr><th>"+localText.craft+u"</th><th>"+localText.nGuides+u"</th><th>"+localText.fGuides+u"</th><th>"+localText.tGuides+u"</th></tr>\n"


    tpage1 += u"</table>\n<br />\n<table>\n<tr><th>"+localText.nGuides+u"</th><th>"+localText.tiers+u" 1</th><th>"+localText.tiers+u" 2</th><th>"+localText.tiers+u" 3</th><th>"+localText.tiers+u" 4</th><th>"+localText.tiers+u" 5</th></tr>\n"
    tpage2 += u"</table>\n<br />\n<table>\n<tr><th>"+localText.fGuides+u"</th><th>"+localText.tiers+u" 1</th><th>"+localText.tiers+u" 2</th><th>"+localText.tiers+u" 3</th><th>"+localText.tiers+u" 4</th><th>"+localText.tiers+u" 5</th></tr>\n"
    tpage3 += u"</table>\n<br />\n<table>\n<tr><th>"+localText.tGuides+u"</th><th>"+localText.tiers+u" 1</th><th>"+localText.tiers+u" 2</th><th>"+localText.tiers+u" 3</th><th>"+localText.tiers+u" 4</th><th>"+localText.tiers+u" 5</th></tr>\n"

    ctnc = 0
    ctfc = 0
    cttc = 0
    for i in [(u'jewelcraft',u'jewelcraft_fast',u'jewelcraft_craft_all',localText.jc),
              (u'artificing',u'artificing_fast',u'artificing_craft_all',localText.art),
              (u'huntsman',u'huntsman_fast',u'huntsman_craft_all',localText.hunt),
              (u'weaponcraft',u'weaponcraft_fast',u'weaponcraft_craft_all',localText.wc),
              (u'armorcraft',u'armorcraft_fast',u'armorcraft_craft_all',localText.ac),
              (u'leatherworking',u'leatherworking_fast',u'leatherworking_craft_all',localText.lw),
              (u'tailor',u'tailor_fast',u'tailor_craft_all',localText.tailor)]:
        page += u'<tr><td>'+i[3]+u'</td><td>'+mFormat(totals[i[0]][u'total'])+u'</td><td>'+mFormat(totals[i[1]][u'total'])+u'</td><td>'+mFormat(totals[i[2]][u'total'])+u'</td></tr>\n'
        tpage1 += u'<tr><td>'+i[3]+u'</td><td>'+mFormat(totals[i[0]][0])+u'</td><td>'+mFormat(totals[i[0]][75])+u'</td><td>'+mFormat(totals[i[0]][150])+u'</td><td>'+mFormat(totals[i[0]][225])+u'</td><td>'+mFormat(totals[i[0]][300])+u'</td></tr>\n'
        tpage2 += u'<tr><td>'+i[3]+u'</td><td>'+mFormat(totals[i[1]][0])+u'</td><td>'+mFormat(totals[i[1]][75])+u'</td><td>'+mFormat(totals[i[1]][150])+u'</td><td>'+mFormat(totals[i[1]][225])+u'</td><td>'+mFormat(totals[i[1]][300])+u'</td></tr>\n'
        tpage3 += u'<tr><td>'+i[3]+u'</td><td>'+mFormat(totals[i[2]][0])+u'</td><td>'+mFormat(totals[i[2]][75])+u'</td><td>'+mFormat(totals[i[2]][150])+u'</td><td>'+mFormat(totals[i[2]][225])+u'</td><td>'+mFormat(totals[i[2]][300])+u'</td></tr>\n'

        ctnc += totals[i[0]][u'total']
        ctfc += totals[i[1]][u'total']
        cttc += totals[i[2]][u'total']

    page += u'<tr><td><strong>'+localText.totals+u'</strong></td><td><strong>'+ mFormat(ctnc)+u'</strong></td><td><strong>'+ mFormat(ctfc)+u'</strong></td><td><strong>'+ mFormat(cttc)+u'</strong></td></tr></table>\n<br />\n'

    tpage1 += u' </table>\n<br />'
    tpage2 += u' </table>\n<br />'
    tpage3 += u' </table>'

    page += tpage1 + tpage2 + tpage3

    page += u'\n</section>\n' + localText.cright + u'\n</body>\n</html>'

    with codecs.open(localText.path+u'total.html', 'wb', encoding='utf-8') as f:
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
    mytime = "<span class=\"localtime\">" + datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S')+u'+00:00</span>'
    print datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
    # Will hold level:total xp pairs (array)
    xp_to_level = [0]
    # populate the xp chart
    for i in range(1,410):
        xp_to_level.append(xpreq(i)+xp_to_level[i-1])

    cList = appendCosts()

    out_q = Queue()
    rList = []
    #TODO change the way flags are passed so it is easier to understand

    cooking_karma = join(Chef.recipes, Chef_karma.recipes)
    rList.append([(u"cooking_karma_fast.html",cooking_karma,True,False),
                  (u"cooking_karma_fast_light.html",cooking_karma,True,False),
                  (u"cooking_fast.html",Chef.recipes,True,False)])
    rList.append([(u"cooking_karma.html",cooking_karma,False,False),
                  (u"cooking_karma_light.html",cooking_karma,False,False),
                  (u"cooking.html",Chef.recipes,False,False)])
    rList.append([(u"jewelcraft_fast.html",Jeweler.recipes,True,False),
                  (u"jewelcraft.html",Jeweler.recipes,False,False),
                  (u"jewelcraft_craft_all.html",Jeweler.recipes,False,True)])
    rList.append([(u"artificing_fast.html",Artificer.recipes,True,False),
                  (u"artificing.html",Artificer.recipes,False,False),
                  (u"artificing_craft_all.html",Artificer.recipes,False,True)])
    rList.append([(u"weaponcraft_fast.html",Weaponsmith.recipes,True,False),
                  (u"weaponcraft.html",Weaponsmith.recipes,False,False),
                  (u"weaponcraft_craft_all.html",Weaponsmith.recipes,False,True)])
    rList.append([(u"huntsman_fast.html",Huntsman.recipes,True,False),
                  (u"huntsman.html",Huntsman.recipes,False,False),
                  (u"huntsman_craft_all.html",Huntsman.recipes,False,True)])
    rList.append([(u"armorcraft_fast.html",Armorsmith.recipes,True,False),
                  (u"armorcraft.html",Armorsmith.recipes,False,False),
                  (u"armorcraft_craft_all.html",Armorsmith.recipes,False,True)])
    rList.append([(u"tailor_fast.html",Tailor.recipes,True,False),
                  (u"tailor.html",Tailor.recipes,False,False),
                  (u"tailor_craft_all.html",Tailor.recipes,False,True)])
    rList.append([(u"leatherworking_fast.html",Leatherworker.recipes,True,False),
                  (u"leatherworking.html",Leatherworker.recipes,False,False),
                  (u"leatherworking_craft_all.html",Leatherworker.recipes,False,True)])

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
    maketotals(totals,mytime,localde)
    maketotals(totals,mytime,localfr)
    maketotals(totals,mytime,locales)

    print datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
    print "Starting upload"
    myFtp = FTP(ftp_url)
    myFtp.login(ftp_user,ftp_pass)
    for lang in ['',u'de/',u'fr/',u'es/']:
        for item in [u"cooking_fast.html", u"cooking_karma_fast.html", u"cooking_karma_fast_light.html",
                     u"cooking.html", u"cooking_karma.html", u"cooking_karma_light.html",
                     u"leatherworking_fast.html", u"leatherworking.html", u"leatherworking_craft_all.html",
                     u"tailor_fast.html", u"tailor.html", u"tailor_craft_all.html",
                     u"artificing_fast.html", u"artificing.html", u"artificing_craft_all.html",
                     u"jewelcraft_fast.html", u"jewelcraft.html", u"jewelcraft_craft_all.html",
                     u"weaponcraft_fast.html", u"weaponcraft.html", u"weaponcraft_craft_all.html",
                     u"huntsman_fast.html", u"huntsman.html", u"huntsman_craft_all.html",
                     u"armorcraft_fast.html", u"armorcraft.html", u"armorcraft_craft_all.html",
                     u"total.html"]:
            with codecs.open(lang+item,u'rb') as f:
                myFtp.storbinary(u'STOR /gw2crafts.net/'+lang+item,f)
            os.remove(lang+item)
    myFtp.close()


# If ran directly, call main
if __name__ == '__main__':
    main()
