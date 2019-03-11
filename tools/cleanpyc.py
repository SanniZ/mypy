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
from pybase.pyinput import get_input_args
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
    show = False
    path = get_current_path()
    args = get_input_args('hp:vc')
    for k in args.keys():
        if k == '-p':
            if re.match('\.', args['-p']):
                path = re.sub('.', get_current_path(), args['-p'])
            else:
                path = args['-p']
        # check show.
        elif k == '-v':
            show = True
        elif k == '-h':
            print_help(HELP_MENU)
    # clean .pyc now.
    clean_pyc(path, show)
