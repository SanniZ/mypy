#!/usr/bin/python

# -*- coding: utf-8 -*-
"""
Created on Thu Jul  5 14:33:36 2018

@author: Byng.Zeng
"""

from Broxton import Broxton

class Fpc(Broxton):
    url = 'ssh://xfeng8-ubuntu2.sh.intel.com:29418/manifests -b master'

    def __init__(self,url, user):
        super(Fpc, self).__init__(url=url, user=user)
        
if __name__ == '__main__':
    fpc = Fpc(Fpc.url, 'yingbin')
    fpc.main()
