#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 2018-12-03

@author: Byng Zeng
"""

import os
import sys
import re

if sys.version_info[0] == 2:
    import Image as PILImg
else:
    from PIL import Image as PILImg


############################################################################
#               Const Vars
############################################################################

VERSION = '1.2.2'
AUTHOR = 'Byng.Zeng'


IMG_W_MIN = 240
IMG_H_MIN = 240

SMALL_IMG_SIZE = 1024 * 8  # 8K


############################################################################
#              Functions
############################################################################

def get_filetype(f, lower=True):
    try:
        ftype = os.path.splitext(f)[1][1:]
        if lower:
            ftype = ftype.lower()
        return ftype
    except AttributeError:
        return None


def get_name_ex(f, lower=True):
    try:
        name_ex = os.path.splitext(f)[1]
        if lower:
            name_ex = name_ex.lower()
        return name_ex
    except AttributeError:
        return None


# check image base on extname, return True or False
def image_file_ex(f):
    exname = get_name_ex(f)
    if exname in ['.jpg', '.png', '.gif', '.jpeg', '.bmp']:
        return True
    else:
        return False


def get_image_format(f=None, obj=None):
    if obj:
        img = obj
    elif image_file_ex(f):
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


# check image, return img or None.
def image_file(f):
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
def remove_small_size_image(path, size=SMALL_IMG_SIZE):
    if os.path.isfile(path):
        if any((image_file(path), image_file_ex(path))):
            if os.path.getsize(path) < size:
                os.remove(path)
    else:
        for rt, dirs, fs in os.walk(path):
            if fs:  # found files.
                for f in fs:
                    f = os.path.join(rt, f)
                    if any((image_file(f),
                            image_file_ex(f))):
                        if os.path.getsize(f) < size:
                                os.remove(f)


def get_image_size(img):
    if img:
        return img.size[0], img.size[1]
    else:
        return None, None


# remove small image, default width < IMG_W_MIN or height < IMG_H_MIN.
def remove_small_image(path, width=IMG_W_MIN, height=IMG_H_MIN,
                       obj=None, remove_small_size_image=False):
    imgs_dict = dict()
    if obj:
        imgs_dict[path] = obj
    elif os.path.isfile(path):
        img = image_file(path)
        if img:
            imgs_dict[path] = img
    elif os.path.isdir(path):
        for rt, dirs, fs in os.walk(path):
            if fs:  # found files.
                for f in fs:
                    f = os.path.join(rt, f)
                    img = image_file(f)
                    if img:
                        imgs_dict[f] = img
    # check size of image.
    for f, img in imgs_dict.items():
        w, h = get_image_size(img)
        if all((w, h)):
            if any((w < width, h < height)):
                os.remove(f)
        else:  # fail to get size, remove it.
            os.remove(f)
        # remove small size of images.
        if remove_small_size_image:
            remove_small_size_image(f)


def reclaim_image(f, obj=None, rm_small_image=False):
    fname = f
    if obj:
        img = obj
    else:
        img = image_file(f)
    # reclaim image.
    if img:
        fmt = img.format.lower()
        if fmt == 'jpeg':
            fmt = 'jpg'
        ftype = get_filetype(f, False)
        if not ftype:  # no ext name
            fname = '%s.%s' % (f, fmt)
        elif fmt != ftype:
            fname = re.sub(ftype, fmt, f)
        try:
            os.rename(f, fname)
        except OSError as e:
            print('%s, failed to rename %s.' % (str(e), f))
        # remove small image.
        if rm_small_image:
            remove_small_image(fname, obj=img)


def reclaim_path_images(path, remove_small_image=False):
    for rt, dr, fs in os.walk(path):
        if fs:
            for f in fs:
                f = os.path.join(rt, f)
                img = image_file(f)
                if img:
                    reclaim_image(f, img, remove_small_image)


def set_order_images(path, rename=None, non_zero=False):
    for rt, dr, fs in os.walk(path):
        if fs:
            index = 1
            num = len(str(len(fs)))
            fdict = dict()
            for f in fs:
                f = os.path.join(rt, f)
                img = image_file(f)
                if img:
                    fmt = get_image_format(obj=img)
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
                            if num <= 2:
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


def get_image_detail(f):
    fmt = size = mode = None
    img = image_file(f)
    if img:
        fmt = img.format
        size = img.size
        mode = img.mode
    return fmt, size, mode


############################################################################
#              PyImage class
############################################################################

class PyImage (object):

    # def __init__(self, name=None):
    #    self._name = name

    # get image format, return format or None.
    @staticmethod
    def get_image_format(f=None, obj=None):
        return get_image_format(f, obj)

    # check image base on extname, return True or False
    @staticmethod
    def image_file_ex(f):
        return image_file_ex(f)

    # check image, return img or None.
    @staticmethod
    def image_file(f):
        return image_file(f)

    # remove small size image.
    @staticmethod
    def remove_small_size_image(path, size=SMALL_IMG_SIZE):
        return remove_small_size_image(path, size)

    # remove small image, default width < IMG_W_MIN or height < IMG_H_MIN.
    @staticmethod
    def remove_small_image(path, width=IMG_W_MIN, height=IMG_H_MIN,
                           obj=None, remove_small_size_image=False):
        return remove_small_image(path, width, height,
                                  obj, remove_small_size_image)

    @staticmethod
    def reclaim_image(f, obj=None, rm_small_image=False):
        return reclaim_image(f, obj, rm_small_image)

    @staticmethod
    def reclaim_path_images(path, remove_small_image=False):
        return reclaim_path_images(path, remove_small_image)

    @staticmethod
    def set_order_images(path, rename=None, non_zero=False):
        return set_order_images(path, rename, non_zero)

    @staticmethod
    def get_image_detail(f):
        return get_image_detail(f)


############################################################################
#              run Functions
############################################################################

if __name__ == '__main__':
    from pybase.pysys import print_help
    from pybase.pyinput import get_input_args
    from pybase.pypath import get_abs_path

    HELP_MENU = (
        '============================================',
        '    PyImage - %s' % VERSION,
        '',
        '    @Author: %s' % AUTHOR,
        '    Copyright (c) %s studio' % AUTHOR,
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
        '    img: the path of image file.',
    )

    Img = PyImage()
    xval = None
    args = get_input_args('hc:r:R:x:o:i:')
    for k in args.keys():
        if k == '-c':
            result = Img.image_file(get_abs_path(args['-c']))
            print(result)
        elif k == '-r':
            data = args['-r'].split(',')
            path = data[0]
            if len(data) >= 3:
                w = data[1]
                h = data[2]
                Img.remove_small_image(path, int(w), int(h))
            else:
                Img.remove_small_image(path)
        elif k == '-R':
            path = args['-R']
            if Img.image_file(path):
                Img.reclaim_image(path)
            else:
                Img.reclaim_path_images(path)
        elif k == '-o':
            val = args['-o'].split(',')
            n = len(val)

            if n >= 3:
                Img.set_order_images(get_abs_path(val[0]), val[1], val[2])
            elif n == 2:
                Img.set_order_images(get_abs_path(val[0]), val[1])
            elif n == 1:
                Img.set_order_images(get_abs_path(val[0]))
            else:
                print('Error, -h for help!')
        elif k == '-i':
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
        elif k == '-h':
            print_help(HELP_MENU)
