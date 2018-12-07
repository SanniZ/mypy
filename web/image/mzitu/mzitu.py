#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on 2018-11-28

@author: Byng Zeng
"""

import re
import os

from mypy import MyBase, MyPath
from webcontent import WebImage
from image import Image

WEB_TXT = 'web.txt'

class Mzitu(object):

    help_menu = (
        '======================================',
        '     Mzitu Pictures',
        '======================================',
        'option: -s number -e number -p path -v',
        '  -s:',
        '    start of web number',
        '  -e:',
        '    end of web number',
        '  -p:',
        '    root path to store images.',
        '  -v:',
        '     show info while download.',
    )

    def __init__(self):
        self._start = None
        self._end = None
        self._dst = None
        self._show = False
        self.__url = 'https://m.mzitu.com'
        self.__re_img_url = re.compile('http(s)?://[a-zA-Z0-9/&_-]*?\.(jpg|gif|png|jpeg)', re.IGNORECASE)
        self.__re_prepages = re.compile('[0-9]+页')
        self.__re_pages = re.compile('[0-9]+')
        self.__re_title = re.compile('<span class="s\d+">.+</span>')

    def get_title(self, html_content):
        title = self.__re_title.search(html_content)
        if title:
            title = title.group()
        return title

    def get_pages(self, html_content):
        pages = self.__re_prepages.search(html_content)
        if pages:
            pages = self.__re_pages.search(pages.group())
            if pages:
                pages = pages.group()
        return pages

    def get_user_input(self):
        args = MyBase.get_user_input('hs:e:t:v')
        if '-h' in args:
            self.print_help()
        if '-s' in args:
            self._start = int(args['-s'])
        if '-e' in args:
            self._end = int(args['-e'])
        if '-t' in args:
            self._dst = os.path.abspath(args['-t'])
        if '-v' in args:
            self._show = True
        # start to check args.
        # start id is must be set, otherwise return..
        if not self._start:
            return False
        # next to start if _end is not set.
        if not self._end:
            self._end = self._start
        # path is not set, set default path now.
        if not self._dst:
            self._dst = MyBase.PATH_DWN
        # check start < end.
        if self._start > self._end:
            MyBase.print_exit('error: %d > %d\n' % (self._start, self._end))
        return True

    def main(self):
        if not self.get_user_input():
            MyBase.print_exit('Invalid input, -h for help.')
        # get web now.
        for index in range(self._start, self._end + 1):
            # get the first page.
            url = '%s/%s' % (self.__url, index)
            url_content = WebImage.get_url_content(url)
            if not url_content:
                print('warning: no content from %s' % url)
                continue
            # get url title.
            title = self.get_title(url_content)
            if not title:
                title = re.sub('(/|:|\.)', '_', url)
            # create path to store data.
            subpath = os.path.join(self._dst, title)
            MyPath.make_path(subpath)
            # get count of pages
            pages = self.get_pages(url_content)
            if not pages:
                MyBase.print_exit('Error, not get number of pages.')
            # loop for all of pages
            for page in range(int(pages)):
                # get sub pages.
                if page > 0:
                    url = '%s/%s/%d' % (self.__url, index, page + 1)
                    url_content = WebImage.get_url_content(url)
                # get pic url.
                imgs = WebImage.get_image_url(url_content, self.__re_img_url)
                for img in imgs:
                    WebImage.retrieve_url_image(subpath, img[0])
            # write web info.
            with open(os.path.join(subpath, WEB_TXT), 'w') as f:
		            f.write( '%s\n%s' % (title, url))
            # remove small image
            Image.remove_small_image(subpath)
            if self._show:
                print('output: %s/%s' % (subpath, title))

if __name__ == "__main__":
    mz = Mzitu()
    mz.main()
