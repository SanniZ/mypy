#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on 2018-12-04

@author: Byng Zeng
"""

import os
import sys
import re
import getopt

class MyBase (object):

    @classmethod
    def print_help(cls, help_menu, _exit=True):
        for help in help_menu:
            print(help)
        if _exit:
            exit()

    @classmethod
    # print msg and exit
    def print_exit(cls, msg=None):
        if msg:
            print msg
        # stop runing and exit.
        exit()

    @classmethod
    def get_user_input(self, opts):
        result=dict()
        try:
            opts, args = getopt.getopt(sys.argv[1:], opts)
        except getopt.GetoptError:
            MyBase.print_exit('Invalid input, -h for help.')
        # get input
        if len(opts) == 0:
            MyBase.print_exit('Invalid input, -h for help.')
        else:
            for name, value in opts:
                # add new value to dict
                result[name] = value
        # return result.
        return result

class MyPath(object):

    @classmethod
    def make_path(cls, path):
        if not os.path.exists(path):
            os.makedirs(path)

    @classmethod
    def get_mypy_path(cls):
        return os.getenv('MYPY')

    @classmethod
    def get_home_path(cls):
        return os.getenv('HOME')

    @classmethod
    def get_abs_path(cls, path):
        return os.path.abspath(path)

    @classmethod
    def get_current_path(cls):
        return os.getcwd()

    @classmethod
    def remove_blank_dir(cls, path, level=4):
        for i in range(level):
            for rt, dr, fs in os.walk(path):
                if len(dr) == 0 and len(fs) == 0:
                    os.rmdir(rt)

class MyFile(object):

    @classmethod
    def get_exname(cls, f):
        return os.path.splitext(f)[1].lower()

    @classmethod
    def get_fname(cls, f):
        return os.path.basename(f)

    @classmethod
    def get_filetype(cls, f):
        return os.path.splitext(f)[1][1:].lower()

    @classmethod
    def remove_small_file(cls, path, size):
        for rt, dirs, fs in os.walk(path):
            if len(fs) != 0:
                for f in fs:
                    f = os.path.join(rt, f)
                    if os.path.getsize(f) < size:
                        os.remove(f)

