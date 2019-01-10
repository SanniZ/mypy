#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Created on: 2018-12-11

@author: Byng Zeng
"""

from mypy.base import Base

from web.webcontent import WebContent
from web.webimage.webimage import WebImage

class Girlsky(WebImage):

    URL_BASE_MAP = {
        # xval : { url_base : path}
        'xgmn' : {'http://m.girlsky.cn/mntp/xgmn/URLID.html' : '性感美女'},
        'swmn' : {'http://m.girlsky.cn/mntp/swmn/URLID.html' : '丝袜美女'},
        'wgmn' : {'http://m.girlsky.cn/mntp/wgmn/URLID.html' : '外国美女'},
        'zpmn' : {'http://m.girlsky.cn/mntp/zpmn/URLID.html' : '自拍美女'},
        'mnxz' : {'http://m.girlsky.cn/mntp/mnxz/URLID.html' : '美女写真'},
        'rtys' : {'http://m.girlsky.cn/mntp/rtys/URLID.html' : '人体艺术'},
        'jpmn' : {'http://m.girlsky.cn/mntp/jpmn/URLID.html' : '街拍美女'},
        'gzmn' : {'http://m.girlsky.cn/mntp/gzmn/URLID.html' : '古装美女'},
        'nrtys' : { 'http://m.girlsky.cn/mntpn/rtys/URLID.html' : '人体艺术'},
    }


    def __init__(self, name=None):
        super(Girlsky, self).__init__(name)
        self._redundant_title = ['_妹子天空']
        self._remove_small_image = False

    def get_user_input(self, args=None):
        args = super(Girlsky, self).get_user_input(args)
        if self._xval in self.URL_BASE_MAP:
            self._url_base = list(self.URL_BASE_MAP[self._xval])[0]
            self._pr.pr_dbg('get url_base: %s from -x %s' % (self._url_base, self._xval))
        if self._url_base:
            for dict_url_base in self.URL_BASE_MAP.values():
                if self._url_base == list(dict_url_base)[0]:
                    if not '-p' in args:
                        path =  dict_url_base[self._url_base]
                        self._path = '%s/%s/%s' %  (Base.DEFAULT_DWN_PATH, self.__class__.__name__, path)
                    break

    def get_url_of_pages(self, num):
        url = list(map(lambda x: WebContent.set_url_base_and_num(self._url_base, '%d_%d' % (int(self._url), x)), range(2, num + 1)))
        url.insert(0, WebContent.set_url_base_and_num(self._url_base, self._url))
        return url

if __name__ == '__main__':
    gs = Girlsky()
    gs.main()
