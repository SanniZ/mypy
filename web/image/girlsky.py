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


class GirlSky(object):

    help_menu = (
        '======================================',
        '     GirlSky Pictures',
        '======================================',
        'option: -u url -n number -p path -v',
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
        self._url_base = 'http://m.girlsky.cn/mntp/rtys/URLID.html'
        self._url = None
        self._num = 1
        self._path = self._path = '%s/Girlsky' % MyBase.PATH_DWN
        self._show = False
        self.__re_img_url = re.compile('src=\"(http(s)?://.*\.(jpg|png|gif))', flags=re.I)

    def get_title(self, title):
        return title[ : len(title) - len(' | 妹子图')]

    def get_user_input(self):
        args = MyBase.get_user_input('hu:n:p:v')
        if '-h' in args:
            self.print_help()
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

    def get_url_pages(self, html):
        pattern = re.compile('\d+/\d+')
        pages =  pattern.findall(html)
        for page in pages:
            page = page.split('/')
            if page[0] < page[1]:
                return int(page[1])

    def main(self):
        self.get_user_input()
        # get web now.
        for index in range(self._num):
            # get the first page.
            url = WebImage.set_url_base_and_num(self._url_base, int(self._url) + index)
            url_content = WebImage.get_url_content(url)
            if not url_content:
                print('warning: no content from %s' % url)
                continue
            # get url title.
            title = WebImage.get_url_title(url_content)
            if title:
                title = self.get_title(title)
            else:
                title = WebImage.convert_url_to_title(url)
            # create path to store data.
            subpath = os.path.join(self._path, title)
            MyPath.make_path(subpath)
            # get count of pages
            pages = self.get_url_pages(url_content)
            if not pages:
                MyBase.print_exit('Error, not get number of pages.')
            # loop for all of pages
            for page in range(1, pages + 1):
                # get sub pages.
                if page > 1:
                    sub_url = WebImage.set_url_base_and_num(self._url_base, '%d_%d' % (int(self._url), page))
                    url_content = WebImage.get_url_content(sub_url, show=False)
                # get pic url.
                imgs = WebImage.get_image_url(url_content, self.__re_img_url)
                #print imgs
                for img in imgs:
                    WebImage.retrieve_url_image(img[0], subpath)
            # write web info.
            with open(os.path.join(subpath, WebImage.WEB_URL_FILE), 'w') as f:
		            f.write( '%s\n%s' % (title, url))
            # remove small image
            Image.remove_small_image(subpath)
            if self._show:
                print('output: %s/%s' % (subpath, title))

if __name__ == "__main__":
    gs = GirlSky()
    gs.main()
