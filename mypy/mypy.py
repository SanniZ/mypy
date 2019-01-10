#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Created on 2018-12-04

@author: Byng Zeng
"""
import os
import re

from base import Base
from file import File
from path import Path
from pr import Print


class MyPy(object):

    @classmethod
    def find(cls, path, wd, ftype=None):
        result = dict()
        fs = None
        pattern = re.compile('%s' % wd, re.I)
        # check files now
        if Path.path_is_file(path):
            with open(path, 'r') as fd:
                data = fd.read()
            data = pattern.findall(data)
            lst = map(lambda x: x, data)
            result[path] = lst
        else:
            # check path.
            fty = re.compile('\*\.\w+$').search(path)
            if fty:
                ftype = fty.group()[2:]
                path = os.path.dirname(path)
            for rt, ds, fs in os.walk(path):
                if fs:
                    for f in fs:
                        if ftype:
                            # check type of file.
                            if File.get_filetype(f) != ftype:
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
        if Path.path_is_file(path):
            with open(path, 'r') as fd:
                data = fd.read()
            data = re.sub(wd, newd, data)
            with open(path, 'w') as fd:
                fd.write(data)
        else:
            # check path.
            fty = re.compile('\*\.\w+$').search(path)
            if fty:
                ftype = fty.group()[2:]
                path = os.path.dirname(path)
            for rt, ds, fs in os.walk(path):
                if fs:
                    for f in fs:
                        if ftype:
                            # check type of file.
                            if File.get_filetype(f) != ftype:
                                continue
                        f = os.path.join(rt, f)
                        with open(f, 'r') as fd:
                            data = fd.read()
                        data = re.sub(wd, newd, data)
                        with open(f, 'wr') as fd:
                            fd.write(data)

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
    )

    pr = Print('MyPy')

    args = Base.get_user_input('hf:s:')
    if '-h' in args:
        Base.print_help(HELP_MENU)
    if '-f' in args:
        values = args['-f'].split(',')
        n = len(values)
        if n < 2:
            Base.print_exit('input error, -h for help')
        elif any((not values[0], not values[1])):
            Base.print_exit('input error, -h for help')
        # get args.
        path = Path.get_abs_path(values[0])
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
            Base.print_exit('input error, -h for help')
        elif any((not values[0], not values[1])):
            Base.print_exit('input error, -h for help')
        path = Path.get_abs_path(values[0])
        wd = values[1]
        newd = values[2]
        if n == 3:
            MyPy.sub(path, wd, newd)
        elif n > 3:
            ftype = values[3]
            MyPy.sub(path, wd, newd, ftype)
