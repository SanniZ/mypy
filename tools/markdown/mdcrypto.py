#!/usr/bin/env python3

VERSION='1.1.0'

import os
import sys

from pybase.pyinput import get_input_args
from pybase.pysys import print_help, print_exit, execute_shell
from crypto.cryptofile import CryptoFile


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
    CryptoFile(key, src, dst, 'md').encrypto_files()

def markdown_decrypto(key, src, dst):
    CryptoFile(key, src, dst, 'md').decrypto_files()


def markdown(args=None):
    key = KEY
    src = os.getcwd()
    dst = src
    if not args:
        args = get_input_args('dek:s:o:h')
    for k, v in args.items():
        if k == '-k':
            key = v
        elif k == '-s':
            src = os.path.abspath(v)
            dst = src
        elif k == '-o':
            dst = os.path.abspath(v)
        elif k == '-d':
            markdown_decrypto(key, src, dst)
        elif k == '-e':
            markdown_encrypto(key, src, dst)
        else:
            markdown_help()


if __name__ == "__main__":
    # import getpass
    # pwd = getpass.getpass("Pls input your key:")
    # if pwd != 'Tb0dT':
    #     print_exit("error, key invalid!", True)
    markdown()
