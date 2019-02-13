#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 2018-12-05

@author: Byng Zeng
"""

# import re
# import os
# import sys
# import getopt

from mypy.pybase import PyBase


def print_help():
    help_menu = (
        '==================================',
        '    help menu',
        '==================================',
        'option: -x xxx',
        '  -x xxx: xxxx',
    )
    # print
    for txt in help_menu:
        print(txt)
    PyBase.print_exit()


def main():
    args = PyBase.get_user_input('h')
    if '-h' in args:
        print_help()


if __name__ == '__main__':
    main()
