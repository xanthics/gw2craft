#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Author: Jeremy Parks
Purpose: Globals
Note: Requires Python 3.7.x
'''

import threading
import math
from collections import defaultdict
from copy import deepcopy
from xpgain_lookup import table


TLcache = threading.local()


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
	for k, v in indict.items():
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


# Nav bar
# path, home, nGuides, fGuides, special, cooking, nHearts, tHearts, aHearts, jc, art, hunt, wc, ac, lw, tailor, scribe, totals, about, lang, current page, free?
header = """<nav>
    <ul>
        <li><a href="/{22}{0}">{1}</a></li>
        <li><a href="#">{2}</a>
        <ul>
            <li><a href="#">{5}</a>
            <ul>
                <li><a href="/{22}{0}cooking.html">{6}</a></li>
                <li><a href="/{22}{0}cooking_karma_light.html">{7}</a></li>
                <li><a href="/{22}{0}cooking_karma.html">{8}</a></li>
            </ul>
            </li>
            <li><a href="/{22}{0}jewelcraft.html">{9}</a></li>
            <li><a href="/{22}{0}artificing.html">{10}</a></li>
            <li><a href="/{22}{0}huntsman.html">{11}</a></li>
            <li><a href="/{22}{0}weaponcraft.html">{12}</a></li>
            <li><a href="/{22}{0}armorcraft.html">{13}</a></li>
            <li><a href="/{22}{0}leatherworking.html">{14}</a></li>
            <li><a href="/{22}{0}tailor.html">{15}</a></li>
            <li><a href="/{22}{0}scribe.html">{16}</a></li>
        </ul>
        </li>
        <li><a href="#">{3}</a>
        <ul>
            <li><a href="#">{5}</a>
            <ul>
                <li><a href="/{22}{0}cooking_fast.html">{6}</a></li>
                <li><a href="/{22}{0}cooking_karma_fast_light.html">{7}</a></li>
                <li><a href="/{22}{0}cooking_karma_fast.html">{8}</a></li>
            </ul>
            </li>
            <li><a href="/{22}{0}jewelcraft_fast.html">{9}</a></li>
            <li><a href="/{22}{0}artificing_fast.html">{10}</a></li>
            <li><a href="/{22}{0}huntsman_fast.html">{11}</a></li>
            <li><a href="/{22}{0}weaponcraft_fast.html">{12}</a></li>
            <li><a href="/{22}{0}armorcraft_fast.html">{13}</a></li>
            <li><a href="/{22}{0}leatherworking_fast.html">{14}</a></li>
            <li><a href="/{22}{0}tailor_fast.html">{15}</a></li>
        </ul>
        </li>
        <li><a href="#">400-500</a>
        <ul>
            <li><a href="/{22}{0}artificing_400.html">{10}</a></li>
            <li><a href="/{22}{0}huntsman_400.html">{11}</a></li>
            <li><a href="/{22}{0}weaponcraft_400.html">{12}</a></li>
            <li><a href="/{22}{0}armorcraft_400.html">{13}</a></li>
            <li><a href="/{22}{0}leatherworking_400.html">{14}</a></li>
            <li><a href="/{22}{0}tailor_400.html">{15}</a></li>
        </ul>
        </li>
        <li><a href="#">{4}</a>
        <ul>
            <li><a href="#">{5} 1-200</a>
            <ul>
                <li><a href="/{22}{0}cooking_fast_200.html">{6}</a></li>
                 <li><a href="/{22}{0}cooking_karma_fast_200.html">{8}</a></li>
            </ul>
            </li>
            <li><a href="#">400-450</a>
            <ul>
                <li><a href="/{22}{0}cooking_450.html">{6}</a></li>
                <li><a href="/{22}{0}cooking_karma_450.html">{8}</a></li>
                <li><a href="/{22}{0}artificing_450.html">{10}</a></li>
                <li><a href="/{22}{0}huntsman_450.html">{11}</a></li>
                <li><a href="/{22}{0}weaponcraft_450.html">{12}</a></li>
                <li><a href="/{22}{0}armorcraft_450.html">{13}</a></li>
                <li><a href="/{22}{0}leatherworking_450.html">{14}</a></li>
                <li><a href="/{22}{0}tailor_450.html">{15}</a></li>
            </ul>
            </li>
        </ul>
        </li>
        <li><a href="/{22}{0}total.html">{17}</a></li>
        <li><a href="/{22}{0}faq.html">{18}</a></li>
        <li><a href="#" class="language" hreflang="{20}">{19}</a>
        <ul>
          <li><a href="/{22}{21}" hreflang="en">English</a></li>
          <li><a href="/{22}fr/{21}" hreflang="fr">Français</a></li>
          <li><a href="/{22}cz/{21}" hreflang="cz">Čeština</a></li>
          <li><a href="/{22}de/{21}" hreflang="de">Deutsch</a></li>
          <li><a href="/{22}es/{21}" hreflang="es">Español</a></li>
          <li><a href="/{22}pt-br/{21}" hreflang="pt-BR">Português do Brasil</a></li>
          <li><a href="/{22}zh/{21}" hreflang="zh">Chinese (Simplified)</a></li>
        </ul>
        </li>
    </ul>
</nav>
"""
