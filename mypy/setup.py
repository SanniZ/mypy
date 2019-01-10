#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on 2018-12-03

@author: Byng.Zeng
"""
import re

from mypy import MyBase, MyRe, MyPath

BASHRC='%s/.bashrc' % MyPath.get_home_path()

class SetupMypy (object):

    help_menu = (
        '======================================',
        '     mypy setup',
        '======================================',
        'option: -a path -s -v',
        '  -a:',
        '    add path to mypys env',
        '  -s:',
        '    setup mypys config',
        '  -v:',
        '    print all of mypys path.',
    )

    def __init__(self):
        self.__re_mypys = MyRe.re_compile('MYPYS=.+')
        self.__re_path_mypys = MyRe.re_compile('PATH=$PATH:$MYPYS')
        self._path = list()

    def add_to_mypy_path(self, path):
        with open(BASHRC, 'r') as f:
            txt = f.read()
        mypys =  self.__re_mypys.findall(txt)
        # delete $.
        if len(re.findall('\$', path)) != 0:
            pattern = path.replace('$', '\$')
        else:
            pattern = path
        # add new path.
        if len(mypys) != 0 and len(re.findall(pattern, mypys[0])) == 0:
            print 'add path: %s' % path
            txt = txt.replace(mypys[0], '%s:%s' % (mypys[0], path))
        with open(BASHRC, 'w') as f:
            f.write(txt)

    def setup_bash_env(self):
        with open(BASHRC, 'r+') as f:
            txt = f.read()
            result = self.__re_mypys.findall(txt)
            if len(result) == 0:
                f.write('export MYPYS=$HOME/mypy\n')
            result = self.__re_path_mypys.findall(txt)
            if len(result) == 0:
                f.write('export PATH=$PATH:$MYPYS\n')
        self.add_to_mypy_path('$MYPY/broxton')
        self.add_to_mypy_path('$MYPY/develop')
        self.add_to_mypy_path('$MYPY/image')
        self.add_to_mypy_path('$MYPY/iOS')
        self.add_to_mypy_path('$MYPY/linux')
        self.add_to_mypy_path('$MYPY/mypy')
        self.add_to_mypy_path('$MYPY/tools')
        self.add_to_mypy_path('$MYPY/web')
        self.add_to_mypy_path('$MYPY/web/mzitu')
        self.add_to_mypy_path('$MYPY/faceID')

    def print_pypys_path(self):
        with open(BASHRC, 'r') as f:
            txt = f.read()
            result = self.__re_mypys.findall(txt)
            if len(result) == 0:
                print('No found MYPYS')
            else:
                mypys = re.split(':', str(result))
                for mypy in mypys:
                    mypy = mypy.replace('[\'MYPYS=', '')
                    mypy = mypy.replace('\']', '')
                    print(mypy)
                print re.search('MYPY=.+', txt).group()

    def get_user_input(self):
        args = MyBase.get_user_input('ha:sv')
        if '-h' in args:
            MyBase.print_help(self.help_menu)
        if '-a' in args:
            self._path.append(args['-a'])
        if '-s' in args:
            self.setup_bash_env()
        if '-v' in args:
            self.print_pypys_path()
        return True

    def main(self):
        if self.get_user_input() != True:
            exit()

        if len(self._path) != 0:
            for path in self._path:
                self.add_to_mypy_path(path)

if __name__ == '__main__':
    mypy = SetupMypy()
    mypy.main()


