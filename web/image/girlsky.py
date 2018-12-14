#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on: 2018-12-11

@author: Byng Zeng
"""
import re

from mypy import MyBase
from webcontent import WebContent
from webimage import WebImage

class Girlsky(WebImage):

    URL_BASE = {
        'xgmn' : 'http://m.girlsky.cn/mntp/xgmn/URLID.html',  # 性感美女
        'swmn' : 'http://m.girlsky.cn/mntp/swmn/URLID.html',  # 丝袜美女
        'wgmn' : 'http://m.girlsky.cn/mntp/wgmn/URLID.html',  # 外国美女
        'zpmn' : 'http://m.girlsky.cn/mntp/zpmn/URLID.html',  # 自拍美女
        'mnxz' : 'http://m.girlsky.cn/mntp/mnxz/URLID.html',  # 美女写真
        'rtys' : 'http://m.girlsky.cn/mntp/rtys/URLID.html',  # 人体艺术
        'jpmn' : 'http://m.girlsky.cn/mntp/jpmn/URLID.html',  # 街拍美女
        'gzmn' : 'http://m.girlsky.cn/mntp/gzmn/URLID.html',  # 古装美女
        'nrtys' : 'http://m.girlsky.cn/mntpn/rtys/URLID.html',  # 人体艺术
    }

    PATH_MAP = {
        'http://m.girlsky.cn/mntp/xgmn/URLID.html' : '性感美女',
        'http://m.girlsky.cn/mntp/swmn/URLID.html' : '丝袜美女',
        'http://m.girlsky.cn/mntp/wgmn/URLID.html' : '外国美女',
        'http://m.girlsky.cn/mntp/zpmn/URLID.html' : '自拍美女',
        'http://m.girlsky.cn/mntp/mnxz/URLID.html' : '美女写真',
        'http://m.girlsky.cn/mntp/rtys/URLID.html' : '人体艺术',
        'http://m.girlsky.cn/mntp/jpmn/URLID.html' : '街拍美女',
        'http://m.girlsky.cn/mntp/gzmn/URLID.html' : '古装美女',
        'http://m.girlsky.cn/mntpn/rtys/URLID.html' : '人体艺术',
    }


    def __init__(self, name=None):
        super(Girlsky, self).__init__(name)
        #self._re_image_url = re.compile('src=\"(http://.*\.[jpg|png|gif])\"', flags=re.I)
        self._re_pages = re.compile('1/\d+')
        self._remove_small_image = False

    def get_user_input(self):
        super(Girlsky, self).get_user_input()
        if self._xval:
            self._url_base = self.URL_BASE[self._xval]
            self._pr.pr_dbg('get url_base: %s from -x %s' % (self._url_base, self._xval))
        if self._url_base in self.PATH_MAP.keys():
            self._path = '%s/%s/%s' %  (MyBase.DEFAULT_DWN_PATH, self.__class__.__name__, self.PATH_MAP[self._url_base])

    def get_title(self, html, pattern=None):
        title = WebContent.get_url_title(html, pattern)
        if title:
            title = title[ : len(title) - len('_妹子天空')]
        return title


    def get_pages(self, html, pattern=None):
        pattern = re.compile('\d+/\d+')
        pages =  pattern.findall(html)
        for page in pages:
            page = page.split('/')
            if all((int(page[0]) == 1, int(page[1]))):
                return int(page[1])

    def get_url_of_pages(self, num):
        url = map(lambda x: WebContent.set_url_base_and_num(self._url_base, '%d_%d' % (int(self._url), x)), range(2, num + 1))
        url.insert(0, WebContent.set_url_base_and_num(self._url_base, self._url))
        return url

if __name__ == '__main__':
    gs = Girlsky()
    gs.main()
