#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on 2018-12-05

@author: Byng Zeng
"""

import os
import re

from base import MyBase as Base

def print_help():
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
        '    clean all of .pyc at current path.',
    )
    for help in help_menu:
        print(help)

def clean_pyc(path=os.getenv('MYPY'), show=False):
    for rt, dr, fs in os.walk(path):
        if len(fs) != 0:
            for f in fs:
                f = os.path.join(rt, f)
                if Base.get_exname(f) == '.pyc':
                    os.remove(f)
                    if show:
                        print('remove: %s' % f)

if __name__ == '__main__':
    args = Base.get_user_input('hp:vc')
    # help
    if '-h' in args:
        print_help()
        Base.print_exit()
    # check path.
    if '-p' in args:
        if re.match('\.', args['-p']):
            path = re.sub('.', Base.get_current_path(), args['-p'])
        else:
            path = args['-p']
    else:
        path = Base.get_current_path()
    # check show.
    if '-v' in args:
        show = True
    else:
        show = False
	# clean .pyc now.
    clean_pyc(path, show)

