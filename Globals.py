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
Purpose: Globals
Note: Requires Python 2.7.x
'''

import threading
import math
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
# TODO: fix this, is creating incomplete guides.
def mydeepcopy(indict):
	ret = deepcopy(indict)
	return ret
'''	
	if not indict:
		return None
	ret = {}
	for k, v in indict.iteritems():
		if type(v) is dict:
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
'''
