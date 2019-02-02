#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Created on 2018-12-26

@author: Byng Zeng
"""

import os
import sys
import getopt


class PyBase (object):

    DEFAULT_DWN_PATH = '%s/Downloads' % os.getenv('HOME')

    @classmethod
    def print_help(cls, help_menu, _exit=True):
        for help in help_menu:
            print(help)
        if _exit:
            exit()

    # print msg and exit
    @classmethod
    def print_exit(cls, msg=None):
        if msg:
            print(msg)
        exit()

    @classmethod
    def get_user_input(cls, opts):
        result = dict()
        try:
            opts, args = getopt.getopt(sys.argv[1:], opts)
        except getopt.GetoptError as e:
            cls.print_exit('%s, -h for help.' % str(e))
        if not opts:
            cls.print_exit('invalid input, -h for help.')
        else:
            for name, value in opts:
                result[name] = value
        return result
