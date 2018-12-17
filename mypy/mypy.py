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
    PR_LVL_ERR = 0x04
    PR_LVL_ALL = 0x07

    def __init__(self, tag=None, lvl= 0x02 | 0x04):
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
    def find(cls, wd, path, mode='word'):
        result = dict()
        fs = None
        pattern = re.compile('%s' % wd)
        # check files now
        if MyPath.path_is_file(path):
            with open(path, 'r') as fd:
                data = fd.read()
            data = pattern.findall(data)
            lst = map(lambda x: x, data)
            result[path] = lst
        else:
            # check path.
            ftype = re.compile('\*\.\w+$').search(path)
            if ftype:
                ftype = ftype.group()
                path = os.path.dirname(path)
            for rt, ds, fs in os.walk(path):
                if fs:
                    for f in fs:
                        if ftype:
                            # check type of file.
                            if MyFile.get_exname(f) != ftype:
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
    def sub(cls, old, new, path):
        if MyPath.path_is_file(path):
            with open(path, 'r') as fd:
                data = fd.read()
            data = re.sub(old, new, data)
            with open(path, 'w') as fd:
                fd.write(data)
        else:
            for rt, ds, fs in os.walk(path):
                if fs:
                    for f in fs:
                        f = os.path.join(rt, f)
                        with open(f, 'r') as fd:
                            data = fd.read()
                        data = re.sub(old, new, data)
                        with open(f, 'wr') as fd:
                            fd.write(data)

if __name__ == '__main__':
    HELP_MENU = (
        '============================================',
        '    mypy help',
        '============================================',
        'options: -p path -c cmd -w word -v val',
        '  -p path:',
        '    path to dir or file',
        '  -c cmd:',
        '    find: find val in file',
        '    sub : sub val in file',
        '  -w word:',
        '    set word to find',
        '  -v val:',
        '    set word to replace for sub',
    )

    pr = MyPrint('MyPy')
    path = None
    cmd = None
    val = None
    wd = None

    args = MyBase.get_user_input('hp:c:v:w:')
    if '-h' in args:
        MyBase.print_help(HELP_MENU)
    if '-p' in args:
        path = MyPath.get_abs_path(args['-p'])
    if '-c' in args:
        cmd = args['-c']
    if '-v' in args:
        val = args['-v']
    if '-w' in args:
        wd = args['-w']
    if not path:
        path = os.getcwd()
        #mypy.print_exit('Error, -h for help!')
    # run cmd now.
    if cmd in ['find', 'sub']:
        if cmd == 'find':
            if wd:
                result = MyPy.find(wd, path)
                for key, values in result.iteritems():
                    pr.pr_info(key)
                    for val in values:
                        pr.pr_info(val)
        elif cmd == 'sub':
            if all((wd, val)):
                MyPy.sub(wd, val, path)