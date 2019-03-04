#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on: 2019-01-16

@author: Byng.Zeng
"""
import re

from web.webimage.webimage import WebImage


class Weibo(WebImage):

    def __init__(self, name=None):
        super(Weibo, self).__init__(name)
        self._url_base = 'https://m.weibo.cn/detail/URLID'
        self._re_image_url = [
            re.compile(
                '\"url\": \"(https://\w+\.sinaimg\.cn/[\w/-]+)\"', re.I),
            re.compile('https://\w+\.sinaimg\.cn/[\w/-]+', re.I),
        ]

    def get_title(self, html, pattern=None):
        html = html.decode()
        # get screen_name and status_title
        screen_name = re.compile(
                        '(?<=\"screen_name": \").+(?=\")', re.I).search(html)
        status_title = re.compile(
                        '(?<=\"status_title\": \").+(?=\")', re.I).search(html)
        # get title.
        if all((screen_name, status_title)):
            title = '%s: %s' % (screen_name.group(), status_title.group())
        elif status_title:
            title = status_title.group()
        else:
            title = None

        return title

if __name__ == '__main__':
    wb = Weibo('Weibo')
    wb.main()
