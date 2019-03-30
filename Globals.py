#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Author: Jeremy Parks
Purpose: Globals
Note: Requires Python 2.7.x
'''

import threading
import math
from collections import defaultdict
from copy import deepcopy

from xpgain_lookup import table

def init():
	# Hold our 5 most popular renown heart karma items for cooking
	global karmin
	karmin = {}
	global TLcache
	TLcache = threading.local()

def xpreq(level):
	if level > 400:
		level = 400
	tmp = 500
	for _i in range(1,level):
		tmp = math.floor(tmp * 1.01)
	return tmp


# replacement for deepcopy for dictionary as the default is overkill(slow)
def mydeepcopy(indict):
#	ret = deepcopy(indict)
#	return ret
	if isinstance(indict, type(None)):
		return None
	ret = {}
	for k, v in indict.iteritems():
		if type(v) in [dict, defaultdict]:
			ret[k] = mydeepcopy(v)
		elif type(v) is set:
			ret[k] = v.copy()
		# not a dict or set
		else:
			try:
				ret[k] = v[:]
			# not a list, string, or tuple
			# should be a simple type(eg int/float)
			except TypeError:
				ret[k] = v

	return ret
