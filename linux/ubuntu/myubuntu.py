#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on: 2018-12-06

@author: Byng Zeng
"""

import os
import re
import sys
import getopt
import subprocess

VERSION = '0.1.0'
AUTHOR = 'Byng.Zeng'


BASHRC = '%s/.bashrc' % os.getenv('HOME')


class MyUbuntu(object):

    HELP_MENU = (
        '==================================',
        '    MyUbuntu - %s' % VERSION,
        '',
        '    @Author: %s' % AUTHOR,
        '    Copyright (c) %s studio' % AUTHOR,
        '==================================',
        'option: -c -P -a path -A path -v',
        '  -c: create MYPATH to PATH',
        '  -P: add MYPYS to PATH',
        '  -a: add path to MYPATH',
        '  -A: add path to MYPYS',
        '  -v: show all of PATH',
    )

    def print_help(self, help_menu, _exit=True):
        for help in help_menu:
            print(help)
        if _exit:
            exit()

    def print_exit(self, msg=None):
        if msg:
            print msg
        exit()

    def get_input_args(self, opts):
        result = dict()
        try:
            opts, args = getopt.getopt(sys.argv[1:], opts)
        except getopt.GetoptError:
            self.print_exit('Invalid input, -h for help.')
        if len(opts) == 0:
            self.print_exit('Invalid input, -h for help.')
        else:
            for name, value in opts:
                result[name] = value
        return result

    def __init__(self):
        # re compile.
        self.__re_path = re.compile('export PATH=.*')
        self.__re_mypath = re.compile('export MYPATH=.*')
        self.__re_mypys = re.compile('export MYPYS=.*')
        self.__re_myshs = re.compile('export MYSHS=.*')
        self.__re_pypath = re.compile('export PYTHONPATH=.*')
        # get .bashrc data.
        with open(BASHRC, 'r') as f:
            self.__bashrc = f.read()

    # support to '$'
    def re_compile(self, pattern):
        return re.compile(pattern.replace('$', '\$'))

    def get_bashrc_data(self):
        return self.__bashrc

    # update __bashrc
    def update_bashrc_data(self, data=None):
        if data:
            self.__bashrc = data
        else:
            with open(BASHRC, 'r') as f:
                self.__bashrc = f.read()

    # config mypath
    def create_mypath(self):
        mypath = (
            'export DWN=$HOME/Downloads\n',
            'export DOC=$HOME/Documents\n',
            'export MYPATH=$DWN:$DOC\n',
            'export PATH=$PATH:$MYPATH\n',
        )
        if not self.check_mypath():
            with open(BASHRC, 'a') as f:
                f.writelines(mypath)
            self.update_bashrc_data()

    def check_mypath(self):
        mypath = self.__re_mypath.search(self.__bashrc)
        if mypath:
            return True
        else:
            return False

    def print_mypath(self):
        mypaths = self.__re_mypath.findall(self.__bashrc)
        for mypath in mypaths:
            print(mypath[len('export '):])

    def print_path(self):
        paths = self.__re_path.findall(self.__bashrc)
        for path in paths:
            print(path[len('export '):])
        mypaths = self.__re_mypath.findall(self.__bashrc)
        for mypath in mypaths:
            print(mypath[len('export '):])
        mypys = self.__re_mypys.findall(self.__bashrc)
        for mypy in mypys:
            print(mypy[len('export '):])
        myshs = self.__re_myshs.findall(self.__bashrc)
        for mysh in myshs:
            print(mysh[len('export '):])
        pypath = self.__re_pypath.findall(self.__bashrc)
        for pyth in pypath:
            print(pyth[len('export '):])

    def print_path2(self):
        cmds = (
            '$PATH',
            '$MYPATH',
            '$MYPYS',
            '$MYSHS',
            '$PYTHONPATH',
        )
        for cmd in cmds:
            print('--------%s----------:' % cmd)
            subprocess.call(cmd, shell=True)

    def add_to_mypath(self, path):
        print('add %s to PATH.' % path)
        if not self.check_mypath():
            self.create_mypath()
        # get mypath
        mypath = self.__re_mypath.search(self.__bashrc)
        # check path in mypath
        new_path = self.re_compile(path).search(mypath.group())
        if not new_path:
            data = self.get_bashrc_data()
            data = data.replace(mypath.group(),
                                '%s:%s' % (mypath.group(), path))
            with open(BASHRC, 'w') as f:
                f.write(data)

    def check_mypys(self):
        mypys = self.__re_mypys.search(self.__bashrc)
        if mypys:
            return True
        else:
            return False

    def add_mypys(self):
        mypys = (
            'export MYPY=$HOME/mypy\n',
            'export PYTHONPATH=$PYTHONPATH:$MYPY',
        )
        # merge mypys
        mys = ''
        for mypy in mypys:
            mys = mys + mypy
        # check mypys and add it.
        if not self.check_mypys():
            # check mypath and create it.
            if not self.check_mypath():
                self.create_mypath()
            # search mypath and replace it.
            mypath = self.__re_mypath.search(self.__bashrc)
            if mypath:
                self.__bashrc = re.sub(self.re_compile(mypath.group()),
                                       '%s%s:$MYPYS' % (mys, mypath.group()),
                                       self.__bashrc)
                with open(BASHRC, 'w') as f:
                    f.write(self.__bashrc)

    def add_to_mypys(self, path):
        # check mypys and create.
        if not self.check_mypys():
            # check mypath and create it.
            if not self.check_mypath():
                self.create_mypath()
            self.add_mypys()
        # search mypys and replace it.
        mypys = self.__re_mypys.search(self.__bashrc)
        if mypys:
            self.__bashrc = re.sub(self.re_compile(mypys.group()),
                                   '%s:%s' % (mypys.group(), path),
                                   self.__bashrc)
            with open(BASHRC, 'w') as f:
                f.write(self.__bashrc)

    def main(self):
        args = self.get_input_args('hcPa:A:vV', True)
        for k in args.keys():
            if k == '-c':
                self.create_mypath()
            elif k == '-P':
                self.add_mypys()
            elif k == '-a':
                self.add_to_mypath(args['-a'])
            elif k == '-A':
                self.add_to_mypys(args['-A'])
            elif k == '-v':
                self.print_path2()
            elif k == '-h':
                self.print_help(self.HELP_MENU)

if __name__ == '__main__':
    ubuntu = MyUbuntu()
    ubuntu.main()
