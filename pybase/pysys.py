#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 2018-12-26

@author: Byng Zeng
"""

import sys
import subprocess

import inspect


VERSION = '1.0.1'
AUTHOR = 'Byng.Zeng'


############################################################################
#               pybase functions
############################################################################

# print msg and exit
def print_exit(msg=None, exit_=True):
    print(msg) if msg else None
    sys.exit() if exit_ else None


def print_help(help_menu, exit_=True):
    for menu in help_menu:
        print(menu)
    print_exit(exit_=exit_)


def quote(msg, symbol='\''):
    return symbol + msg + symbol


def align_length(text, length):
    n = len(text) % length
    if n:
        text += '\0' * (length - n)
    return text


def get_funcname():
    return inspect.stack()[1][3]


def bytes2str(data):
    return str(data, 'utf-8')


def execute_shell(cmd):
    try:
        result = subprocess.check_output(cmd, shell=True)
    except subprocess.CalledProcessError as e:
        return -1, str(e)
    else:
        return 0, result


############################################################################
#               PySys class
############################################################################

class PySys (object):

    @staticmethod
    def print_help(help_menu, exit_=True):
        return print_help(help_menu, exit_)

    # print msg and exit
    @staticmethod
    def print_exit(msg=None):
        return print_exit(msg)

    @staticmethod
    def quote(msg, symbol='\''):
        return quote(msg, symbol)

    @staticmethod
    def align_length(text, length):
        return align_length(text, length)

    @staticmethod
    def execute_shell(cmd):
        return execute_shell(cmd)
