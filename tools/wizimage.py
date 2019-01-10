#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Created on 2018-12-04

@author: Byng Zeng
"""

import os
import zipfile
import shutil

from mypy.base import Base
from mypy.path import Path
from mypy.file import File

from image.image import Image


class WizImage(object):

    help_menu = (
        '======================================',
        '     Unzip Wiz',
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

    def get_user_input(self):
        args = Base.get_user_input('hs:t:v')
        # help
        if '-h' in args:
            Base.print_help(self.help_menu)
        # src path
        if '-s' in args:
            self._src = Path.get_abs_path(args['-s'])
        # dst path
        if '-t' in args:
            self._dst = Path.get_abs_path(args['-t'])
        # show
        if '-v' in args:
            self._show = True
        # start to check args.
        # start id is must be set, otherwise return..
        if self._src == None:
            return False
        # next to start if _end is not set.
        if self._dst == None:
            self._dst = Path.get_current_path()
            print('warnning: no found -t, output to: %s' % self._dst)
        return True

    def get_all_of_wiz(self):
        for root, dirs, fs in os.walk(self._src):
            if len(fs) != 0:
                for f in fs:
                    if File.get_exname(f) == '.ziw':
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
            path = os.path.join(os.path.dirname(f).replace(self._src, self._dst), File.get_fname(f))
            path = os.path.splitext(path)[0]
            Path.make_path(path)
            self.unzip_file(f, path)
            # remove small image.
            Image.remove_small_image(path)
            # move image.
            if os.path.exists('%s/index_files' % path):
                for ff in os.listdir('%s/index_files' % path):
                    if Image.image_file('%s/index_files/%s' % (path, ff)):
                        shutil.copyfile('%s/index_files/%s' % (path, ff), '%s/%s' % (path, ff))
                # remove invalid files and dirs.
                shutil.rmtree('%s/index_files' % path)
            if os.path.exists('%s/index.html' % path):
                os.remove('%s/index.html' % path)

    def main(self):
        self.get_user_input()
        # get all of .wiz
        self.get_all_of_wiz()
        # unzip all of wiz files.
        self.unzip_wiz()
        # remove blank dir.
        Path.remove_blank_dir(self._dst)

if __name__ == '__main__':
    wiz = WizImage()
    wiz.main()
