#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on 2018-12-04

@author: Byng Zeng
"""

import os
import sys
import getopt

class MyBase (object):

    @classmethod
    # print msg and exit
    def print_exit(cls, msg=None):
        if msg:
            print msg
        # stop runing and exit.
        exit()

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
    def remove_small_file(cls, path, size):
        for rt, dirs, fs in os.walk(path):
            if len(fs) != 0:
                for f in fs:
                    f = os.path.join(rt, f)
                    if os.path.getsize(f) < size:
                        os.remove(f)

    @classmethod
    def remove_blank_dir(cls, path, level=4):
        for i in range(level):
            for rt, dr, fs in os.walk(path):
                if len(dr) == 0 and len(fs) == 0:
                    os.rmdir(rt)

    @classmethod
    def get_user_input(self, opts):
        result=None
        try:
            opts, args = getopt.getopt(sys.argv[1:], opts)
        except getopt.GetoptError:
            MyBase.print_exit('Invalid input, -h for help.')
        # get input
        if len(opts) == 0:
            MyBase.print_exit('Invalid input, -h for help.')
        else:
            for name, value in opts:
                # create dict.
                if result == None:
                    result = dict()
                # add new value to dict
                result[name] = value
        # return result.
        return result

