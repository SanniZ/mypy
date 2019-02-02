#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Created on: 2018-12-19

@author: Byng Zeng
"""
import os
import re

from mypy.pybase import PyBase
from mypy.pypath import PyPath
from mypy.pyprint import PyPrint


class WebURLCrawler(object):

    HELP_MENU = (
        '==================================',
        '    WebURLCrawler help',
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
        urls = list()
        # read all of web_url.txt
        for rt, ds, fs in os.walk(self._src):
            if fs:
                for f in fs:
                    if f == 'web_url.txt':
                        f = os.path.join(rt, f)
                        with open(f, 'r') as fd:
                            fd.readline()
                            urls.append(fd.readline())
        # write to file
        with open(self._tgt, 'w') as fd:
            for url in urls:
                fd.write('%s\n' % url)

    def get_user_input(self):
        args = PyBase.get_user_input('hs:t:')
        if '-h' in args:
            PyBase.print_help(self.HELP_MENU)
        if '-s' in args:
            self._src = re.sub('/$', '', args['-s'])
        if '-t' in args:
            self._tgt = PyPath.get_abs_path(args['-t'])
        return args

    def main(self):
        self.get_user_input()
        if not self._src:
            PyBase.print_exit('no -s, -h for help!')
        if not self._tgt:
            self._tgt = '%s/%s.txt' % (
                self._src, os.path.basename(self._src))
        # collect urls.
        self.collect_web_url()

if __name__ == '__main__':
    wc = WebURLCrawler()
    wc.main()
