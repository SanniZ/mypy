#!/usr/bin/env python3

AUTHOR  = 'Byng Zeng'
VERSION = '1.2.3'

import os
import sys
import subprocess

from pybase.pyinput import get_input_args
from pybase.pysys import print_help, print_exit
from pybase.pyfile import remove_type_file
from crypto.cryptofile.cryptofile import CryptoFile
from crypto.cryptokey.key import get_key_form_file 

cur_dir = os.path.dirname(os.path.abspath(__file__))

def markdown_help():
    help_menus = (
        "=====================================",
        "    markdown crypto - %s" % VERSION,
        "=====================================",
        " usage: python3 mdcrypto.py option",
        "",
        " options:",
        "  -k: 16 Bytes key password",
        "  -K: path of key file", 
        "  -s: path of source",
        "  -o: path of output",
        "  -d: decrypto markdown",
        "  -e: encrypto markdown",
    )
    print_help(help_menus, True)


def markdown_encrypto(key, src, dst):
    if CryptoFile(key, src, dst, 'md', 'mdx').encrypto_files():
        remove_type_file(src, 'md')


def markdown_decrypto(key, src, dst):
    if CryptoFile(key, src, dst, 'mdx', 'md').decrypto_files():
        remove_type_file(dst, 'mdx')


def markdown(args=None):
    key = None
    key_file_path = None
    src = os.getcwd()
    dst = src
    opts = []
    if not args:
        args = get_input_args('dek:K:s:o:h')
    # set vars.
    for k, v in args.items():
        if v:  # transfer v.
            v = v if type(v) == str else v[0]
        if k == '-k':  # key
            key = v
        elif k == '-K':  # key file.
            key_file_path = os.path.abspath(v)
        elif k == '-s':  # path of source.
            src = os.path.abspath(v)
            dst = src
        elif k == '-o':  # path of output.
            dst = os.path.abspath(v)
        elif k == '-d':  # decrypto.
            opts.append(k)
        elif k == '-e':  # encrypto.
            opts.append(k)
        else:
            markdown_help()
    # get key.
    if not key:
        # get key from md5 key file.
        key = get_key_form_file(key_file_path)
        if not key:
            print('error, get key from file fail!!!')
            return False
    # run opts.
    for opt in opts:
        if opt == '-d':  # decrypto.
            markdown_decrypto(key, src, dst)
        elif opt == '-e':  # encrypto.
            markdown_encrypto(key, src, dst)
    return True

if __name__ == "__main__":
    markdown()
