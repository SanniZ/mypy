#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on 2018-12-03

@author: Byng Zeng
"""

import os
from PIL import Image as PilImg

from mypy import MyFile

IMG_W_MIN = 480
IMG_H_MIN = 480

SMALL_IMG_SIZE = 1024 * 10 # 10K

class Image (object):

    def __init__(self):
        #super(Image, self).__init__()
        pass

    @classmethod
    def is_image(cls, f):
        exname = MyFile.get_exname(f)
        if exname in ['.jpg', '.png', '.gif', '.jpeg', '.bmp']:
            return True
        else:
            return False

    # remove small size image, default size is 10K.
    @classmethod
    def remove_small_size_image(cls, path, size=SMALL_IMG_SIZE):
        for rt, dirs, fs in os.walk(path):
            if len(fs) != 0:  # found files.
                for f in fs:
                    f = os.path.join(rt, f)
                    if Image.is_image(f) and os.path.getsize(f) < size:
                        os.remove(f)

    # remove small image, default width < IMG_W_MIN or height < IMG_H_MIN.
    @classmethod
    def remove_small_image(cls, path, width=IMG_W_MIN, height=IMG_H_MIN):
        for rt, dirs, fs in os.walk(path):
            if len(fs) != 0:  # found files.
                for f in fs:
                    f = os.path.join(rt, f)
                    if Image.is_image(f):
                        w, h = Image.get_image_size(f)
                        # check size
                        if w and h:
                            if w < width or h < height:
                                os.remove(f)
                        else:  # fail to get size, remove it.
                            os.remove(f)

    @classmethod
    def get_image_size(self, f):
        w = None
        h = None
        if Image.is_image(f):
            try:
                img = PilImg.open(f)
                w, h = img.size[0], img.size[1]
            except IOError: # it is bad if open failed.
                w, h = None, None
        return w, h

if __name__ == '__main__':
    Img = Image()
    w, h = Img.get_image_size('/home/yingbin/Downloads/10.jpg')
    if w and h:
        print w, h
