#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Created on 2018-12-26

@author: Byng Zeng
"""

import os
import re

import gzip
import io


class File(object):

    @classmethod
    def get_fname(cls, f):
        return os.path.basename(f)

    @classmethod
    def get_exname(cls, f):
        try:
            return os.path.splitext(f)[1].lower()
        except AttributeError:
            return None

    @classmethod
    def get_filetype(cls, f):
        try:
            return os.path.splitext(f)[1][1:].lower()
        except AttributeError:
            return None

    @classmethod
    def remove_small_file(cls, path, size):
        for rt, dirs, fs in os.walk(path):
            if len(fs) != 0:
                for f in fs:
                    f = os.path.join(rt, f)
                    if os.path.getsize(f) < size:
                        os.remove(f)

    @classmethod
    def reclaim_name(cls, name, name_dict=None):
        if not name_dict:
            name_dict = {'/': '%', '\s' : '_'}
        for key, value in name_dict.items():
            name = re.sub(key, value, name)
        return name

    @classmethod
    def unzip(cls, data):
        data = io.StringIO.StringIO(data)
        gz = gzip.GzipFile(fileobj=data)
        data = gz.read()
        gz.close()
        return data
