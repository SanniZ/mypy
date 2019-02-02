#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Created on 2018-12-04

@author: Byng Zeng
"""
import os
import re
import shutil

from pybase import PyBase
from pyfile import PyFile
from pypath import PyPath
from pypr import PyPrint


class MyPy(object):

    @classmethod
    def find(cls, path, wd, ftype=None):
        result = dict()
        fs = None
        pattern = re.compile('%s' % wd, re.I)
        # check files now
        if PyPath.path_is_file(path):
            with open(path, 'r') as fd:
                data = fd.read()
            data = pattern.findall(data)
            lst = map(lambda x: x, data)
            result[path] = lst
        else:
            # check PyPath.
            fty = re.compile('\*\.\w+$').search(path)
            if fty:
                ftype = fty.group()[2:]
                path = os.path.dirname(path)
            for rt, ds, fs in os.walk(path):
                if fs:
                    for f in fs:
                        if ftype:
                            # check type of PyFile.
                            if PyFile.get_filetype(f) != ftype:
                                continue
                        f = os.path.join(rt, f)
                        lst = list()
                        with open(f, 'r') as fd:
                            data = fd.read()
                        data = pattern.findall(data)
                        lst = map(lambda x: x, data)
                        if lst:
                            result[f] = lst
        return result

    # -v val: old
    # -w word: new
    @classmethod
    def sub(cls, path, wd, newd, ftype=None):
        if PyPath.path_is_file(path):
            with open(path, 'r') as fd:
                data = fd.read()
            data = re.sub(wd, newd, data)
            with open(path, 'w') as fd:
                fd.write(data)
        else:
            # check PyPath.
            fty = re.compile('\*\.\w+$').search(path)
            if fty:
                ftype = fty.group()[2:]
                path = os.path.dirname(path)
            for rt, ds, fs in os.walk(path):
                if fs:
                    for f in fs:
                        if ftype:
                            # check type of PyFile.
                            if PyFile.get_filetype(f) != ftype:
                                continue
                        f = os.path.join(rt, f)
                        with open(f, 'r') as fd:
                            data = fd.read()
                        data = re.sub(wd, newd, data)
                        with open(f, 'wr') as fd:
                            fd.write(data)

    @classmethod
    def copy(cls, src, dst):
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

    @classmethod
    def move(cls, src, dst):
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

if __name__ == '__main__':
    HELP_MENU = (
        '============================================',
        '    mypy help',
        '============================================',
        'options:',
        '  -f path,wd,ftype: find wd in path',
        '    path : path to dir or file',
        '    wd   : word will be find',
        '    ftype: file type will be find',
        '  -s path,wd,ftype: sub wd with newd in path',
        '    path : path to dir or file',
        '    wd   : word will be find',
        '    newd : new word to replace wd',
        '    ftype: file type will be find',
        '  -c src,dst: copy files',
        '    src: path of source files.',
        '    dst: path to copy files',
        '  -m src,dst: move files',
        '    src: path of source files.',
        '    dst: path to copy files',
    )

    pr = PyPrint('MyPy')

    args = PyBase.get_user_input('hf:s:c:m:')
    if '-h' in args:
        PyBase.print_help(HELP_MENU)
    if '-f' in args:
        values = args['-f'].split(',')
        n = len(values)
        if n < 2:
            PyBase.print_exit('input error, -h for help')
        elif any((not values[0], not values[1])):
            PyBase.print_exit('input error, -h for help')
        # get args.
        path = PyPath.get_abs_path(values[0])
        wd = values[1]
        if n == 2:
            result = MyPy.find(path, wd)
        elif n > 2:
            ftype = values[2]
            result = MyPy.find(path, wd, ftype)
        # print result
        for key, values in result.iteritems():
            pr.pr_info(key)
            for val in values:
                pr.pr_info(val)
    if '-s' in args:
        values = args['-s'].split(',')
        n = len(values)
        if n < 3:
            PyBase.print_exit('input error, -h for help')
        elif any((not values[0], not values[1])):
            PyBase.print_exit('input error, -h for help')
        path = PyPath.get_abs_path(values[0])
        wd = values[1]
        newd = values[2]
        if n == 3:
            MyPy.sub(path, wd, newd)
        elif n > 3:
            ftype = values[3]
            MyPy.sub(path, wd, newd, ftype)
    if '-c' in args:
        values = args['-c'].split(',')
        n = len(values)
        src = dst = None
        if n >= 2:
            src = PyPath.get_abs_path(values[0])
            dst = PyPath.get_abs_path(values[1])
        if all((src, dst)):
            MyPy.copy(src, dst)

    if '-m' in args:
        values = args['-m'].split(',')
        n = len(values)
        src = dst = None
        if n >= 2:
            src = PyPath.get_abs_path(values[0])
            dst = PyPath.get_abs_path(values[1])
        if all((src, dst)):
            MyPy.move(src, dst)
