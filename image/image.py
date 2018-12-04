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

SMALL_IMG_SIZE = 1024 * 128 # 128K

class Image (object):

	def __init__(self):
		#super(Image, self).__init__()
		pass

	@classmethod
	def is_image(cls, f):
		exname = Base.get_exname(f)
		if exname in ['.jpg', 'png', 'gif']:
			return True
		else:
			return False

	@classmethod
	def remove_small_size_image(cls, path):
		for rt, dirs, fs in os.walk(path):
			if len(fs) != 0:
				for f in fs:
					f = os.path.join(rt, f)
					if Image.is_image(f) and os.path.getsize(f) < SMALL_IMG_SIZE:
						os.remove(f)

	@classmethod
	def remove_small_size_image2(cls, path):
		for rt, dirs, fs in os.walk(path):
			for i in range(len(fs)):
				f = os.path.join(rt, fs[i])
				if os.path.isfile(f) and Image.is_image(f):
					try:
						img = PilImg.open(f)
						if img.size[0] < IMG_W_MIN or img.size[1] < IMG_H_MIN:
							os.remove(f)
					except IOError as e:
						os.remove(f)

