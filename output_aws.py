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
Purpose: Function for writing output files to AWS.
Note: Requires Python 2.7.x
'''

import os
import time
from random import randint
from StringIO import StringIO

import boto
import boto.s3
from boto.s3.key import Key

# Credentials
from Ftp_info import amakey, amasec


def write_file(directory, filename, contents):
	while True:
		try:
			keyname = os.path.join( '{}'.format(directory), filename)
			conn = boto.connect_s3(amakey, amasec)
			bucket = conn.get_bucket('gw2crafts.net')
			k = Key(bucket)
			k.key = keyname
			k.metadata.update({'Content-Type':'text/html'})
			k.set_contents_from_string(contents.encode('utf8'))
			return
		except Exception, err:
			print u'ERROR: %s.' % str(err)
			time.sleep(randint(1,10))