#!/usr/bin/python

# -*- coding: utf-8 -*-
"""
Created on Thu Jul  5 14:33:36 2018

@author: Byng.Zeng
"""

from broxton import Broxton
from debug import Debug as d

class Fpc(Broxton):
    URL = 'ssh://xfeng8-ubuntu2.sh.intel.com:29418/manifests -b master'
    PDT = 'gordon_peak'
    OPT = 'userdebug'
    USR = 'yingbin'

    def __init__(self,url=URL, pdt=PDT, opt=OPT, user=USR):
        super(Fpc, self).__init__(url=url, pdt=pdt, opt=opt, user=user)

    def help(self, cmds):
        super(Fpc, self).help(cmds)
        for cmd in cmds:
            if cmd == 'help':
                d.info('make:mmm,ftest')
                d.info('  build fingerprint test binary')

    def make_image(self, images):
        for i in range(len(images)):
            if images[i] == 'mmm' and images[i + 1] == 'ftest':
                images[i + 1] = r'vendor/intel/hardware/fingerprint/fingerprint_tac/normal'

        super(Fpc, self).make_image(images)

if __name__ == '__main__':
    fpc = Fpc()
    fpc.run()