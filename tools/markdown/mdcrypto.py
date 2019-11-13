#!/usr/bin/env python3

VERSION='1.0.0'

import os
import sys

from pybase.pyinput import get_input_args
from pybase.pysys import print_help, print_exit, execute_shell
from crypto.cryptohelper import CryptoHelper
from pybase.pyfile import find

KEY = "Byng-00-markdown"

def print_help_menu():
    help_menus = (
        "=====================================",
        "    markdown command set - %s" % VERSION,
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


def get_md_files(path):
    return find(path, ftype='md')


def encrypt_markdown(key, src_path, dst_path):
    fs = get_md_files(src_path)
    if fs:
        enc=CryptoHelper(key)
        for k, v in fs.items():
            with open(os.path.join(v, k), 'r') as fd:
                f = fd.read()
            f = enc.encrypt(f)
            if not f:
                print('error, no file!')
            dr = v.replace(src_path + '/', '')
            if not os.path.exists(os.path.join(dst_path, dr)):
                os.makedirs(os.path.join(dst_path, dr))
            with open(os.path.join(dst_path, dr, k), 'w') as fd:
                fd.write(f.decode())


def decrypto_markdown(key, src_path, dst_path):
    fs = get_md_files(src_path)
    if fs:
        enc=CryptoHelper(key)
        for k, v in fs.items():
            with open(os.path.join(v, k), 'r') as fd:
                f = fd.read()
            f = enc.decrypt(f.encode())
            dr = v.replace(src_path + '/', '')
            if not os.path.exists(os.path.join(dst_path, dr)):
                os.makedirs(os.path.join(dst_path, dr))
            with open(os.path.join(dst_path, dr, k), 'w') as fd:
                fd.write(f)

def open_markdown(name):
    execute_shell("remarkable %s" % name)

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
            decrypto_markdown(key, src, dst)
        elif k == '-e':
            encrypt_markdown(key, src, dst)
        else:
            print_help_menu()


if __name__ == "__main__":
    # import getpass
    # pwd = getpass.getpass("Pls input your key:")
    # if pwd != 'Tb0dT':
    #     print_exit("error, key invalid!", True)
    markdown()
