#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 2019-01-30

@author: Byng.Zeng
"""

import os
import re
import subprocess

from bypy import ByPy

from mypy.base import Base
from mypy.path import Path


############################################################################
#               Const Vars
############################################################################

REMOTEROOT = 'apps/bypy'

LISTROOT = ['ROOT', 'Root', 'root']

LOCALROOT = r'LocalRoot'

def pr_info(msg, view=False):
    if view:
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
        '  -d dirname: set dirname of baidu yun',
        '    dirname : dirname of baidu yun',
        '  -l dirname: list of dirname of baidu yun',
        '    dirname : dirname of baidu yun',
        '  -s path: upload local files to baidu yun',
        '    path : path of dir or file',
        '  -v True/False: view info of uploading',
        '  -o: order to show files',
        '  -r: recursion of path',
        '',
        'Note:',
        ' if it is not able to access BaiduYun,',
        ' run \'bypy info\' to setup first!\n'
    )

    def __init__(self, src=None, dirname=None, view=True):
        self._src = src
        self._dst = dirname
        self._view = view
        self._o_print = False
        self._recursion_path = False
        self._count = 0
        # create baiduyun
        self._bp = ByPy()

    def get_input(self):
        return Base.get_user_input('hs:d:v:l:or')

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
            if dr == LOCALROOT:
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
                self._bp.upload(localpath=f, remotepath=dst, ondup='overwrite')

    def get_upload_files(self):
        dfs = dict()
        self._count = 0
        if os.path.isfile(self._src):
            dfs[LOCALROOT] = [self._src]
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
                        dr = LOCALROOT
                    dfs[dr] = ls
        return dfs

    def __list_of_dir(self, path):
        ds = list()
        fs = list()
        if path in LISTROOT:
            cmd = 'bypy -r 3 list \'\' \$t\$f'
        else:
            cmd = 'bypy -r 3 list %s \$t\$f' % re.sub(' ', '\ ', path)
        try:
            res = subprocess.check_output(cmd, shell=True).decode()
        except subprocess.CalledProcessError:
            print('warnning: access %s failed!', path)
        else:
            ls = res.split('\n')
            for f in ls:
                if f:
                    if f[0] == 'D':
                        ds.append(f[1:])
                    if f[0] == 'F':
                        fs.append(f[1:])
        return ds, fs

    def list_of_path(self, path, recursion=False):
        lfs = dict()
        if not recursion:
            ds, fs = self.__list_of_dir(path)
            lfs[path] = fs
            if ds:
                for dr in ds:
                    lfs[dr] = None
        else:
            ds = [path]
            while ds:
                ds3 = list()
                for d in ds:
                    ds2, fs2 = self.__list_of_dir(d)
                    if ds2:
                        for d2 in ds2:
                            if d in LISTROOT:
                                lfs['%s' % d2] = None
                                ds3.append('%s' % d2)
                            else:
                                lfs['%s/%s' % (d, d2)] = None
                                ds3.append('%s/%s' % (d, d2))
                    if fs2:
                        lfs[d] = fs2
                ds = ds3
        return lfs

    def main(self, args=None):
        if not args:
            args = self.get_input()
        if '-h' in args:
            Base.print_help(self.HELP_MENU)
            return
        if '-v' in args:
            if args['-v'] in ['True', '1', 'true']:
                self._view = True
            else:
                self._view = False
        if '-o' in args:
            self._o_print = True
        if '-r' in args:
            self._recursion_path = True
        if '-s' in args:
            self._src = Path.recliam_path(os.path.abspath(args['-s']))
        if '-d' in args:
            self._dst = Path.recliam_path(args['-d'])
        if '-l' in args:
            fs = self.list_of_path(args['-l'], self._recursion_path)
            if fs:
                for dr, lfs in fs.items():
                    if dr in LISTROOT:
                        print('%s:' % (REMOTEROOT))
                    else:
                        print('%s/%s:' % (REMOTEROOT, dr))
                    if self._o_print:
                        if lfs:
                            for f in lfs:
                                print(f)
                    else:
                        print(lfs)
                    print('')
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
