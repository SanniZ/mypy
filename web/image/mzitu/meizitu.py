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


class Meizitu(object):

    help_menu = (
        '======================================',
        '     Meizitu Pictures',
        '======================================',
        'option: -u number -n number -p path -v',
        '  -u:',
        '    url of web to be download',
        '  -n:',
        '    number of web number to be download',
        '  -p:',
        '    root path to store images.',
        '  -v:',
        '     show info while download.',
    )

    def __init__(self):
        self._url_base = 'http://www.meizitu.com/a/URLID.html'
        self._url = None
        self._num = 1
        self._path = '%s/Meizitu' % MyBase.PATH_DWN
        self._show = False
        self.__re_img_url = re.compile('src="(http://.*?(png|jpg|gif))"', re.IGNORECASE)


    def get_url(self, data):
        nums = re.compile('^\d+$').match(data)
        if nums:  # all of numbers.
            self._url = int(nums.group())
        else:  # parse url and base_url.
            nums = re.compile('\d+$').search(data)
            if nums:
                self._url_base = data[ : len(data) - len(nums.group())]
                self._url = int(nums.group())

    def get_user_input(self):
        args = MyBase.get_user_input('hu:n:p:v')
        if '-h' in args:
            MyBase.print_help(self.help_menu)
        if '-u' in args:
            self._url = args['-u']
        if '-n' in args:
            self._num = int(args['-n'])
        if '-p' in args:
            self._path = os.path.abspath(args['-p'])
        if '-v' in args:
            self._show = True
        # check url
        if self._url:
            base, num = WebImage.get_url_base_and_num(self._url)
            if base:
                self._url_base = base
            if num:
                self._url = num
        else:
            MyBase.print_exit('Error, no set url, -h for help!')

    def get_title(self, title):
        return title[ : len(title) - len(' | 妹子图')]

    def main(self):
        self.get_user_input()
        # get web now.
        for index in range(self._num):
            url = WebImage.set_url_base_and_num(self._url_base, int(self._url) + index)
            url_content = WebImage.get_url_content(url)
            if not url_content:
                print('warning: no content from %s' % url)
                continue
            title = WebImage.get_url_title(url_content)
            if title:
                title = self.get_title(title)
            else:
                title = WebImage.convert_url_to_title(url)
            subpath = os.path.join(self._path, title)
            imgs = WebImage.get_image_url(url_content, self.__re_img_url)
            for img in imgs:
                WebImage.retrieve_url_image(img[0], subpath)
            if imgs:
                # write web info.
                with open(os.path.join(subpath, WebImage.WEB_URL_FILE), 'w') as f:
                    f.write( '%s\n%s' % (title, url))
                # remove small image
                Image.remove_small_image(subpath)
                if self._show:
                    print('output: %s/%s' % (subpath, title))


if __name__ == "__main__":
    mz = Meizitu()
    mz.main()

