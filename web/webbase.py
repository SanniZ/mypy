#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on: 2019-01-09

@author: Zbyng Zeng
"""

import re

from mypy.pyfile import PyFile

VERSION = '2.0.0'


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
    return PyFile.reclaim_name(re.sub('/$', '', url))


def reclaim_url_address(url):
    for key, value in {'/$': '', '\n$': ''}.items():
        url = re.sub(key, value, url)
    return url


############################################################################
#               WebBase Class
############################################################################

class WebBase(object):

    @classmethod
    def get_url_base_and_num(cls, url):
        return get_url_base_and_num(url)

    @classmethod
    def set_url_base_and_num(cls, base, num):
        return set_url_base_and_num(base, num)

    @classmethod
    def convert_url_to_title(cls, url):
        return convert_url_to_title(url)

    @classmethod
    def reclaim_url_address(cls, url):
        return reclaim_url_address(url)
