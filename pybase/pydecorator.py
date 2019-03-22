#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 2019-02-11

@author: Byng.Zeng
"""

import sys
import getopt
import subprocess

import inspect

from collections import OrderedDict


############################################################################
#               Const Vars
############################################################################

VERSION = '1.2.3'


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

def execute_shell(func):
    def execute_shell_warpper(*args, **kwargs):
        cmd = func(*args, **kwargs)
        try:
            result = subprocess.check_output(cmd, shell=True)
        except subprocess.CalledProcessError as e:
            return -1, str(e)
        else:
            return 0, result
    return execute_shell_warpper


############################################################################
#             Decorator definition
############################################################################

# =========================================================
# get_input
#
# it will get args from sys.argv[1:] and return kwargs at args.
# sample function:
# @get_input_args(True/False)
# def process_input([self,] opts, args=None):
#     print(args)
#
# [self.]process_input('hx:', args=args)
# =========================================================

def get_input_args(ordered_args=False):
    def __get_input_args(opts, ordered_args=False):
        if ordered_args:
            dt = OrderedDict()
        else:
            dt = {}
        try:
            opts, args = getopt.getopt(sys.argv[1:], opts)
        except getopt.GetoptError as e:
            print('%s, -h for help.' % str(e))
            return None
        if opts:
            for name, value in opts:
                dt[name] = value
        return dt

    def get_input_args_decorator(func):
        def get_input_wrapper(*args, **kwargs):
            func_args = inspect.getcallargs(func, *args, **kwargs)
            if all((func_args['args'], isinstance(func_args['args'], dict))):
                return func(*args, **kwargs)
            elif func_args['opts']:
                kwargs['args'] = __get_input_args(func_args['opts'],
                                                  ordered_args)
            return func(*args, **kwargs)
        return get_input_wrapper
    return get_input_args_decorator


# =========================================================
# get_dict_args
#
# it will return dt with dict data.
# sample function:
# @get_dict_args
# def process_args([self,] args, dt=None):
#     print(dt)
# =========================================================

def get_args_dict(symbol=[':']):
    def get_args_dict_decorator(func):
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

        def get_args_dict_warpper(*args, **kwargs):
            func_args = inspect.getcallargs(func, *args, **kwargs)
            if func_args['args']:
                kwargs['dt'] = __get_args_dict(func_args['args'])
                return func(*args, **kwargs)
            else:
                return None
        return get_args_dict_warpper
    return get_args_dict_decorator
