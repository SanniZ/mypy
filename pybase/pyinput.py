#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 2018-12-26

@author: Byng Zeng
"""
import sys
import getopt


VERSION = '1.0.1'


############################################################################
#               functions
############################################################################

def get_user_input(opts, err_exit=True):
    result = dict()
    try:
        opts, args = getopt.getopt(sys.argv[1:], opts)
    except getopt.GetoptError as e:
        print('%s, -h for help.' % str(e), err_exit)
        sys.exit()
    else:
        if opts:
            for name, value in opts:
                result[name] = value
    return result


def get_args_dict(args, symbol=[':']):
    result = dict()
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
                        result[data[0]] = data[1]
                        key = data[0]
                        break
                if n == 1:
                    result[key] = result[key] + ', ' + element
    return result


############################################################################
#               PySys class
############################################################################

class PyInput (object):

    @staticmethod
    def get_user_input(opts):
        return get_user_input(opts)

    @staticmethod
    def get_args_dict(args, symbol=[':']):
        return get_args_dict(args, symbol)
