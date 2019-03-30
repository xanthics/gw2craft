#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Author: Jeremy Parks
Purpose: Interface for writing output files, regardless of method.
Note: Requires Python 2.7.x
'''


# Switch which line is commented out to switch output method.
from output_aws import write_file		# For uploading files to AWS
# from output_ftp import write_file		# For uploading files via FTP
# from output_local import write_file	# For writing files to disk
