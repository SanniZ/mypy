#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 2018-12-05

@author: Byng.Zeng
"""

from mypy.pybase import print_help
from mypy.pyprint import PyPrint
from mypy.pydecorator import get_input

VERSION = '1.0.0'


############################################################################
#               functions
############################################################################

def xxx_func(values):
    print('xxx_func: values=%s' % values)


############################################################################
#               PyPath Class
############################################################################

class Template(object):
    HELP_MENU = [
        '==================================',
        '    Template menu',
        '==================================',
        'option:',
        '  -x xxx: xxxx',
    ]

    pr = PyPrint('Template')
    opts = 'hx:'

    def __init__(self, name=None):
        self._name = name if name else self.__class__.__name__
        self._xxx = None

    @get_input('Template')
    def get_input(self, opt, args=None):
        if '-h' in args:
            print_help(self.HELP_MENU)
        if '-x' in args:
            self._xxx = args['-x']
        return args

    def run(self, args):
        if self._xxx:
            xxx_func(self._xxx)

    def main(self, args=None):
        if not args:
            args = self.get_input(self.opts)
        self.run(args)


############################################################################
#               Entrance main
############################################################################

if __name__ == '__main__':
    template = Template()
    template.main()
