#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on: 2018-12-06

@author: Byng Zeng
"""

import re

from mypy import MyBase, MyRe, MyPath

BASHRC = '%s/.bashrc' % MyPath.get_home_path()

class MyUbuntu(object):

    help_menu = (
        '==================================',
        '    MyUbuntu Help',
        '==================================',
        'option: -c -P -a path -A path -V -v',
        '  -c: create MYPATH to PATH',
        '  -P: add MYPYS to PATH',
        '  -a: add path to MYPATH',
        '  -A: add path to MYPYS',
        '  -V: show all of PATH',
        '  -v: show MYPATH',
    )

    def __init__(self):
        # re compile.
        self.__re_path = MyRe.re_compile('export PATH=.*')
        self.__re_mypath = MyRe.re_compile('export MYPATH=.*')
        self.__re_mypys = MyRe.re_compile('export MYPYS=.*')
        self.__re_myshs = MyRe.re_compile('export MYSHS=.*')
        # get .bashrc data.
        with open(BASHRC, 'r') as f:
            self.__bashrc = f.read()

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

    def add_to_mypath(self, path):
        print('add %s to PATH.' % path)
        if not self.check_mypath():
            self.create_mypath()
        # get mypath
        mypath = self.__re_mypath.search(self.__bashrc)
        # check path in mypath
        new_path = MyRe.re_compile(path).search(mypath.group())
        if not new_path:
            data = self.get_bashrc_data()
            data = data.replace(mypath.group(), '%s:%s' % (mypath.group(), path))
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
            'export MYPYS=$MYPY:$MYPY/broxton:$MYPY/develop:$MYPY/linux:$MYPY/linux/ubuntu:$MYPY/linux/ibus:$MYPY/iOS:$MYPY/tools:$MYPY/image:$MYPY/web:$MYPY/web/mzitu:$MYPY/faceID\n',
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
                self.__bashrc = re.sub(MyRe.re_compile(mypath.group()), '%s%s:$MYPYS' % (mys, mypath.group()), self.__bashrc)
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
            self.__bashrc = re.sub(MyRe.re_compile(mypys.group()), '%s:%s' % (mypys.group(), path), self.__bashrc)
            with open(BASHRC, 'w') as f:
                f.write(self.__bashrc)

    def main(self):
        args = MyBase.get_user_input('hcPa:A:vV')
        if '-h' in args:
            MyBase.print_help(self.help_menu)
        if '-c' in args:
            self.create_mypath()
        if '-P' in args:
            self.add_mypys()
        if '-a' in args:
            self.add_to_mypath(args['-a'])
        if '-A' in args:
            self.add_to_mypys(args['-A'])
        if '-V' in args:
            self.print_path()
        if '-v' in args:
            self.print_mypath()

if __name__ == '__main__':
    ubuntu = MyUbuntu()
    ubuntu.main()
