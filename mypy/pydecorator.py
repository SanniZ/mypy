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
# sample function:
# @get_input
# def get_input_func([self,] opt, args=None):
#     return args
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
            if 'args' in kwargs:
                if type(kwargs['args']) == dict:
                    return func(*args, **kwargs)
            if 'opts' in kwargs:
                opts = kwargs['opts']
        if args:
            n = len(args)
            if all((args[0],  # class function
                    not isinstance(args[0], (float, int, str, list, dict)))):
                if n >= 3:  # (self, opts, args)
                    if type(args[2]) == dict:  # args is done.
                        return func(*args, **kwargs)
                    elif all((args[1], not opts)):  # set opts
                        opts = args[1]
                elif n == 2:  # (self, opts)
                    if all((args[1], not opts)):  # set opts
                        opts = args[1]
            elif n == 2:  # (opts, args)
                if type(args[1]) == dict:  # args is done
                    return func(*args, **kwargs)
                elif all((args[0], not opts)):  # set opts
                    opts = args[0]
            elif n == 1:  # (opts)
                if all((args[0], not opts)):  # set opts
                    opts = args[0]
            else:
                return None
        if opts:
            kwargs['args'] = __get_user_input(opts)
        return func(*args, **kwargs)
    return get_input_wrapper
