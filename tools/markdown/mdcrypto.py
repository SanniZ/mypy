#!/usr/bin/env python3

AUTHOR  = 'Byng Zeng'
VERSION = '1.2.1'

import os
import sys
import subprocess
import getpass
from ctypes import cdll, c_char_p, create_string_buffer

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


def markdown_get_key_from_libkey():
    '''
    Note:
      pls put libmarkdown-key.so under mdcrypto.py folder, or 
      set 'export LIBMD-KEY_SO=xxx/libmarkdown-key.so' to .bashrc
    '''
    libkey = os.path.join(
                os.path.dirname(os.path.abspath(__file__)), 
                'libmarkdown-key.so')
    if not os.path.exists(libkey):  # no found .so under folder.
        libkey = os.getenv("LIBMD-KEY_SO")  # get from env var.
        if not libkey:
            print("no get libkey from env!")
            return None
        if not os.path.exists(libkey):  # exist?
            print("no found %s!" % libkey)
            return None
    lib = cdll.LoadLibrary(libkey)
    lib.get_key.argtype = (c_char_p)
    lib.get_key.restype = (c_char_p)
    passwd = create_string_buffer(16)
    passwd.raw = str(getpass.getpass("Input your passwd:")).encode()
    return lib.get_key(passwd)


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
        key = markdown_get_key_from_libkey()
        if not key:
            # key = getpass.getpass('input your key:')
            print("Error, it is failed to get key.")
            return None
    # run opts.
    for opt in opts:
        if opt == '-d':
            markdown_decrypto(key, src, dst)
        elif opt == '-e':
            markdown_encrypto(key, src, dst)


if __name__ == "__main__":
    markdown()
