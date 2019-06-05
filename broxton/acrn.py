#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul  5 14:33:36 2018

@author: Byng.Zeng
"""
import os

from broxton import Broxton
# from develop.debug import Debug as d

VERSION = '1.0.1'


class Acrn(Broxton):
    URL = r'ssh://android.intel.com/manifests -b android/o/mr1/master -m r0'
    PDT = r'gordon_peak_acrn'
    OPT = r'userdebug'
    USR = os.getenv('USER')

    def __init__(self, url=URL, pdt=PDT, opt=OPT, user=USR):
        super(Acrn, self).__init__(url=url, pdt=pdt, opt=opt, user=user)
        # d.set_debug_level('dbg,info,err')

if __name__ == '__main__':
    acrn = Acrn()
    acrn.run_sys_input()
