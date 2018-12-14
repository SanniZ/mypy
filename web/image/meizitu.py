#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on: 2018-12-11

@author: Byng Zeng
"""
#import re

from webcontent import WebContent
from webimage import WebImage

class Meizitu(WebImage):

    def __init__(self, name=None):
        super(Meizitu, self).__init__(name)
        self._url_base = 'http://www.meizitu.com/a/URLID.html'
        #self._re_image_url = re.compile('src=\"(http://.*?(?:png|jpg|gif))\"', re.IGNORECASE)

    def get_title(self, html, pattern=None):
        title = WebContent.get_url_title(html, pattern)
        if title:
            title = title[ : len(title) - len(' | 妹子图')]
        return title

if __name__ == '__main__':
    mz = Meizitu()
    mz.main()
