#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 2018-12-26

@author: Byng Zeng
"""

import os
import re

VERSION = '1.1.0'

DEFAULT_DWN_PATH = '%s/Downloads' % os.getenv('HOME')


############################################################################
#               functions
############################################################################

def path_is_file(path):
    return os.path.isfile(path)


def make_path(path):
    if not os.path.exists(path):
        os.makedirs(path)


def get_mypy_path():
    return os.getenv('MYPY')


def get_home_path():
    return os.getenv('HOME')


def get_download_path():
    return '%s/Downloads' % os.getenv('HOME')


def get_abs_path(path):
    path = re.sub('~', os.getenv('HOME'), path)
    return os.path.abspath(path)


def get_current_path():
    return os.getcwd()


def remove_blank_dir(path, level=4):
    for i in range(level):
        for rt, dr, fs in os.walk(path):
            if len(dr) == 0 and len(fs) == 0:
                os.rmdir(rt)


def recliam_path(path, start=False, end=True):
    if start:
        if path[0] == '/':
            path = path[1:]
    if end:
        if path[-1] == '/':
            path = path[:len(path) - 1]
    return path


############################################################################
#               PyPath Class
############################################################################

class PyPath(object):

    @staticmethod
    def path_is_file(path):
        return path_is_file(path)

    @staticmethod
    def make_path(path):
        return make_path(path)

    @staticmethod
    def get_mypy_path():
        return get_mypy_path()

    @staticmethod
    def get_home_path():
        return get_home_path()

    @staticmethod
    def get_download_path():
        return get_download_path()

    @staticmethod
    def get_abs_path(path):
        return get_abs_path(path)

    @staticmethod
    def get_current_path():
        return get_current_path()

    @staticmethod
    def remove_blank_dir(path, level=4):
        return remove_blank_dir(path, level)

    @staticmethod
    def recliam_path(path, start=False, end=True):
        return recliam_path(path, start, end)
