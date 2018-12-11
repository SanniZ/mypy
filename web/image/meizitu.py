#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on: 2018-12-11

@author: Byng Zeng
"""
import re

from mypy import MyPy
from webimage import WebImage

class Meizitu(WebImage):

    def __init__(self):
        super(Meizitu, self).__init__()
        self._url_base = 'http://www.meizitu.com/a/URLID.html'
        self._path = '%s/Meizitu' %  MyPy.DEFAULT_DOWNLOAD_PATH
        self._re_image_url = re.compile('src="(http://.*?(png|jpg|gif))"', re.IGNORECASE)

    def get_title(self, html, pattern=None):
        title = self.get_url_title(html, pattern)
        if title:
            title = title[ : len(title) - len(' | 妹子图')]
        return title

    def get_image_raw_url(self, url):
        return url[0]

if __name__ == '__main__':
    mz = Meizitu()
    mz.main()
