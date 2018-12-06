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

WEB_URL = r'WebUrl'

class Meizitu(object):

    help_menu = (
        '======================================',
        '     Meizitu Pictures',
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
        self.__re_picurl = re.compile('src="(http://.*?(png|jpg|gif))"', re.IGNORECASE)
        self.__url_base = 'http://www.meizitu.com/a'
        self._start = None
        self._end = None
        self._path = None

    def get_user_input(self):
        args = MyBase.get_user_input('hs:e:p:')
        if '-h' in args:
            MyBase.print_help(self.help_menu)
        if '-s' in args:
            self._start = int(args['-s'])
        if '-e' in args:
            self._end = int(args['-e'])
        if '-p' in args:
            self._path = os.path.abspath(args['-p'])
        # start to check args.
        # start id is must be set, otherwise return..
        if self._start == None:
            return False
        # next to start if _end is not set.
        if self._end == None:
            self._end = self._start
        # path is not set, set default path now.
        if self._path == None:
            self._path = '%s/Meizitu' % os.getcwd()
        # check start < end.
        if self._start > self._end:
            MyBase.print_exit('error: %d > %d\n' % (self._start, self._end))
        return True

    def get_pic_title(self, title):
		if title != None:
		    title = title.group()
		    title = title[len('<title>') : len(title) - len(' | 妹子图</title>')]
		return title

    def main(self):
        if self.get_user_input() != True:
            MyBase.print_exit('Invalid input, -h for help.')
        # get web now.
        for index in range(self._start, self._end + 1):
            url = '%s/%s.html' % (self.__url_base, index)
            url_content = WebImage.get_url_content(url)
            if url_content:
                title = WebImage.get_url_title(url_content)
                if title == None:
                    title = index
                else:
                    title = self.get_pic_title(title)
                subpath = os.path.join(self._path, title)
                pic_list = WebImage.get_pic_url(url_content, self.__re_picurl)
                for i in range(len(pic_list)):
                    pic_url = pic_list[i][0]
                    WebImage.retrieve_url_pic(subpath, pic_url)
                # write web info.
                with open(os.path.join(subpath, WEB_URL), 'w') as f:
                    f.write( '%s\n%s' % (title, url))
                # remove small image
                Image.remove_small_image(subpath)

if __name__ == "__main__":
    mz = Meizitu()
    mz.main()

