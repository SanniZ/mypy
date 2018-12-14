#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on: 2018-12-11

@author: Byng Zeng
"""
import re

from webcontent import WebContent
from webimage import WebImage

class Pstatp(WebImage):

    def __init__(self, name=None):
        super(Pstatp, self).__init__(name)
        self._url_base = 'https://www.toutiao.com/aURLID'
        self._re_image_url = re.compile('\"url\":\"(http://\w+\.pstatp\.com/[\w/-]+)\"')

    def get_url_content(self, url, view=False):
        url_content = WebContent.get_url_content(url=url, view=view)
        if url_content:
            return re.sub('\\\\', '', url_content)

if __name__ == '__main__':
    ps = Pstatp('toutiao')
    ps.main()
