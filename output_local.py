#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Author: Jeremy Parks
Purpose: Function for writing output files to local filesystem.
Note: Requires Python 2.7.x
'''

import codecs
import os

def write_file(directory, filename, contents):
	if directory and not os.path.exists(directory):
		os.makedirs(directory)

	with codecs.open(directory+filename, 'wb', encoding='utf-8') as f:
		f.write(contents)