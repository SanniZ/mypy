#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on 2018-12-04

@author: Byng Zeng
"""

import os

class MyBase (object):

	@classmethod
	# print msg and exit
	def print_exit(cls, msg=None):
		if msg != None:
		    print msg
		# stop runing and exit.
		exit()

	@classmethod
	def get_exname(cls, f):
		return os.path.splitext(f)[1].lower()

	@classmethod
	def get_fname(cls, f):
		return os.path.basename(f)

	@classmethod
	def make_path(cls, path):
		if not os.path.exists(path):
			os.makedirs(path)

	@classmethod
	def get_home_path(cls):
		return os.getenv('HOME')

	@classmethod
	def get_abs_path(cls, path):
		return os.path.abspath(path)

	@classmethod
	def get_current_path(cls):
		return os.getcwd()

	@classmethod
	def remove_small_file(cls, path, size):
		for rt, dirs, fs in os.walk(path):
			if len(fs) != 0:
				for f in fs:
					f = os.path.join(rt, f)
					if os.path.getsize(f) < size:
						os.remove(f)

	@classmethod
	def remove_blank_dir(cls, path, level=4):
		for i in range(level):
			for rt, dr, fs in os.walk(path):
				if len(dr) == 0 and len(fs) == 0:
					os.rmdir(rt)

