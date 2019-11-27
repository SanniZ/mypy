#!/usr/bin/env python3

AUTHOR  = 'Byng Zeng'
VERSION = '1.2.0'

import os
import sys
import subprocess
import getpass
from ctypes import *

from pybase.pyinput import get_input_args
from pybase.pysys import print_help, print_exit
from pybase.pyfile import remove_type_file
from crypto.cryptofile import CryptoFile


def markdown_help():
    help_menus = (
        "=====================================",
        "    markdown crypto - %s" % VERSION,
        "=====================================",
        " options: [-k xxx] [-s xxx] [-o xxx] -d/-e",
        " -h: print help",
        " -k: 16 Bytes key password",
        " -s: path of source",
        " -o: path of output",
        " -d: decrypto markdown",
        " -e: encrypto markdown",
    )
    print_help(help_menus, True)


def markdown_get_key_from_so():
    mdkey_so = os.getenv("MDKEY_SO")
    if not os.path.exists(mdkey_so):
        print('Error, no found mdkey.so, set export MDKEY_SO to .bashrc')
        return None
    lib = cdll.LoadLibrary(mdkey_so)
    func_get_md_key = lib.get_md_key
    func_get_md_key.argtype = (c_char_p)
    func_get_md_key.restype = (c_char_p)
    pwd = create_string_buffer(16)
    pwd.raw = str(getpass.getpass("Input your pwd:")).encode()
    return func_get_md_key(pwd)


def markdown_encrypto(key, src, dst):
    if CryptoFile(key, src, dst, 'md', 'mdx').encrypto_files():
        remove_type_file(src, 'md')


def markdown_decrypto(key, src, dst):
    if CryptoFile(key, src, dst, 'mdx', 'md').decrypto_files():
        remove_type_file(dst, 'mdx')


def markdown(args=None):
    key = None
    src = os.getcwd()
    dst = src
    opts = []
    if not args:
        args = get_input_args('dek:s:o:h')
    # set vars.
    for k, v in args.items():
        if k == '-k':
            key = v[0]
        elif k == '-s':
            src = os.path.abspath(v[0])
            dst = src
        elif k == '-o':
            dst = os.path.abspath(v[0])
        elif k == '-d':
            opts.append(k)
        elif k == '-e':
            opts.append(k)
        else:
            markdown_help()
    # get key.
    if not key:
        key = markdown_get_key_from_so()
        if not key:
            # key = getpass.getpass('input your key:')
            print("Error, found invalid pwd!")
            return None
    # run opts.
    for opt in opts:
        if opt == '-d':
            markdown_decrypto(key, src, dst)
        elif opt == '-e':
            markdown_encrypto(key, src, dst)


if __name__ == "__main__":
    markdown()
