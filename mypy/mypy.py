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

    PATH_DWN=os.getenv('DWN')

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
    def get_exname(cls, f):
        return os.path.splitext(f)[1].lower()

    @classmethod
    def get_fname(cls, f):
        return os.path.basename(f)

    @classmethod
    def get_filetype(cls, f):
        return os.path.splitext(f)[1][1:].lower()

    @classmethod
    def remove_small_file(cls, path, size):
        for rt, dirs, fs in os.walk(path):
            if len(fs) != 0:
                for f in fs:
                    f = os.path.join(rt, f)
                    if os.path.getsize(f) < size:
                        os.remove(f)


    @classmethod
    def unzip(cls, data):
        data = StringIO.StringIO(data)
        gz = gzip.GzipFile(fileobj=data)
        data = gz.read()
        gz.close()
        return data

class MyPy(MyBase, MyPath, MyFile):

    help_menu = (
        '============================================',
        '    mypy help',
        '============================================',
        'options: -f file -c cmd -v val -w word',
        '  -f file:',
        '    set file to be process',
        '  -c cmd:',
        '    find: find val in file',
        '  -v val:',
        '    set value for cmd',
        '  -w word:',
        '    set word to find',
    )

    def __init__(self):
        super(MyPy, self).__init__()
        self._fs = None
        self._cmd = None
        self._val = None
        self._wd = None
        self.__handlers = {
            'find' : self.find,
            'sub' : self.sub,
        }


    # -v val:
    def find(self):
        result = dict()
        pattern = re.compile('%s' % self._wd)
        # check path.
        fnane = os.path.basename(self._fs)
        if re.compile('\*\.\w+').match(fnane):
            self._fs = os.path.dirname(self._fs)
        # check files now
        if self.path_is_file(self._fs):
            with open(self._fs, 'r') as f:
                data = f.read()
            data = pattern.findall(data)
            lst = list()
            for index in data:
                lst.append(index)
            result[self._fs] = lst
        else:
            for rt, dr, fs in os.walk(self._fs):
                if fs:
                    for f in fs:
                        if self.get_exname(f) != self.get_exname(self._val):
                            continue
                        f = os.path.join(rt, f)
                        lst = list()
                        with open(f, 'r') as fd:
                            data = fd.read()
                        data = pattern.findall(data)
                        for index in data:
                            if index:
                                lst.append(index)
                        if lst:
                            result[str(f)] = lst
        return result

    # -v val: old
    # -w word: new
    def sub(self):
        if self.path_is_file(self._fs):
            with open(self._fs, 'r') as fd:
                data = fd.read()
            data = re.sub(self._val, self._wd, data)
            with open(self._fs, 'wr') as fd:
                fd.write(data)
        else:
            for rt, dr, fs in os.walk(self._fs):
                if fs:
                    for f in fs:
                        f = os.path.join(rt, f)
                        with open(f, 'r') as fd:
                            data = fd.read()
                        data = re.sub(self._val, self._wd, data)
                        with open(self._fs, 'wr') as fd:
                            fd.write(data)
        return None

    def main(self):
        args = self.get_user_input('hf:c:v:w:')
        if '-h' in args:
            self.print_help(self.help_menu)
        if '-f' in args:
            self._fs = self.get_abs_path(args['-f'])
        if '-c' in args:
            self._cmd = args['-c']
        if '-v' in args:
            self._val = args['-v']
        if '-w' in args:
            self._wd = args['-w']
        if not self._fs or not self._cmd:
            self.print_exit('Error, -h for help!')
        # run cmd now.
        if self._cmd in self.__handlers:
            result = self.__handlers[self._cmd]()
            if result:
                for key, values in result.items():
                    print '----%s----: ' % key
                    for val in values:
                        print(val)
                    print('')

if __name__ == '__main__':
    mypy = MyPy()
    mypy.main()
