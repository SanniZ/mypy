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

WEB_TXT = r'web.txt'

class PstatpImage(object):

    help_menu = (
        '==================================',
        '    TestHttps help',
        '==================================',
        'option: -p path -u url -x num',
        '  -p path: path to store data',
        '  -u url : web url address',
        '  -x num : number of web will be download.',
    )

    URL_BASE = 'https://www.toutiao.com/a'

    def __init__(self):
        self._path = None
        self._url = None
        self._max = None
        self._show = False

    def get_input(self):
        args = MyBase.get_user_input('hp:u:x:v')
        if '-h' in args:
            MyBase.print_help(self.help_menu)
        if '-p' in args:
            self._path = os.path.abspath(args['-p'])
        if '-u' in args:
            self._url = args['-u']
        if '-x' in args:
            self._max = int(args['-x'])
        if '-v' in args:
            self._show = True

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
            title = re.sub('(/|:|\.)', '_', url)
        path = '%s/%s' % (self._path, title)
        imgs = WebImage.get_image_url(url_content, re.compile('\"url\":\"http://\w+\.pstatp\.com/[a-zA-Z0-9/-]+\"'))
        for img in imgs:
            img = img[len('\"url\":\"') : len(img) - len('\"')]
            WebImage.retrieve_url_image(path, img)
        if imgs:
            with open('%s/%s' % (path, WEB_TXT), 'w') as f:
                f.write('%s\n%s' % (title, url))
            if self._show:
                print('output: %s' % path)

    def download_images(self):
        if self._max:
            data = re.compile('\d+').search(self._url)
            if data:
                url_num = int(data.group())
            else:
                MyBase.print_exit('Error, can`t get URL.')
            for index in range(self._max):
                url = '%s%d' % (self.URL_BASE, url_num + index)
                self.download_image(url)
        else:
            self.download_image(self._url)


    def main(self):
        self.get_input()
        if not self._url:
            MyBase.print_exit('Error, no set url, -h for help!')
        if not self._path:
            self._path = MyBase.PATH_DWN
        # download image of url.
        self.download_images()

if __name__ == '__main__':
    pstatp = PstatpImage()
    pstatp.main()
