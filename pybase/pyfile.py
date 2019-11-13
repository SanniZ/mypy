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
import shutil


VERSION = '1.1.0'
AUTHOR = 'Byng.Zeng'


############################################################################
#               functions
############################################################################

def path_is_file(path):
    return os.path.isfile(path)


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


def find(path, wd=None, ftype=None):
    result = dict()
    fs = None
    pattern = re.compile('%s' % wd, re.I)
    # check files now
    if path_is_file(path):
        with open(path, 'r') as fd:
            data = fd.read()
        data = pattern.findall(data)
        lst = map(lambda x: x, data)
        result[path] = lst
    else:
        # check path
        fty = re.compile('\*\.\w+$').search(path)
        if fty:
            ftype = fty.group()[2:]
            path = os.path.dirname(path)
        for rt, ds, fs in os.walk(path):
            if fs:
                for f in fs:
                    if ftype:
                        # check type of file.
                        if get_filetype(f) != ftype:
                            continue
                    pf = os.path.join(rt, f)
                    if wd:
                        lst = list()
                        with open(pf, 'r') as fd:
                            data = fd.read()
                        data = pattern.findall(data)
                        lst = map(lambda x: x, data)
                        if lst:
                            result[pf] = lst
                    else:
                        result[f] = rt
    return result


# -v val: old
# -w word: new
def sub(path, wd, newd, ftype=None):
    if path_is_file(path):
        with open(path, 'r') as fd:
            data = fd.read()
        data = re.sub(wd, newd, data)
        with open(path, 'w') as fd:
            fd.write(data)
    else:
        # check path
        fty = re.compile('\*\.\w+$').search(path)
        if fty:
            ftype = fty.group()[2:]
            path = os.path.dirname(path)
        for rt, ds, fs in os.walk(path):
            if fs:
                for f in fs:
                    if ftype:
                        # check type of file.
                        if get_filetype(f) != ftype:
                            continue
                    f = os.path.join(rt, f)
                    with open(f, 'r') as fd:
                        data = fd.read()
                    data = re.sub(wd, newd, data)
                    with open(f, 'w') as fd:
                        fd.write(data)


def copy(src, dst):
    lfs = list()
    if os.path.isdir(src):
        for rt, ds, fs in os.walk(src):
            if fs:
                for f in fs:
                    lfs.append(os.path.join(rt, f))
    if lfs:
        for f in lfs:
            fname = os.path.basename(f)
            if not os.path.exists(dst):
                os.makedirs(dst)
            shutil.copy(f, '%s/%s' % (dst, fname))


def move(src, dst):
    lfs = list()
    if os.path.isdir(src):
        for rt, ds, fs in os.walk(src):
            if fs:
                for f in fs:
                    lfs.append(os.path.join(rt, f))
    if lfs:
        for f in lfs:
            fname = os.path.basename(f)
            if not os.path.exists(dst):
                os.makedirs(dst)
            shutil.move(f, '%s/%s' % (dst, fname))


############################################################################
#               PyFile Class
############################################################################

class PyFile(object):

    @staticmethod
    def get_fname(f):
        return get_fname(f)

    @staticmethod
    def get_name_ex(f, lower=True):
        return get_name_ex(f, lower)

    @staticmethod
    def get_filetype(f, lower=True):
        return get_filetype(f, lower)

    @staticmethod
    def remove_small_file(path, size):
        return remove_small_file(path, size)

    @staticmethod
    def reclaim_name(name, name_dict=None):
        return reclaim_name(name, name_dict)

    @staticmethod
    def unzip(data):
        return unzip(data)

    @staticmethod
    def find(path, wd, ftype=None):
        return find(path, wd, ftype)

    # -v val: old
    # -w word: new
    @staticmethod
    def sub(path, wd, newd, ftype=None):
        return sub(path, wd, newd, ftype)

    @staticmethod
    def copy(src, dst):
        return copy(src, dst)

    @staticmethod
    def move(src, dst):
        return move(src, dst)

if __name__ == '__main__':
    from pybase.pysys import print_help, print_exit
    from pybase.pyinput import get_input_args
    from pybase.pypath import get_abs_path
    from pybase.pyprint import PyPrint

    HELP_MENU = (
        '============================================',
        '    PyFile  - %s' % VERSION,
        '',
        '    @Author: %s' % AUTHOR,
        '    Copyright (c) %s studio' % AUTHOR,
        '============================================',
        'options:',
        '  -r path,size: remove small size of images',
        '    path  : path of dir or file',
        '    size : min of size',
        '  -f path,wd,ftype: find wd in path',
        '    path : path to dir or file',
        '    wd   : word will be find',
        '    ftype: file type will be find',
        '  -s path,wd,newd,ftype: sub wd with newd in path',
        '    path : path to dir or file',
        '    wd   : word will be find',
        '    newd : new word to replace wd',
        '    ftype: file type, example: txt',
        '  -c src,dst: copy files',
        '    src: path of source files.',
        '    dst: path to copy files',
        '  -m src,dst: move files',
        '    src: path of source files.',
        '    dst: path to copy files',
    )

    pr = PyPrint('PyFile')
    args = get_input_args('hr:f:s:c:m:', True)
    for k in args.keys():
        if k == '-r':
            remove_small_file(args['-r'])
        elif k == '-f':
            values = args['-f'].split(',')
            n = len(values)
            if n < 2:
                print_exit('input error, -h for help')
            elif any((not values[0], not values[1])):
                print_exit('input error, -h for help')
            # get args.
            path = get_abs_path(values[0])
            wd = values[1]
            if n == 2:
                result = find(path, wd)
            elif n > 2:
                ftype = values[2]
                result = find(path, wd, ftype)
            # print result
            for key, values in result.iteritems():
                pr.pr_info(key)
                for val in values:
                    pr.pr_info(val)
        elif k == '-s':
            values = args['-s'].split(',')
            n = len(values)
            if n < 3:
                print_exit('input error, -h for help')
            elif any((not values[0], not values[1])):
                print_exit('input error, -h for help')
            path = get_abs_path(values[0])
            wd = values[1]
            newd = values[2]
            if n == 3:
                sub(path, wd, newd)
            elif n > 3:
                ftype = values[3]
                sub(path, wd, newd, ftype)
        elif k == '-c':
            values = args['-c'].split(',')
            n = len(values)
            src = dst = None
            if n >= 2:
                src = get_abs_path(values[0])
                dst = get_abs_path(values[1])
            if all((src, dst)):
                copy(src, dst)

        elif k == '-m':
            values = args['-m'].split(',')
            n = len(values)
            src = dst = None
            if n >= 2:
                src = get_abs_path(values[0])
                dst = get_abs_path(values[1])
            if all((src, dst)):
                move(src, dst)
        elif k == '-h':
            print_help(HELP_MENU)
