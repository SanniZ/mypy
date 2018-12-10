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
from image import Image


class DownloadWebImage(object):

    help_menu = (
        '==================================',
        '    DownloadWebImage help',
        '==================================',
        'option: -u number -p path -v',
        '  -u:',
        '    url of web to be download',
        '  -p:',
        '    root path to store images.',
        '  -v:',
        '     show info while download.',
    )

    def __init__(self):
        self._url = None
        self._path = '%s/DownloadWebImage' % MyBase.PATH_DWN
        self._show = False
        self.__re_img_url = re.compile('(src=|src=\'|src=\")(http(s)?://[\w\-\/\.]*?\.(jpg|png|gif))(\'|\")?', re.IGNORECASE)
        self._show = True

    def get_user_input(self):
        args = MyBase.get_user_input('hu:n:p:v')
        if '-h' in args:
            MyBase.print_help(self.help_menu)
        if '-p' in args:
            self._path = os.path.abspath(args['-p'])
        if '-u' in args:
            self._url = args['-u']
        if '-v' in args:
            self._show = True
        if not self._url:
            MyBase.print_exit('Error, no set url, -h for help!')


    def download_image(self, url):
        url_content = WebImage.get_url_content(url, self._show)
        if not url_content:
            print('warning: no content from %s' % url)
            return
        #print url_content
        title = WebImage.get_url_title(url_content)
        if not title:
            title = WebImage.convert_url_to_title(url)
        # path for store image.
        path = '%s/%s' % (self._path, title)
        # get all of image url.
        imgs = WebImage.get_image_url(url_content, self.__re_img_url)
        for img in imgs:
            WebImage.retrieve_url_image(img[1], path)
        if imgs:
            with open('%s/%s' % (path, WebImage.WEB_URL_FILE), 'w') as f:
                f.write('%s\n%s' % (title, url))
            # remove small image
            Image.remove_small_image(path, width=320, height=320)
            if self._show:
                print('output: %s' % (path))

    def main(self):
        self.get_user_input()
        # download image of url.
        self.download_image(self._url)

if __name__ == '__main__':
    dwimg = DownloadWebImage()
    dwimg.main()
