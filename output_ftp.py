#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Author: Jeremy Parks
Purpose: Function for writing output files over FTP.
Note: Requires Python 2.7.x
'''

import time
from ftplib import FTP
from random import randint
from StringIO import StringIO

# FTP Login
from Ftp_info import ftp_url, ftp_user, ftp_pass


def write_file(directory, filename, contents):
	while True:
		try:
			myFtp = FTP(ftp_url)
			myFtp.login(ftp_user,ftp_pass)
			f = StringIO(contents.encode('utf8'))
			myFtp.storbinary(u'STOR /gw2crafts.net/'+directory+filename,f)
			myFtp.close()
			return
		except Exception, err:
			print u'ERROR: %s.' % str(err)
			time.sleep(randint(1,10))