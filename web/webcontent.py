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
import subprocess

from mypy import MyPath, MyFile

URL_HEADER = {
    #'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; rv:16.0) Gecko/20100101 Firefox/16.0',
    'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.204 Safari/534.16',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Connection': 'keep-alive',
    #'Accept-Language': 'zh-CN,zh;q=0.8',
    #'Accept-Encoding': 'gzip, deflate, sdch, br',

    #'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.204 Safari/534.16',
    #'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; rv:16.0) Gecko/20100101 Firefox/16.0'
    #'Cache-Control': 'max-age=0'
    #'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.137 Safari/537.36 LBBROWSER',
    #'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11',
    #'User-Agent': 'Opera/9.25 (Windows NT 5.1; U; en)',
    #'User-Agent': 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
    #'User-Agent': 'Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5 (like Gecko) (Kubuntu)',
    #'User-Agent': 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.0.12) Gecko/20070731 Ubuntu/dapper-security Firefox/1.5.0.12',
    #'User-Agent': 'Lynx/2.8.5rel.1 libwww-FM/2.14 SSL-MM/1.4.1 GNUTLS/1.2.9',
    #'User-Agent': 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.7 (KHTML, like Gecko) Ubuntu/11.04 Chromium/16.0.912.77 Chrome/16.0.912.77 Safari/535.7',
    #'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:10.0) Gecko/20100101 Firefox/10.0',
    #'Host': 'ptlogin2.qq.com',
}

UserAgent = r'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.204 Safari/534.16'

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
    def get_html(cls, url, context=None, retry_times=3, view=True):
        if view:
            print('Downloading: %s' % url)
        for index in range(retry_times):
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
            # get content and break.
            if html_content:
                break
        return html_content

    @classmethod
    def get_url_content(cls, url, retry_times=3, view=True):
        if re.match('https://', url):
            return cls.get_html(url = url, context = cls.CONTEXT_UNVERIFIED, retry_times = retry_times,view = view)
        else:
            return cls.get_html(url = url, retry_times = retry_times, view = view)

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
    def requests_get_url_file(cls, url, path):
        path = path.strip()
        MyPath.make_path(path)
        fname = os.path.join(path, url.split('/')[len(url.split('/')) - 1])
        if not os.path.exists(fname):
            r = requests.get(url)
            with open(fname, 'wb') as f:
                f.write(r.content)

    @classmethod
    def wget_url_file(cls, url, path, view=False):
        if view:
            cmd = 'wget -c --tries=3 --timeout=10 -P %s %s -nv -U \'%s\'' % (path, url, UserAgent)
        else:
            cmd = 'wget -c --tries=3 --timeout=10 -P %s %s -q -U \'%s\'' % (path, url, UserAgent)
        try:
            return subprocess.check_output(cmd, shell=True)
        except subprocess.CalledProcessError:
            return None

    @classmethod
    def get_url_title(cls, html_content, pattern=None):
        if pattern:
            return pattern.search(html_content)
        else:
            pattern=re.compile('<title>.+</title>')
            data = pattern.search(html_content)
            if data:
                data = data.group()
                return re.sub(' ', '_', data[len('<title>') : len(data) - len('</title>')])
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
        return MyFile.reclaim_name(re.sub('/$', '', url))

if __name__ == '__main__':

    from mypy import MyBase, MyPrint

    HELP_MENU = (
        '==================================',
        '    WebContentApp help',
        '==================================',
        'option: -u url -p path -c cmd',
        '  -u url:',
        '    url of web to be download',
        '  -p path:',
        '    path to store data.',
        '  -c cmd:',
        '    wget: using wget to download file',
        '    retrv: using retrieve to download file',
        '    reqget: using requests to download file',
        '    html: download html of url'
    )

    CMD_LIST = ('wget', 'retrv', 'reqget', 'html')

    path = None
    url = None
    cmd = None

    args = MyBase.get_user_input('hp:u:c:')
    if '-h' in args:
        MyBase.print_help(HELP_MENU)
    if '-p' in args:
        path = MyPath.get_abs_path(args['-p'])
    if '-u' in args:
        url = args['-u']
    if '-c' in args:
        if all((args['-c'] in CMD_LIST, url)):
            cmd = args['-c']
        else:
            MyBase.print_exit('-c or -u error, -h for help!')

    wc = WebContent()
    pr = MyPrint('WebContent')

    # config default path
    if not path:
        path = '%s/%s' % (MyPath.get_download_path(), wc.__class__.__name__)
    # run cmd
    if cmd == 'wget':
        wc.wget_url_file(url, path)
        pr.pr_info('wget %s to %s' % (url, path))
    elif cmd == 'retrv':
        wc.retrieve_url_file(url, path)
        pr.pr_info('retrieve %s to %s' % (url, path))
    elif cmd == 'reqget':
        wc.requests_get_url_file(url, path)
        pr.pr_info('requests_get %s to %s' % (url, path))
    elif cmd == 'html':
        html = wc.get_url_content(url)
        if html:
            MyPath.make_path(path)
            f = '%s/%s' % (path, wc.convert_url_to_title(url))
            if MyFile.get_exname(f) != '.html':
                f = f + '.html'
            with open(f, 'w') as fd:
                fd.write(html)
        else:
            pr.pr_err('Error, failed to store html data.')