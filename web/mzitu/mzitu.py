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

from PIL import Image as PILImg

from base import MyBase as Base
from webcontent import WebImage as WebImg
from image import Image as Img

WEB_URL = 'WebUrl'

class Mzitu(object):

    # print(help menu.
    @classmethod
    def print_help(cls):
        print('======================================')
        print('     Mzitu Pictures')
        print('======================================')
        print('option: -s number -e number -p path')
        print('  -s:')
        print('    start of web number')
        print('  -e:')
        print('    end of web number')
        print('  -t:')
        print('    root path to store images.')
        # exit here
        Base.print_exit()

    def __init__(self):
        self._start = None
        self._end = None
        self._dst = None
        self.__url = 'https://m.mzitu.com'
        self.__re_pic = re.compile('http(s)?://[a-zA-Z0-9/&_-]*?\.(jpg|gif|png)', re.IGNORECASE)
        self.__re_prepages = re.compile('[0-9]+页')
        self.__re_pages = re.compile('[0-9]+')
        self.__re_title = re.compile('<span class="s\d+">.+</span>')

	def get_title(self, html_content):
		title = __re_title.search(html_content)
		return title.group()

	def get_pages(self, html_content):
		pages = self.__re_prepages.search(html_content)
		if pages != None:
		     pages = self.__re_pages.search(pages.group())
		     if pages != None:
		         pages = pages.group()
		return pages

    def get_user_input(self):
        try:
            opts, args = getopt.getopt(sys.argv[1:], "hs:e:t:")
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
                elif name == '-t':
                    self._dst = os.path.abspath(value)
            # start to check args.
            # start id is must be set, otherwise return..
            if self._start == None:
                return False
            # next to start if _end is not set.
            if self._end == None:
                self._end = self._start
            # path is not set, set default path now.
            if self._dst == None:
                self._dst = '%s/妹子图' % os.getcwd()
            # check start < end.
            if self._start > self._end:
                Base.print_exit('error: %d > %d\n' % (self._start, self._end))
        return True

    def main(self):
        if self.get_user_input() != True:
            Base.print_exit('Invalid input, -h for help.')
        # get web now.
        for index in range(self._start, self._end + 1):
            # get the first page.
            url = '%s/%s' % (self.__url, index)
            url_content = WebImg.get_url_content(url)
            if url_content:
                # get url title.
                title = self.get_title(url_content)
                if title == None:
                    tilte = 'mzitu_%s' % index
                # create path to store data.
	            subpath = os.path.join(self._dst, title)
                # get count of pages
                pages = self.get_pages(url_content)
                # loop for all of pages
                for page in range(1, pages + 1):
                    # get sub pages.
                    if page != 1:
                        url = '%s/%s/%s' % (self.__url, index, page)
                        url_content = WebImg.get_url_content(url)
                    # get pic url.
	                pic_list = WebImg.get_pic_url(url_content, self.__re_pic)
                    # get all of pic.
                    for i in range(len(pic_list)):
                        pic_url = pic_list[i]
                        WebImg.save_url_pic(subpath, pic_url)
		        # write web info.
                with open(os.path.join(subpath, WEB_URL), 'w') as f:
		            f.write( '%s\n%s' % (title, url))
        # remove small size of pic
        Img.remove_small_size_image(self._dst)

if __name__ == "__main__":
    mz = Mzitu()
    mz.main()
