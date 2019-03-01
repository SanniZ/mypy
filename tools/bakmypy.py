#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 2019-02-20

@author: Zbyng.Zeng
"""

import os
import shutil
import tarfile
import time

from mypy.pybase import print_help, print_exit
from baiduyun import BaiduYun

VERSION = '1.2.0'


MYPY = os.path.join(os.getenv('HOME'), 'mypy')


def clean_cache(path):
    for rt, ds, fs in os.walk(path):
        if ds:
            for d in ds:
                if d == '__pycache__':
                    shutil.rmtree(os.path.join(rt, d))


def create_tar(path):
    os.chdir(path)
    dt = time.strftime('%Y%m%d-%H%M', time.localtime())
    tar = '%s/mypy_%s.tar.bz2' % (path, dt)
    with tarfile.open(tar, 'w:bz2') as fd:
        for rt, ds, fs in os.walk(os.path.curdir):
            if fs:
                for f in fs:
                    f = os.path.join(rt, f)
                    fd.add(f)
    return tar


if __name__ == '__main__':
    from mypy.pybase import get_user_input

    HELP_MENU = (
        '============================================',
        '    bakmypy help',
        '============================================',
        'options:',
        ' -a: upload all of files to baiduyun.',
        ' -f: upload source files to baiduyun.',
        ' -z: tar files to mypy_(date-time).bz2 and upload to baiduyun.',

    )

    args = get_user_input('hafz')
    if args:
        dt = time.strftime('%Y%m%d-%H%M', time.localtime())
        clean_cache(MYPY)  # clear all of cache files: *.pyc and __pyc__ dirs
        by = BaiduYun('BackupMypy')
        if '-h' in args:
            print_help(HELP_MENU)
        elif '-a' in args:
            args = {'-l': MYPY, '-y': 'Mypy/mypy_%s' % dt, '-c': 'upload'}
            by.main(args)
        elif '-f' in args:
            args = {'-l': MYPY, '-y': 'Mypy/mypy_%s' % dt,
                    '-f': ('.py', '.txt'), '-c': 'upload'}
            by.main(args)
        elif '-z' in args:
            tar = create_tar(MYPY)
            args = {'-l': tar, '-y': 'Mypy', '-c': 'upload'}
            by.main(args)
            os.remove(tar)
    else:
        print_exit('no input, -h for help')

