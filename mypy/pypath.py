#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 2018-12-26

@author: Byng Zeng
"""

import os
import re


class PyPath(object):

    @classmethod
    def path_is_file(self, path):
        return os.path.isfile(path)

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
    def get_download_path(cls):
        return '%s/Downloads' % os.getenv('HOME')

    @classmethod
    def get_abs_path(cls, path):
        path = re.sub('~', os.getenv('HOME'), path)
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

    @classmethod
    def recliam_path(cls, path, start=False, end=True):
        if start:
            if path[0] == '/':
                path = path[1:]
        if end:
            if path[-1] == '/':
                path = path[:len(path) - 1]
        return path
