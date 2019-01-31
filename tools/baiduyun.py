#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Created on 2019-01-30

@author: Byng.Zeng
"""

import os
import re

from bypy import ByPy

from mypy.base import Base
from mypy.path import Path


############################################################################
#               Const Vars
############################################################################

ROOTDIR = r'RootDir'


def pr_info(msg, view=False):
    if view in [True, 'True', '1']:
        print(msg)


def pr_warn(msg):
    print(msg)


############################################################################
#               BaiduYun class
############################################################################

class BaiduYun(object):

    HELP_MENU = (
        '============================================',
        '    BaiduYun help',
        '============================================',
        'options:',
        '  -s path: upload local files to baidu yun',
        '    path : path of dir or file',
        '  -d dirname: set dirname of baidu yun',
        '    dirname : dirname of baidu yun',
        '  -v True/False: view info of uploading',
        '',
        'Note:',
        ' if it is not able to access BaiduYun,',
        ' run \'bypy info\' to setup first!\n'
    )

    def __init__(self, src=None, dirname=None, view=True):
        self._src = src
        self._dst = dirname
        self._view = view
        self._count = 0
        # create baiduyun
        self._bp = ByPy()

    def get_input(self):
        return Base.get_user_input('hs:d:v:')

    def join_path(self, rt, dr):
        if all((rt, dr)):
            return '%s/%s' % (rt, dr)
        elif all((not rt, dr)):
            return dr
        else:
            return None

    def upload_files(self, files):
        index = 0
        for dr, fs in files.items():
            # create dir
            if dr == ROOTDIR:
                dst = self._dst
            else:
                dst = self.join_path(self._dst, dr)
                if not dst:
                    pr_warn('Warnning: failed to get remote path of %s' % dr)
                    continue
            self._bp.mkdir(dst)
            # upload files
            for f in fs:
                index += 1
                pr_info('[%s/%s] uploading: %s ===> %s' % (index, self._count,
                        re.sub('%s/' % self._src, '', f), dst), self._view)
                self._bp.upload(localpath=f, remotepath=dst, ondup='newcopy')

    def get_upload_files(self):
        dfs = dict()
        self._count = 0
        if os.path.isfile(self._src):
            dfs[ROOTDIR] = [self._src]
            self._count += 1
            self._src = os.path.dirname(self._src)
        elif os.path.isdir(self._src):
            for rt, ds, fs in os.walk(self._src):
                if fs:
                    ls = list()
                    # append file to list
                    for f in fs:
                        f = os.path.join(rt, f)
                        ls.append(f)
                        self._count += 1
                    # get dir
                    dr = re.sub('%s' % self._src, '', rt)
                    if dr.startswith('/'):
                        dr = dr[1:]
                    if not dr:
                        dr = ROOTDIR
                    dfs[dr] = ls
        return dfs

    def main(self, args=None):
        if not args:
            args = self.get_input()
        if '-h' in args:
            Base.print_help(self.HELP_MENU)
            return
        if '-v' in args:
            self._view = args['-v']
        if '-s' in args:
            self._src = Path.recliam_path(os.path.abspath(args['-s']))
        if '-d' in args:
            self._dst = Path.recliam_path(args['-d'])
        # start to upload files.
        if self._src:
            if os.path.exists(self._src):
                fs = self.get_upload_files()
                if fs:
                    self.upload_files(fs)
            else:
                pr_warn('Error, %s in invalid!' % self._src)


############################################################################
#               main entrance
############################################################################

if __name__ == '__main__':
    by = BaiduYun()
    by.main()
