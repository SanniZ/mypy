#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on: 2019-02-01

@author: Byng.Zeng
"""
import re

from pybase.pysys import print_help
from pybase.pypath import DEFAULT_DWN_PATH
from pybase.pydecorator import get_input_args
from web.webimage.webimage import WebImage, OPTS

VERSION = '1.0.2'
AUTHOR = 'Byng.Zeng'


class Meitulu(WebImage):

    URL_BASE_MAP = {
        # xval:  [url_base, class]
        'meitulu_t': ['https://www.meitulu.com/t/URLID', None],

    }

    def __init__(self, name=None):
        super(Meitulu, self).__init__(name)
        self._url_base = 'https://www.meitulu.com/item/URLID.html'
        self._sub_url_base = '_'

    @get_input_args()
    def process_input(self, opts, args=None):
        args = super(Meitulu, self).process_input(opts, args=args)
        cls = None
        if self._xval in self.URL_BASE_MAP:
            self._url_base = self.URL_BASE_MAP[self._xval][0]
            cls = self.URL_BASE_MAP[self._xval][1]
            self._pr.pr_dbg(
                'get url_base: %s from -x %s' % (self._url_base, self._xval))
        if self._url_base:
            if all((not self._path, cls)):
                self._path = '%s/%s/%s' % (
                    DEFAULT_DWN_PATH, self.__class__.__name__, cls)

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

    def search_urls_from_keyword(self, url):
        result = None
        if url:
            if url.startswith('https://www.meitulu.com/t/'):
                urls = self.get_url_from_search_links(url)
                if urls:
                    result = {'search_urls': urls}
        return result


if __name__ == '__main__':
    mt = Meitulu('Meitulu')
    args = get_input_args(OPTS + 'S:')
    for k in args.keys():
        if k == '-S':
                urls = mt.get_url_from_search_links(args['-S'])
                del args['-S']
                n = len(urls)
                for index, url in enumerate(urls):
                    print('[%d/%d] downloading: %s' % (index, n, url))
                    args['-u'] = url
                    mt.main(args)
        elif k == '-h':
            mt.HELP_MENU.append('  -S url:')
            mt.HELP_MENU.append('    url of web of search')
            print_help(mt.HELP_MENU)
        else:
            mt.main(args)
