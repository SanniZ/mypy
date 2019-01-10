#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Created on 2018-12-05

@author: Byng Zeng
"""

import re
import os
import sys
import getopt

from mypy.base import Base

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
    Base.print_exit()

def main():
    args = Base.get_user_input('h')
    if '-h' in args:
        print_help()

if __name__ == '__main__':
    main()
