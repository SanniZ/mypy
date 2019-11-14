#!/usr/bin/env python3

VERSION='1.1.0'

import os
import sys
import subprocess

from pybase.pyinput import get_input_args
from pybase.pysys import print_help, print_exit
from pybase.pyfile import remove_type_file
from crypto.cryptofile import CryptoFile

import getpass

KEY = "Byng-00-markdown"

def markdown_help():
    help_menus = (
        "=====================================",
        "    markdown crypto - %s" % VERSION,
        "=====================================",
        " options: [-k xxx] [-s xxx] [-o xxx] -d/-e"
        " -h: print help",
        " -k: 16 Bytes key password",
        " -s: path of source",
        " -o: path of output",
        " -d: decrypto markdown",
        " -e: encrypto markdown",
    )
    print_help(help_menus, True)


def markdown_encrypto(key, src, dst):
    if CryptoFile(key, src, dst, 'md', 'mdx').encrypto_files():
        remove_type_file(src, 'md')


def markdown_decrypto(key, src, dst):
    if CryptoFile(key, src, dst, 'mdx', 'md').decrypto_files():
        remove_type_file(dst, 'mdx')


def markdown(args=None):
    key = KEY
    src = os.getcwd()
    dst = src
    opts = []
    if not args:
        args = get_input_args('dek:s:o:h')
    # get key.
    if '-k' not in args:
        k = getpass.getpass('input your key:')
        if k:
            args['-k'] = k
    # set vars.
    for k, v in args.items():
        if k == '-k':
            key = v
        elif k == '-s':
            src = os.path.abspath(v)
            dst = src
        elif k == '-o':
            dst = os.path.abspath(v)
        elif k == '-d':
            opts.append(k)
        elif k == '-e':
            opts.append(k)
        else:
            markdown_help()
    # run opts.
    for opt in opts:
        if opt == '-d':
            markdown_decrypto(key, src, dst)
        elif opt == '-e':
            markdown_encrypto(key, src, dst)


if __name__ == "__main__":
    # if getpass.getpass('input your key:') != 'xxx':
    #     print_exit("error, invalid key!", True)
    markdown()
