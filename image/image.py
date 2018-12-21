#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on 2018-12-03

@author: Byng Zeng
"""

import os
import re
from PIL import Image as PILImg

from mypy import MyFile

IMG_W_MIN = 320
IMG_H_MIN = 320

SMALL_IMG_SIZE = 1024 * 20 # 20K

class Image (object):

    def __init__(self, name=None):
        self._name = name

    # check image base on extname.
    @classmethod
    def image_file2(cls, f):
        exname = MyFile.get_exname(f)
        if exname in ['.jpg', '.png', '.gif', '.jpeg', '.bmp']:
            return True
        else:
            return False

    # check image base on image attr.
    @classmethod
    def image_file(cls, f):
        try:
            img = PILImg.open(f)
            if img.format in ['PNG', 'JPEG', 'GIF']:
                return img
            else:
                return None
        except IOError: # it is bad if open failed.
            return None

    # remove small size image, default size is 10K.
    @classmethod
    def remove_small_size_image(cls, path, size=SMALL_IMG_SIZE):
        if os.path.isfile(path):
            if all((os.path.getsize(path) < size, any((cls.image_file(path), cls.image_file2(path))))):
                print 'remove: ', path
                os.remove(path)
        else:
            for rt, dirs, fs in os.walk(path):
                if len(fs) != 0:  # found files.
                    for f in fs:
                        f = os.path.join(rt, f)
                        if all((os.path.getsize(f) < size, any((cls.image_file(f), cls.image_file2(f))))):
                                os.remove(f)

    # remove small image, default width < IMG_W_MIN or height < IMG_H_MIN.
    @classmethod
    def remove_small_image(cls, path, width=IMG_W_MIN, height=IMG_H_MIN, obj=None, remove_small_size_image=True):
        imgs_dict = dict()
        if obj:
            imgs_dict[obj]=path
        elif os.path.isfile(path):
            img = cls.image_file(path)
            if img:
                imgs_dict[img] = path
        elif os.path.isdir(path):
            for rt, dirs, fs in os.walk(path):
                if fs:  # found files.
                    for f in fs:
                        f = os.path.join(rt, f)
                        img = cls.image_file(f)
                        if img:
                            imgs_dict[img] = f
        # check size of image.
        for img in imgs_dict:
            w, h = cls.get_image_size(img)
            if all((w, h)):
                if any((w < width, h < height)):
                    os.remove(imgs_dict[img])
            else:  # fail to get size, remove it.
                os.remove(imgs_dict[img])
        # remove small size of images.
        if remove_small_size_image:
            cls.remove_small_size_image(path)

    @classmethod
    def get_image_size(cls, img):
        return img.size[0], img.size[1]

    @classmethod
    def reclaim_image(cls, f, obj=None, xfunc=None):
        fname = f
        if obj:
            img = obj
        else:
            img = cls.image_file(f)
        if img:
            fmt = img.format.lower()
            if fmt == 'jpeg':
                fmt = 'jpg'
            ftype = MyFile.get_filetype(f)
            if not ftype: # no ext name
                fname = '%s.%s' % (f, fmt)
            elif fmt != ftype:
                fname = re.sub(ftype, fmt, f)
            try:
                os.rename(f, fname)
            except OSError as e:
                print('%s, failed to rename %s.' % (str(e), f))
        # run xfunc
        if xfunc:
            xfunc(fname)

    @classmethod
    def reclaim_path_images(cls, path, xfunc=None):
        for rt, dr, fs in os.walk(path):
            if len(fs):
                for f in fs:
                    f = os.path.join(rt, f)
                    img = cls.image_file(f)
                    if img:
                        cls.reclaim_image(f, obj=img, xfunc=xfunc)
                    elif xfunc:
                        xfunc(f)

if __name__ == '__main__':
    from mypy import MyBase, MyPrint, MyPath

    HELP_MENU = (
        '============================================',
        '    Image help',
        '============================================',
        'options: -c img -r path -R path -x val',
        '  -c img:',
        '    check img is image format',
        '    sub : sub val in file',
        '  -r path:',
        '    remove small size of images: dir or file',
        '  -R path:',
        '    reclaim image format: dir or file',
        '  -x val:',
        '    xval for cmd ext functions.',
    )

    pr = MyPrint('Image')
    Img = Image()
    xval = None
    args = MyBase.get_user_input('hc:r:R:x:')
    if '-h' in args:
        MyBase.print_help(HELP_MENU)
    if '-x' in args:
        xval = args['-x']
    if '-c' in args:
        result = Img.image_file(MyPath.get_abs_path(args['-c']))
        pr.pr_info(result)
    if '-r' in args:
        path = args['-r']
        if xval:
            Img.remove_small_image(path, int(xval), int(xval))
        else:
            Img.remove_small_image(path)
    if '-R' in args:
        path = args['-R']
        if Img.image_file(path):
            Img.reclaim_image(path)
        else:
            Img.reclaim_path_images(path)