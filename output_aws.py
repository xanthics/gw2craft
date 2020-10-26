#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Author: Jeremy Parks
Purpose: Function for writing output files to AWS.
Note: Requires Python 3.7.x
'''

import os
import time
from random import randint

import boto3


def write_file(directory, filename, contents, backupdir=''):
	while True:
		try:
			keyname = os.path.join('{}'.format(directory), filename)
			s3 = boto3.resource('s3')
			s3.Object('gw2crafts.net', keyname).put(Body=contents.encode('utf8'), ContentType='text/html', CacheControl='public, max-age=1260')
			if backupdir:
				copy_source = {
					'Bucket': 'gw2crafts.net',
					'Key': keyname
				}
				b_keyname = os.path.join('{}'.format(backupdir + '/' + directory), filename)
				#s3.meta.client.copy(copy_source, 'gw2crafts.net', b_keyname)
				s3.Object('gw2crafts.net', b_keyname).copy_from(CopySource='gw2crafts.net/' + keyname, ContentType='text/html', CacheControl='public', Metadata={'X-Robots-Tag': 'noindex'}, MetadataDirective="REPLACE")
			return
		except Exception as err:
			print('ERROR: %s.' % str(err))
			time.sleep(randint(1, 10))
