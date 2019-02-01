#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Created on 2018-12-03

@author: Byng Zeng
"""

import os
import re
from PIL import Image as PILImg

from mypy.file import File

IMG_W_MIN = 240
IMG_H_MIN = 240

SMALL_IMG_SIZE = 1024 * 8  # 8K


class Image (object):

    def __init__(self, name=None):
        self._name = name

    # get image format, return format or None.
    @classmethod
    def get_image_format(cls, f=None, obj=None):
        if obj:
            img = obj
        elif cls.image_file_ex(f):
            img = PILImg.open(f)
        else:
            img = None
        # get format of image.
        if img:
            fmt = img.format.lower()
            if fmt == 'jpeg':
                fmt = 'jpg'
            return fmt
        else:
            return None

    # check image base on extname, return True or False
    @classmethod
    def image_file_ex(cls, f):
        exname = File.get_name_ex(f)
        if exname in ['.jpg', '.png', '.gif', '.jpeg', '.bmp']:
            return True
        else:
            return False

    # check image, return img or None.
    @classmethod
    def image_file(cls, f):
        try:
            img = PILImg.open(f)
        except IOError:  # it is bad if open failed.
            return None
        else:
            if img.format in ['PNG', 'JPEG', 'GIF']:
                return img
            else:
                return None

    # remove small size image.
    @classmethod
    def remove_small_size_image(cls, path, size=SMALL_IMG_SIZE):
        if os.path.isfile(path):
            if any((cls.image_file(path), cls.image_file_ex(path))):
                if os.path.getsize(path) < size:
                    os.remove(path)
        else:
            for rt, dirs, fs in os.walk(path):
                if fs:  # found files.
                    for f in fs:
                        f = os.path.join(rt, f)
                        if any((cls.image_file(f), cls.image_file_ex(f))):
                            if os.path.getsize(f) < size:
                                    os.remove(f)

    # remove small image, default width < IMG_W_MIN or height < IMG_H_MIN.
    @classmethod
    def remove_small_image(cls, path, width=IMG_W_MIN, height=IMG_H_MIN,
                           obj=None, remove_small_size_image=False):
        imgs_dict = dict()
        if obj:
            imgs_dict[path] = obj
        elif os.path.isfile(path):
            img = cls.image_file(path)
            if img:
                imgs_dict[path] = img
        elif os.path.isdir(path):
            for rt, dirs, fs in os.walk(path):
                if fs:  # found files.
                    for f in fs:
                        f = os.path.join(rt, f)
                        img = cls.image_file(f)
                        if img:
                            imgs_dict[f] = img
        # check size of image.
        for f, img in imgs_dict.items():
            w, h = cls.get_image_size(img)
            if all((w, h)):
                if any((w < width, h < height)):
                    os.remove(f)
            else:  # fail to get size, remove it.
                os.remove(f)
            # remove small size of images.
            if remove_small_size_image:
                cls.remove_small_size_image(f)

    @classmethod
    def get_image_size(cls, img):
        if img:
            return img.size[0], img.size[1]
        else:
            return None, None

    @classmethod
    def reclaim_image(cls, f, obj=None, remove_small_image=False):
        fname = f
        if obj:
            img = obj
        else:
            img = cls.image_file(f)
        # reclaim image.
        if img:
            fmt = img.format.lower()
            if fmt == 'jpeg':
                fmt = 'jpg'
            ftype = File.get_filetype(f, False)
            if not ftype:  # no ext name
                fname = '%s.%s' % (f, fmt)
            elif fmt != ftype:
                fname = re.sub(ftype, fmt, f)
            try:
                os.rename(f, fname)
            except OSError as e:
                print('%s, failed to rename %s.' % (str(e), f))
            # remove small image.
            if remove_small_image:
                cls.remove_small_image(fname, obj=img)

    @classmethod
    def reclaim_path_images(cls, path, remove_small_image=False):
        for rt, dr, fs in os.walk(path):
            if fs:
                for f in fs:
                    f = os.path.join(rt, f)
                    img = cls.image_file(f)
                    if img:
                        cls.reclaim_image(f, img, remove_small_image)

    @classmethod
    def set_order_images(cls, path, rename=None, non_zero=False):
        for rt, dr, fs in os.walk(path):
            if fs:
                index = 1
                num = len(str(len(fs)))
                fdict = dict()
                for f in fs:
                    f = os.path.join(rt, f)
                    img = cls.image_file(f)
                    if img:
                        fmt = cls.get_image_format(obj=img)
                        if non_zero:
                            if rename:
                                fname = os.path.join(
                                    rt, '%s_%d.%s' % (rename, index, fmt))
                            else:
                                fname = os.path.join(
                                    rt, '%d.%s' % (index, fmt))
                        else:
                            if rename:
                                if num == 2:
                                    fname = os.path.join(
                                      rt, '%s_%02d.%s' % (rename, index, fmt))
                                elif num == 3:
                                    fname = os.path.join(
                                      rt, '%s_%03d.%s' % (rename, index, fmt))
                                else:
                                    fname = os.path.join(
                                      rt, '%s_%0d.%s' % (rename, index, fmt))
                            else:
                                if num == 2:
                                    fname = os.path.join(
                                      rt, '%02d.%s' % (index, fmt))
                                elif num == 3:
                                    fname = os.path.join(
                                      rt, '%03d.%s' % (index, fmt))
                                else:
                                    fname = os.path.join(
                                      rt, '%0d.%s' % (index, fmt))
                        fdict[f] = fname
                        index = index + 1
                # rename all of image under this dr
                for f, fname in fdict.items():
                    os.rename(f, fname)

    @classmethod
    def get_image_detail(cls, f):
        fmt = size = mode = None
        img = cls.image_file(f)
        if img:
            fmt = img.format
            size = img.size
            mode = img.mode
        return fmt, size, mode

if __name__ == '__main__':
    from mypy.base import Base
    from mypy.path import Path

    HELP_MENU = (
        '============================================',
        '    Image help',
        '============================================',
        'options:',
        '  -c img: check img is a image file',
        '    img: the path of image file',
        '  -r path,width,height: remove small size of images',
        '    path  : path of dir or file',
        '    width : min of width',
        '    height: min of height',
        '  -R path: reclaim image format',
        '    path: path of dir or file',
        '  -o path,rename,nz: rename image to order',
        '    path  : path of images',
        '    rename: the format of image to be rename',
        '    nz    : True is set %0d, False is set %d',
        '  -i img: show detail info of image file',
        '    img: the path of image file',
    )

    Img = Image()
    xval = None
    args = Base.get_user_input('hc:r:R:x:o:i:')
    if '-h' in args:
        Base.print_help(HELP_MENU)
    if '-c' in args:
        result = Img.image_file(Path.get_abs_path(args['-c']))
        print(result)
    if '-r' in args:
        data = args['-r'].split(',')
        path = data[0]
        if len(data) >= 3:
            w = data[1]
            h = data[2]
            Img.remove_small_image(path, int(w), int(h))
        else:
            Img.remove_small_image(path)
    if '-R' in args:
        path = args['-R']
        if Img.image_file(path):
            Img.reclaim_image(path)
        else:
            Img.reclaim_path_images(path)
    if '-o' in args:
        val = args['-o'].split(',')
        n = len(val)

        if n >= 3:
            Img.set_order_images(Path.get_abs_path(val[0]), val[1], val[2])
        elif n == 2:
            Img.set_order_images(Path.get_abs_path(val[0]), val[1])
        elif n == 1:
            Img.set_order_images(Path.get_abs_path(val[0]))
        else:
            print('Error, -h for help!')
    if '-i' in args:
        f = args['-i']
        dt = dict()
        if os.path.isfile(f):
            fmt, size, mode = Img.get_image_detail(f)
            if all((fmt, size, mode)):
                dt[f] = (fmt, size, mode)
        elif os.path.isdir(f):
            for rt, dr, fs in os.walk(f):
                if fs:
                    for f in fs:
                        f = os.path.join(rt, f)
                        fmt, size, mode = Img.get_image_detail(f)
                        if all((fmt, size, mode)):
                            dt[f] = (fmt, size, mode)
        # print result.
        for img, detail in dt.items():
            print('file  :', os.path.basename(img))
            print('format:', detail[0])
            print('size  :', detail[1])
            print('mode  :', detail[2])
            print('------------------')
