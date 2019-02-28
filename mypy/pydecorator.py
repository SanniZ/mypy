#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 2019-02-11

@author: Byng.Zeng
"""

import sys
import getopt
import subprocess


############################################################################
#               Const Vars
############################################################################

VERSION = '1.2.0'


############################################################################
#               Function definition
############################################################################

def object_valid_types(obj, types=(int, str, list, dict)):
    return obj if all((obj, isinstance(obj, types))) else None


# =========================================================
# run_shell
#
# it will run shell command.
# sample function:
# @run_shell
# def adb_power():
#     return 'adb shell input keyevent 26'
# =========================================================

def run_shell(func):
    def run_shell_warpper(*args, **kwargs):
        return subprocess.check_output(func(*args, **kwargs), shell=True)
    return run_shell_warpper


############################################################################
#             Decorator definition
############################################################################

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
        kw = {}
        try:
            opts, args = getopt.getopt(sys.argv[1:], opts)
        except getopt.GetoptError as e:
            print('%s, -h for help.' % str(e))
            return None
        if opts:
            for name, value in opts:
                kw[name] = value
        return kw

    def get_input_decorator(func):
        def get_input_wrapper(*args, **kwargs):
            opts = None
            if kwargs:
                if 'args' in kwargs:
                    if isinstance(kwargs['args'], dict):
                        return func(*args, **kwargs)
                if 'opts' in kwargs:
                    opts = kwargs['opts']
            if args:
                n = len(args)
                if classname:
                    if n >= 3:  # (self, opts, args)
                        if isinstance(args[2], dict):  # args is done.
                            return func(*args, **kwargs)
                        elif all((args[1], not opts)):  # set opts
                            opts = args[1]
                    elif n == 2:  # (self, opts)
                        if all((args[1], not opts)):  # set opts
                            opts = args[1]
                elif n == 2:  # (opts, args)
                    if isinstance(args[1], dict):  # args is done
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
            result = {}
            key = None
            if isinstance(args, dict):
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
