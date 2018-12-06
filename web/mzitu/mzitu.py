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

WEB_URL = 'WebUrl'

class Mzitu(object):

    help_menu = (
        '======================================',
        '     Mzitu Pictures',
        '======================================',
        'option: -s number -e number -p path',
        '  -s:',
        '    start of web number',
        '  -e:',
        '    end of web number',
        '  -p:',
        '    root path to store images.',
    )

    def __init__(self):
        self._start = None
        self._end = None
        self._dst = None
        self.__url = 'https://m.mzitu.com'
        self.__re_pic = re.compile('http(s)?://[a-zA-Z0-9/&_-]*?\.(jpg|gif|png|jpeg)', re.IGNORECASE)
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
        args = MyBase.get_user_input('hs:e:t:')
        if '-h' in args:
            self.print_help()
        if '-s' in args:
            self._start = int(args['-s'])
        if '-e' in args:
            self._end = int(args['-e'])
        if '-t' in args:
            self._dst = os.path.abspath(args['-t'])
        # start to check args.
        # start id is must be set, otherwise return..
        if self._start == None:
            return False
        # next to start if _end is not set.
        if self._end == None:
            self._end = self._start
        # path is not set, set default path now.
        if self._dst == None:
            self._dst = '%s/Mzitu' % os.getcwd()
        # check start < end.
        if self._start > self._end:
            MyBase.print_exit('error: %d > %d\n' % (self._start, self._end))
        return True

    def main(self):
        if self.get_user_input() != True:
            MyBase.print_exit('Invalid input, -h for help.')
        # get web now.
        for index in range(self._start, self._end + 1):
            # get the first page.
            url = '%s/%s' % (self.__url, index)
            url_content = WebImage.get_url_content(url)
            if url_content:
                # get url title.
                title = self.get_title(url_content)
                if title == None:
                    title = 'Mzitu_%s' % index
                # create path to store data.
	        subpath = os.path.join(self._dst, title)
                MyPath.make_path(subpath)
                # get count of pages
                pages = self.get_pages(url_content)
                if not pages:
                    pages = 1
                # loop for all of pages
                for page in range(1, int(pages) + 1):
                    # get sub pages.
                    if page != 1:
                        url = '%s/%s/%s' % (self.__url, index, page)
                        url_content = WebImage.get_url_content(url)
                    # get pic url.
	            pic_list = WebImage.get_pic_url(url_content, self.__re_pic)
                    # get all of pic.
                    for i in range(len(pic_list)):
                        pic_url = pic_list[i]
                        WebImage.save_url_pic(subpath, pic_url)
		        # write web info.
                with open(os.path.join(subpath, WEB_URL), 'w') as f:
		            f.write( '%s\n%s' % (title, url))
                # remove small image
                Image.remove_small_image(subpath)

if __name__ == "__main__":
    mz = Mzitu()
    mz.main()
