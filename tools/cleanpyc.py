#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 2018-12-05

@author: Byng Zeng
"""

import os
import re
import subprocess

from pybase.pysys import print_help
from pybase.pyinput import get_user_input
from pybase.pypath import get_current_path
from pybase.pyfile import get_name_ex

VERSION = '1.1.0'


HELP_MENU = (
    '===================================',
    '    clean .pyc',
    '===================================',
    'option:',
    '  -p path:',
    '    root path to clean .pyc',
    '  -v',
    '    show file to be removed.',
    '  -c',
    '    clean all of .pyc at current path.'
)


def clean_pyc_shell():
    cmd = 'find . -name *.pyc -o -name __pycache__ | xargs rm -rf {}'
    subprocess.call(cmd, shell=True)


def clean_pyc(path=os.getenv('MYPY'), show=False):
    for rt, dr, fs in os.walk(path):
        if fs:
            for f in fs:
                f = os.path.join(rt, f)
                if get_name_ex(f) == '.pyc':
                    os.remove(f)
                    if show:
                        print('remove: %s' % f)
            if dr:
                for d in dr:
                    if d == '__pycache__':
                        os.remove(d)

if __name__ == '__main__':
    args = get_user_input('hp:vc')
    # help
    if '-h' in args:
        print_help(HELP_MENU)
    # check path.
    if '-p' in args:
        if re.match('\.', args['-p']):
            path = re.sub('.', get_current_path(), args['-p'])
        else:
            path = args['-p']
    else:
        path = get_current_path()
    # check show.
    if '-v' in args:
        show = True
    else:
        show = False
    # clean .pyc now.
    clean_pyc(path, show)
