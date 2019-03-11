#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on: 2018-12-19

@author: Byng Zeng
"""
import os
import re

from pybase.pysys import print_help, print_exit
from pybase.pypath import get_abs_path
from pybase.pydecorator import get_input_args
from pybase.pyprint import PyPrint
from web.webcontent import DEFAULT_WEB_URL_FILE

VERSION = '1.0.2'
AUTHOR = 'Byng.Zeng'


class WebURLCrawler(object):

    HELP_MENU = (
        '==================================',
        '    WebURLCrawler - %s' % VERSION,
        '',
        '    @Author: %s' % AUTHOR,
        '    Copyright (c) %s studio' % AUTHOR,
        '==================================',
        'option:',
        '  -s path: path to be collect',
        '  -t file: file to be save urls',
    )

    pr = PyPrint('WebURLCrawler')

    def __init__(self, name=None):
        self._name = name
        self._src = None
        self._tgt = None

    def collect_web_url(self):
        urls = []
        # read all of web_url.txt
        for rt, ds, fs in os.walk(self._src):
            if fs:
                for f in fs:
                    if f == DEFAULT_WEB_URL_FILE:
                        f = os.path.join(rt, f)
                        with open(f, 'r') as fd:
                            fd.readline()
                            urls.append(fd.readline())
        # write to file
        with open(self._tgt, 'w') as fd:
            for url in urls:
                fd.write('%s\n' % url)

    @get_input_args()
    def process_input(self, opts, args=None):
        if args:
            for k in args.keys():
                if k == '-s':
                    self._src = re.sub('/$', '', args['-s'])
                elif k == '-t':
                    self._tgt = get_abs_path(args['-t'])
                elif k == '-h':
                    print_help(self.HELP_MENU)
        return args

    def main(self):
        self.process_input('hs:t:')
        if not self._src:
            print_exit('no -s, -h for help!')
        if not self._tgt:
            self._tgt = '%s/%s.txt' % (
                self._src, os.path.basename(self._src))
        # collect urls.
        self.collect_web_url()

if __name__ == '__main__':
    wc = WebURLCrawler()
    wc.main()
