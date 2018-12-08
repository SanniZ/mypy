#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on 2018-11-28

@author: Byng Zeng
"""

import re
import os

from mypy import MyBase
from webcontent import WebImage
from image import Image

WEB_TXT = r'web.txt'

class Meizitu(object):

    help_menu = (
        '======================================',
        '     Meizitu Pictures',
        '======================================',
        'option: -u number -e number -p path -v',
        '  -u:',
        '    start of web url number',
        '  -e:',
        '    end of web number',
        '  -p:',
        '    root path to store images.',
        '  -v:',
        '     show info while download.',
    )

    def __init__(self):
        self.__re_img_url = re.compile('src="(http://.*?(png|jpg|gif))"', re.IGNORECASE)
        self.__base_url = 'http://www.meizitu.com/a'
        self._url = None
        self._end = None
        self._path = None
        self._show = False

    def get_user_input(self):
        args = MyBase.get_user_input('hu:e:p:v')
        if '-h' in args:
            MyBase.print_help(self.help_menu)
        if '-u' in args:
            self._url = int(args['-u'])
        if '-e' in args:
            self._end = int(args['-e'])
        if '-p' in args:
            self._path = os.path.abspath(args['-p'])
        if '-v' in args:
            self._show = True

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
        if self.get_user_input() != True:
            MyBase.print_exit('Invalid input, -h for help.')
        # get web now.
        for index in range(self._url, self._end + 1):
            url = '%s/%s.html' % (self.__base_url, index)
            url_content = WebImage.get_url_content(url)
            if not url_content:
                print('warning: no content from %s' % url)
                continue
            title = WebImage.get_url_title(url_content)
            if title:
                title = title[ : len(title) - len(' | 妹子图')]
            else:
                title = re.sub('(/|:|\.)', '_', url)
            subpath = os.path.join(self._path, title)
            imgs = WebImage.get_image_url(url_content, self.__re_img_url)
            for img in imgs:
                WebImage.retrieve_url_image(subpath, img[0])
            if imgs:
                # write web info.
                with open(os.path.join(subpath, WEB_TXT), 'w') as f:
                    f.write( '%s\n%s' % (title, url))
                # remove small image
                Image.remove_small_image(subpath)
                if self._show:
                    print('output: %s/%s' % (subpath, title))

if __name__ == "__main__":
    mz = Meizitu()
    mz.main()

