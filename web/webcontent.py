#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on 2018-12-03

@author: Byng Zeng
"""

from urllib2 import Request, URLError, urlopen
import re
import urllib
import os
import ssl

from mypy import MyPath

URL_HEADER = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; rv:16.0) Gecko/20100101 Firefox/16.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Connection': 'keep-alive',
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'Accept-Encoding': 'gzip, deflate, sdch, br',
    'Cache-Control': 'max-age=0'
}


class WebContent (object):

    CONTEXT_UNVERIFIED = ssl._create_unverified_context()
    CONTEXT_TLSv1 = ssl.SSLContext(ssl.PROTOCOL_TLSv1)

    @classmethod
    def get_html(cls, url, retry_times=3, context=None):
        print('Downloading: %s' % url)
        req = Request(url, headers=URL_HEADER)
        try:
            if context:
                data = urlopen(req, context=context).read()
            else:

                data = urlopen(req).read()
            html_content = data.decode('gbk', 'ignore').encode('utf-8')
        except URLError, e:
            print(e.reason)
            html_content = None
            print("retry times: %s" % retry_times)
            if retry_times > 0:
                if hasattr(e, 'code') and 500 <= e.code < 600:
                    WebContent.get_url_content(url, retry_times - 1)
        return html_content

    @classmethod
    def get_url_content(cls, url):
        if re.match('https://', url):
            return WebContent.get_html(url, WebContent.CONTEXT_UNVERIFIED)
        else:
            return WebContent.get_html(url)

    @classmethod
    def retrieve_url_file(cls, path, url):
        path = path.strip()
        MyPath.make_path(path)
        fname = os.path.join(path, url.split('/')[len(url.split('/')) - 1])
        if not os.path.exists(fname):
            urllib.urlretrieve(url, fname)

    @classmethod
    def get_url_title(self, html_content, re_patten=re.compile('<title>.+</title>')):
        return re_patten.search(html_content)

class WebImage (WebContent):

    def __init__(self):
        super(WebImage, self).__init__()

    @classmethod
    def get_pic_url(cls, html, patten=re.compile('http(s)?://.+\.(jpg|png|gif)')):
        return patten.findall(html)

    @classmethod
    def retrieve_url_pic(cls, path, url):
        return WebContent.retrieve_url_file(path, url)
