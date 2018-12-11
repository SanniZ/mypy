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
import gzip
from StringIO import StringIO
import requests

from mypy import MyPath

URL_HEADER = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; rv:16.0) Gecko/20100101 Firefox/16.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Connection': 'keep-alive',
    #'Accept-Language': 'zh-CN,zh;q=0.8',
    #'Accept-Encoding': 'gzip, deflate, sdch, br',
    #'Cache-Control': 'max-age=0'
}


DEFAULT_CHARSET = r'GB2312'

CHARSETS = ('UTF-8', 'GB2312', 'GBK')

class WebContent (object):

    CONTEXT_UNVERIFIED = ssl._create_unverified_context()
    CONTEXT_TLSv1 = ssl.SSLContext(ssl.PROTOCOL_TLSv1)

    WEB_URL_FILE = r'web_url.txt'

    @classmethod
    def get_url_charset(cls, html):
        charset = re.compile('charset=[a-z0-8-]*', flags=re.I).search(re.sub('charset=(\"|\')', 'charset=', html))
        if charset:
            charset = charset.group()
            charset = charset[len('charset='):].upper()
        return charset

    @classmethod
    def get_html(cls, url, context=None, retry_times=3, show=True):
        if show:
            print('Downloading: %s' % url)
        url_charset = None
        req = Request(url, headers=URL_HEADER)
        try:
            html = urlopen(req, context=context)
            data = html.read()
            encoding = html.info().getheader('Content-Encoding')
            if encoding == 'gzip':
                 data = gzip.GzipFile(fileobj=StringIO(data)).read()
                 url_charset = cls.get_url_charset(data)
            if data:
                for charset in CHARSETS:
                    if url_charset:
                        html_content = data.decode(url_charset, 'ignore').encode('utf-8')
                        break
                    else:
                        html_content = data.decode(charset, 'ignore').encode('utf-8')
                        if html_content:
                            url_charset = cls.get_url_charset(html_content)
                            if not url_charset:
                                url_charset = DEFAULT_CHARSET
                            elif charset == url_charset:
                                break
            else:
                print('Error: fail to get data from html')
                html_content = None
        except URLError as e:
            print(e.reason)
            html_content = None
            print("retry times: %s" % retry_times)
            if retry_times > 0:
                #if hasattr(e, 'code') and 500 <= e.code < 600:
                cls.get_url_content(url, retry_times - 1, False)
        return html_content

    @classmethod
    def get_url_content(cls, url, retry_times=3, show=True):
        if re.match('https://', url):
            return cls.get_html(url = url, context = cls.CONTEXT_UNVERIFIED, retry_times = retry_times,show = show)
        else:
            return cls.get_html(url = url, retry_times = retry_times, show = show)

    @staticmethod
    def urlretrieve_callback(blocknum, blocksize, totalsize):
        percent = 100.0 * blocknum * blocksize / totalsize
        if percent > 100:
            percent = 100
        print("%.2f%%" % percent)

    @classmethod
    def retrieve_url_file(cls, url, path):
        path = path.strip()
        MyPath.make_path(path)
        fname = os.path.join(path, url.split('/')[len(url.split('/')) - 1])
        if not os.path.exists(fname):
            #urllib.urlretrieve(url, fname, cls.urlretrieve_callback)
            urllib.urlretrieve(url, fname)

    @classmethod
    def retrieve_get_url_file(cls, url, path):
        path = path.strip()
        MyPath.make_path(path)
        fname = os.path.join(path, url.split('/')[len(url.split('/')) - 1])
        if not os.path.exists(fname):
            r = requests.get(url)
            with open(fname, 'wb') as f:
                f.write(r.content)

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
        if not pattern:
            pattern = re.compile('/\d+页')
        data = pattern.search(html.strip())
        if data:
            pattern = re.compile('\d+')
            data = pattern.search(data.group())
            if data:
                data = int(data.group())
        return data

    @classmethod
    def get_url_base_and_num(cls, url):
        base = None
        num = None
        # numbers.
        num = re.compile('^\d+$').search(url)
        if num:
            num = num.group()
        else:
            num = re.compile('(\d)+(/)?(.html)?$').search(url)
            if num:
                num = re.compile('\d+').search(num.group()).group()
                base = re.sub(num, 'URLID', url)
        return base, num

    @classmethod
    def set_url_base_and_num(cls, base, num):
        if base:
            return re.sub('URLID', str(num), base)
        else:
            return num

    @classmethod
    def convert_url_to_title(cls, url):
        return re.sub('(/|:|\.)', '_', url)

