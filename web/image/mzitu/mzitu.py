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
        self._url = None
        self._end = None
        self._path = None
        self._show = False
        self.__base_url = 'https://m.mzitu.com'
        self.__re_img_url = re.compile('src=\"https://i.meizitu\.net/.+\.jpg', flags=re.I)
        self.__re_prepages = re.compile('/[0-9]+页')
        self.__re_pages = re.compile('[0-9]+')

    def get_title(self, title):
        return title[ : len(title) - len(' | 妹子图')]

    def get_pages(self, html_content):
        pages = self.__re_prepages.search(html_content)
        if pages:
            pages = self.__re_pages.search(pages.group())
            if pages:
                pages = pages.group()
        return pages

    def get_user_input(self):
        args = MyBase.get_user_input('hu:e:p:v')
        if '-h' in args:
            self.print_help()
        if '-u' in args:
            self._url = int(args['-u'])
        if '-e' in args:
            self._end = int(args['-e'])
        if '-p' in args:
            self._path = os.path.abspath(args['-p'])
        if '-v' in args:
            self._show = True
        # start to check args.
        # start id is must be set, otherwise return..
        if not self._url:
            return False
        # next to start if _end is not set.
        if not self._end:
            self._end = self._url
        # path is not set, set default path now.
        if not self._path:
            self._path = MyBase.PATH_DWN
        # check start < end.
        if self._url > self._end:
            MyBase.print_exit('error: %d > %d\n' % (self._url, self._end))
        return True

    def main(self):
        if not self.get_user_input():
            MyBase.print_exit('Invalid input, -h for help.')
        # get web now.
        for index in range(self._url, self._end + 1):
            # get the first page.
            url = '%s/%s' % (self.__base_url, index)
            url_content = WebImage.get_url_content(url)
            if not url_content:
                print('warning: no content from %s' % url)
                continue
            # get url title.
            title = WebImage.get_url_title(url_content)
            if title:
                title = self.get_title(title)
            else:
                title = re.sub('(/|:|\.)', '_', url)
            # create path to store data.
            subpath = os.path.join(self._path, title)
            MyPath.make_path(subpath)
            # get count of pages
            pages = self.get_pages(url_content)
            if not pages:
                MyBase.print_exit('Error, not get number of pages.')
            # loop for all of pages
            for page in range(int(pages)):
                # get sub pages.
                if page > 0:
                    url = '%s/%s/%d' % (self.__base_url, index, page + 1)
                    url_content = WebImage.get_url_content(url, show=False)
                # get pic url.
                imgs = WebImage.get_image_url(url_content, self.__re_img_url)
                #print imgs
                for img in imgs:
                    WebImage.retrieve_url_image(re.sub('src=\"', '', img), subpath)
            # write web info.
            with open(os.path.join(subpath, WebImage.WEB_URL_FILE), 'w') as f:
		            f.write( '%s\n%s' % (title, url))
            # remove small image
            Image.remove_small_image(subpath)
            if self._show:
                print('output: %s/%s' % (subpath, title))

if __name__ == "__main__":
    mz = Mzitu()
    mz.main()
