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
    #'Accept-Language': 'zh-CN,zh;q=0.8',
    #'Accept-Encoding': 'gzip, deflate, sdch, br',
    #'Cache-Control': 'max-age=0'
}


DEFAULT_CHARSET=r'gb2312'

class WebContent (object):

    CONTEXT_UNVERIFIED = ssl._create_unverified_context()
    CONTEXT_TLSv1 = ssl.SSLContext(ssl.PROTOCOL_TLSv1)

    @classmethod
    def get_charset(cls, data):
        charset = re.compile('charset=(gb2312|gbk|utf-8)', flags=re.I).search(data)
        if charset:
            charset = charset.group()
            return charset[len('charset='):].lower()
        else:
            return None

    @classmethod
    def get_html(cls, url, retry_times=3, context=None):
        print('Downloading: %s' % url)
        req = Request(url, headers=URL_HEADER)
        try:
            data = urlopen(req, context=context).read()
            html_content = data.decode(DEFAULT_CHARSET, 'ignore').encode('utf-8')
            charset = WebContent.get_charset(html_content)
            if charset != DEFAULT_CHARSET:
                html_content = data.decode(charset).encode('utf-8')
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
    def get_url_title(cls, html_content, pattern=None):
        if pattern:
            return pattern.search(html_content)
        else:
            pattern=re.compile('<title>.+</title>')
            data = pattern.search(html_content)
            if data:
                data = data.group()
                return data[len('<title>') : len(data) - len('</title>')]
            else:
                return None

    @classmethod
    def get_url_pages(cls, html, pattern=None):
        if pattern:
            return pattern.search(html)
        else:
            pattern = re.compile('\d+/\d+')
            data = pattern.search(html)
            if data:
                print data.group()
                pattern = re.compile('/\d+')
                data = pattern.search(data.group())
                if data:
                    return data.group()[len('/') : ]
                else:
                    return None
            else:
                return None

class WebImage (WebContent):

    def __init__(self):
        super(WebImage, self).__init__()

    @classmethod
    def get_image_url(cls, html, pattern=None):
        if not pattern:
            pattern = re.compile('http(s)?://.+\.(jpg|png|gif|bmp|jpeg)')
        return pattern.findall(html)

    @classmethod
    def retrieve_url_image(cls, path, url):
        return WebContent.retrieve_url_file(path, url)
