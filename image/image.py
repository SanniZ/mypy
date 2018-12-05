#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on 2018-12-03

@author: Byng Zeng
"""

import os
from PIL import Image as PilImg

from base import MyBase as Base

IMG_W_MIN = 480
IMG_H_MIN = 480

SMALL_IMG_SIZE = 1024 * 10 # 10K

class Image (object):

    def __init__(self):
        #super(Image, self).__init__()
        pass

    @classmethod
    def is_image(cls, f):
        exname = Base.get_exname(f)
        if exname in ['.jpg', 'png', 'gif', '.jpeg', '.bmp']:
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
                        try:
                            img = PilImg.open(f)
                            if img.size[0] < width or img.size[1] < height:
                                os.remove(f)
                        except IOError: # it is bad if open failed.
                            os.remove(f)

