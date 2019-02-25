#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 2018-12-26

@author: Byng Zeng
"""

import os
import sys
import getopt

VERSION = '2.0.0'


############################################################################
#               pybase functions
############################################################################

def print_help(help_menu, _exit=True):
    for help in help_menu:
        print(help)
    if _exit:
        exit()


# print msg and exit
def print_exit(msg=None):
    if msg:
        print(msg)
    exit()


def get_user_input(opts):
    result = dict()
    try:
        opts, args = getopt.getopt(sys.argv[1:], opts)
    except getopt.GetoptError as e:
        print_exit('%s, -h for help.' % str(e))
    if not opts:
        print_exit('invalid input, -h for help.')
    else:
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
