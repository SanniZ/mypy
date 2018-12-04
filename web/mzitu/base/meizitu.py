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
        print msg
    # stop runing and exit.
    exit()

def make_path(path):
	path = path.strip()
	if not os.path.exists(path):
	    os.makedirs(path)
	return path


def get_url_title(html_content):
    title_reg = '<title>.+</title>'
    patten = re.compile(title_reg)
    title = patten.search(html_content)
    if title != None:
        title = title.group()
        title = title[len('<title>') : len(title) - len(' | 妹子图</title>')]
    return title

def get_url_content(url, retry_times=2):
    print 'Downloading: ' , url
    try:
        send_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; rv:16.0) Gecko/20100101 Firefox/16.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Connection': 'keep-alive'
        }
        req = Request(url, headers=send_headers)
        html_content = urlopen(req).read().decode('gbk', 'ignore').encode('utf-8')
    except URLError, e:
        print e.reason
        html_content = None
        print "retry times:", retry_times
        if retry_times > 0:
            if hasattr(e, 'code') and 500 <= e.code < 600:
                get_url_content(url, retry_times - 1)
    return html_content

def get_pic_url(html_content):
    pic_reg = 'src="(http://.*?(png|jpg|gif))"'
    patten = re.compile(pic_reg, re.IGNORECASE)
    return patten.findall(html_content)

def save_pic_urllib(save_path, pic_url):
    save_pic_name = os.path.join(save_path, pic_url.split('/')[len(pic_url.split('/')) - 1])
    if not os.path.exists(save_pic_name):
        #print save_pic_name
        urllib.urlretrieve(pic_url, save_pic_name)
        # remove invalid pic
        remove_invalid_pic(save_pic_name)

def remove_invalid_pic(f):
    if os.path.exists(f) and os.path.isfile(f):
        try:
            img = Image.open(f)
            # remove low size image.
            if img.size[0] < IMG_MIN_W or img.size[1] < IMG_MIN_H:
                #print '%s: %s x %s, remove it' % (f, img.size[0], img.size[1])
                os.remove(f)
        except IOError as e:
            #print 'open %s failed, remove it' % f
            os.remove(f)


class Meizitu(object):

    # print help menu.
    @classmethod
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
        print_exit()

    def __init__(self):
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
            # check args.
            if self._path == None:  # set default path.
                self._path = '%s/妹子图' % os.getcwd()
            # no set start id.
            if self._start == None:
                return False
            # no set end id, set next to start.
            if self._end == None:
                self._end = self._start + 1
            # check start and end.
            if self._end < self._start:
                temp = self._start
                self._start = self._end
                self._end = temp
        return True

    def main(self):
        if self.get_user_input() != True:
            print_exit('Invalid input, -h for help.')
        # get web now.
        for index in range(self._start, self._end):
            url = 'http://www.meizitu.com/a/%s.html' % index
            url_content = get_url_content(url)
            if url_content:
                title = get_url_title(url_content)
                if title == None:
                    tilte = index
                subpath = os.path.join(self._path, title)
                make_path(subpath)
                pic_list = get_pic_url(url_content)
                for i in range(len(pic_list)):
                    pic_url = pic_list[i][0]
                    save_pic_urllib(subpath, pic_url)
                # write web info.
                with open(os.path.join(subpath, 'web.txt'), 'w') as f:
                    f.write( '%s\n%s' % (title, url))

if __name__ == "__main__":
    mz = Meizitu()
    mz.main()

