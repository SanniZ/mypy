#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 2019-02-11

@author: Byng.Zeng
"""

import sys
import getopt


VERSION = '1.2.0'


# =========================================================
# get_input
#
# it will get args from sys.argv[1:] and return kwargs at args.
# sample function:
# @get_input
# def process_input([self,] opts, args=None):
#     print(args)
#
# [self.]process_input(opts='hx:', args=args)
# =========================================================

def get_input(classname=None):
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

    def get_input_decorator(func):
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
                if classname:
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
    return get_input_decorator


# =========================================================
# get_dict_args
#
# it will return dt with dict data.
# sample function:
# @get_dict_args
# def xxx([self,] args, dt=None):
#     print(dt)
# =========================================================

def get_dict_args(classname=None, symbol=[':']):
    def get_dict_args_decorator(func):
        def __get_args_dict(args):
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

        def get_dict_args_warpper(*args, **kwargs):
            args_ = None
            if kwargs:
                if 'args' in kwargs:
                    args_ = kwargs['args']
            elif all((classname, len(args) >= 2)):
                args_ = args[1]
            else:
                args_ = args[0]
            kwargs['dt'] = __get_args_dict(args_)
            return func(*args, **kwargs)
        return get_dict_args_warpper
    return get_dict_args_decorator
