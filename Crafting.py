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
Purpose: Generates a crafting guide, for all crafts in Guild Wars 2, based on current market prices
Note: Requires Python 2.7.x
'''

import datetime
import math
import os
import codecs
import sys
import threading
import time
# recipe and item lists
import Armorsmith, Artificer, Chef, Chef_karma, Huntsman, Jeweler, Leatherworker, Tailor, Weaponsmith, items, Globals
# Localized text
import localen, localde, localfr, locales, localcz
from multiprocessing import Process, Queue, cpu_count
from copy import deepcopy
from MyPrint import maketotals
from MyPrices import appendCosts
from MakeGuide import costCraft

# Join 2 recipe dicts
def join(A, B):
		if not isinstance(A, dict) or not isinstance(B, dict):
				return A or B
		return dict([(a, join(A.get(a), B.get(a))) for a in set(A.keys()) | set(B.keys())])

def recipeworker(cmds, cList, mytime, xp_to_level, out_q):
	totals = {}
	for cmd in cmds:
		if len(cmd) == 2:
			Globals.karmin = {}
			for subcmd in cmd:
				totals.update(costCraft(subcmd[0],subcmd[1],subcmd[2],subcmd[3],subcmd[4],deepcopy(cList),mytime,xp_to_level))
		else:
			totals.update(costCraft(cmd[0],cmd[1],cmd[2],cmd[3],cmd[4],deepcopy(cList),mytime,xp_to_level))
	out_q.put(totals)

def main():
	Globals.init()
	# Uncomment these lines if you are writing files to disk
#	if not os.path.exists("de"):
#		os.makedirs("de")
#	if not os.path.exists("es"):
#		os.makedirs("es")
#	if not os.path.exists("fr"):
#		os.makedirs("fr")
	mytime = "<span class=\"localtime\">" + datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S')+u'+00:00</span>'
	print "Start: ", datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
	# will hold our guide names, so no more manually creating upload list
	guides = []
	# Will hold level:total xp pairs (array)
	xp_to_level = [0]
	# populate the xp chart
	for i in range(1,510):
		xp_to_level.append(Globals.xpreq(i)+xp_to_level[i-1])

	cList = appendCosts()

	out_q = Queue()
	#TODO change the way flags are passed so it is easier to understand

	cooking_karma = join(Chef.recipes, Chef_karma.recipes)
	rList = [[(u"cooking_karma_fast.html",cooking_karma,True,False,range(0,400,25)),
			 (u"cooking_karma_fast_light.html",cooking_karma,True,False,range(0,400,25))],
			 [(u"cooking_karma.html",cooking_karma,False,False,range(0,400,25)),
			 (u"cooking_karma_light.html",cooking_karma,False,False,range(0,400,25))],
			 (u"cooking_fast.html",Chef.recipes,True,False,range(0,400,25)),
			 (u"cooking.html",Chef.recipes,False,False,range(0,400,25)),
			 (u"cooking_fast_200.html",Chef.recipes,True,False,range(0,200,25)),
			 (u"cooking_karma_fast_200.html",cooking_karma,True,False,range(0,200,25)),
			 (u"jewelcraft_fast.html",Jeweler.recipes,True,False,range(0,400,25)),
			 (u"jewelcraft.html",Jeweler.recipes,False,False,range(0,400,25)),
			 (u"jewelcraft_400.html",Jeweler.recipes,False,True,range(400,500,25)),
			 (u"jewelcraft_450.html",Jeweler.recipes,False,True,range(400,450,25)),
			 (u"artificing_fast.html",Artificer.recipes,True,False,range(0,400,25)),
			 (u"artificing.html",Artificer.recipes,False,False,range(0,400,25)),
			 (u"artificing_400.html",Artificer.recipes,False,True,range(400,500,25)),
			 (u"artificing_450.html",Artificer.recipes,False,True,range(400,450,25)),
			 (u"weaponcraft_fast.html",Weaponsmith.recipes,True,False,range(0,400,25)),
			 (u"weaponcraft.html",Weaponsmith.recipes,False,False,range(0,400,25)),
			 (u"weaponcraft_400.html",Weaponsmith.recipes,False,True,range(400,500,25)),
			 (u"weaponcraft_450.html",Weaponsmith.recipes,False,True,range(400,450,25)),
			 (u"huntsman_fast.html",Huntsman.recipes,True,False,range(0,400,25)),
			 (u"huntsman.html",Huntsman.recipes,False,False,range(0,400,25)),
			 (u"huntsman_400.html",Huntsman.recipes,False,True,range(400,500,25)),
			 (u"huntsman_450.html",Huntsman.recipes,False,True,range(400,450,25)),
			 (u"armorcraft_fast.html",Armorsmith.recipes,True,False,range(0,400,25)),
			 (u"armorcraft.html",Armorsmith.recipes,False,False,range(0,400,25)),
			 (u"armorcraft_400.html",Armorsmith.recipes,False,True,range(400,500,25)),
			 (u"armorcraft_450.html",Armorsmith.recipes,False,True,range(400,450,25)),
			 (u"tailor_fast.html",Tailor.recipes,True,False,range(0,400,25)),
			 (u"tailor.html",Tailor.recipes,False,False,range(0,400,25)),
			 (u"tailor_400.html",Tailor.recipes,False,True,range(400,500,25)),
			 (u"tailor_450.html",Tailor.recipes,False,True,range(400,450,25)),
			 (u"leatherworking_fast.html",Leatherworker.recipes,True,False,range(0,400,25)),
			 (u"leatherworking.html",Leatherworker.recipes,False,False,range(0,400,25)),
			 (u"leatherworking_400.html",Leatherworker.recipes,False,True,range(400,500,25)),
			 (u"leatherworking_450.html",Leatherworker.recipes,False,True,range(400,450,25))]

	nprocs = cpu_count() * 2

	procs = []
	global header
	global cright

	chunksize = int(math.ceil(len(rList) / float(nprocs)))

	for i in range(nprocs):
		p = Process(target=recipeworker,args=(rList[chunksize * i:chunksize * (i + 1)],cList,mytime,xp_to_level,out_q))
		procs.append(p)
		p.start()

	totals = {}
	for i in range(nprocs):
		totals.update(out_q.get())

	for p in procs:
		p.join(180)
		# if thread is still alive after 180 seconds, something is wrong.  Kill the script.
		if p.is_alive():
			sys.exit(0)

	maketotals(totals,mytime,localen)
	maketotals(totals,mytime,localde)
	maketotals(totals,mytime,localfr)
	maketotals(totals,mytime,locales)
	maketotals(totals,mytime,localcz)

	print "End: ", datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S')


# If ran directly, call main
if __name__ == '__main__':
	main()
