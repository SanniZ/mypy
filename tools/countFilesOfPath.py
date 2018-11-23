#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on 2018-11-23

@author: Byng Zeng
"""

import sys, os, getopt

class countFilesOfPath(object):
    def __init__(self):
        self.path=None
        self.name=None

    def printHelp(self):
        print 'option: -p path -n .name'
        print '  path : it will find the path.'
        print '  .name: it will find .name files.'
        print ''
        print 'example: -p ~/Downloads -n .jpg'

    def getCount(self, path, ext_name):
        max=0
        for root, dirs, files in os.walk(path):
            if len(files) != 0:
                for f in files:
                    if os.path.splitext(f)[1] == '.patch':
                        max=max+1
        return max

    def getUserInput(self):
        try:
            opts, args = getopt.getopt(sys.argv[1:], 'hp:n:')
        except getopt.GetoptError:
            self.printHelp()
            return False
        # process input
        if len(opts) == 0 and len(args) != 0: # input error
            self.printHelp()
            return False
        else:
            for name, value in opts:
                if name == r'-h':
                    self.printHelp()
                elif name == r'-p':
                    self.path=value
                elif name == r'-n':
                    self.name=value
        # check args.
        if self.path == None or self.name == None:
            return False
        else:
            return True

    def main(self):
        if self.getUserInput() == False:
            self.printHelp()
        else:
            print self.getCount(self.path, self.name)

if __name__ == '__main__':
    count=countFilesOfPath()
    count.main()
