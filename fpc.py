#!/usr/bin/python

# -*- coding: utf-8 -*-
"""
Created on Tue Jul  3 17:18:13 2018

@author: Byng.Zeng
"""
import sys
from BxtDevelop import BxtDevelop


class Fpc(BxtDevelop):
    url=r'ssh://xfeng8-ubuntu2.sh.intel.com:29418/manifests -b master'    
    
    def __init__(self, url):
        #print('Fpc init now.')
        super(Fpc, self).__init__()
        self._url = url
        

    def help(self, cmd=''):
        #print('Class Fpc help.')
        super(Fpc, self).help(cmd)
        

    def makeImage(self, image):
        ab = BxtDevelop.AndroidBase()
        ab.buildImage(image)
        
    def flashImage(self, image):
        ab = BxtDevelop.AndroidBase()
        ab.flashImage(image)

    def main(self, cmds):
        BxtDevelop.main(self,cmds)

# main entry
if __name__ == '__main__':
    fpc = Fpc(Fpc.url)
    fpc.main(sys.argv[1:])