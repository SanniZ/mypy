#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Created on 2018-12-05

@author: Byng Zeng
"""

import os
import re
import subprocess

from mypy.base import Base
from mypy.path import Path
from mypy.file import File

help_menu = (
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
    subprocess.call(cmd,shell = True)

def clean_pyc(path=os.getenv('MYPY'), show=False):
    for rt, dr, fs in os.walk(path):
        if fs:
            for f in fs:
                f = os.path.join(rt, f)
                if File.get_exname(f) == '.pyc':
                    os.remove(f)
                    if show:
                        print('remove: %s' % f)
            if dr:
                for d in dr:
                    if d == '__pycache__':
                        os.remove(d)

if __name__ == '__main__':
    args = Base.get_user_input('hp:vc')
    # help
    if '-h' in args:
        Base.print_help(help_menu)
    # check path.
    if '-p' in args:
        if re.match('\.', args['-p']):
            path = re.sub('.', Path.get_current_path(), args['-p'])
        else:
            path = args['-p']
    else:
        path = Path.get_current_path()
    # check show.
    if '-v' in args:
        show = True
    else:
        show = False
	# clean .pyc now.
    clean_pyc(path, show)
