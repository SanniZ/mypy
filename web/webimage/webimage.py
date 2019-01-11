#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Created on: 2018-12-07

@author: Byng Zeng
"""
import os
import re
import sys

if sys.version_info[0] == 2:
    import Queue
else:
    from queue import Queue

import threading

from mypy.base import Base
from mypy.path import Path
from mypy.pr import Print

from web.webcontent import WebContent, USER_AGENTS
from image.image import Image


class WebImage(object):

    help_menu = (
        '==================================',
        '    WebImage help',
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
        '    val for expand cmd.',
        '  -m mode:',
        '    wget: using wget to download imgages',
        '    rtrv: using retrieve to download images',
        '    rget: using requests to download images',
        '    uget: using urlopen to download images',
        '  -R file:',
        '    re config file for re_image_url.'
        '  -t num:',
        '    set max number of thread to download web.'
    )

    def __init__(self, name=None):
        self._name = name
        self._com = None
        self._url_base = None
        self._url = None
        self._num = 1
        self._path = '%s/%s' %  (Base.DEFAULT_DWN_PATH, self.__class__.__name__)
        self._re_image_url = [
            #re.compile('src=[\'|\"]?(http[s]?://.+\.(?:jpg|png|gif|bmp|jpeg))[\'|\"]?', re.I),
            #re.compile('src=[\'|\"]?(/.+\.(?:jpg|png|gif|bmp|jpeg))[\'|\"]?', re.I),
            re.compile('src=[\'|\"]?(http[s]?://[a-z0-9\./-]+\.(?:jpg|png|gif|bmp|jpeg))[\'|\"]?', re.I),
            re.compile('src=[\'|\"]?(/[a-z0-9\./-]+\.(?:jpg|png|gif|bmp|jpeg))[\'|\"]?', re.I),
        ]
        self._ex_re_image_url = None
        self._title = None
        self._remove_small_image = True
        self._view = False
        self._xval = None
        self._dl_image = self.urlopen_get_url_image
        self._redundant_title = None
        self._pr = Print(self.__class__.__name__)
        self.__dbg = 0
        self._thread_max = 5
        self._thread_queue = None


    def get_image_url(self, html):
        pattern = self._re_image_url
        imgs = list()
        # find image.
        try:
            if type(pattern) == list:
                for pt in pattern:
                    imgs = imgs + pt.findall(str(html))
            else:
                imgs = pattern.findall(str(html))
            #self._pr.pr_dbg('%s' % imgs)
        except TypeError as e:
           self._pr.pr_err('%s: failed to findall image url' % str(e))
        return imgs

    def get_image_url_of_pages(self, pages, header_content=None):
        limg = list()
        url_pages = self.get_url_of_pages(pages)
        for index in range(len(url_pages)):
            if all((index == 0, header_content)):
                url_content = header_content
            else:
                url_content = self.get_url_content(url_pages[index])
            if not url_content:
                self._pr.pr_err('failed to download %s sub web' % url_pages[index])
                continue
            imgs = self.get_image_url(url_content)
            for img in imgs:
                limg.append(img)
        return limg

    def get_image_raw_url(self, url):
        if not re.match('http(s)?:', url):
            url = '%s%s' % (self._com, url)
        return url

    def retrieve_url_image(self, url, path, view=False):
        return WebContent.retrieve_url_file(url, path, view=view)

    def wget_url_image(self, url, path, view=False):
        return WebContent.wget_url_file(url, path,
                                        config="-c -t 3 -T 10 -U \'%s\'" % USER_AGENTS['AppleWebKit/537.36'],
                                        view=view)

    def requests_get_url_image(self, url, path, view=False):
        return WebContent.requests_get_url_file(url, path, view=view)



    def urlopen_get_url_image(self, url, path, view=False):
        headers = {
            'User-Agent': '%s' % USER_AGENTS['AppleWebKit/537.36'],
            'GET' : url,
            'Referer' : self._com,
        }
        return WebContent.urlopen_get_url_file(url, path,
                                               ssl=WebContent.url_is_https(url),
                                               headers=headers, view=view)

    # download image of url.
    def download_image(self, url, path):
        if self._dl_image:
            Path.make_path(path)
            self._dl_image(url, path, self.__dbg)

    def get_url_content(self, url, view=False):
        return WebContent.get_url_content(url=url, view=view)

    def get_title(self, html, pattern=None):
        title = WebContent.get_url_title(html, pattern).decode()
        if self._redundant_title:
            for rt in self._redundant_title:
                title = title.replace(rt, '')
        return title

    def get_pages(self, html, pattern=None):
        return WebContent.get_url_pages(html, pattern)

    def download_images(self, imgs, path):
        for img in imgs:
            self.download_image(self.get_image_raw_url(img), path)

    def get_url_of_pages(self, num):
        url = map(lambda x: WebContent.set_url_base_and_num(self._url_base,
                                                            '%s/%d' % (int(self._url), x)),
                                                            range(2, num + 1))
        url.insert(0, WebContent.set_url_base_and_num(self._url_base, self._url))
        return url

    def get_url_address(self, url_base, url):
        return WebContent.set_url_base_and_num(url_base, url)

    def convert_url_to_title(self, url):
        return WebContent.convert_url_to_title(url)

    def store_web_info(self, path, title, url):
        with open('%s/%s' % (path, WebContent.WEB_URL_FILE), 'w') as fd:
            fd.write('%s\n%s' % (title, url))

    def store_url_of_images(self, path, urls):
        with open('%s/%s' % (path, WebContent.WEB_URL_FILE), 'a') as fd:
            fd.write('\n')
            fd.write('\n')
            fd.write('url of imgs:\n')
            for url in urls:
                fd.write('%s\n' % url)

    def output_image_exists(self, path):
        for rt, ds, fs in os.walk(path):
            if fs:
                for f in fs:
                    f = os.path.join(rt, f)
                    if Image.image_file_ex(f):
                        return True
        return False

    def add_external_re_image_url(self):
        if self._ex_re_image_url:
            relist = list()
            try:
                with open(self._ex_re_image_url, 'r') as fd:
                    lines = fd.readlines()
                # list all of lines.
                for line in lines:
                    line = re.sub('\n', '', line)
                    relist.append(re.compile(line))
                # add old lines.
                if type(self._re_image_url) == list:
                    for r in self._re_image_url:
                        relist.append(r)
                else:
                    relist.append(self._re_image_url)
                # update re_image_url
                self._re_image_url = relist
            except IOError as e:
                self._pr.pr_err('%s, failed to open %s' % (str(e), self._ex_re_image_url))

    # process url web images.
    def process_url_web(self, url, data=None):
        # get header web
        header_content = self.get_url_content(url, view=False)
        if not header_content:
            if self._thread_queue:
                self._thread_queue.get()
            self._pr.pr_err('failed to download %s header web.' % url)
            return
        # get url title.
        title = self.get_title(header_content, self._title)
        if not title:
            title = self.convert_url_to_title(url)
        self._pr.pr_dbg('title: %s' % title)
        # create path of title to store data.
        subpath = os.path.join(self._path, title)
        self._pr.pr_dbg('subpath: %s' % subpath)
        # get count of pages
        pages = self.get_pages(header_content)
        self._pr.pr_dbg('get pages: %s' % pages)
        if not pages:
            limg = self.get_image_url(header_content)
        else:
            limg = self.get_image_url_of_pages(pages, header_content)
        # filter images
        limg = set(limg)
        # self._pr.pr_dbg('image url list: %s' % limg)
        # download images
        if limg:
            # download all of images.
            self.download_images(limg, subpath)
            # write web info
            self.store_web_info(subpath, title, url)
            # reclaim image, remove small image
            Image.reclaim_path_images(subpath, self._remove_small_image)
            # show output info.
            if self._view:
                if self.output_image_exists(subpath):
                    self._pr.pr_info('output: %s' % (subpath))
                else:
                    self._pr.pr_info('output no images: %s' % (subpath))
            # save url of images if it is full debug.
            if self.__dbg >= 2:
                self.store_url_of_images(subpath, limg)
        # release queue
        if self._thread_queue:
            self._thread_queue.get()
        if data:
            self._pr.pr_info('%d/%d: process %s done!' % (data[0], data[1], url))
        return subpath

    def get_user_input(self, args=None):
        if not args:
            args = Base.get_user_input('hu:n:p:x:m:i:R:t:vdD')
        if '-h' in args:
            Base.print_help(self.help_menu)
        if '-u' in args:
            self._url = re.sub('/$', '', args['-u'])
        if '-n' in args:
            self._num = int(args['-n'])
        if '-p' in args:
            self._path = os.path.abspath(args['-p'])
        if '-R' in args:
            self._ex_re_image_url = os.path.abspath(args['-R'])
        if '-t' in args:
            try:
                n = int(args['-t'])
            except ValueError as e:
                Base.print_exit('%s, -h for help!' % str(e))
            if n:
                self._thread_max = n
        if '-v' in args:
            self._view = True
            self._pr.set_pr_level(self._pr.get_pr_level() | Print.PR_LVL_WARN)
        if '-x' in args:
            self._xval = args['-x']
        if '-m' in args:
            dl_image_funcs = {
                'wget': self.wget_url_image,
                'rtrv' : self.retrieve_url_image,
                'rget' : self.requests_get_url_image,
                'uget' : self.urlopen_get_url_image,
            }
            if args['-m'] in dl_image_funcs.keys():
                self._dl_image = dl_image_funcs[args['-m']]
        if '-d' in args:
            self.__dbg = 1
            self._pr.set_pr_level(self._pr.get_pr_level() | Print.PR_LVL_ALL )
        if '-D' in args:
            self.__dbg = 2
            self._pr.set_pr_level(self._pr.get_pr_level() | Print.PR_LVL_DBG)
            WebContent.pr.set_pr_level(self._pr.get_pr_level() | Print.PR_LVL_DBG)
        # check url
        if self._url:
            base, num = WebContent.get_url_base_and_num(self._url)
            if base:
                self._url_base = base
            if num:
                self._url = num
            self._pr.pr_dbg('get base: %s, url: %s' % (base, self._url))
        else:
            Base.print_exit('[WebImage] Error, no set url, -h for help!')
        if self._url_base:
            www_com = re.match('http[s]?://.+\.(com|cn|net)', self._url_base)
            if www_com:
                self._com = www_com.group()
        return args

    def main(self, args=None):
        self.get_user_input(args)
        # get external re file.
        if self._ex_re_image_url:
            self.add_external_re_image_url()
        # create queue.
        if self._num > self._thread_max:
            self._thread_queue = Queue(self._thread_max)
        # get web now.
        for index in range(self._num):
            # get the first page.
            if self._url_base:
                url = self.get_url_address(self._url_base, int(self._url) + index)
            else:
                url = self.get_url_address(None, self._url)
            if self._thread_queue:
                # create thread and put to queue.
                t = threading.Thread(target=self.process_url_web, args=(url, (index + 1, self._num)))
                self._thread_queue.put(url)
                t.start()
            else:
                return self.process_url_web(url)


if __name__ == '__main__':
    wi = WebImage('WebImage')
    wi.main()
