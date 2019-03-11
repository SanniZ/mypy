#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 2018-11-23

@author: Byng Zeng
"""

import sys
import os
import getopt


class PathCounter(object):
    def __init__(self):
        self._path = None
        self._name = None
        self._opt = None

    def print_help(self):
        print('option:')
        print('  -p path,name,type: get count of path')
        print('    path : path to be find.')
        print('    name : name of file to be find.')
        print('    type : (f/e/d) - file/extname/dir')
        print('')
        print('example: -p ~/Downloads,.jpg,e')
        print('example: -p ~/Downloads,123.jpg,f')
        print('example: -p ~/Downloads,,d')
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
        if all((self._opt == 'f', self._name)):
            return self.get_count_of_name(self._path, self._name)
        elif all((self._opt == 'e', self._name)):
            return self.get_count_of_extname(self._path, self._name)
        elif all((self._opt == 'd')):
            return self.get_count_of_dir(self._path)
        else:
            print('Error, invalid vars!')

    def get_input_args(self):
        try:
            opts, args = getopt.getopt(sys.argv[1:], 'hp:n:o:')
        except getopt.GetoptError:
            self.print_help()
            return False
        # process input
        if len(opts) == 0 and len(args) != 0:  # input error
            self.print_help()
            return False
        else:
            for name, value in opts:
                if name == r'-h':
                    self.print_help()
                elif name == r'-p':
                    data = value.split(',')
                    self._path = data[0]
                    if len(data) < 3:
                        return False
                    else:
                        self._path = data[0]
                        self._name = data[1]
                        if data[2] in ['f', 'e', 'd']:
                            self._opt = data[2]
                        else:
                            return False
            return True

    def main(self):
        if not self.get_input_args():
            print('Error, -h for help!')
        else:
            count = self.get_count()
            print(count)

if __name__ == '__main__':
    pc = PathCounter()
    pc.main()
