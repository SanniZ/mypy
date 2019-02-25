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

from baiduyun import BaiduYun

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
    clean_cache(MYPY)
    tar = create_tar(MYPY)
    args = {'-l': tar, '-y': 'Mypy', '-c': 'upload'}
    by = BaiduYun('BackupMypy', True)
    by.main(args)
    os.remove(tar)
