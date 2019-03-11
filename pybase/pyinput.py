#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 2018-12-26

@author: Byng Zeng
"""
import sys
import getopt

from collections import OrderedDict


VERSION = '1.1.0'


############################################################################
#               functions
############################################################################

def get_input_args(opts, ordered_args=False, err_exit=True):
    if ordered_args:
        dt = OrderedDict()
    else:
        dt = {}
    try:
        opts, args = getopt.getopt(sys.argv[1:], opts)
    except getopt.GetoptError as e:
        print('%s, -h for help.' % str(e), err_exit)
        sys.exit()
    else:
        if opts:
            for key, value in opts:
                dt[key] = value
    return dt


def get_args_dict(args, symbol=[':']):
    dt = {}
    key = None
    if type(args) == dict:
        return args
    elif args:
        lt = args.split(',')
        if lt:
            for element in lt:
                for sym in symbol:
                    data = element.split(sym)
                    n = len(data)
                    if n == 2:
                        dt[data[0]] = data[1]
                        key = data[0]
                        break
                if n == 1:
                    dt[key] = dt[key] + ', ' + element
    return dt


############################################################################
#               PySys class
############################################################################

class PyInput (object):

    @staticmethod
    def get_input_args(opts, ordered_args=False):
        return get_input_args(opts, ordered_args)

    @staticmethod
    def get_args_dict(args, symbol=[':']):
        return get_args_dict(args, symbol)
