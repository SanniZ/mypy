#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Created on: 2018-12-11

@author: Byng Zeng
"""

import os
import sys
import re

import threading

from mypy.base import Base
from mypy.path import Path
from mypy.pr import Print

from web.webcontent import WebContent
from web.webimage.girlsky import Girlsky
from web.webimage.pstatp import Pstatp
from web.webimage.meizitu import Meizitu
from web.webimage.mzitu import Mzitu
from web.webimage.webimage import WebImage, get_input
from web.webimage.weibo import Weibo

if sys.version_info[0] == 2:
    import Queue as queue
else:
    import queue

URL_BASE = {
    # xval: { url_base: class}
    'xgmn': {'http://m.girlsky.cn/mntp/xgmn/URLID.html': Girlsky('Girlsky')},
    'swmn': {'http://m.girlsky.cn/mntp/swmn/URLID.html': Girlsky('Girlsky')},
    'wgmn': {'http://m.girlsky.cn/mntp/wgmn/URLID.html': Girlsky('Girlsky')},
    'zpmn': {'http://m.girlsky.cn/mntp/zpmn/URLID.html': Girlsky('Girlsky')},
    'mnxz': {'http://m.girlsky.cn/mntp/mnxz/URLID.html': Girlsky('Girlsky')},
    'rtys': {'http://m.girlsky.cn/mntp/rtys/URLID.html': Girlsky('Girlsky')},
    'jpmn': {'http://m.girlsky.cn/mntp/jpmn/URLID.html': Girlsky('Girlsky')},
    'gzmn': {'http://m.girlsky.cn/mntp/gzmn/URLID.html': Girlsky('Girlsky')},
    'nrtys': {'http://m.girlsky.cn/mntpn/rtys/URLID.html': Girlsky('Girlsky')},
    # pstatp
    'pstatp': {'https://www.toutiao.com/aURLID': Pstatp('Pstatp')},
    'pstatp_i': {'https://www.toutiao.com/iURLID': Pstatp('Pstatp')},
    # meizitu
    'meizitu': {'http://www.meizitu.com/a/URLID.html': Meizitu('Meizitu')},
    # mzitu
    'mzitu': {'https://m.mzitu.com/URLID': Mzitu('Mzitu')},
    'weibo': {'https://m.weibo.cn/detail/URLID': Weibo('Weibo')},
}


class WebImageCrawler(WebContent):

    HELP_MENU = (
        '==================================',
        '    WebImageCrawler help',
        '==================================',
        'option:',
        '  -u url:',
        '    url of web to be download',
        '  -n num:',
        '    number of web number to be download',
        '  -p path:',
        '    root path to store images.',
        '  -v:',
        '    view info while download.',
        '  -x val:',
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
        '  -m mode:',
        '    wget: using wget to download imgages',
        '    rtrv: using retrieve to download images',
        '    rget: using requests to download images',
        '    uget: using urlopen to download images',
        '  -R file:',
        '    re config file for re_image_url.',
        '  -t num:',
        '    set number of thread to download images.',
        '  -U:',
        '    run UI version of WebImageCrawler.',
    )

    def __init__(self, name=None):
        self._name = name
        self._web_base = None
        self._url_base = None
        self._url_file = None
        self._url = None
        self._xval = None
        self._pr = Print(self.__class__.__name__)
        self._class = None
        self._thread_max = 5
        self._thread_queue = None

    def get_input_args(self, args):
        if not args:
            args = get_input()
        if '-h' in args:
            Base.print_help(self.HELP_MENU)
        if '-u' in args:
            if os.path.isfile(args['-u']):
                self._url_file = Path.get_abs_path(args['-u'])
            else:
                self._url = re.sub('/$', '', args['-u'])
        if '-x' in args:
            self._xval = args['-x']
        if '-d' in args:
            self._pr.set_pr_level(self._pr.get_pr_level() | Print.PR_LVL_DBG)
        # get url_base from xval
        if self._xval:
            if self._xval in URL_BASE:
                self._url_base = list(URL_BASE[self._xval])[0]
                self._class = URL_BASE[self._xval][self._url_base]
            else:
                Base.print_exit('[WebImageCrawler] Error, invalid -x val!')
        # get class from url
        if self._url:
            base, num = self.get_url_base_and_num(self._url)
            if base:
                self._url_base = base
        # get class from url_base
        if all((not self._class, self._url_base)):
                for dict_url_base in URL_BASE.values():
                    if self._url_base == list(dict_url_base)[0]:
                        self._class = dict_url_base[self._url_base]
                        break
        return args

    def process_input(self, args=None, info=None):
        if self._class:
            hdr = self._class
        else:
            hdr = WebImage('WebImage')
        if hdr:
            hdr.main(args)
        else:
            self._pr.pr_err('[WebImageCrawler] Error, no found handler!')
        # release queue
        if self._thread_queue:
            self._thread_queue.get()
        if info:
            index = info[0]
            total = info[1]
            self._pr.pr_info('process %d/%d input file done' % (index, total))

    def process_file_input(self, args=None):
        if self._url_file:
            with open(self._url_file, 'r') as fd:
                lines = set(fd.readlines())
            self._thread_queue = queue.Queue(self._thread_max)
            total = len(lines)
            index = 1
            # delete -u arg.
            if '-u' in args:
                del args['-u']
            # process all of url.
            for url in lines:
                self._class = None
                # remove invalid chars.
                for key, value in {'/$': '', '\n$': ''}.items():
                    url = re.sub(key, value, url)
                # get base and num
                base, num = self.get_url_base_and_num(url)
                if base:
                    for dict_url_base in URL_BASE.values():
                        if base == list(dict_url_base)[0]:
                            self._class = dict_url_base[base]
                            break
                if self._class:
                    url_args = {'-u': url}
                    url_args.update(args)
                    info = (index, total)
                    # create thread and put to queue.
                    t = threading.Thread(target=self.process_input,
                                         args=(url_args, info))
                    self._thread_queue.put(url)
                    t.start()
                index = index + 1

    def main(self, args=None):
        args = self.get_input_args(args)
        if self._url_file:
            self.process_file_input(args)
        else:
            self.process_input(args)

if __name__ == '__main__':
    args = get_input(None, 'U')
    if '-U' in args:
        from webimagecrawlerUI import WebImageCrawlerUI
        del args['-U']  # delete -U value.
        wc = WebImageCrawlerUI()
    else:
        wc = WebImageCrawler()
    wc.main(args)
