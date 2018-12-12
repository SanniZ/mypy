#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on: 2018-12-11

@author: Byng Zeng
"""

import re

from mypy import MyBase, MyPrint

from webcontent import WebContent
from girlsky import Girlsky
from pstatp import Pstatp
from meizitu import Meizitu
from mzitu import Mzitu
from webimage import WebImage


class DWImage(WebContent):

    HELP_MENU = (
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

    XHELP_MENU = (
        '==================================',
        '    -x val help',
        '==================================',
        '  xgmn:    xgmn of girlsky',
        '  swmn:    swmn of girlsky',
        '  wgmn:    wgmn of girlsky',
        '  zpmn:    zpmn of girlsky',
        '  mnxz:    mnxz of girlsky',
        '  rtys:    rtys of girlsky',
        '  jpmn:    jpmn of girlsky',
        '  gzmn:    gzmn of girlsky',
        '  toutiao: toutiao for pstatp',
        '  meizitu: meizitu of meizitu',
        '  mzitu:   mzitu of mzitu',
    )

    BASE_MAP = {
        # girlsky
        'http://m.girlsky.cn/mntp/xgmn/URLID.html' : 'girlsky',  # 性感美女
        'http://m.girlsky.cn/mntp/swmn/URLID.html' : 'girlsky',  # 丝袜美女
        'http://m.girlsky.cn/mntp/wgmn/URLID.html' : 'girlsky',  # 外国美女
        'http://m.girlsky.cn/mntp/zpmn/URLID.html' : 'girlsky',  # 自拍美女
        'http://m.girlsky.cn/mntp/mnxz/URLID.html' : 'girlsky',  # 美女写真
        'http://m.girlsky.cn/mntp/rtys/URLID.html' : 'girlsky',  # 人体艺术
        'http://m.girlsky.cn/mntp/jpmn/URLID.html' : 'girlsky',  # 街拍美女
        'http://m.girlsky.cn/mntp/gzmn/URLID.html' : 'girlsky',  # 古装美女
        # pstatp
         'https://www.toutiao.com/aURLID' : 'pstatp',
        # meizitu
        'http://www.meizitu.com/a/URLID.html' : 'meizitu',
        # mzitu
        'https://m.mzitu.com/URLID' : 'mzitu',
    }


    def __init__(self):
        self._web_base = None
        self._url_base = None
        self._url = None
        self._xval = None
        self._pr = MyPrint('DWImage')

    def get_url_base_filter(self, url_base):
        pattern = re.compile(self._xval)
        if pattern.search(url_base):
            return url_base

    def get_input(self):
        args = MyBase.get_user_input('hHu:n:p:x:vd')
        if '-h' in args:
            MyBase.print_help(self.HELP_MENU)
        if '-H' in args:
            MyBase.print_help(self.XHELP_MENU)
        if '-u' in args:
            self._url = re.sub('/$', '', args['-u'])
        if '-x' in args:
            self._xval = args['-x']
        if '-d' in args:
            self._pr.set_pr_level(self._pr.get_pr_level() | MyPrint.PR_LVL_DBG)
        # get url_base from xval
        if self._xval:
            url_base = filter(self.get_url_base_filter, self.BASE_MAP.iterkeys())
            if url_base:
                self._url_base = url_base[0]
        # check url
        if self._url:
            base, num = self.get_url_base_and_num(self._url)
            if base:
                self._url_base = base
            if num:
                self._url = num
            self._pr.pr_dbg('get base: %s, url: %s' % (base, self._url))
        else:
            MyBase.print_exit('Error, no set url, -h for help!')

    def process_input(self):
        hdr = None
        if self._url_base in self.BASE_MAP:
            if self.BASE_MAP[self._url_base] == 'girlsky':
                hdr = Girlsky()
            elif self.BASE_MAP[self._url_base] == 'pstatp':
                hdr = Pstatp()
            elif self.BASE_MAP[self._url_base] == 'meizitu':
                hdr = Meizitu()
            elif self.BASE_MAP[self._url_base] == 'mzitu':
                hdr = Mzitu()
        else:
            hdr = WebImage()
        if hdr:
            self._pr.pr_dbg('run %s class' % hdr.__class__.__name__)
            hdr.main()
        else:
            self._pr.pr_err('Error, no found handler!')


    def main(self):
        self.get_input()
        self.process_input()

if __name__ == '__main__':
    dwimg = DWImage()
    dwimg.main()
