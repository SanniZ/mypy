#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on: 2018-12-07

@author: Byng Zeng
"""
import os
import re

from mypy import MyBase
from webcontent import WebImage

class PstatpImage(object):

    help_menu = (
        '==================================',
        '    PstatpImage help',
        '==================================',
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
        self._url_base = 'https://www.toutiao.com/aURLID'
        self._url = None
        self._num = 1
        self._path = '%s/PstatpImage' % MyBase.PATH_DWN
        self._show = False
        self.__re_img_url = re.compile('\"url\":\"(http://\w+\.pstatp\.com/[\w/-]+)\"')

    def get_user_input(self):
        args = MyBase.get_user_input('hu:n:p:v')
        if '-h' in args:
            MyBase.print_help(self.help_menu)
        if '-p' in args:
            self._path = os.path.abspath(args['-p'])
        if '-u' in args:
            self._url = args['-u']
        if '-n' in args:
            self._num = int(args['-n'])
        if '-v' in args:
            self._show = True
        if self._url:
            base, num = WebImage.get_url_base_and_num(self._url)
            if base:
                self._url_base = base
            if num:
                self._url = num
        else:
            MyBase.print_exit('Error, no set url, -h for help!')

    def get_image_url(self, url):
        return url[len('\"url\":\"') : len(url) - len('\"')]

    def download_image(self, url):
        url_content = WebImage.get_url_content(url)
        try:
            url_content = re.sub('\\\\', '', url_content)
        except TypeError as e:
            print(e.message)
        if not url_content:
            print('warning: no content from %s' % url)
            return
        title = WebImage.get_url_title(url_content)
        if not title:
            title = WebImage.convert_url_to_title(url)
        # path for store image.
        path = '%s/%s' % (self._path, title)
        # get all of image url.
        imgs = WebImage.get_image_url(url_content, self.__re_img_url)
        for img in imgs:
            WebImage.retrieve_url_image(img, path)
        if imgs:
            with open('%s/%s' % (path, WebImage.WEB_URL_FILE), 'w') as f:
                f.write('%s\n%s' % (title, url))
            if self._show:
                print('output: %s' % path)

    def download_images(self):
        for index in range(self._num):
            url = WebImage.set_url_base_and_num(self._url_base, int(self._url) + index)
            self.download_image(url)


    def main(self):
        self.get_user_input()
        # download image of url.
        self.download_images()

if __name__ == '__main__':
    pstatp = PstatpImage()
    pstatp.main()