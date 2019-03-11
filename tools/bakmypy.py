#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 2019-02-20

@author: Byng.Zeng
"""

import os
import shutil
import tarfile
import time

from pybase.pysys import print_help, print_exit
from baiduyun import BaiduYun

VERSION = '1.2.2'
AUTHOR = 'Byng.Zeng'


MYPYPATH = os.path.join(os.getenv('HOME'), 'mypy')


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
    from pybase.pyinput import get_input_args

    HELP_MENU = (
        '============================================',
        '    bakmypy - %s' % VERSION,
        '',
        '    @Author: %s' % AUTHOR,
        '    Copyright (c) %s studio' % AUTHOR,
        '============================================',
        'options:',
        ' -a: upload all of files to baiduyun.',
        ' -f: upload source files to baiduyun.',
        ' -z: tar files to mypy_(date-time).bz2 and upload to baiduyun.',

    )

    args = get_input_args('hafz', True)
    if args:
        date_ = time.strftime('%Y%m%d', time.localtime())
        time_ = time.strftime('%H%M', time.localtime())
        clean_cache(MYPYPATH)  # clear all of cache files.
        by = BaiduYun('BackupMypy')
        for k in args.keys():
            if k == '-a':
                args = {'-c': 'upload', '-l': MYPYPATH,
                        '-y': 'Mypy/%s/mypy_%s-%s_all' % (date_, date_, time_)}
                by.main(args)
            elif k == '-f':
                args = {'-c': 'upload', '-f': ('.py', '.txt'), '-l': MYPYPATH,
                        '-y': 'Mypy/%s/mypy_%s-%s' % (date_, date_, time_)}
                by.main(args)
            elif k == '-z':
                tar = create_tar(MYPYPATH)
                args = {'-c': 'upload', '-l': tar, '-y': 'Mypy/%s' % date_}
                try:
                    by.main(args)
                finally:
                    os.remove(tar)
            elif k == '-h':
                print_help(HELP_MENU)
    else:
        print_exit('no input, -h for help')
