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

import gzip
import StringIO


class MyBase (object):

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
    def get_user_input(self, opts):
        result=dict()
        try:
            opts, args = getopt.getopt(sys.argv[1:], opts)
        except getopt.GetoptError:
            MyBase.print_exit('Invalid input, -h for help.')
        if not opts:
            MyBase.print_exit('Invalid input, -h for help.')
        else:
            for name, value in opts:
                result[name] = value
        return result

class MyPath(object):

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
        data = StringIO.StringIO(data)
        gz = gzip.GzipFile(fileobj=data)
        data = gz.read()
        gz.close()
        return data


class MyPrint(object):

    PR_LVL_DBG = 0x01
    PR_LVL_INFO = 0x02
    PR_LVL_WARN = 0x04
    PR_LVL_ERR = 0x08
    PR_LVL_ALL = 0x0F

    def __init__(self, tag=None, lvl= 0x02 | 0x04 | 0x08):
        self._tag = tag
        self._pr_lvl = lvl

    def pr_dbg(self, fmt):
        if all((self._pr_lvl & self.PR_LVL_DBG, fmt)):
            if self._tag:
                print('[%s] %s' % (self._tag, fmt))
            else:
                print('%s' % (fmt))

    def pr_info(self, fmt):
        if all((self._pr_lvl & self.PR_LVL_INFO , fmt)):
            if self._tag:
                print('[%s] %s' % (self._tag, fmt))
            else:
                print('%s' % (fmt))

    def pr_warn(self, fmt):
        if all((self._pr_lvl & self.PR_LVL_WARN , fmt)):
            if self._tag:
                print('[%s] %s' % (self._tag, fmt))
            else:
                print('%s' % (fmt))


    def pr_err(self, fmt):
        if all((self._pr_lvl & self.PR_LVL_ERR , fmt)):
            if self._tag:
                print('[%s] %s' % (self._tag, fmt))
            else:
                print('%s' % (fmt))

    def set_pr_level(self, val):
        self._pr_lvl = val

    def get_pr_level(self):
        return self._pr_lvl

class MyPy(object):

    @classmethod
    def find(cls, path, wd, ftype=None):
        result = dict()
        fs = None
        pattern = re.compile('%s' % wd, re.I)
        # check files now
        if MyPath.path_is_file(path):
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
                            if MyFile.get_filetype(f) != ftype:
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
        if MyPath.path_is_file(path):
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
                            if MyFile.get_filetype(f) != ftype:
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
        'options: -f path,wd[,ftype] -s path,wd,newd[,ftype]',
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

    pr = MyPrint('MyPy')

    args = MyBase.get_user_input('hf:s:')
    if '-h' in args:
        MyBase.print_help(HELP_MENU)
    if '-f' in args:
        values = args['-f'].split(',')
        n = len(values)
        if n < 2:
            MyBase.print_exit('input error, -h for help')
        elif any((not values[0], not values[1])):
            MyBase.print_exit('input error, -h for help')
        # get args.
        path = MyPath.get_abs_path(values[0])
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
            MyBase.print_exit('input error, -h for help')
        elif any((not values[0], not values[1])):
            MyBase.print_exit('input error, -h for help')
        path = MyPath.get_abs_path(values[0])
        wd = values[1]
        newd = values[2]
        if n == 3:
            MyPy.sub(path, wd, newd)
        elif n > 3:
            ftype = values[3]
            MyPy.sub(path, wd, newd, ftype)