#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 2018-02-19

@author: Byng.Zeng
"""

from pybase.pysys import print_help
from pybase.pyprint import PyPrint
from pybase.pydecorator import get_input_args

VERSION = '1.0.0'
AUTHOR = 'Byng.Zeng'


HELP_MENU = [
    '==================================',
    '    Template - %s' % VERSION,
    '',
    '    @Author: %s' % AUTHOR,
    '    Copyright (c) %s studio' % AUTHOR,
    '==================================',
    'option:',
    '  -x xxx: xxxx',
]

pr = PyPrint('Template')

OPTS = 'hx:w:q:e:'


def xxx_func(values):
    pr.pr_info('xxx_func: values=%s' % values)


@get_input_args()
def process_input(opts, args=None):
    if args:
        for k in args.keys():
            if k == '-x':
                xxx_func(args['-x'])
            elif k == '-h':
                print_help(HELP_MENU)
    return args


def main(args=None):
    args = process_input(OPTS, args=args)

if __name__ == '__main__':
    main()
