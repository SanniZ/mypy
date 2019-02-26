#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 2018-02-19

@author: Byng.Zeng
"""

from mypy.pybase import print_help
from mypy.pyprint import PyPrint
from mypy.pydecorator import get_input

VERSION = '1.0.0'


HELP_MENU = [
    '==================================',
    '    Template menu',
    '==================================',
    'option:',
    '  -x xxx: xxxx',
]

pr = PyPrint('Template')

opts = 'hx:'


def xxx_func(values):
    print('xxx_func: values=%s' % values)


@get_input()
def get_input(opt, args=None):
    return args


def run(args):
    if '-h' in args:
        print_help(HELP_MENU)
    if '-x' in args:
        xxx_func(args['-x'])
    return args


def main(args=None):
    if not args:
        args = get_input(opts)
    run(args)

if __name__ == '__main__':
    main()
