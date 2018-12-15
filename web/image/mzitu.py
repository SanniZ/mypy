#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on: 2018-12-11

@author: Byng Zeng
"""
import re

from webimage import WebImage

class Mzitu(WebImage):

    def __init__(self, name=None):
        super(Mzitu, self).__init__(name)
        self._url_base = 'https://m.mzitu.com/URLID'
        self._re_image_url = re.compile('src=\"(http[s]?://.*meizitu.*\.(?:jpg|png|gif))\"', flags=re.I)
        self._redundant_title = [' | 妹子图', ' - 妹子图', ' | 性感妹子', ' - 性感妹子']

if __name__ == '__main__':
    mz = Mzitu()
    mz.main()
