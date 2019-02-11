#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Created on 2019-02-11

@author: Byng.Zeng
"""

import sys
import getopt


# =========================================================
# get_input
#
# it will get args from sys.argv[1:] and return kwargs.
# input : [self,] opts
# output: kwargs
# =========================================================
def get_input(func):
    def __get_user_input(opts):
        kw = None
        try:
            opts, args = getopt.getopt(sys.argv[1:], opts)
        except getopt.GetoptError as e:
            print('%s, -h for help.' % str(e))
            return None
        if opts:
            kw = dict()
            for name, value in opts:
                kw[name] = value
        return kw

    def get_input_wrapper(*args, **kwargs):
        opts = None
        if kwargs:
            if 'opts' in kwargs:
                opts = kwargs['opts']
        if args:
            # check args[0] for class function.
            if not isinstance(args[0], (float, int, str, list, dict)):
                if all((len(args) >= 2, not opts)):
                    opts = args[1]
            elif not opts:
                    opts = args[0]
        if opts:
            kwargs['args'] = __get_user_input(opts)
        return func(*args, **kwargs)
    return get_input_wrapper
