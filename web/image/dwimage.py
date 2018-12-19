#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on: 2018-12-11

@author: Byng Zeng
"""

import re
import sys

from mypy import MyBase, MyPrint, MyPath

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
        'option: -u url -n number -p path -x val -m mode -v',
        '  -u:',
        '    url of web to be download',
        '  -n:',
        '    number of web number to be download',
        '  -p:',
        '    root path to store images.',
        '  -v:',
        '    view info while download.',
        '  -x:',
        '    xgmn:    xgmn of girlsky',
        '    swmn:    swmn of girlsky',
        '    wgmn:    wgmn of girlsky',
        '    zpmn:    zpmn of girlsky',
        '    mnxz:    mnxz of girlsky',
        '    rtys:    rtys of girlsky',
        '    jpmn:    jpmn of girlsky',
        '    gzmn:    gzmn of girlsky',
        '    pstatp:  pstatp of toutiao',
        '    toutiao: toutiao of toutiao',
        '    meizitu: meizitu of meizitu',
        '    mzitu:   mzitu of mzitu',
        '  -m:',
        '    wget: using wget to download imgages',
        '    rtrv: using retrieve to download images',
        '    rget: using requests to download images',
        '    uget: using urlopen to download images',
    )

    URL_BASE = {
        # xval : { url_base : class}
        'xgmn' : {'http://m.girlsky.cn/mntp/xgmn/URLID.html' : 'girlsky'},  # 性感美女
        'swmn' : {'http://m.girlsky.cn/mntp/swmn/URLID.html' : 'girlsky'},  # 丝袜美女
        'wgmn' : {'http://m.girlsky.cn/mntp/wgmn/URLID.html' : 'girlsky'},  # 外国美女
        'zpmn' : {'http://m.girlsky.cn/mntp/zpmn/URLID.html' : 'girlsky'},  # 自拍美女
        'mnxz' : {'http://m.girlsky.cn/mntp/mnxz/URLID.html' : 'girlsky'},  # 美女写真
        'rtys' : {'http://m.girlsky.cn/mntp/rtys/URLID.html' : 'girlsky'},  # 人体艺术
        'jpmn' : {'http://m.girlsky.cn/mntp/jpmn/URLID.html' : 'girlsky'},  # 街拍美女
        'gzmn' : {'http://m.girlsky.cn/mntp/gzmn/URLID.html' : 'girlsky'},  # 古装美女
        'nrtys' : {'http://m.girlsky.cn/mntpn/rtys/URLID.html' : 'girlsky'},  # 人体艺术
        # pstatp
        'pstatp'  : {'https://www.toutiao.com/aURLID' : 'pstatp'},
        'toutiao' : {'https://www.toutiao.com/aURLID' : 'pstatp'},
        # meizitu
        'meizitu' : {'http://www.meizitu.com/a/URLID.html' : 'meizitu'},
        # mzitu
        'mzitu'   : {'https://m.mzitu.com/URLID' : 'mzitu'},
    }

    def __init__(self, name=None):
        self._name = name
        self._web_base = None
        self._url_base = None
        self._url = None
        self._xval = None
        self._in_file = None
        self._pr = MyPrint('DWImage')
        self._class = None

    def get_input(self):
        args = MyBase.get_user_input('hu:n:p:x:m:i:vDd')
        if '-h' in args:
            MyBase.print_help(self.HELP_MENU)
        if '-u' in args:
            self._url = re.sub('/$', '', args['-u'])
        if '-x' in args:
            self._xval = args['-x']
        if '-d' in args:
            self._pr.set_pr_level(self._pr.get_pr_level() | MyPrint.PR_LVL_DBG)
        # get url_base from xval
        if self._xval:
            if self._xval in self.URL_BASE:
                self._url_base = list(self.URL_BASE[self._xval])[0]
                self._class = self.URL_BASE[self._xval][self._url_base]
            else:
                MyBase.print_exit('Error, invalid -x val!')
        # get class from url
        if self._url:
            base, num = self.get_url_base_and_num(self._url)
            if base:
                self._url_base = base
        # get class from url_base
        if all((not self._class, self._url_base)):
                for dict_url_base in self.URL_BASE.itervalues():
                    if self._url_base == list(dict_url_base)[0]:
                        self._class =  dict_url_base[self._url_base]
                        break
        if '-i' in args:
            self._in_file = MyPath.get_abs_path(args['-i'])


    def process_input(self):
        if self._class:
            if self._class == 'girlsky':
                hdr = Girlsky('Girlsky')
            elif self._class == 'pstatp':
                hdr = Pstatp('Pstatp')
            elif self._class == 'meizitu':
                hdr = Meizitu('Meizitu')
            elif self._class == 'mzitu':
                hdr = Mzitu('Mzitu')
        else:
            hdr = WebImage('WebImage')
        if hdr:
            hdr.main()
        else:
            self._pr.pr_err('Error, no found handler!')


    def process_file_input(self):
        if self._in_file:
            with open(self._in_file, 'r') as fd:
                lines = fd.readlines()
            for url in lines:
                url = re.sub('/$', '', url)
                url = re.sub('\n$', '', url)
                self._class = None
                base, num = self.get_url_base_and_num(url)
                if base:
                    for dict_url_base in self.URL_BASE.itervalues():
                        if base == list(dict_url_base)[0]:
                            self._class =  dict_url_base[base]
                            break
                if self._class:
                    # remove invalid cmds.
                    if '-i' in sys.argv:
                        sys.argv.remove('-i')
                        sys.argv.remove(self._in_file)
                    if '-u' in sys.argv:
                        sys.argv.pop(sys.argv.index('-u') + 1)
                        sys.argv.remove('-u')
                    # config new cmd line.
                    sys.argv.append('-u')
                    sys.argv.append(url)
                    self.process_input()

    def main(self):
        self.get_input()
        if self._in_file:
            self.process_file_input()
        else:
            self.process_input()

if __name__ == '__main__':
    dwimg = DWImage()
    dwimg.main()
