#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 2018-12-26

@author: Byng Zeng
"""

import os
import re

import gzip
import io


############################################################################
#               functions
############################################################################

def get_fname(f):
    return os.path.basename(f)


def get_name_ex(f, lower=True):
    try:
        name_ex = os.path.splitext(f)[1]
        if lower:
            name_ex = name_ex.lower()
        return name_ex
    except AttributeError:
        return None


def get_filetype(f, lower=True):
    try:
        ftype = os.path.splitext(f)[1][1:]
        if lower:
            ftype = ftype.lower()
        return ftype
    except AttributeError:
        return None


def remove_small_file(path, size):
    for rt, dirs, fs in os.walk(path):
        if len(fs) != 0:
            for f in fs:
                f = os.path.join(rt, f)
                if os.path.getsize(f) < size:
                    os.remove(f)


def reclaim_name(name, name_dict=None):
    if not name_dict:
        name_dict = {'/': '%', '\s': '_'}
    for key, value in name_dict.items():
        name = re.sub(key, value, name)
    return name


def unzip(data):
    data = io.StringIO.StringIO(data)
    gz = gzip.GzipFile(fileobj=data)
    data = gz.read()
    gz.close()
    return data


############################################################################
#               PyFile Class
############################################################################

class PyFile(object):

    @classmethod
    def get_fname(cls, f):
        return get_fname(f)

    @classmethod
    def get_name_ex(cls, f, lower=True):
        return get_name_ex(f, lower)

    @classmethod
    def get_filetype(cls, f, lower=True):
        return get_filetype(f, lower)

    @classmethod
    def remove_small_file(cls, path, size):
        return remove_small_file(path, size)

    @classmethod
    def reclaim_name(cls, name, name_dict=None):
        return reclaim_name(name, name_dict)

    @classmethod
    def unzip(cls, data):
        return unzip(data)


if __name__ == '__main__':
    from pybase import PyBase

    HELP_MENU = (
        '============================================',
        '    File help',
        '============================================',
        'options:',
        '  -r path,size: remove small size of images',
        '    path  : path of dir or file',
        '    size : min of size',
    )

    args = PyBase.get_user_input('hr:')
    if '-h' in args:
        PyBase.print_help(HELP_MENU)
    if '-r' in args:
        PyFile.remove_small_file(args['-r'])
