#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on: 2018-12-11

@author: Byng Zeng
"""

import os
import sys
import re

import threading

from mypy.pybase import PyBase
from mypy.pypath import PyPath
from mypy.pyprint import PyPrint, PR_LVL_DBG

from web.webbase import WebBase
from web.webimage.webimage import get_input

if sys.version_info[0] == 2:
    import Queue as queue
else:
    import queue


############################################################################
#               XBaseClass Class
############################################################################

class XBaseClass(object):

    URL_BASE = {
        # xval: { url_base: class}
        'xgmn': {'http://m.girlsky.cn/mntp/xgmn/URLID.html': 'Girlsky'},
        'swmn': {'http://m.girlsky.cn/mntp/swmn/URLID.html': 'Girlsky'},
        'wgmn': {'http://m.girlsky.cn/mntp/wgmn/URLID.html': 'Girlsky'},
        'zpmn': {'http://m.girlsky.cn/mntp/zpmn/URLID.html': 'Girlsky'},
        'mnxz': {'http://m.girlsky.cn/mntp/mnxz/URLID.html': 'Girlsky'},
        'rtys': {'http://m.girlsky.cn/mntp/rtys/URLID.html': 'Girlsky'},
        'jpmn': {'http://m.girlsky.cn/mntp/jpmn/URLID.html': 'Girlsky'},
        'gzmn': {'http://m.girlsky.cn/mntp/gzmn/URLID.html': 'Girlsky'},
        'nrtys': {'http://m.girlsky.cn/mntpn/rtys/URLID.html': 'Girlsky'},
        # pstatp
        'pstatp': {'https://www.toutiao.com/aURLID': 'Pstatp'},
        'pstatp_i': {'https://www.toutiao.com/iURLID': 'Pstatp'},
        # meizitu
        'meizitu': {'http://www.meizitu.com/a/URLID.html': 'Meizitu'},
        # mzitu
        'mzitu': {'https://m.mzitu.com/URLID': 'Mzitu'},
        'weibo': {'https://m.weibo.cn/detail/URLID': 'Weibo'},
        'meitulu': {'https://www.meitulu.com/item/URLID.html': 'Meitulu'},
        'meitulu_t': {'https://www.meitulu.com/t/URLID': 'Meitulu'},

    }

    @classmethod
    def get_class_instance(cls, c):
        if c == 'Girlsky':
            from web.webimage.girlsky import Girlsky
            hdr = Girlsky(c)
        elif c == 'Pstatp':
            from web.webimage.pstatp import Pstatp
            hdr = Pstatp(c)
        elif c == 'Meizitu':
            from web.webimage.meizitu import Meizitu
            hdr = Meizitu(c)
        elif c == 'Mzitu':
            from web.webimage.mzitu import Mzitu
            hdr = Mzitu(c)
        elif c == 'Weibo':
            from web.webimage.weibo import Weibo
            hdr = Weibo(c)
        elif c == 'Meitulu':
            from web.webimage.meitulu import Meitulu
            hdr = Meitulu(c)
        else:
            from web.webimage.webimage import WebImage
            hdr = WebImage('WebImage')
        return hdr

    @classmethod
    def get_base_class_from_xval(cls, xval):
        if xval in cls.URL_BASE:
            url_base = list(cls.URL_BASE[xval])[0]
            cls = cls.URL_BASE[xval][url_base]
            return url_base, cls
        else:
            return None, None

    @classmethod
    def get_num_url_from_xval(cls, xval, num):
        if xval in cls.URL_BASE:
            url_base = list(cls.URL_BASE[xval])[0]
            return url_base.replace('URLID', num)
        return None

    @classmethod
    def get_class_from_base(cls, base):
        for dict_url_base in cls.URL_BASE.values():
            if base == list(dict_url_base)[0]:
                return dict_url_base[base]
        return None

    @classmethod
    def get_class_from_url(cls, url):
        result = None
        for dict_url_base in cls.URL_BASE.values():
            base = list(dict_url_base)[0]
            if url.startswith(base.replace('URLID', '')):
                return dict_url_base[base]
        return result


############################################################################
#               WebImageCrawler Class
############################################################################

class WebImageCrawler(object):

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
        '  -s fnum:',
        '    set number of sub pages and formal of url.',
        '  -U:',
        '    run GUI of WebImageCrawler.',
    )

    def __init__(self, name=None):
        self._name = name
        self._web_base = None
        self._url_base = None
        self._url_file = None
        self._url = None
        self._xval = None
        self._pr = PyPrint(self.__class__.__name__)
        self._class = None
        self._thread_max = 5
        self._thread_queue = None
        self._byname = None
        self._search_urls = list()

    def get_input_args(self, args):
        if not args:
            args = get_input(exopt='y:')
        if '-h' in args:
            PyBase.print_help(self.HELP_MENU)
        if '-u' in args:
            if os.path.isfile(args['-u']):
                self._url_file = PyPath.get_abs_path(args['-u'])
            else:
                self._url = re.sub('/$', '', args['-u'])
        if '-x' in args:
            self._xval = args['-x']
        if '-d' in args:
            self._pr.add_pr_level(PR_LVL_DBG)
            self._pr.set_funcname(True)
        if '-y' in args:
            self._byname = args['-y']
        # get url_base from xval
        if self._xval:
            self._url_base, self._class = \
                XBaseClass.get_base_class_from_xval(self._xval)
            if not all((self._url_base, self._class)):
                PyBase.print_exit('[WebImageCrawler] Error, invalid -x val!')
        # get class from url
        if all((self._url, not self._class)):
            base, num = WebBase.get_url_base_and_num(self._url)
            if base:
                self._class = XBaseClass.get_class_from_base(base)
            else:
                self._class = XBaseClass.get_class_from_url(self._url)
        # get class from url_base
        if all((not self._class, self._url_base)):
            self._class = XBaseClass.get_class_from_base(self._url_base)
        return args

    def upload_to_baiduyun(self, fs, localpath, remotepath):
        from baiduyun import BaiduYun
        by = BaiduYun()
        for url, path in fs:
            if path:
                dst = '%s/%s' % (
                    remotepath,
                    re.sub('%s/' % os.path.dirname(localpath), '', path))
                vargs = {'-d': dst, '-s': path}
                by.main(vargs)

    def process_input(self, args=None, info=None):
        hdr = XBaseClass.get_class_instance(self._class)
        if hdr:
            output = hdr.main(args)
            # upload to baidu yun.
            url = args['-u']
            if output:
                for k, data in output.items():
                    if 'search_urls' in data:
                        self._search_urls += data['search_urls']
            if all((self._byname, output)):
                self.upload_to_baiduyun(
                    output.items(), hdr._path, self._byname)
        else:
            self._pr.pr_err('[WebImageCrawler] Error, no found handler!')
        # release queue
        if self._thread_queue:
            self._thread_queue.get()
        if info:
            index = info[0]
            total = info[1]
            self._pr.pr_info('[%d/%d] %s done' % (index, total, url))

    def process_list_input(self, urls, args=None):
        if urls:
            self._thread_queue = queue.Queue(self._thread_max)
            total = len(urls)
            index = 1
            threads = list()
            # delete -u arg.
            if '-u' in args:
                del args['-u']
            # process all of url.
            for url in urls:
                self._class = None
                # remove invalid chars.
                for key, value in {'/$': '', '\n$': ''}.items():
                    url = re.sub(key, value, url)
                # get base and num
                base, num = WebBase.get_url_base_and_num(url)
                if base:
                    self._class = XBaseClass.get_class_from_base(base)
                if self._class:
                    url_args = {'-u': url}
                    url_args.update(args)
                    info = (index, total)
                    # create thread and put to queue.
                    t = threading.Thread(target=self.process_input,
                                         args=(url_args, info))
                    threads.append(t)
                    self._thread_queue.put(url)
                    t.start()
                index += 1
            for t in threads:
                t.join()

    def main(self, args=None):
        args = self.get_input_args(args)
        if self._url_file:
            with open(self._url_file, 'r') as fd:
                urls = set(fd.readlines())
            self.process_list_input(urls, args)
        else:
            self.process_input(args)
        if self._search_urls:
            if '-x' in args:
                del args['-x']
            self.process_list_input(self._search_urls, args)
            self._search_urls = list()

if __name__ == '__main__':
    args = get_input(None, 'Uy:')
    if '-U' in args:
        from webimagecrawlerUI import WebImageCrawlerUI
        del args['-U']  # delete -U value.
        wc = WebImageCrawlerUI()
    else:
        wc = WebImageCrawler()
    wc.main(args)
