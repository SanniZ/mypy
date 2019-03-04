#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on: 2019-01-09

@author: Byng.Zeng
"""

import re

from pybase.pyfile import reclaim_name

VERSION = '2.0.1'
AUTHOR = 'Byng.Zeng'


############################################################################
#               functions
############################################################################

def get_url_base_and_num(url):
    base = None
    num = None
    if url:
        txt = url.replace('.html', '')
        index = txt.rfind('/')
        if index != -1:
            num = txt[index + 1:]
            if not num.isdigit():
                n = re.compile('\d+').search(num)
                if n:
                    num = n.group()
        if num:
            base = url.replace(num, 'URLID')
    return base, num


def set_url_base_and_num(base, num):
    if type(num) is not str:
        num = str(num)
    if base:
        return re.sub('URLID', num, base)
    else:
        return num


def convert_url_to_title(url):
    return reclaim_name(re.sub('/$', '', url))


def reclaim_url_address(url):
    for key, value in {'/$': '', '\n$': ''}.items():
        url = re.sub(key, value, url)
    return url


############################################################################
#               WebUrl Class
############################################################################

class WebUrl(object):

    @staticmethod
    def get_url_base_and_num(url):
        return get_url_base_and_num(url)

    @staticmethod
    def set_url_base_and_num(base, num):
        return set_url_base_and_num(base, num)

    @staticmethod
    def convert_url_to_title(url):
        return convert_url_to_title(url)

    @staticmethod
    def reclaim_url_address(url):
        return reclaim_url_address(url)
