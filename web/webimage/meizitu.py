#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on: 2018-12-11

@author: Byng Zeng
"""

from web.webimage.webimage import WebImage


class Meizitu(WebImage):

    def __init__(self, name=None):
        super(Meizitu, self).__init__(name)
        self._url_base = 'http://www.meizitu.com/a/URLID.html'
        self._redundant_title = [' | 妹子图', ' - 妹子图', ' | 性感妹子', ' - 性感妹子']

if __name__ == '__main__':
    mz = Meizitu()
    mz.main()
