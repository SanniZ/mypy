#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Created on: 2019-01-16

@author: Zbyng.Zeng
"""
import re

from web.webimage.webimage import WebImage


class Meitulu(WebImage):

    def __init__(self, name=None):
        super(Meitulu, self).__init__(name)
        self._url_base = 'https://www.meitulu.com/item/URLID.html'
        self._sub_url_base = '_'

    def get_pages(self, html, pattern=None):
        if not pattern:
            pattern = re.compile(
                '<a href="/item/%s_\d+.html">(\d+)</a>' % (
                    self._url))
        data = pattern.findall(str(html))
        return int(data[-1])


if __name__ == '__main__':
    mt = Meitulu('Weibo')
    mt.main()