#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on: 2018-12-11

@author: Byng Zeng
"""
import re

from mypy import MyPy
from webimage import WebImage

class Pstatp(WebImage):

    def __init__(self):
        super(Pstatp, self).__init__()
        self._url_base = 'https://www.toutiao.com/aURLID'
        self._path = '%s/Pstatp' %  MyPy.DEFAULT_DOWNLOAD_PATH
        self._re_image_url = re.compile('\"url\":\"(http://\w+\.pstatp\.com/[\w/-]+)\"')

    def update_url_content(self, url_content):
        if url_content:
            return re.sub('\\\\', '', url_content)

    def get_image_raw_url(self, url):
        return url

if __name__ == '__main__':
    ps = Pstatp()
    ps.main()
