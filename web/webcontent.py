#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 2018-12-03

@author: Byng Zeng
"""

import sys
import re
import urllib
import os
import ssl
import gzip
import io
import requests
import subprocess
import socket

from pybase.pypath import make_path, get_abs_path, get_download_path
from pybase.pyfile import get_name_ex
from pybase.pyprint import PyPrint, PR_LVL_ALL
from web.weburl import convert_url_to_title

if sys.version_info[0] == 2:
    from urllib2 import Request, urlopen, URLError, HTTPError
else:
    from urllib.request import Request, urlopen, URLError, HTTPError


VERSION = '1.1.0'
AUTHOR = 'Byng.Zeng'


DEFAULT_WEB_URL_FILE = r'weburl.txt'


CONTEXT_UNVERIFIED = ssl._create_unverified_context()
CONTEXT_TLSv1 = ssl.SSLContext(ssl.PROTOCOL_TLSv1)

USER_AGENTS = {
    'AppleWebKit/537.36':
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 '
        '(KHTML, like Gecko) Chrome/34.0.1847.137 Safari/537.36 LBBROWSER',
    'Gecko/20071127':
        'Mozilla/5.0 (Windows NT 6.2; rv:16.0) Gecko/20100101 Firefox/16.0',
    'Gecko/20070731':
        'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.0.12) '
        'Gecko/20070731 Ubuntu/dapper-security Firefox/1.5.0.12',
    'Gecko/20100101':
        'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:10.0) '
        'Gecko/20100101 Firefox/10.0',
    'Lynx/2.8.5rel.1':
        'Lynx/2.8.5rel.1 libwww-FM/2.14 SSL-MM/1.4.1 GNUTLS/1.2.9',
    'AppleWebKit/535.7':
        'Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.7 (KHTML, like Gecko) '
        'Ubuntu/11.04 Chromium/16.0.912.77 Chrome/16.0.912.77 Safari/535.7',
    'Kubuntu':
        'Mozilla/5.0 (compatible; Konqueror/3.5; Linux) '
        'KHTML/3.5.5 (like Gecko) (Kubuntu)',
}

URL_HEADER = {
    'User-Agent': '%s' % USER_AGENTS['AppleWebKit/537.36'],
    'Accept': 'text/html,application/xhtml+xml,application/xml;'
              'q=0.9,*/*;q=0.8',
    'Connection': 'keep-alive',
}

DEFAULT_CHARSET = r'GB2312'

CHARSETS = ('UTF-8', 'GB2312', 'GBK')


pr = PyPrint('WebContent')


def url_is_https(url):
    if re.match('https://', url):
        return True
    else:
        return False


def get_url_charset(html=None, content_type=None):
    charset = None
    pattern = re.compile('charset=[a-z0-8-]*', flags=re.I)
    if content_type:
        charset = pattern.search(
                    re.sub('charset=(\"|\')', 'charset=', content_type))
    if all((html, not charset)):
        charset = pattern.search(
                    re.sub('charset=(\"|\')', 'charset=', str(html)))
    # get data
    if charset:
        charset = charset.group()
        charset = charset[len('charset='):].upper()
    return charset


def get_html(url, context=None, retry_times=3, view=False, pr=pr):
    if view:
        pr.pr_info('Downloading: %s' % url)
    html_content = None
    while all((retry_times, not html_content)):
        retry_times -= 1
        url_charset = None
        req = Request(url, headers=URL_HEADER)
        try:
            html = urlopen(req, context=context)
        except URLError as e:
            pr.pr_warn(str(e))
            html_content = None
        else:
            try:
                content_type = html.getheader('Content-Type')
            except AttributeError as e:
                pr.pr_warn(str(e))
            else:
                if content_type:
                    url_charset = \
                        get_url_charset(content_type=content_type)
            data = html.read()
            try:
                encoding = html.getheader('Content-Encoding')
            except AttributeError as e:
                pr.pr_warn(str(e))
            else:
                if encoding == 'gzip':
                    data = gzip.GzipFile(fileobj=io.StringIO(data)).read()
            if data:
                for charset in CHARSETS:
                    if url_charset:
                        html_content = \
                            data.decode(url_charset,
                                        'ignore').encode('utf-8')
                        break
                    else:
                        html_content = \
                            data.decode(charset, 'ignore').encode('utf-8')
                        if html_content:
                            url_charset = get_url_charset(html_content)
                            if not url_charset:
                                url_charset = DEFAULT_CHARSET
                            elif charset == url_charset:
                                break
            else:
                # cls.pr.pr_err('Error: fail to get data from html')
                html_content = None
    return html_content


def get_url_content(url, retry_times=3, view=True, path=None):
    if url_is_https(url):
        content = get_html(url=url, context=CONTEXT_UNVERIFIED,
                           retry_times=retry_times, view=view)
    else:
        content = get_html(url=url, retry_times=retry_times, view=view)
    if all((content, path)):
        make_path(path)
        f = '%s/%s' % (path, convert_url_to_title(url))
        if get_name_ex(f) != '.html':
            f = f + '.html'
        with open(f, 'w') as fd:
            fd.write(content.decode())
    return content


def urlretrieve_callback(blocknum, blocksize, totalsize, pr=pr):
    if not totalsize:
        return
    percent = 100.0 * blocknum * blocksize / totalsize
    if percent > 100:
        percent = 100
    pr.pr_dbg("%.2f%%" % percent)


def retrieve_url_file(url, path, view=False, pr=pr):
    fname = os.path.join(path, url.split('/')[len(url.split('/')) - 1])
    if not os.path.exists(fname):
        if view:
            pr.pr_info('retrieve: %s' % fname)
            try:
                urllib.urlretrieve(url, fname, urlretrieve_callback)
            except socket.error or ZeroDivisionError as e:
                pr.pr_info('urlretrieve error: %s' % e.errno)
        else:
            try:
                urllib.urlretrieve(url, fname)
            except socket.error as e:
                pr.pr_warn('%s, retrieve %s failed.' % (str(e), url))


def urlopen_get_url_file(url, path,
                         ssl=False, headers=None, view=False, pr=pr):
    fname = os.path.join(path, url.split('/')[len(url.split('/')) - 1])
    if not os.path.exists(fname):
        req = Request(url=url)
        if headers:
            for key, value in headers.items():
                req.add_header(key, value)
        if ssl:
            context = CONTEXT_UNVERIFIED
        else:
            context = None
        try:
            r = urlopen(req, context=context)
        except (URLError, HTTPError) as e:
            pr.pr_warn('%s, uget %s failed.' % (str(e), url))
        else:
            try:
                data = r.read()
            except socket.ConnectionResetError as e:
                pr.pr_err(str(e))
            else:
                with open(fname, 'wb') as f:
                    if view:
                        pr.pr_info('uget: %s' % fname)
                    f.write(data)


def requests_get_url_file(url, path, view=False, pr=pr):
    fname = os.path.join(path, url.split('/')[len(url.split('/')) - 1])
    if not os.path.exists(fname):
        r = requests.get(url)
        with open(fname, 'wb') as f:
            if view:
                pr.pr_info('requests get: %s' % fname)
            f.write(r.content)


def wget_url_file(
        url, path, view=False,
        config='-c -t 3 -T 10 -U \'%s\'' % USER_AGENTS['Kubuntu'], pr=pr):
    if view:
        cmd = 'wget %s -P %s %s -nv' % (config, path, url)
    else:
        cmd = 'wget %s -P %s %s -q' % (config, path, url)
    try:
        pr.pr_dbg('wget cmd: %s' % cmd)
        return subprocess.check_output(cmd, shell=True)
    except subprocess.CalledProcessError:
        return None


def get_url_title(html_content, pattern=None):
    if not pattern:
        pattern = re.compile(b'(?<=<title>).+(?=</title>)')
    data = pattern.search(html_content)
    if data:
        return data.group()
    else:
        return None


def get_url_pages(html, pattern=None):
    if not pattern:
        # find all of \d+/\d+
        pattern = re.compile('\d+/\d+')
    data = pattern.findall(str(html))
    if data:
        # match ^1/\d+$ to get number of pages.
        pattern = re.compile('^1/\d+$')
        for d in data:
            d = pattern.match(d)
            if d:
                # getnumber of pages and return int.
                pages = int(re.compile('\d+').findall(d.group())[1])
                break
            else:
                pages = None
    else:
        pages = None
    return pages


class WebContent (object):

    pr = PyPrint('WebContent')

    @staticmethod
    def url_is_https(url):
        return url_is_https(url)

    @staticmethod
    def get_url_charset(html=None, content_type=None):
        return get_url_charset(html, content_type)

    @classmethod
    def get_html(cls, url, context=None, retry_times=3, view=False):
        return get_html(url, context, retry_times, view, cls.pr)

    @staticmethod
    def get_url_content(url, retry_times=3, view=True, path=None):
        return get_url_content(url, retry_times, view, path)

    @classmethod
    def urlretrieve_callback(cls, blocknum, blocksize, totalsize):
        return urlretrieve_callback(blocknum, blocksize, totalsize, cls.pr)

    @staticmethod
    def retrieve_url_file(cls, url, path, view=False):
        return retrieve_url_file(url, path, view, cls.pr)

    @classmethod
    def urlopen_get_url_file(cls, url, path,
                             ssl=False, headers=None, view=False):
        return urlopen_get_url_file(url, path, ssl, headers, view, cls.pr)

    @classmethod
    def requests_get_url_file(cls, url, path, view=False):
        return requests_get_url_file(url, path, view, cls.pr)

    @classmethod
    def wget_url_file(
            cls, url, path, view=False,
            config='-c -t 3 -T 10 -U \'%s\'' % USER_AGENTS['Kubuntu']):
        return wget_url_file(url, path, view, config, cls.pr)

    @staticmethod
    def get_url_title(html_content, pattern=None):
        return get_url_title(html_content, pattern)

    @staticmethod
    def get_url_pages(html, pattern=None):
        return get_url_pages(html, pattern)


if __name__ == '__main__':
    from pybase.pysys import print_help, print_exit
    from pybase.pyinput import get_input_args

    HELP_MENU = (
        '==================================',
        '    WebContentApp - %s' % VERSION,
        '',
        '    @Author: %s' % AUTHOR,
        '    Copyright (c) %s studio' % AUTHOR,
        '==================================',
        'option:',
        '  -u url:',
        '    url of web to be download',
        '  -p path:',
        '    path to store data.',
        '  -d mode:',
        '    wget: using wget to download file',
        '    rtrv: using retrieve to download file',
        '    rget: using requests to download file',
        '    uget: using urlopen to download file',
        '    html: download html of url',
        '  -v:',
        '    view info of webcontent.',
    )

    wc = WebContent()
    pr = PyPrint(wc.__class__.__name__)

    path = '%s/%s' % (get_download_path(), wc.__class__.__name__)
    url = None
    df = None
    view = False

    args = get_input_args('hp:u:d:v')
    for k in args.keys():
        if k == '-u':
            url = args['-u']
        elif k == '-v':
            view = True
            wc.pr.level = PR_LVL_ALL
        elif k == '-d':
            df_funcs = {
                'wget': wc.wget_url_file,
                'rtrv': wc.retrieve_url_file,
                'rget': wc.requests_get_url_file,
                'uget': wc.urlopen_get_url_file,
                'html': wc.get_url_content,
            }
            w = args[k]
            if w in df_funcs:
                df = df_funcs[w]
            else:
                print_exit('-d %s error, -h for help!' % args['-d'])
        elif k == '-p':
            path = get_abs_path(args['-p'])
        elif k == '-h':
            print_help(HELP_MENU)
    # run cmd
    if all((df, url)):
        df(url=url, path=path, view=view)
