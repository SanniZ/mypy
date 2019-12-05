#!/usr/bin/env python3

AUTHOR  = 'Byng Zeng'
VERSION = '1.2.3'

import os
import sys
import subprocess
import getpass
import hashlib
from ctypes import cdll, c_char_p, create_string_buffer

from pybase.pyinput import get_input_args
from pybase.pysys import print_help, print_exit
from pybase.pyfile import remove_type_file
from crypto.cryptofile import CryptoFile
from crypto.cryptohelper import CryptoHelper

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


def narkdown_get_md5_key(f_key=None):
    '''
      get markdown key from file.
      file format:
        passwd: xxxx
        key: xxxx

       return passwd, key.
    '''
    passwd = None
    key = None

    # get mdcrypto.key file.
    if f_key:
        if not os.path.exists(f_key):  # check f_key file.
            return None, None
    else:
        # check current folder for mdcrypto.key.
        if os.path.exists(os.path.join(cur_dir, 'mdcrypto.key')):
            f_key = os.path.join(cur_dir, 'mdcrypto.key')
        else:  # get file from system env vars.
            f_key = os.getenv("MDCRYPTO-KEY")
            if not f_key:
                return None, None
            if not os.path.exists(f_key):  # no found.
                return None, None

    # get passwd and key from file.
    with open(f_key) as fd:
        lines = fd.readlines()
    for txt in lines:
        lt = txt.strip().split(':')
        if all((lt, len(lt) >= 2)):
            if lt[0].strip() == 'passwd':
                passwd = lt[1].strip()
            elif lt[0].strip() == 'key':
                key = lt[1].strip()
    # return result.
    return passwd, key


def markdown_get_key_from_libkey():
    '''
    Note:
      pls put libmarkdown-key.so under mdcrypto.py folder, or 
      set 'export LIBMD-KEY_SO=xxx/libmarkdown-key.so' to .bashrc
    '''
    libkey = os.path.join(cur_dir, 'libmarkdown-key.so')
    if not os.path.exists(libkey):  # no found .so under folder.
        libkey = os.getenv("LIBMD-KEY_SO")  # get from env var.
        if not libkey:
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
    f_key = None
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
            f_key = os.path.abspath(v)
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
        # get passwd and key from md5 key file.
        passwd_md5, key_md5 = narkdown_get_md5_key(f_key)
        if all((key_md5, passwd_md5)):  # get key.
            passwd = getpass.getpass('input your passwd:')
            md5 = hashlib.md5()
            md5.update(passwd.encode())
            if md5.hexdigest() != passwd_md5:
                print("error, passwd invalid!")
                return None
            key = CryptoHelper(passwd_md5).decrypt(key_md5)
        else:  # try to get key from libkey.
            key = markdown_get_key_from_libkey()
        if not key:  # error, no found key.
            print("error, no found key.")
            return None
    # run opts.
    for opt in opts:
        if opt == '-d':  # decrypto.
            markdown_decrypto(key, src, dst)
        elif opt == '-e':  # encrypto.
            markdown_encrypto(key, src, dst)


if __name__ == "__main__":
    markdown()
