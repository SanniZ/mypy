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

IMG_W_MIN = 480
IMG_H_MIN = 480

SMALL_IMG_SIZE = 1024 * 10 # 10K

class Image (object):

    def __init__(self):
        #super(Image, self).__init__()
        pass

    @classmethod
    def image_file2(cls, f):
        exname = MyFile.get_exname(f)
        if exname in ['.jpg', '.png', '.gif', '.jpeg', '.bmp']:
            return True
        else:
            return False

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
        for rt, dirs, fs in os.walk(path):
            if len(fs) != 0:  # found files.
                for f in fs:
                    f = os.path.join(rt, f)
                    if cls.is_image(f) and os.path.getsize(f) < size:
                        os.remove(f)

    # remove small image, default width < IMG_W_MIN or height < IMG_H_MIN.
    @classmethod
    def remove_small_image(cls, f, width=IMG_W_MIN, height=IMG_H_MIN, obj=None):
        if obj:
            img = obj
        else:
            img = cls.image_file(f)
        # check size of image.
        if img:
            w, h = cls.get_image_size(img)
            if all((w, h)):
                if any((w < width, h < height)):
                    os.remove(f)
            else:  # fail to get size, remove it.
                os.remove(f)

    # remove small image, default width < IMG_W_MIN or height < IMG_H_MIN.
    @classmethod
    def remove_path_small_images(cls, path, width=IMG_W_MIN, height=IMG_H_MIN):
        for rt, dirs, fs in os.walk(path):
            if len(fs):  # found files.
                for f in fs:
                    f = os.path.join(rt, f)
                    cls.remove_small_image(f, width=width, height=height)

    @classmethod
    def get_image_size(cls, img):
        return img.size[0], img.size[1]

    @classmethod
    def reclaim_image(cls, f, obj=None, xfunc=None):
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
                os.rename(f, '%s.%s' % (f, fmt))
            elif fmt != ftype:
                    name = re.sub(ftype, fmt, f)
                    os.rename(f, name)
            # run xfunc
            if xfunc:
                xfunc(f, obj=img)

    @classmethod
    def reclaim_path_images(cls, path, xfunc=None):
        for rt, dr, fs in os.walk(path):
            if len(fs):
                for f in fs:
                    f = os.path.join(rt, f)
                    img = cls.image_file(f)
                    if img:
                        cls.reclaim_image(f, img, xfunc)

if __name__ == '__main__':
    Img = Image()
    w, h = Img.get_image_size('/home/yingbin/Downloads/10.jpg')
    if w and h:
        print w, h
