#!/usr/bin/python

# -*- coding: utf-8 -*-
"""
Created on Thu Jul  5 15:18:47 2018

@author: Byng.Zeng
"""

from Broxton import Broxton

class Cwp(Broxton):
    url_acrn = r'ssh://android.intel.com/manifests -b android/o/mr1/master -m r0'
    url_sos = r'ssh://android.intel.com/h/hypervisor/manifests -b hypervisor/master'
    
    def __init__(self,url):
        super(Cwp, self).__init__(url=url)
        self._pdt = ''
        self._opt = ''
        self._out = r'pub'
        self._flashfiles = 'pub'

    def code_handler(self, cmds=''):
        for cmd in cmds.values():
            if cmd == 'init' or cmd == 'sync':
                super(Broxton, self).code_handler(cmd)
            elif cmd == 'acrn':
                self._url = self.url_acrn
            elif cmd == 'sos':
                self._url = self.url_sos
     
if __name__ == '__main__':
    cwp = Cwp(Cwp.url_sos)
    cwp.main()
