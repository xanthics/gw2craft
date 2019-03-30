#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Author: Jeremy Parks
Purpose: Function for writing output files to AWS.
Note: Requires Python 2.7.x
'''

import os
import time
from random import randint

import boto3


def write_file(directory, filename, contents):
	while True:
		try:
			keyname = os.path.join('{}'.format(directory), filename)
			s3 = boto3.resource('s3')
			s3.Object('gw2crafts.net', keyname).put(Body=contents.encode('utf8'), ContentType='text/html')
			return
		except Exception, err:
			print u'ERROR: %s.' % str(err)
			time.sleep(randint(1, 10))
