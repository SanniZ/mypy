#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on: 2018-12-11

@author: Byng Zeng
"""
import re

from mypy import MyPy
from webimage import WebImage

class Mzitu(WebImage):

    def __init__(self):
        super(Mzitu, self).__init__()
        self._url_base = 'https://m.mzitu.com/URLID'
        self._path = '%s/Mzitu' %  MyPy.DEFAULT_DOWNLOAD_PATH
        self._re_image_url = re.compile('src=\"(http(s)?://.*meizitu.*\.(jpg|png|gif))', flags=re.I)

    def get_title(self, html, pattern=None):
        title = self.get_url_title(html, pattern)
        if title:
            title = title[ : len(title) - len(' | 妹子图')]
        return title

    def get_image_raw_url(self, url):
        return url[0]

if __name__ == '__main__':
    mz = Mzitu()
    mz.main()
