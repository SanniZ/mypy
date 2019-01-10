#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on 2018-11-23

@author: Byng Zeng
"""

import sys
import os
import getopt

class CounterOfPath(object):
    def __init__(self):
        self._path = None
        self._name = None
        self._opt  = None

    def print_help(self):
        print 'option: -p path -n name -o f/e/d'
        print '  path : set path to be find.'
        print '  name : set name of file to be find.'
        print '  f/e/d: sepcial opt to find file/extname/dir'
        print ''
        print 'example: -p ~/Downloads -n .jpg -o e'
        print 'example: -p ~/Downloads -n 123.jpg -o f'
        print 'example: -p ~/Downloads -o d'
        exit()

    def get_count_of_name(self, path, name):
        max = 0
        for root, dirs, files in os.walk(path):
            if len(files) != 0:
                for f in files:
                    if f == name:
                        max = max + 1
        return max

    def get_count_of_extname(self, path, ext_name):
        max = 0
        for root, dirs, files in os.walk(path):
            if len(files) != 0:
                for f in files:
                    if os.path.splitext(f)[1] == ext_name:
                        max = max + 1
        return max

    def get_count_of_dir(self, path):
        max = 0
        for root, dirs, files in os.walk(path):
            if len(files) != 0:
                for d in dirs:
                    max = max + 1
        return max

    def get_count(self):
        if self._opt == 'f' and self._name != None:
            return self.get_count_of_name(self._path, self._name)
        elif self._opt == 'e' and self._name != None:
            return self.get_count_of_extname(self._path, self._name)
        elif self._opt == 'd':
            return self.get_count_of_dir(self._path)
        else:
            self.print_help()

    def get_user_input(self):
        try:
            opts, args = getopt.getopt(sys.argv[1:], 'hp:n:o:')
        except getopt.GetoptError:
            self.print_help()
            return False
        # process input
        if len(opts) == 0 and len(args) != 0: # input error
            self.print_help()
            return False
        else:
            for name, value in opts:
                if name == r'-h':
                    self.print_help()
                elif name == r'-p':
                    self._path = value
                elif name == r'-n':
                    self._name = value
                elif name == r'-o':
                    self._opt = value
        # check args.
        if self._path == None or self._name == None:
            return False
        else:
            return True

    def main(self):
        if self.get_user_input() == False:
            self.print_help()
        else:
            print self.get_count()

if __name__ == '__main__':
    ctr = CounterOfPath()
    ctr.main()
