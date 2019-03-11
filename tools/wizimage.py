#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 2018-12-04

@author: Byng Zeng
"""

import os
import zipfile
import shutil

from pybase.pysys import print_help
from pybase.pyinput import get_input_args
from pybase.pypath import get_abs_path, get_current_path, \
                        make_path, remove_blank_dir
from pybase.pyfile import get_name_ex, get_fname
from pybase.pyimage import remove_small_image, image_file

VERSION = '1.1.0'
AUTHOR = 'Byng.Zeng'


class WizImage(object):

    HELP_MENU = (
        '======================================',
        '     WizImage - %s' % VERSION,
        '',
        '    @Author: %s' % AUTHOR,
        '    Copyright (c) %s studio' % AUTHOR,
        '======================================',
        'option:',
        '  -s path: root path of files',
        '  -t path: root path to output.',
        '  -v True/False: show infomation of unzip.',
    )

    def __init__(self):
        self._src = None
        self._dst = None
        self._fs = list()
        self._show = False

    def get_input(self):
        args = get_input_args('hs:t:v')
        for k in args.keys():
            # src path
            if k == '-s':
                self._src = get_abs_path(args['-s'])
            # dst path
            elif k == '-t':
                self._dst = get_abs_path(args['-t'])
            # show
            elif k == '-v':
                self._show = True
            elif k == '-h':
                print_help(self.HELP_MENU)
        # start to check args.
        # start id is must be set, otherwise return..
        if not self._src:
            return False
        # next to start if _end is not set.
        if not self._dst:
            self._dst = get_current_path()
            print('warnning: no found -t, output to: %s' % self._dst)
        return True

    def get_all_of_wiz(self):
        for root, dirs, fs in os.walk(self._src):
            if len(fs) != 0:
                for f in fs:
                    if get_name_ex(f) == '.ziw':
                        self._fs.append(os.path.join(root, f))

    def unzip_file(self, f, dst):
        r = zipfile.is_zipfile(f)
        if r:
            if self._show:
                print('unzip: %s' % f)
            fz = zipfile.ZipFile(f, 'r')
            for f in fz.namelist():
                fz.extract(f, dst)

    def unzip_wiz(self):
        for f in self._fs:
            path = os.path.join(os.path.dirname(f).replace(
                                self._src, self._dst), get_fname(f))
            path = os.path.splitext(path)[0]
            make_path(path)
            self.unzip_file(f, path)
            # remove small image.
            remove_small_image(path)
            # move image.
            if os.path.exists('%s/index_files' % path):
                for ff in os.listdir('%s/index_files' % path):
                    if image_file('%s/index_files/%s' % (path, ff)):
                        shutil.copyfile('%s/index_files/%s' % (path, ff),
                                        '%s/%s' % (path, ff))
                # remove invalid files and dirs.
                shutil.rmtree('%s/index_files' % path)
            if os.path.exists('%s/index.html' % path):
                os.remove('%s/index.html' % path)

    def main(self):
        self.get_input()
        # get all of .wiz
        self.get_all_of_wiz()
        # unzip all of wiz files.
        self.unzip_wiz()
        # remove blank dir.
        remove_blank_dir(self._dst)

if __name__ == '__main__':
    wiz = WizImage()
    wiz.main()
