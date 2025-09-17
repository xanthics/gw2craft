#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
* Copyright (c) 2013-2016 Jeremy Parks. All rights reserved.
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
Purpose: Generates a crafting guide, for all crafts in Guild Wars 2, based on current market prices
Note: Requires Python 3.7.x
'''

import datetime
# recipe and item lists
import sys
from copy import deepcopy

import Globals
from auto_gen import Armorsmith, Artificer, Chef, Chef_karma, Huntsman, Jeweler, Leatherworker, Scribe, Tailor, Weaponsmith
# Localized text
from translations import Localcz, Localde, Localen, Locales, Localfr, Localptbr, Localzh
from multiprocessing import Pool, cpu_count
from MyPrint import maketotals
from MyPrices import appendCosts
from MakeGuide import costCraft
from time import time


# helper class to time main function
class mytimer:
	def __init__(self, name):
		self.__name = name

	def __enter__(self):
		print(("Start: {}".format(self.__name)))
		self.__t = time()

	def __exit__(self, exc_type, exc_val, exc_tb):
		t2 = time()
		print(("  End: {}, took {:.3f} seconds".format(self.__name, t2 - self.__t)))


# Join 2 recipe dicts
def join(A, B):
	if not isinstance(A, dict) or not isinstance(B, dict):
		return A or B
	return dict([(a, join(A.get(a), B.get(a))) for a in set(A.keys()) | set(B.keys())])


def recipeworker(inc_params):  # , out_q):
	cmds, cList, free, mytime, xp_to_level, backupkey = inc_params
	Globals.init()
	totals = {}

	if type(cmds) is list:
		Globals.karmin = {}
		for cmd in cmds:
			with mytimer(cmd[0]):
				totals.update(costCraft(cmd[0], cmd[1], cmd[2], cmd[3], cmd[4], Globals.mydeepcopy(cList), mytime, xp_to_level, backupkey, free))
	else:
		with mytimer(cmds[0]):
			totals.update(costCraft(cmds[0], cmds[1], cmds[2], cmds[3], cmds[4], Globals.mydeepcopy(cList), mytime, xp_to_level, backupkey, free))
	return totals


def main():
	backupkey = 'archive/' + datetime.datetime.utcnow().strftime('%Y%m%dT%H%M')
	mytime = "<span class=\"localtime\">" + datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M') + '+00:00</span>'
	# Will hold level:total xp pairs (array)
	xp_to_level = [0]
	# populate the xp chart
	for i in range(1, 510):
		xp_to_level.append(Globals.xpreq(i) + xp_to_level[i - 1])

	with mytimer('costs'):
		cList = appendCosts()

	# create a copy of our pricelist and update the prices for non-whitelisted items
	cList_free = deepcopy(cList)
	for item in cList_free:
		if not cList_free[item]['whitelist']:
			cList_free[item]['cost'] = sys.maxsize
		del cList[item]['whitelist']
		del cList_free[item]['whitelist']

	cooking_karma = join(Chef.recipes, Chef_karma.recipes)
	rList = [
		[("cooking_karma_fast.html", cooking_karma, True, False, list(range(0, 400, 25))),
		 ("cooking_karma_fast_light.html", cooking_karma, True, False, list(range(0, 400, 25)))],
		[("cooking_karma.html", cooking_karma, False, False, list(range(0, 400, 25))),
		 ("cooking_karma_light.html", cooking_karma, False, False, list(range(0, 400, 25)))],
		("cooking_fast.html", Chef.recipes, True, False, list(range(0, 400, 25))),
		("cooking.html", Chef.recipes, False, False, list(range(0, 400, 25))),
		("cooking_fast_200.html", Chef.recipes, True, False, list(range(0, 200, 25))),
		("cooking_karma_fast_200.html", cooking_karma, True, False, list(range(0, 200, 25))),

#		(u"cooking_karma_400.html", cooking_karma, False, False, range(400, 500, 25)),
		("cooking_karma_450.html", cooking_karma, False, False, list(range(400, 450, 25))),
#		(u"cooking_400.html", Chef.recipes, False, False, range(400, 500, 25)),
		("cooking_450.html", Chef.recipes, False, False, list(range(400, 450, 25))),

		("jewelcraft_fast.html", Jeweler.recipes, True, False, list(range(0, 400, 25))),
		("jewelcraft.html", Jeweler.recipes, False, False, list(range(0, 400, 25))),
#		(u"jewelcraft_400.html", Jeweler.recipes, False, True, range(400, 500, 25)),
#		(u"jewelcraft_450.html", Jeweler.recipes, False, True, range(400, 450, 25)),
		("artificing_fast.html", Artificer.recipes, True, False, list(range(0, 400, 25))),
		("artificing.html", Artificer.recipes, False, False, list(range(0, 400, 25))),
		("artificing_400.html", Artificer.recipes, False, True, list(range(400, 500, 25))),
		("artificing_450.html", Artificer.recipes, False, True, list(range(400, 450, 25))),
		("weaponcraft_fast.html", Weaponsmith.recipes, True, False, list(range(0, 400, 25))),
		("weaponcraft.html", Weaponsmith.recipes, False, False, list(range(0, 400, 25))),
		("weaponcraft_400.html", Weaponsmith.recipes, False, True, list(range(400, 500, 25))),
		("weaponcraft_450.html", Weaponsmith.recipes, False, True, list(range(400, 450, 25))),
		("huntsman_fast.html", Huntsman.recipes, True, False, list(range(0, 400, 25))),
		("huntsman.html", Huntsman.recipes, False, False, list(range(0, 400, 25))),
		("huntsman_400.html", Huntsman.recipes, False, True, list(range(400, 500, 25))),
		("huntsman_450.html", Huntsman.recipes, False, True, list(range(400, 450, 25))),
		("armorcraft_fast.html", Armorsmith.recipes, True, False, list(range(0, 400, 25))),
		("armorcraft.html", Armorsmith.recipes, False, False, list(range(0, 400, 25))),
		("armorcraft_400.html", Armorsmith.recipes, False, True, list(range(400, 500, 25))),
		("armorcraft_450.html", Armorsmith.recipes, False, True, list(range(400, 450, 25))),
		("tailor_fast.html", Tailor.recipes, True, False, list(range(0, 400, 25))),
		("tailor.html", Tailor.recipes, False, False, list(range(0, 400, 25))),
		("tailor_400.html", Tailor.recipes, False, True, list(range(400, 500, 25))),
		("tailor_450.html", Tailor.recipes, False, True, list(range(400, 450, 25))),
		("leatherworking_fast.html", Leatherworker.recipes, True, False, list(range(0, 400, 25))),
		("leatherworking.html", Leatherworker.recipes, False, False, list(range(0, 400, 25))),
		("leatherworking_400.html", Leatherworker.recipes, False, True, list(range(400, 500, 25))),
		("leatherworking_450.html", Leatherworker.recipes, False, True, list(range(400, 450, 25))),
	]

	p = Pool(cpu_count() - 1 if cpu_count() > 1 else 1)
	#p = Pool(1)
	# create params for the core and free guides
#	for my_list, free in [(cList, False), (cList_free, True)]:
#	from hanging_threads import start_monitoring
#	monitoring_thread = start_monitoring()
	params = []
	for i in range(0, len(rList)):
		params.append((rList[i], cList, False, mytime, xp_to_level, backupkey))
		params.append((rList[i], cList_free, True, mytime, xp_to_level, backupkey))
	# free accounts can't follow scribe guides
	params.append((("scribe.html", Scribe.recipes, False, False, list(range(0, 400, 25))), cList, False, mytime, xp_to_level, backupkey))

	procs = p.map(recipeworker, params)

	totals = {}
	totals_free = {'scribe': {0: 0, 75: 0, 150: 0, 225: 0, 300: 0, 'total': 0}}
	# this needs to be rewritten so that we can do the free and core guides in the same queue
	for i in procs:
		val = i['free']
		del i['free']
		if val:
			totals_free.update(i)
		else:
			totals.update(i)

	for lang in [Localen, Localde, Localfr, Locales, Localcz, Localptbr, Localzh]:
		maketotals(totals, mytime, lang, False)
		maketotals(totals_free, mytime, lang, True)


# If ran directly, call main
if __name__ == '__main__':
	with mytimer('main'):
		main()
