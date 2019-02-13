#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on: 2018-12-11

@author: Byng Zeng
"""
import re

from web.webcontent import WebContent, USER_AGENTS
from web.webimage.webimage import WebImage


class Mzitu(WebImage):

    def __init__(self, name=None):
        super(Mzitu, self).__init__(name)
        self._url_base = 'https://m.mzitu.com/URLID'
        self._re_image_url = \
            re.compile('src=\"(http[s]?://.*meizitu.*\.(?:jpg|png|gif))\"',
                       flags=re.I)
        self._redundant_title = [' | 妹子图', ' - 妹子图', ' | 性感妹子', ' - 性感妹子']
        self._dl_image = self.urlopen_get_url_image

    def urlopen_get_url_image(self, url, path, view=False):
        headers = {
            'User-Agent': '%s' % USER_AGENTS['AppleWebKit/537.36'],
            'GET': url,
            'Referer': 'https://m.mzitu.com/',
        }
        return WebContent.urlopen_get_url_file(url, path,
                                               ssl=True,
                                               headers=headers, view=view)


if __name__ == '__main__':
    mz = Mzitu()
    mz.main()
