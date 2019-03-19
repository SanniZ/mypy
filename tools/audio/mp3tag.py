#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 2019-03-19

@author: Byng.Zeng
"""

import os

import eyed3

from pybase.pysys import print_help
from pybase.pyprint import PyPrint, PR_LVL_ALL
from pybase.pyfile import get_name_ex
from pybase.pydecorator import get_input_args

VERSION = '1.0.0'
AUTHOR = 'Byng.Zeng'


HELP_MENU = [
    '==================================',
    '    MP3Tag - %s' % VERSION,
    '',
    '    @Author: %s' % AUTHOR,
    '    Copyright (c) %s studio' % AUTHOR,
    '==================================',
    'option:',
    '  -t path: reclaim mp3 tag',
    '  -n path: reclaim mp3 name',
]

pr = PyPrint('MP3Tag')

OPTS = 'ht:n:v'


def scan_mp3_files(path):
    lt = []
    if path:
        for rt, ds, fs in os.walk(path):
            if fs:
                for f in fs:
                    if get_name_ex(f) in ['.mp3', '.MP3', 'mp3', 'MP3']:
                        lt.append(os.path.join(rt, f))
    return lt


def get_artist_title_from_filename(f, tag='-'):
    name = os.path.splitext(os.path.basename(f))[0]
    data = name.split(tag)
    if len(data) >= 2:
        artist = data[0].strip()
        title = data[1].strip()
    else:
        artist = 'unknown'
        title = data[0]
    return artist, title


def reclaim_mp3_tag(path):
    fs = scan_mp3_files(path)
    for f in fs:
        artist, title = get_artist_title_from_filename(f)
        mp3 = eyed3.load(f)
        if mp3:
            pr.pr_dbg('reclaim tag %s' % f)
            retry_times = 2
            while retry_times:
                if not mp3.tag:
                    mp3.initTag()
                mp3.tag.artist = artist
                mp3.tag.title = title
                try:
                    mp3.tag.save()
                except (UnicodeEncodeError, NotImplementedError, TypeError,
                        eyed3.id3.tag.TagException):
                    mp3.initTag()  # recreate tag for execpt
                    retry_times -= 1
                else:
                    retry_times = 0


def reclaim_mp3_filename(path):
    fs = scan_mp3_files(path)
    for f in fs:
        for tag in ['_', '-']:
            artist, title = get_artist_title_from_filename(f, tag)
            if artist != 'unknown':
                pr.pr_dbg('reclaim name %s' % f)
                newf = os.path.join(
                        os.path.dirname(f), '%s - %s.mp3' % (artist, title))
                os.rename(f, newf)


@get_input_args()
def process_input(opts, args=None):
    if args:
        for k in args.keys():
            if k == '-v':
                pr.level = PR_LVL_ALL
            elif k == '-h':
                print_help(HELP_MENU)
    return args


def main(args=None):
    args = process_input(OPTS, args=args)
    if args:
        if '-t' in args:
            reclaim_mp3_tag(os.path.abspath(args['-t']))
        if '-n' in args:
            reclaim_mp3_filename(os.path.abspath(args['-n']))


if __name__ == '__main__':
    main()
