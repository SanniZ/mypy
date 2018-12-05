#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on 2018-12-05

@author: Byng Zeng
"""

import re
import os
import sys
import getopt

from base import MyBase as Base


class Template(object):

    @classmethod
    def print_help(cls):
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

    def main(self):
        args = Base.get_user_input('h')
        if '-h' in args:
            self.print_help()

if __name__ == '__main__':
    template = Template()
    template.main()
