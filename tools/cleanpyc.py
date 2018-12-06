#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on 2018-12-05

@author: Byng Zeng
"""

import os
import re

from mypy import MyBase, MyFile, MyPath


help_menu = (
    '===================================',
    '    clean .pyc',
    '===================================',
    'option: [-p path] [-v]',
    '  -p path:',
    '    root path to clean .pyc',
    '  -v',
    '    show file to be removed.',
    '  -c',
    '    clean all of .pyc at current path.'
)


def clean_pyc(path=os.getenv('MYPY'), show=False):
    for rt, dr, fs in os.walk(path):
        if len(fs) != 0:
            for f in fs:
                f = os.path.join(rt, f)
                if MyFile.get_exname(f) == '.pyc':
                    os.remove(f)
                    if show:
                        print('remove: %s' % f)

if __name__ == '__main__':
    args = MyBase.get_user_input('hp:vc')
    # help
    if '-h' in args:
        MyBase.print_help(help_menu)
    # check path.
    if '-p' in args:
        if re.match('\.', args['-p']):
            path = re.sub('.', MyPath.get_current_path(), args['-p'])
        else:
            path = args['-p']
    else:
        path = MyPath.get_current_path()
    # check show.
    if '-v' in args:
        show = True
    else:
        show = False
	# clean .pyc now.
    clean_pyc(path, show)
