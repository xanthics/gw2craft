from autogen.items import ilist
from helperfiles.good_items import good_vendor, good_items

import aiohttp
import asyncio
import sys
import time
from pyrate_limiter import *

# import monkey patch for aiohttp to allow response headers > 8190 bytes
from helperfiles.aiohttp_monkey import set_response_params

aiohttp.client_proto.ResponseHandler.set_response_params = set_response_params

# api request limit.  stored in a queue.Queue
limiter = Limiter(RequestRate(20, Duration.SECOND), RequestRate(575, Duration.MINUTE))


@limiter.ratelimit('api', delay=True, max_delay=128)
async def _api_call(session, endpoint, first=False):
	x = 1
	while True:
		print(f"Running: {endpoint[:100]}")
		async with session.get(endpoint) as req:
			reply = await req.json()
			if req.status not in [200, 206]:
				# attempt to sleep with a too many requests response.  Fail if backoff limit reached
				if req.status == 429 and x < 65:
					print(f"API Get sleeping for {x} second(s).")
					time.sleep(x)
					x *= 2
					continue
				raise Exception('API response: {} {}'.format(req.status, req.content))
			if first:
				return int(req.headers['x-page-total']), reply
			return reply


async def getprices():
	api_root = "https://api.guildwars2.com"
	async with aiohttp.ClientSession(api_root) as session:
		api_item_ids = [str(x) for x in await _api_call(session, '/v2/commerce/prices') if x in ilist and not any(v in ilist[x]['flags'] for v in ['SoulbindOnAcquire', 'AccountBound'])]
		api_item_data = (','.join(api_item_ids[i:i + 200]) for i in range(0, len(api_item_ids), 200))
		jobs = (asyncio.ensure_future(_api_call(session, f'/v2/commerce/prices?lang=en&ids={page}')) for page in api_item_data)
		tasks = await asyncio.gather(*jobs)
		outdict = {}
		for p in tasks:
			for sitem in p:
				item = sitem["id"]
				# set value to greater of buy and vendor.  If 0 set to minimum sell value
				w = ilist[item]['vendor_value']
				sell_method = 'vendor'
				if sitem['buys']['unit_price'] * .85 > w:
					w = int(sitem['buys']['unit_price'] * .85)
					sell_method = 'maxbuyout'
				if w == 0:
					w = int(sitem['sells']['unit_price'] * .85)
					sell_method = 'minsell'

				# Save all the information we care about
				outdict[item] = {'value': w, 'cost': sitem['sells']['unit_price'], 'recipe': None, 'rarity': ilist[item]['rarity'],
				                 'type': ilist[item]['type'], 'icon': ilist[item]['img_url'],
				                 'output_item_count': ilist[item]['output_item_count'], 'sellMethod': sell_method,
				                 "discover": True if 'Discover' in ilist[item]['flags'] else False, 'whitelist': sitem[u'whitelisted']}

				if outdict[item]['type'] == 'UpgradeComponent' and outdict[item]['rarity'] == 'Exotic':
					outdict[item]['rarity'] = 'Exotic UpgradeComponent'

				# if the item has a low supply, ignore it
				if sitem['sells']['quantity'] <= 25:
					outdict[item]['cost'] = sys.maxsize

	# set up data for items that you can't buy from tp
	for item in (x for x in ilist if x not in outdict):
		outdict[item] = {'value': 0, 'cost': sys.maxsize, 'recipe': None, 'rarity': ilist[item]['rarity'],
		                 'type': ilist[item]['type'], 'icon': ilist[item]['img_url'],
		                 'output_item_count': ilist[item]['output_item_count'], 'sellMethod': 'vendor',
		                 "discover": True if 'Discover' in ilist[item]['flags'] else False, 'whitelist': False}

		if outdict[item]['type'] == 'UpgradeComponent' and outdict[item]['rarity'] == 'Exotic':
			outdict[item]['rarity'] = 'Exotic UpgradeComponent'

	for item in good_items:
		outdict[item]['cost'] = 0
		outdict[item]['whitelist'] = True

	for item in good_vendor:
		outdict[item]['cost'] = good_vendor[item]
		outdict[item]['whitelist'] = True

	return outdict
