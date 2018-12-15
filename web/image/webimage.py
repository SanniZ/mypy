#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on: 2018-12-07

@author: Byng Zeng
"""
import os
import re

from mypy import MyBase, MyPath, MyPrint
from webcontent import WebContent, UserAgent
from image import Image


class WebImage(object):

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
        '     view info while download.',
        '  -x:',
        '     val for expand cmd.',
    )

    def __init__(self, name=None):
        self._name = name
        self._url_base = None
        self._url = None
        self._num = 1
        self._path = '%s/%s' %  (MyBase.DEFAULT_DWN_PATH, self.__class__.__name__)
        self._re_image_url = re.compile('src=[\'|\"]?(http[s]?://.+\.(?:jpg|png|gif|bmp|jpeg))[\'|\"]?')
        self._title = None
        self._remove_small_image = True
        self._view = False
        self._xval = None
        self._redundant_title = None
        self._pr = MyPrint('WebImage')

    def get_user_input(self):
        args = MyBase.get_user_input('hu:n:p:x:vd')
        if '-h' in args:
            MyBase.print_help(self.help_menu)
        if '-u' in args:
            self._url = re.sub('/$', '', args['-u'])
        if '-n' in args:
            self._num = int(args['-n'])
        if '-p' in args:
            self._path = os.path.abspath(args['-p'])
        if '-v' in args:
            self._view = True
        if '-x' in args:
            self._xval = args['-x']
        if '-d' in args:
            self._pr.set_pr_level(self._pr.get_pr_level() | MyPrint.PR_LVL_DBG)
        # check url
        if self._url:
            base, num = WebContent.get_url_base_and_num(self._url)
            if base:
                self._url_base = base
            if num:
                self._url = num
            self._pr.pr_dbg('get base: %s, url: %s' % (base, self._url))
        else:
            MyBase.print_exit('Error, no set url, -h for help!')
        return args

    def get_image_url(self, html):
        if not self._re_image_url:
            pattern = re.compile('src=[\'|\"]?(http[s]?://.+\.(?:jpg|png|gif|bmp|jpeg))[\'|\"]?')
        else:
            pattern = self._re_image_url
        # find image.
        try:
            imgs = pattern.findall(html)
            #self._pr.pr_dbg('%s' % imgs)
        except TypeError as e:
           self._pr.pr_err('%s: failed to findall image url' , (e.reason))
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
                self._pr.pr_err('Error, failed to download %s sub web' % url_pages[index])
                continue
            imgs = self.get_image_url(url_content)
            for img in imgs:
                limg.append(img)
        return limg

    def get_image_raw_url(self, url):
        return url

    def retrieve_url_image(self, url, path):
        return WebContent.retrieve_url_file(url, path)

    def wget_url_image(self, url, path):
        return WebContent.wget_url_file(url, path, '-c -t 3 -T 10 -U \'%s\'' % UserAgent, self._view)

    def requests_get_url_image(self, url, path):
        return WebContent.requests_get_url_file(url, path)

    def download_image(self, url, path):
        self.retrieve_url_image(url, path)

    def get_url_content(self, url, view=False):
        return WebContent.get_url_content(url=url, view=view)

    def get_title(self, html, pattern=None):
        title = WebContent.get_url_title(html, pattern)
        if self._redundant_title:
            for rt in self._redundant_title:
                title = title.replace(rt, '')
        return title

    def get_pages(self, html, pattern=None):
        return WebContent.get_url_pages(html, pattern)

    def download_images(self, imgs, path):
        for img in imgs:
            self.download_image(self.get_image_raw_url(img), path)

    def store_web_info(self, path, title, url):
        with open('%s/%s' % (path, WebContent.WEB_URL_FILE), 'w') as fd:
            fd.write('%s\n%s' % (title, url))

    def get_url_of_pages(self, num):
        url = map(lambda x: WebContent.set_url_base_and_num(self._url_base, '%s/%d' % (int(self._url), x)), range(2, num + 1))
        url.insert(0, WebContent.set_url_base_and_num(self._url_base, self._url))
        return url

    def get_url_address(self, url_base, url):
        return WebContent.set_url_base_and_num(url_base, url)

    def convert_url_to_title(self, url):
        return WebContent.convert_url_to_title(url)

    def main(self):
        self.get_user_input()
        # get web now.
        for index in range(self._num):
            # get the first page.
            if self._url_base:
                url_header = self.get_url_address(self._url_base, int(self._url) + index)
            else:
                url_header = self.get_url_address(None, self._url)
            # get header web
            header_content = self.get_url_content(url_header, True)
            if not header_content:
                self._pr.pr_err('Error, failed to download %s header web.' % url_header)
                continue
            # get url title.
            title = self.get_title(header_content, self._title)
            if not title:
                title = self.convert_url_to_title(url_header)
            self._pr.pr_dbg('title: %s' % title )
            # create path of title to store data.
            subpath = os.path.join(self._path, title)
            self._pr.pr_dbg('subpath: %s' % subpath)
            # get count of pages
            pages = self.get_pages(header_content)
            self._pr.pr_dbg('get pages: %s' % pages)
            if not pages:
                imglist = self.get_image_url(header_content)
            else:
                imglist = self.get_image_url_of_pages(pages, header_content)
            # filter images
            imglist = set(imglist)
            self._pr.pr_dbg('image url list: %s' % imglist)
            # download images
            if imglist:
                # create path
                MyPath.make_path(subpath)
                # download all of images.
                self.download_images(imglist, subpath)
                # write web info
                self.store_web_info(subpath, title, url_header)
                # reclaim image, remove small image
                if self._remove_small_image:
                    print 'remove small image'
                    Image.reclaim_path_images(subpath, xfunc=Image.remove_small_image)
                else:
                    Image.reclaim_path_images(subpath)
                # show output info.
                if self._view:
                    self._pr.pr_info('output: %s' % (subpath))

if __name__ == '__main__':
    dwimg = WebImage()
    dwimg.main()
