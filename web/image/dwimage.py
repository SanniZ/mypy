#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on: 2018-12-11

@author: Byng Zeng
"""

import os

from mypy import MyPy

from webcontent import WebContent
from girlsky import Girlsky
from pstatp import Pstatp
from meizitu import Meizitu
from mzitu import Mzitu

enable_debug = False

def pr_dbg(fmt):
    if enable_debug and fmt:
        print(fmt)

class DWImage(WebContent):

    help_menu = (
        '==================================',
        '    DWImage help',
        '==================================',
        'option: -u url -n number -p path -x val -v',
        '  -u:',
        '    url of web to be download',
        '  -n:',
        '    number of web number to be download',
        '  -p:',
        '    root path to store images.',
        '  -v:',
        '     show info while download.',
        '  -x:',
        '     val for expand cmd.',
    )

    def register_web_handler(self):
        self._girlsky = Girlsky()
        self._pstatp = Pstatp()
        self._meizitu = Meizitu()
        self._mzitu = Mzitu()

        self._web_base = {
            # girlsky
            'http://m.girlsky.cn/mntp/xgmn/URLID.html' : self._girlsky,  # 性感美女
            'http://m.girlsky.cn/mntp/swmn/URLID.html' : self._girlsky,  # 丝袜美女
            'http://m.girlsky.cn/mntp/wgmn/URLID.html' : self._girlsky,  # 外国美女
            'http://m.girlsky.cn/mntp/zpmn/URLID.html' : self._girlsky,  # 自拍美女
            'http://m.girlsky.cn/mntp/mnxz/URLID.html' : self._girlsky,  # 美女写真
            'http://m.girlsky.cn/mntp/rtys/URLID.html' : self._girlsky,  # 人体艺术
            'http://m.girlsky.cn/mntp/jpmn/URLID.html' : self._girlsky,  # 街拍美女
            'http://m.girlsky.cn/mntp/gzmn/URLID.html' : self._girlsky,  # 古装美女
            # pstatp
             'https://www.toutiao.com/aURLID' : self._pstatp,
            # meizitu
            'http://www.meizitu.com/a/URLID.html' : self._meizitu,
            # mzitu
            'https://m.mzitu.com/URLID' : self._mzitu,
        }

    def __init__(self):
        self._web_base = None
        self._url_base = None
        self._url = None
        self._xval = None

    def get_input(self):
        args = MyPy.get_user_input('hu:n:p:x:v')
        if '-h' in args:
            MyPy.print_help(self.help_menu)
        if '-u' in args:
            self._url = args['-u']
        if '-x' in args:
            self._xval = args['-x']
        # check url
        if self._url:
            base, num = self.get_url_base_and_num(self._url)
            if base:
                self._url_base = base
            if num:
                self._url = num
            pr_dbg('get base: %s, url: %s' % (base, self._url))
        else:
            MyPy.print_exit('Error, no set url, -h for help!')

    def get_web_handler(self):
        if self._url_base in self._web_base:
            return self._web_base[self._url_base]

    def main(self):
        self.get_input()
        self.register_web_handler()
        hdr = self.get_web_handler()
        if hdr:
            hdr.main()

if __name__ == '__main__':
    dwimg = DWImage()
    dwimg.main()
