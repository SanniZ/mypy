#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Created on: 2019-01-16

@author: Zbyng.Zeng
"""
import re

from mypy.pybase import PyBase

from web.webimage.webimage import WebImage, get_input


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

    def get_url_from_search_links(self, url):
        html = self.get_url_content(url)
        pattern = re.compile("https://www.meitulu.com/item/\d+\.html")
        urls = pattern.findall(str(html))
        return urls


if __name__ == '__main__':
    mt = Meitulu('Weibo')
    args = get_input(exopt='S:')
    if '-h' in args:
        mt.help_menu.append('  -S url:')
        mt.help_menu.append('    url of web of search')
        PyBase.print_help(mt.help_menu)
    elif '-S' in args:
            urls = mt.get_url_from_search_links(args['-S'])
            del args['-S']
            for url in urls:
                args['-u'] = url
                mt.main(args)
    else:
        mt.main(args)
