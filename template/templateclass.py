#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 2018-12-05

@author: Byng.Zeng
"""

from pybase.pysys import print_help
from pybase.pyprint import PyPrint
from pybase.pydecorator import get_input_args

VERSION = '1.0.0'
AUTHOR = 'Byng.Zeng'


############################################################################
#               functions
############################################################################

pr = PyPrint('TemplateClass')


def xxx_func(values):
    pr.pr_info('xxx_func: values=%s' % values)


############################################################################
#               PyPath Class
############################################################################

OPTS = 'hx:'


class TemplateClass(object):
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

    def __init__(self, name=None):
        self._name = name if name else self.__class__.__name__
        self._xxx = None

    @get_input_args()
    def process_input(self, opts, args=None):
        if args:
            for k in args.keys():
                if k == '-x':
                    xxx_func(args['-x'])
                elif k == '-h':
                    print_help(self.HELP_MENU)
        return args

    def main(self, args=None):
        args = self.process_input(OPTS, args=args)
        if self._xxx:
            xxx_func(self._xxx)


############################################################################
#               Entrance main
############################################################################

if __name__ == '__main__':
    temp = TemplateClass()
    temp.main()
