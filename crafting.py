import asyncio
import sys

from time import time
from datetime import datetime

from getprices import getprices


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


def main():
	backupkey = 'archive/' + datetime.utcnow().strftime('%Y%m%dT%H%M')
	mytime = "<span class=\"localtime\">" + datetime.utcnow().strftime('%Y-%m-%dT%H:%M') + '+00:00</span>'

	with mytimer('costs'):
		# Special exception for windows.
#		if (4, 0, 0) > sys.version_info >= (3, 8, 0) and sys.platform.startswith('win'):
#			asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
#		clist = asyncio.run(getprices())
		# save/load temporary until guide generation is complete
		import pickle
#		import json
#		with open('clist.pickle', 'wb') as f:
#			pickle.dump(clist, f)
		with open('clist.pickle', 'rb') as f:
			clist = pickle.load(f)
#		with open('clist.json', 'w') as f:
#			json.dump(clist, f, indent=2, sort_keys=True)


# If ran directly, call main
if __name__ == '__main__':
	with mytimer('main'):
		main()