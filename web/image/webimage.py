#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on: 2018-12-07

@author: Byng Zeng
"""
import os
import re

from mypy import MyPy
from webcontent import WebContent
from image import Image



enable_debug = False

def pr_dbg(fmt):
    if enable_debug and fmt:
        print(fmt)

class WebImage(WebContent):

    help_menu = (
        '==================================',
        '    WebImage help',
        '==================================',
        'option: -u url -n number -p path -x val -v',
        '  -u:',
        '    url of web to be download',
        '  -n:',
        '    number of web number to be download',
        '  -p:',
        '    root path to store images.',
        '  -v:',
        '     show info while download.',
        '  -x:',
        '     val for expand cmd.',
    )

    def get_image_url(self, html):
        if not self._re_image_url:
            pattern = re.compile('http(s)?://.+\.(jpg|png|gif|bmp|jpeg)')
        else:
            pattern = self._re_image_url
        # find image.
        try:
            imgs = pattern.findall(html)
            pr_dbg('get image url: %s' % imgs)
        except TypeError as e:
            print('%s: failed to findall image url' , (e.reason))
        return imgs

    def get_image_url_of_pages(self, pages):
        limg = list()
        url_pages = self.get_url_of_pages(pages)
        pr_dbg('get url_pages: %s' % url_pages)
        for url in url_pages:
            url_content = self.get_url_content(url, show=False)
            if not url_content:
                print('Error, failed to download %s' % url)
                continue
            pr_dbg('start to get image from: %s' % url)
            imgs = self.get_image_url(url_content)
            for img in imgs:
                limg.append(img)
        return limg

    def get_image_raw_url(self, url):
        return url[1]

    def retrieve_url_image(self, url, path):
        return self.retrieve_get_url_file(url, path)

    def __init__(self):
        super(WebContent, self).__init__()
        self._url_base = None
        self._url = None
        self._num = 1
        self._path = '%s/WebImage' % MyPy.DEFAULT_DOWNLOAD_PATH
        self._re_image_url = re.compile('(src=|src=\'|src=\")(http(s)?://[\w\-\/\.]*?\.(jpg|png|gif))(\'|\")?', re.IGNORECASE)
        self._re_pages = None
        self._title = None
        self._remove_small_image = True
        self._show = False
        self._xval = None

    def get_user_input(self):
        args = MyPy.get_user_input('hu:n:p:x:v')
        if '-h' in args:
            MyPy.print_help(self.help_menu)
        if '-u' in args:
            self._url = args['-u']
        if '-n' in args:
            self._num = int(args['-n'])
        if '-p' in args:
            self._path = os.path.abspath(args['-p'])
        if '-v' in args:
            self._show = True
        if '-x' in args:
            self._xval = args['-x']
        # check url
        if self._url:
            base, num = self.get_url_base_and_num(self._url)
            if base:
                self._url_base = base
            if num:
                self._url = num
            pr_dbg('get base: %s, url: %s' % (base, self._url))
        else:
            MyPy.print_exit('Error, no set url, -h for help!')

    def update_url_content(self, url_content):
        return url_content

    def get_title(self, html, pattern=None):
        return self.get_url_title(html, pattern)

    def get_pages(self, html, pattern=None):
        return self.get_url_pages(html, pattern)

    def download_images(self, imgs, path):
        for img in imgs:
            self.retrieve_url_image(self.get_image_raw_url(img), path)

    def store_web_info(self, path, title, url):
        with open('%s/%s' % (path, self.WEB_URL_FILE), 'w') as fd:
            fd.write('%s\n%s' % (title, url))

    def get_url_of_pages(self, num):
        url = map(lambda x: self.set_url_base_and_num(self._url_base, '%s/%d' % (int(self._url), x)), range(2, num + 1))
        url.insert(0, self.set_url_base_and_num(self._url_base, self._url))
        return url

    def main(self):
        self.get_user_input()
        # get web now.
        for index in range(self._num):
            # get the first page.
            if self._url_base:
                url_header = self.set_url_base_and_num(self._url_base, int(self._url) + index)
            else:
                url_header = self.set_url_base_and_num(None, self._url)
            url_content = self.get_url_content(url_header)
            if not url_content:
                print('Error, failed to download %s' % url_header)
                continue
            # overwrite it to update url content
            url_content = self.update_url_content(url_content)
            # get url title.
            title = self.get_title(url_content, self._title)
            if not title:
                title = self.convert_url_to_title(url_header)
            pr_dbg('title: %s' % title )
            # create path of title to store data.
            subpath = os.path.join(self._path, title)
            pr_dbg('subpath: %s' % subpath)
            MyPy.make_path(subpath)
            # get count of pages
            pages = self.get_pages(url_content)
            pr_dbg('get pages: %s' % pages)
            if not pages:
                limgs = self.get_image_url(url_content)
            else:
                limgs = self.get_image_url_of_pages(pages)
            # filter images
            limgs = set(limgs)
            pr_dbg('image url: %s' % limgs)
            # download images
            if limgs:
                self.download_images(limgs, subpath)
                # write web info
                self.store_web_info(subpath, title, url_header)
            # remove small image
            if self._remove_small_image:
                Image.remove_small_image(subpath)
            if self._show:
                print('output: %s' % (subpath))

if __name__ == '__main__':
    dwimg = WebImage()
    dwimg.main()
