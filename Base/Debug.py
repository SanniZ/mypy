# -*- coding: utf-8 -*-
"""
Created on Fri Jul  6 12:24:15 2018

@author: Byng.Zeng
"""
import re

class Debug(object):
    def __init__(self, level='info,err'):
        self._debug = level    
    
    def help(self, cmds=''):
        pass

    def dbg(self, fmt):
        if re.search('dbg', self._debug) != None:
            print(fmt)
            
    def info(self, fmt):
        if re.search('info', self._debug) != None:
            print(fmt)

    def err(self, fmt):
        if re.search('err', self._debug) != None:
            print(fmt)
            
    def set_debug_level(self, val):
        self._debug = val
        
    def get_debug_level(self):
        return self._debug
            
if __name__ == '__main__':
    dbg = Debug()
    dbg.dbg('It is dbg info')
    dbg.info('It is info info')
    dbg.err('It is err info')