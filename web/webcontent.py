#!/usr/bin/python3
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

from mypy.path import Path
from mypy.file import File
from mypy.pr import Print

if sys.version_info[0] == 2:
    from urllib2 import Request, urlopen, URLError, HTTPError
else:
    from urllib.request import Request, urlopen, URLError, HTTPError

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


class WebContent (object):

    CONTEXT_UNVERIFIED = ssl._create_unverified_context()
    CONTEXT_TLSv1 = ssl.SSLContext(ssl.PROTOCOL_TLSv1)

    WEB_URL_FILE = r'weburl.txt'

    pr = Print('WebContent')

    @classmethod
    def url_is_https(cls, url):
        if re.match('https://', url):
            return True
        else:
            return False

    @classmethod
    def get_url_charset(cls, html=None, content_type=None):
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

    @classmethod
    def get_html(cls, url, context=None, retry_times=3, view=False):
        if view:
            cls.pr.pr_info('Downloading: %s' % url)
        html_content = None
        while all((retry_times, not html_content)):
            retry_times -= 1
            url_charset = None
            req = Request(url, headers=URL_HEADER)
            try:
                html = urlopen(req, context=context)
            except URLError as e:
                cls.pr.pr_warn(str(e))
                html_content = None
            else:
                try:
                    content_type = html.getheader('Content-Type')
                except AttributeError as e:
                    cls.pr.pr_warn(str(e))
                else:
                    if content_type:
                        url_charset = \
                            cls.get_url_charset(content_type=content_type)
                data = html.read()
                try:
                    encoding = html.getheader('Content-Encoding')
                except AttributeError as e:
                    cls.pr.pr_warn(str(e))
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
                                url_charset = cls.get_url_charset(html_content)
                                if not url_charset:
                                    url_charset = DEFAULT_CHARSET
                                elif charset == url_charset:
                                    break
                else:
                    # cls.pr.pr_err('Error: fail to get data from html')
                    html_content = None
        return html_content

    @classmethod
    def get_url_content(cls, url, retry_times=3, view=True, path=None):
        if cls.url_is_https(url):
            content = cls.get_html(url=url, context=cls.CONTEXT_UNVERIFIED,
                                   retry_times=retry_times, view=view)
        else:
            content = cls.get_html(url=url, retry_times=retry_times, view=view)
        # save content to path.
        if all((content, path)):
            Path.make_path(path)
            f = '%s/%s' % (path, cls.convert_url_to_title(url))
            if File.get_name_ex(f) != '.html':
                f = f + '.html'
            with open(f, 'w') as fd:
                fd.write(content.decode())
        return content

    @classmethod
    def urlretrieve_callback(cls, blocknum, blocksize, totalsize):
        if not totalsize:
            return
        percent = 100.0 * blocknum * blocksize / totalsize
        if percent > 100:
            percent = 100
        cls.pr.pr_dbg("%.2f%%" % percent)

    @classmethod
    def retrieve_url_file(cls, url, path, view=False):
        fname = os.path.join(path, url.split('/')[len(url.split('/')) - 1])
        if not os.path.exists(fname):
            if view:
                cls.pr.pr_info('retrieve: %s' % fname)
                try:
                    urllib.urlretrieve(url, fname, cls.urlretrieve_callback)
                except socket.error or ZeroDivisionError as e:
                    cls.pr.pr_info('urlretrieve error: %s' % e.errno)
            else:
                try:
                    urllib.urlretrieve(url, fname)
                except socket.error as e:
                    cls.pr.pr_warn('%s, retrieve %s failed.' % (str(e), url))

    @classmethod
    def urlopen_get_url_file(cls, url, path,
                             ssl=False, headers=None, view=False):
        fname = os.path.join(path, url.split('/')[len(url.split('/')) - 1])
        if not os.path.exists(fname):
            req = Request(url=url)
            if headers:
                for key, value in headers.items():
                    req.add_header(key, value)
            if ssl:
                context = cls.CONTEXT_UNVERIFIED
            else:
                context = None
            try:
                r = urlopen(req, context=context)
            except (URLError, HTTPError) as e:
                cls.pr.pr_warn('%s, uget %s failed.' % (str(e), url))
            else:
                try:
                    data = r.read()
                except socket.ConnectionResetError as e:
                    cls.pr.pr_err(str(e))
                else:
                    with open(fname, 'wb') as f:
                        if view:
                            cls.pr.pr_info('uget: %s' % fname)
                        f.write(data)

    @classmethod
    def requests_get_url_file(cls, url, path, view=False):
        fname = os.path.join(path, url.split('/')[len(url.split('/')) - 1])
        if not os.path.exists(fname):
            r = requests.get(url)
            with open(fname, 'wb') as f:
                if view:
                    cls.pr.pr_info('requests get: %s' % fname)
                f.write(r.content)

    @classmethod
    def wget_url_file(
            cls, url, path, view=False,
            config='-c -t 3 -T 10 -U \'%s\'' % USER_AGENTS['Kubuntu']):
        if view:
            cmd = 'wget %s -P %s %s -nv' % (config, path, url)
        else:
            cmd = 'wget %s -P %s %s -q' % (config, path, url)
        try:
            cls.pr.pr_dbg('wget cmd: %s' % cmd)
            return subprocess.check_output(cmd, shell=True)
        except subprocess.CalledProcessError:
            return None

    @classmethod
    def get_url_title(cls, html_content, pattern=None):
        if not pattern:
            pattern = re.compile(b'(?<=<title>).+(?=</title>)')
        data = pattern.search(html_content)
        if data:
            return data.group()
        else:
            return None

    @classmethod
    def get_url_pages(cls, html, pattern=None):
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
        return File.reclaim_name(re.sub('/$', '', url))

    @classmethod
    def reclaim_url_address(cls, url):
        for key, value in {'/$': '', '\n$': ''}.items():
            url = re.sub(key, value, url)
        return url


if __name__ == '__main__':

    from mypy.base import Base

    HELP_MENU = (
        '==================================',
        '    WebContentApp help',
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

    path = None
    url = None
    df = None
    view = False

    wc = WebContent()
    pr = Print(wc.__class__.__name__)

    args = Base.get_user_input('hp:u:d:v')
    if '-h' in args:
        Base.print_help(HELP_MENU)
    if '-p' in args:
        path = Path.get_abs_path(args['-p'])
    if '-u' in args:
        url = args['-u']
    if '-v' in args:
        view = True
        wc.pr.set_pr_level(0x07)
    if '-d' in args:
        df_funcs = {
            'wget': wc.wget_url_file,
            'rtrv': wc.retrieve_url_file,
            'rget': wc.requests_get_url_file,
            'uget': wc.urlopen_get_url_file,
            'html': wc.get_url_content,
        }
        if all((args['-d'] in df_funcs.keys(), url)):
            df = df_funcs[args['-d']]
        else:
            Base.print_exit('-d %s error, -h for help!' % args['-d'])

    # config default path
    if not path:
        path = '%s/%s' % (Path.get_download_path(), wc.__class__.__name__)
    # run cmd
    if df:
        df(url=url, path=path, view=view)
