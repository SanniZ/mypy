#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on 2018-12-04

@author: Byng Zeng
"""

import os
import sys
import getopt
import zipfile
import shutil

from base import MyBase as Base
from image import Image as Img


class WizImage(object):

	# print(help menu.
	@classmethod
	def print_help(cls):
		print('======================================')
		print('     Unzip Wiz')
		print('======================================')
		print('option: -s path -p path')
		print('  -s:')
		print('    root path of files')
		print('  -t:')
		print('    root path to output.')
		# exit here
		Base.print_exit()

	def __init__(self):
		self._src = None
		self._dst = None
		self._fs = list()

	def get_user_input(self):
		try:
			opts, args = getopt.getopt(sys.argv[1:], "hs:t:")
		except getopt.GetoptError:
			Base.print_exit('Invalid input, -h for help.')
		# get input
		if len(opts) == 0:
			Base.print_exit('Invalid input, -h for help.')
		else:        
			for name, value in opts:
				if name == '-h':
					self.print_help()
				elif name == '-s':
					self._src = Base.get_abs_path(value)
				elif name == '-t':
					self._dst = Base.get_abs_path(value)
			# start to check args.
			# start id is must be set, otherwise return..
			if self._src == None:
				return False
			# next to start if _end is not set.
			if self._dst == None:
				self._dst = Base.get_current_path()
		return True

	def get_all_of_wiz(self):
		for root, dirs, fs in os.walk(self._src):
			if len(fs) != 0:
				for f in fs:
					if Base.get_exname(f) == '.ziw':
						self._fs.append(os.path.join(root, f))

	def unzip_file(self, f, dst):
		r = zipfile.is_zipfile(f)
		if r:
			fz = zipfile.ZipFile(f, 'r')
			for file in fz.namelist():
				fz.extract(file, dst)

	def unzip_wiz(self):
		for f in self._fs:
			print('unzip: %s/%s' % (os.path.dirname(f).replace(self._src, ''), os.path.basename(f)))
			path = os.path.join(os.path.dirname(f).replace(self._src, self._dst), Base.get_fname(f))
			path = os.path.splitext(path)[0]
			Base.make_path(path)
			self.unzip_file(f, path)
			# remove small image.
			Img.remove_small_image(path)
			# move image.
			if os.path.exists('%s/index_files' % path):
				for ff in os.listdir('%s/index_files' % path):
					if Img.is_image(ff):
						shutil.copyfile('%s/index_files/%s' % (path, ff), '%s/%s' % (path, ff))
					os.remove('%s/index_files/%s' % (path, ff))
				# remove invalid files and dirs.
				os.rmdir('%s/index_files' % path)
			if os.path.exists('%s/index.html' % path):
				os.remove('%s/index.html' % path)

	def main(self):
		if self.get_user_input() == False:
			Base.print_exit('Invalid input, -h for help.')
		# get all of .wiz
		self.get_all_of_wiz()
		# unzip all of wiz files.
		self.unzip_wiz()
		# remove blank dir.
		Base.remove_blank_dir(self._dst)

if __name__ == '__main__':
	wiz = WizImage()
	wiz.main()
