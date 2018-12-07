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

IMG_MIN_W = 480
IMG_MIN_H = 480


# print msg and exit
def print_exit(msg=None):
    if msg != None:
        print(msg)
    # stop runing and exit.
    exit()

def make_path(path):
	path = path.strip()
	if not os.path.exists(path):
	    os.makedirs(path)
	return path


def get_title(html_content):
    title_reg = '<title>.+</title>'
    patten = re.compile(title_reg)
    title = patten.search(html_content)
    if title != None:
        title = title.group()
        title = title[len('<title>') : len(title) - len(' | 妹子图</title>')]
    return title

def get_pages(html_content):
    pre_reg = re.compile('[0-9]+页')
    cnt_reg = re.compile('[0-9]+')
    pages = pre_reg.search(html_content)
    if pages != None:
         pages = cnt_reg.search(pages.group())
         if pages != None:
             pages = pages.group()
    return pages

def get_url_content(url, retry_times=2):
    print('Downloading: ' , url)
    try:
        send_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; rv:16.0) Gecko/20100101 Firefox/16.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Connection': 'keep-alive'
        }
        req = Request(url, headers=send_headers)
        html_content = urlopen(req).read().decode('gbk', 'ignore').encode('utf-8')
    except URLError, e:
        print(e.reason)
        html_content = None
        print("retry times: %s" % retry_times)
        if retry_times > 0:
            if hasattr(e, 'code') and 500 <= e.code < 600:
                get_url_content(url, retry_times - 1)
    return html_content

def get_pic_url(html_content, patten):
    return patten.findall(html_content)

def save_pic_urllib(save_path, pic_url):
    save_pic_name = os.path.join(save_path, pic_url.split('/')[len(pic_url.split('/')) - 1])
    if not os.path.exists(save_pic_name):
        #print(save_pic_name
        urllib.urlretrieve(pic_url, save_pic_name)
        # remove invalid pic
        remove_invalid_pic(save_pic_name)

def remove_invalid_pic(f):
    if os.path.exists(f) and os.path.isfile(f):
        try:
            img = Image.open(f)
            # remove low size image.
            if img.size[0] < IMG_MIN_W or img.size[1] < IMG_MIN_H:
                os.remove(f)
        except IOError as e:
            os.remove(f)


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
        print('  -p:')
        print('    root path to store images.')
        # exit here
        print_exit()

    def __init__(self):
        self.__url = 'https://www.mzitu.com'
        self.__re_pic = re.compile('http(s)?://(www|m)\.mzitu\.(com|cn)/[a-z0-9/&_-]*?\.(jpg|gif|png)', re.IGNORECASE)
        self._start = None
        self._end = None
        self._path = None

    def get_user_input(self):
        try:
            opts, args = getopt.getopt(sys.argv[1:], "hs:e:p:")
        except getopt.GetoptError:
            print_exit('Invalid input, -h for help.')
        # get input
        if len(opts) == 0:
            print_exit('Invalid input, -h for help.')
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
                print_exit('error: %d > %d\n' % (self._start, self._end))
        return True

    def main(self):
        if self.get_user_input() != True:
            print_exit('Invalid input, -h for help.')
        # get web now.
        for index in range(self._start, self._end + 1):
            # get the first page.
            url_content = get_url_content('%s/%s' % (self.__url, index))
            if url_content:
                # get url title.
                title = get_title(url_content)
                if title == None:
                    tilte = index
                # create path to store data.
	            subpath = os.path.join(self._path, title)
	            make_path(subpath)
                # get count of pages
                pages = get_pages(url_content)
                # loop for all of pages
                for page in range(1, pages + 1):
                    # the first page had been read while get web title.
                    if page != 1:
                        url_content = get_url_content('%s/%s/%s' % (self.__url, index, page))
                    # get pic url.
	                pic_list = get_pic_url(url_content, self.__re_pic)
                    # get all of pic.
                    for i in range(len(pic_list)):
                        pic_url = pic_list[i][0]
                        save_pic_urllib(subpath, pic_url)
		        # write web info.
		        with open(os.path.join(subpath, 'web.txt'), 'w') as f:
		            f.write( '%s\n%s' % (title, url))

if __name__ == "__main__":
    mz = Mzitu()
    mz.main()
