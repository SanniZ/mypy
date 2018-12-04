#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on 2018-12-03

@author: Byng.Zeng
"""

import os
import sys
import getopt
import re

from base import MyBase as Base

BASHRC='%s/.bashrc' % Base.get_home_path()

class SetupMypy (object):

	def print_help(self):
		print '======================================'
		print '     mypy setup'
		print '======================================'
		print 'option: -a path -s -v'
		print '  -a:'
		print '    add path to mypys env'
		print '  -s:'
		print '    setup mypys config'
		print '  -v:'
		print '    print all of mypys path.'
		# exit here
		Base.print_exit()

	def __init__(self):
		self.__re_mypys = re.compile('MYPYS=.+')
		self.__re_path_mypys = re.compile('PATH=\$PATH:\$MYPYS')
		self._path = list()

	def add_to_mypy_path(self, path):
		with open(BASHRC, 'r') as f:
			txt = f.read()
		mypys =  self.__re_mypys.findall(txt)
		# delete $.
		if len(re.findall('\$', path)) != 0:
			patten = path.replace('$', '\$')
		else:
			patten = path
		# add new path. 
		if len(mypys) != 0 and len(re.findall(patten, mypys[0])) == 0:
			print 'add path: %s' % path
			txt = txt.replace(mypys[0], '%s:%s' % (mypys[0], path))
		with open(BASHRC, 'w') as f:
			f.write(txt)

	def setup_bash_env(self):
		with open(BASHRC, 'r+') as f:
			txt = f.read()
			result = self.__re_mypys.findall(txt)
			if len(result) == 0:
				f.write('export MYPYS=$HOME/mypy\n')
			result = self.__re_path_mypys.findall(txt)
			if len(result) == 0:
				f.write('export PATH=$PATH:$MYPYS\n')
		self.add_to_mypy_path('$MYPY/broxton')
		self.add_to_mypy_path('$MYPY/develop')
		self.add_to_mypy_path('$MYPY/image')
		self.add_to_mypy_path('$MYPY/iOS')
		self.add_to_mypy_path('$MYPY/linux')
		self.add_to_mypy_path('$MYPY/mypy')
		self.add_to_mypy_path('$MYPY/tools')
		self.add_to_mypy_path('$MYPY/web')
		self.add_to_mypy_path('$MYPY/web/mzitu')

	def print_pypys_path(self):
		with open(BASHRC, 'r') as f:
			txt = f.read()
			result = self.__re_mypys.findall(txt)
			if len(result) == 0:
				print('No found MYPYS')
			else:
				print re.search('MYPY=.+', txt).group()
				mypys = re.split(':', str(result))
				for mypy in mypys:
					mypy = mypy.replace('[\'MYPYS=', '')
					mypy = mypy.replace('\']', '')
					print(mypy)

	def get_user_input(self):
		try:
			opts, args = getopt.getopt(sys.argv[1:], "ha:sv")
		except getopt.GetoptError:
			Base.print_exit('Invalid input, -h for help.')
		# get input
		if len(opts) == 0:
			Base.print_exit('Invalid input, -h for help.')
		else:        
			for name, value in opts:
				if name == '-h':
					self.print_help()
				elif name == '-a':
					self._path.append(value)
				elif name == '-s':
					self.setup_bash_env()
				elif name == '-v':
					self.print_pypys_path()
		return True

	def main(self):
		if self.get_user_input() != True:
			exit()

		if len(self._path) != 0:
			for path in self._path:
				self.add_to_mypy_path(path)

if __name__ == '__main__':
	mypy = SetupMypy()
	mypy.main()


