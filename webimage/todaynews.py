#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on 2018-11-29

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
def stop_and_exit(msg=None):
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
    pic_reg = 'http://p[0-9]+\.pstatp\.com[a-z0-9/-]+'
    patten = re.compile(pic_reg, re.IGNORECASE)
    return patten.findall(html_content)

def save_pic_urllib(save_path, pic_url):
    save_pic_name = os.path.join(save_path, 'img.jpg')
    if not os.path.exists(save_pic_name):
        print pic_url
        print save_pic_name
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


class WebPic(object):

    # print help menu.
    @classmethod
    def print_help(cls):
        print '======================================'
        print '     WebPic Pictures'
        print '======================================'
        print 'option: -u url -p path'
        print '  -u:'
        print '    url of web'
        print '  -p:'
        print '    root path to store images.'
        # exit here
        stop_and_exit()

    def __init__(self):
        self._url = None
        self._path = None

    def set_url(self, url):
        patten = re.compile('http(s)?://.+')
        if patten.findall(url) == None:
            self._url = 'http://%s' % url
        else:
            self._url = url

    def set_path(self, path):
        self._path = os.path.abspath(path)

    def get_user_input(self):
        try:
            opts, args = getopt.getopt(sys.argv[1:], "hu:p:")
        except getopt.GetoptError:
            stop_and_exit('Invalid input, -h for help.')
        # get input
        if len(opts) == 0:
            stop_and_exit('Invalid input, -h for help.')
        else:        
            for name, value in opts:
                if name == '-h':
                    self.print_help()
                elif name == '-u':
                    patten = re.compile('http(s)?://.+')
                    if patten.match(value) == None:
                        self._url = 'http://%s' % value
                    else:
                        self._url = value
                elif name == '-p':
                    self._path = os.path.abspath(value)
        # set default path.
        if self._path == None:  # set default path.
            self._path = '%s/WebPic' % os.getcwd()

    def get_web_count(self, url_content):
    

    def save_web_pic(self):
        if self._url == None:
            stop_and_exit('Not set url, -h for help.')
        if self._path == None:
            stop_and_exit('Not set path, -h for help.')
        # get web now.
        url_content = get_url_content(self._url)
        if url_content:
            url_content = url_content.replace(r'\\', '')
            title = get_url_title(url_content)
            if title == None:
                title = 'images'
            subpath = os.path.join(self._path, title)
            make_path(subpath)
            pic_list = get_pic_url(url_content)
            for i in range(len(pic_list)):
                pic_url = pic_list[i]
                save_pic_urllib(subpath, pic_url)
            # write web info.
            with open(os.path.join(subpath, 'web.txt'), 'w') as f:
                f.write( '%s\n%s' % (title, self._url))
                #f.write(url_content)

    def main(self):
        # get user input
        self.get_user_input()
        # check url
        if self._url == None:
            stop_and_exit('Not set url, -h for help.')
        self.save_web_pic()

if __name__ == "__main__":
    wp = WebPic()
    wp.main()

