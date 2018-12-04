#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on 2018-11-28

@author: Byng Zeng
"""

from urllib2 import Request, URLError, urlopen
import re
import urllib
import os
import sys
import getopt
from PIL import Image

from base import MyBase as Base
from webcontent import WebImage as WebImg
from image import Image as Img

WEB_URL = r'WebUrl'

class Meizitu(object):

    @classmethod
    # print help menu.
    def print_help(cls):
        print '======================================'
        print '     Meizitu Pictures'
        print '======================================'
        print 'option: -s number -e number -p path'
        print '  -s:'
        print '    start of web number'
        print '  -e:'
        print '    end of web number'
        print '  -p:'
        print '    root path to store images.'
        # exit here
        Base.print_exit()

    def __init__(self):
        self.__re_picurl = re.compile('src="(http://.*?(png|jpg|gif))"', re.IGNORECASE)
        self.__url_base = 'http://www.meizitu.com/a'
        self._start = None
        self._end = None
        self._path = None

    def get_user_input(self):
        try:
            opts, args = getopt.getopt(sys.argv[1:], "hs:e:p:")
        except getopt.GetoptError:
            Base.print_exit('Invalid input, -h for help.')
        # get input
        if len(opts) == 0:
            Base.print_exit('Invalid input, -h for help.')
        else:        
            for name, value in opts:
                if name == '-h':
                    self.print_help()
                elif name == '-s':
                    self._start = int(value)
                elif name == '-e':
                    self._end = int(value)
                elif name == '-p':
                    self._path = os.path.abspath(value)
            # start to check args.
            # start id is must be set, otherwise return..
            if self._start == None:
                return False
            # next to start if _end is not set.
            if self._end == None:
                self._end = self._start
            # path is not set, set default path now.
            if self._path == None:
                self._path = '%s/妹子图' % os.getcwd()
            # check start < end.
            if self._start > self._end:
                Base.print_exit('error: %d > %d\n' % (self._start, self._end))
        return True

    def get_pic_title(self, title):
		if title != None:
		    title = title.group()
		    title = title[len('<title>') : len(title) - len(' | 妹子图</title>')]
		return title

    def main(self):
        if self.get_user_input() != True:
            Base.print_exit('Invalid input, -h for help.')
        # get web now.
        for index in range(self._start, self._end + 1):
            url = '%s/%s.html' % (self.__url_base, index)
            url_content = WebImg.get_url_content(url)
            if url_content:
                title = WebImg.get_url_title(url_content)
                if title == None:
                    title = index
                else:
                    title = self.get_pic_title(title)
                subpath = os.path.join(self._path, title)
                pic_list = WebImg.get_pic_url(url_content, self.__re_picurl)
                for i in range(len(pic_list)):
                    pic_url = pic_list[i][0]
                    WebImg.retrieve_url_pic(subpath, pic_url)
                # write web info.
                with open(os.path.join(subpath, WEB_URL), 'w') as f:
                    f.write( '%s\n%s' % (title, url))
                # remove small image
                Img.remove_small_size_image(subpath)

if __name__ == "__main__":
    mz = Meizitu()
    mz.main()

