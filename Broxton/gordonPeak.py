#!/usr/bin/python

# -*- coding: utf-8 -*-
"""
Created on Thu Jul  5 14:33:36 2018

@author: Byng.Zeng
"""

from broxton import Broxton
#from debug import Debug as d

class GordonPeak(Broxton):
    url = r'ssh://android.intel.com/manifests -b android/master -m r0'
    pdt = r'gordon_peak'
    opt = r'userdebug'
    user = r'yingbin'

    def __init__(self,url, pdt, opt, user):
        super(GordonPeak, self).__init__(url=url, pdt=pdt, opt=opt, user=user)
        #d.set_debug_level('dbg,info,err')

if __name__ == '__main__':
    gp = GordonPeak(GordonPeak.url, GordonPeak.pdt, GordonPeak.opt, GordonPeak.user)
    gp.run()