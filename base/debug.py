#!/usr/bin/python

# -*- coding: utf-8 -*-
"""
Created on Fri Jul  6 12:24:15 2018

@author: Byng.Zeng
"""
import re

class Debug(object):    
    BIT_DBG  = (0x01 << 0)
    BIT_INFO = (0x01 << 1)
    BIT_ERR  = (0x01 << 2)

    __PRINT_LEVEL = BIT_INFO | BIT_ERR
    
    @staticmethod
    def dbg(fmt):
        if Debug.__PRINT_LEVEL & Debug.BIT_DBG:
            print(fmt)

    @staticmethod
    def info(fmt):
        if Debug.__PRINT_LEVEL & Debug.BIT_INFO:
            print(fmt)

    @staticmethod
    def err(fmt):
        if Debug.__PRINT_LEVEL & Debug.BIT_ERR:
            print(fmt)

    @staticmethod
    def set_debug_level(level):
        t = type(level)        
        if t == int:
            Debug.__PRINT_LEVEL = level
        elif t == str:
            if re.search('dbg', level) != None:
                Debug.__PRINT_LEVEL = Debug.__PRINT_LEVEL | Debug.BIT_DBG
            else:
                Debug.__PRINT_LEVEL = Debug.__PRINT_LEVEL & (~Debug.BIT_DBG)
    
            if re.search('info', level) != None:
                Debug.__PRINT_LEVEL = Debug.__PRINT_LEVEL | Debug.BIT_INFO
            else:
                Debug.__PRINT_LEVEL = Debug.__PRINT_LEVEL & (~Debug.BIT_INFO)
                
            if re.search('err', level) != None:
                Debug.__PRINT_LEVEL = Debug.__PRINT_LEVEL | Debug.BIT_ERR
            else:
                Debug.__PRINT_LEVEL = Debug.__PRINT_LEVEL & (~Debug.BIT_ERR)
        else:
            print('set_debug_level(): invalid input!')

    @staticmethod
    def get_debug_level():
        return Debug.__PRINT_LEVEL
   
          
if __name__ == '__main__':    
    print('set level: %s' % 'dbg,info,err')
    Debug.set_debug_level('dbg,info,err')
    Debug.dbg('It is Debug dbg info')
    Debug.info('It is Debug info info')
    Debug.err('It is Debug err info')
    print('set level: %s' % 'info,err')
    Debug.set_debug_level('info,err')
    Debug.dbg('It is Debug dbg info')
    Debug.info('It is Debug info info')
    Debug.err('It is Debug err info')
    print('set level: %s' % 'err')
    Debug.set_debug_level('err')
    Debug.dbg('It is Debug dbg info')
    Debug.info('It is Debug info info')
    Debug.err('It is Debug err info')