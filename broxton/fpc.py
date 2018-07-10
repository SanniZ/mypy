#!/usr/bin/python

# -*- coding: utf-8 -*-
"""
Created on Thu Jul  5 14:33:36 2018

@author: Byng.Zeng
"""

from broxton import Broxton
#from Debug import Debug

class Fpc(Broxton):
    URL = 'ssh://xfeng8-ubuntu2.sh.intel.com:29418/manifests -b master'
    PDT = 'gordon_peak'
    OPT = 'userdebug'
    USR = 'yingbin'

    def __init__(self,url=URL, pdt=PDT, opt=OPT, user=USR):
        super(Fpc, self).__init__(url=url, pdt=pdt, opt=opt, user=user)
        #self.set_debug_level('dbg,info,err')

if __name__ == '__main__':
    fpc = Fpc()
    fpc.run()