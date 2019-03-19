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

from pybase.pysys import print_help
from pybase.pypath import get_abs_path
from pybase.pyprint import PyPrint, PR_LVL_DEFAULT, PR_LVL_ALL
from pybase.pydecorator import get_input_args

############################################################################
#               Const Vars
############################################################################

VERSION = '1.2.0'
AUTHOR = 'Byng.Zeng'


REMOTEROOT = 'apps/bypy'

LISTROOT = ['ROOT', 'Root', 'root']

LOCALROOT = r'LocalRoot'


############################################################################
#               BaiduYun class
############################################################################

class BaiduYun(object):

    HELP_MENU = (
        '============================================',
        '    BaiduYun - %s' % VERSION,
        '',
        '    @Author: %s' % AUTHOR,
        '    Copyright (c) %s studio' % AUTHOR,
        '============================================',
        'options:',
        '  -y path: set path of baidu yun',
        '    path : path of baidu yun',
        '  -c xxx: run command',
        '    list(l): list path of baidu yun',
        '    upload(u): upload local path to baidu yun',
        '    download(d): download file from baidu yun',
        '  -l path: set local path',
        '    path : path of dir or file',
        '  -v: view info of uploading',
        '  -o: order to show files',
        '  -r: recursion of path',
        '  -m o/n: set upload mode, overwrite or newcopy.',
        '  -x .xxx: except files of type',
        '  -f .xxx: files of type',
        '',
        'Note:',
        ' if it is not able to access BaiduYun,',
        ' run \'bypy info\' to setup first!\n'
    )

    UPLOAD_MODES = {'o': 'overwrite', 'n': 'newcopy'}

    __slots__ = ('_name', '_local_path', '_remote_path', '_upload_mode',
                 '_cmd', '_order', '_recursion_path', '_count', '_bp',
                 '_ftype', '_xftype', '_input_opts', '_pr')

    def __init__(self, name='BaiduYun', view=False,
                 local_path=None, yun_path=None, upload_mode='overwrite'):
        self._name = name
        self._local_path = local_path
        self._remote_path = yun_path
        self._upload_mode = upload_mode
        self._cmd = None
        self._order = False
        self._recursion_path = False
        self._count = 0
        self._bp = None
        self._ftype = None
        self._xftype = None
        self._input_opts = 'hy:l:c:m:vorf:x:'
        self._pr = PyPrint('BaiduYun',
                           lvl=PR_LVL_ALL if view else PR_LVL_DEFAULT)

    @get_input_args()
    def process_input(self, opts, args=None):
        if args:
            for k in args.keys():
                if k == '-v':
                    self._pr.add_level(PR_LVL_ALL)
                elif k == '-o':
                    self._order = True
                elif k == '-r':
                    self._recursion_path = True
                elif k == '-l':
                    self._local_path = get_abs_path(args['-l'])
                elif k == '-y':
                    self._remote_path = args['-y']
                elif k == '-m':
                    mode = args['-m'].lower()
                    if mode in self.UPLOAD_MODES:
                        self._upload_mode = self.UPLOAD_MODES[mode]
                elif k == '-c':
                    self._cmd = args['-c'].lower()
                elif k == '-f':
                    self._ftype = args['-f']
                elif k == '-x':
                    self._xftype = args['-x']
                elif k == '-h':
                    print_help(self.HELP_MENU)
        return args

    def join_path(self, rt, dr):
        if all((rt, dr)):
            return '%s/%s' % (rt, dr)
        elif all((not rt, dr)):
            return dr
        else:
            return None

    def create_bypy(self):
        if not self._bp:
            self._bp = ByPy()
        return self._bp

    def upload_files(self, files, path=None):
        index = 0
        bypy = self.create_bypy()
        for dr, fs in files.items():
            # create dir
            if dr == LOCALROOT:
                dst = self._remote_path
            else:
                if path:
                    dst = self.join_path(path, dr)
                else:
                    dst = self.join_path(self._remote_path, dr)
                if not dst:
                    self._pr.pr_warn(
                        'Warnning: failed to get remote path of %s' % dr)
                    continue
            bypy.mkdir(dst)
            # upload files
            for f in fs:
                index += 1
                self._pr.pr_info(
                    '[%s/%s] uploading: %s ===> %s' % (
                        index, self._count,
                        re.sub('%s/' % self._local_path, '', f), dst))
                bypy.upload(localpath=f, remotepath=dst,
                            ondup=self._upload_mode)

    def get_upload_files(self, src):
        dfs = dict()
        self._count = 0
        if os.path.isfile(src):
            dfs[LOCALROOT] = [src]
            self._count += 1
            self._local_path = os.path.dirname(src)
        elif os.path.isdir(src):
            for rt, ds, fs in os.walk(src):
                if fs:
                    ls = list()
                    # append file to list
                    for f in fs:
                        if self._ftype:
                            if f.endswith(self._ftype):
                                f = os.path.join(rt, f)
                                ls.append(f)
                                self._count += 1
                        elif self._xftype:
                            if not f.endswith(self._xftype):
                                f = os.path.join(rt, f)
                                ls.append(f)
                                self._count += 1
                        else:
                            f = os.path.join(rt, f)
                            ls.append(f)
                            self._count += 1
                    # get dir
                    if ls:
                        dr = re.sub('%s' % src, '', rt)
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
            self._pr.pr_warn('warnning: access %s failed!', path)
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

    def download_files(self, remotepath, localpath):
        if not os.path.exists(localpath):
            os.makedirs(localpath)
        bypy = self.create_bypy()
        if remotepath.endswith('/'):
            dirname = os.path.basename(remotepath[:-1])
            localpath = os.path.join(localpath, dirname)
        bypy.download(remotepath, localpath)

    def main(self, args=None):
        self.process_input(opts=self._input_opts, args=args)
        if self._cmd in ('list', 'l', 'L'):
            fs = self.list_of_path(self._remote_path, self._recursion_path)
            if fs:
                for dr, lfs in fs.items():
                    if dr in LISTROOT:
                        self._pr.pr_info('%s:' % (REMOTEROOT))
                    else:
                        self._pr.pr_info('%s/%s:' % (REMOTEROOT, dr))
                    if self._order:
                        if lfs:
                            for f in lfs:
                                self._pr.pr_info(f)
                    else:
                        self._pr.pr_info(lfs)
                    self._pr.pr_info('')
        elif self._cmd in ('upload', 'u', 'U'):
            fs = self.get_upload_files(self._local_path)
            if fs:
                self.upload_files(fs)
        elif self._cmd in ('download', 'd', 'D'):
            self.download_files(self._remote_path, self._local_path)


############################################################################
#               main entrance
############################################################################

if __name__ == '__main__':
    by = BaiduYun()
    by.main()
