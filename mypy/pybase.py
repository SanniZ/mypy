#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 2018-12-26

@author: Byng Zeng
"""

import os
import sys
import getopt

import inspect


VERSION = '2.0.1'


############################################################################
#               pybase functions
############################################################################

# print msg and exit
def print_exit(msg=None, exit_=True):
    print(msg) if msg else None
    exit() if exit_ else None


def print_help(help_menu, exit_=True):
    for menu in help_menu:
        print(menu)
    print_exit(exit_=exit_)


def get_user_input(opts, err_exit=True):
    result = dict()
    try:
        opts, args = getopt.getopt(sys.argv[1:], opts)
    except getopt.GetoptError as e:
        print_exit('%s, -h for help.' % str(e), err_exit)
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


def quote(msg, symbol='\''):
    return symbol + msg + symbol


def align_length(text, length):
    n = len(text) % length
    if n:
        text += '\0' * (length - n)
    return text


def get_funcname():
    return inspect.stack()[1][3]


############################################################################
#               PyBase class
############################################################################

class PyBase (object):

    DEFAULT_DWN_PATH = '%s/Downloads' % os.getenv('HOME')

    @classmethod
    def print_help(cls, help_menu, _exit=True):
        return print_help(help_menu, _exit)

    # print msg and exit
    @classmethod
    def print_exit(cls, msg=None):
        return print_exit(msg)

    @classmethod
    def get_user_input(cls, opts):
        return get_user_input(opts)

    @classmethod
    def get_args_dict(cls, args, symbol=[':']):
        return get_args_dict(args, symbol)

    @classmethod
    def quote(cls, msg, symbol='\''):
        return quote(msg, symbol)

    @classmethod
    def align_length(cls, text, length):
        return align_length(text, length)
