#!/usr/bin/python

# -*- coding: utf-8 -*-
"""
Created on Fri Jul  6 12:24:15 2018

@author: Byng.Zeng
"""
import re

class Debug(object):
    __print_level = 'info,err'
    
    @staticmethod
    def dbg(fmt):
        if re.search('dbg', Debug.__print_level) != None:
            print(fmt)

    @staticmethod
    def info(fmt):
        if re.search('info', Debug.__print_level) != None:
            print(fmt)

    @staticmethod
    def err(fmt):
        if re.search('err', Debug.__print_level) != None:
            print(fmt)

    @staticmethod
    def set_debug_level(level):
        Debug.__print_level = level

    @staticmethod
    def get_debug_level():
        return Debug.__print_level
   
          
if __name__ == '__main__':
    Debug.info('It is class test')
    Debug.dbg('It is classs dbg info')
    Debug.info('It is class info info')