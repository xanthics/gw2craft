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
Purpose: Generates(or updates) all the recipes and the item list used by Crafting.py
Note: Requires Python 2.7.x
'''
import urllib, json, math
from collections import defaultdict
from multiprocessing import Process, Queue

API_ROOT = "https://api.guildwars2.com/v1/"

# Helper Function
def recipelistWorker(items, out_q):
    outdict = {}

    for index, i in enumerate(items, 1):
        print index, len(items)
        item = _api_call('recipe_details.json?recipe_id=%d' % i)
        outdict[i] = item

    out_q.put(outdict)

# Get and return all available recipes from the API
def get_recipes():
    temp = _api_call('recipes.json')
    out_q = Queue()
    nprocs = 32
    lister = temp['recipes']
    chunksize = int(math.ceil(len(lister) / float(nprocs)))
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
    # We don't care about feasts
    # key is item_id
    feasts = [12551, 12552, 12554, 12555, 12556, 12557, 12558, 12560, 12561,
              12562, 12564, 12565, 12570, 12571, 12572, 12573, 12574, 12575,
              12577, 12578, 12579, 12580, 12581, 12582, 12583, 12584, 12594,
              12595, 12596, 12597, 12599, 12601, 12604, 12605, 12607, 12608,
              12609, 12611, 12615, 12617, 12618, 12620, 12622, 12624, 12625,
              12627, 12628, 12629, 12630, 12631, 12632, 12644, 12647, 12648,
              12649, 12650, 12651, 12652, 12654, 12655, 12661, 12664, 12665,
              12669, 12672, 12673, 12674, 12677, 12690, 12691, 12698, 12699,
              12707, 12708, 12711, 12712, 12713, 12719, 12563]

    # Karma items so cooking lists are built properly
    # key is item_id
    karma = [12165, 12232, 12237, 12239, 12240, 12249, 12251, 12252, 12256,
             12337, 12338, 12339, 12340, 12350, 12502, 12503, 12514, 12515,
             12516, 12517, 12518, 12543]

    # These recipes have to be purchased from AH, therefore we don't want them
    # Glazed Peach Tart[s], Glazed Pear Tart[s], Piece[s] of Candy Corn Almond
    # Brittle, Strawberry Ghost[s], Bowl[s] of Candy Corn Custard
    # key is recipe_id
    bad_recipes = [6479, 6478, 6475, 6474, 6472]

    # Recipes learned from Master Craftsmen that we still want to consider
    # key is item_id
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
                    24924, 24898, 24918, 24925]

    crafts = {u'Weaponsmith':{}, u'Chef':{}, u'Chef_karma':{}, u'Huntsman':{},
              u'Armorsmith':{}, u'Jeweler':{}, u'Artificer':{}, u'Tailor':{},
              u'Leatherworker':{}}
    item_ids = {}

    new_recipes = {r[0]:r[1] for r in recipes.items() if
                   r[0] not in [bad_recipes, feasts]}
    for recipe, data in new_recipes.items():
        min_rating = data['min_rating']
        item_id = data['output_item_id']
        item_count = data['output_item_count']
        ingredient_set = set(int(i[u'item_id']) for i in data[u'ingredients'])

        if min_rating == u'400' or 19717 in ingredient_set:
            continue
            
        for it in data[u'disciplines']:
            key = it
            
            if it == u'Chef' and set(karma) & ingredient_set:
                key = u'Chef_karma'

            crafts[key].setdefault(str(min_rating), {})
            crafts[key][min_rating][item_id] = data[u'ingredients']
            item_ids[item_id] = {u'output_item_count': item_count,
                                 u'type': data[u'type'],
                                 u'flags': data[u'flags']}

    for craft in crafts:
        with open(craft+".py","wb") as f:
            f.write(u'# coding=unicode-escape\nrecipes = {\n')
            for lvl in crafts[craft]:
                f.write(u"\t" + lvl + ":{\n")
                for obj in crafts[craft][lvl]:
                    mystr = u""
                    for part in crafts[craft][lvl][obj]:
                        if not part[u'item_id'] in item_ids:
                            item_ids[part[u'item_id']] = {u'type':u'Other',u'output_item_count':u'0',u'flags':[]}
                        mystr += part[u'item_id']+":"+part[u'count'] +","
                    f.write(u"\t\t" + obj +u":{"+ mystr[:-1] +u"},\n" )
                f.write(u"\t},\n")
            f.write(u"}")

    return item_ids

# helper function
def itemlistWorker(items, out_q):
    outdict = {}
    for index, i in enumerate(items, 1):
        print index, len(items)
        item = _api_call('item_details.json?item_id=%s' % i)
        outdict[i] = item
    out_q.put(outdict)

# get more information on every item the recipes use
def itemlist(item_list):
    out_q = Queue()
    nprocs = 32
    lister = item_list.keys()

    chunksize = int(math.ceil(len(lister) / float(nprocs)))
    procs = []

    for i in range(nprocs):
        p = Process(target=itemlistWorker,
                    args=(lister[chunksize * i:chunksize * (i + 1)], out_q))
        procs.append(p)
        p.start()

    flags = {}
    for i in range(nprocs):
        flags.update(out_q.get())

    for p in procs:
        p.join()

    with open("items.py","wb") as f:
        f.write('# coding=unicode-escape\nilist = {\n')
        # sorted is only so we can easily spot new items with diff
        for i in sorted(flags): # otherwise output is semi random order
            item_list[i][u'name'] = flags[i][u'name']
            item_list[i][u'rarity'] = flags[i][u'rarity']
            item_list[i][u'vendor_value'] = int(flags[i][u'vendor_value'])
            if item_list[i][u'flags']:
                item_list[i][u'discover'] = 0
            del(item_list[i][u'flags'])
            f.write("\t"+ str(i) +":"+ str(item_list[i])+",\n")
        f.write('}')

def _api_call(endpoint):
    try:
        f = urllib.urlopen(API_ROOT + endpoint)
        item = json.load(f)
    except Exception, err:
        print 'Error: %s.\n' % str(err)
        exit(-1)

    return item
    
def main():
    recipes = get_recipes()
    item_list = parse_recipes(recipes)
    itemlist(item_list)

# If ran directly, call main
if __name__ == '__main__':
    main()
