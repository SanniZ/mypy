#!/usr/bin/env python3

AUTHOR = 'Byng Zeng'
VERSION = '1.0.0'

import os
import hashlib 
import getpass

from crypto.cryptohelper import CryptoHelper

KEY_FILE = 'crypto.key'

pr_lvl = ['info', 'err']

def pr_dbg(msg, exit_=False):
    if 'dbg' in pr_lvl:
        print(msg)
    if exit_:
        exit()

def pr_info(msg, exit_=False):
    if 'info' in pr_lvl:
        print(msg)
    if exit_:
        exit()

def pr_err(msg, exit_=False):
    if 'err' in pr_lvl:
        print(msg)
    if exit_:
        exit()

def encrypto_passwd_key(passwd, key):
    if any((not passwd, not key)):
        return None, None
    md5 = hashlib.md5()
    md5.update(passwd.encode())
    passwd_md5 = md5.hexdigest()
    key_md5 = CryptoHelper(passwd_md5).encrypt(key)
    return passwd_md5, key_md5


def write_passwd_key_to_file(passwd, key, path=None):
    out = KEY_FILE
    passwd_md5, key_md5 = encrypto_passwd_key(passwd, key)
    if any((not passwd_md5, not key_md5)):
        print('error, passwd and key invalid!')
        return False
    if path:
        out = path
    with open(out, 'w') as fd:
        fd.write("%s%s" % (passwd_md5, key_md5.decode()))
    return True


def read_passwd_key_from_file(path=None):
    # get md.key file.
    if path:
        if not os.path.exists(path):  # check path file.
            pr_dbg('error, not exist %s' % path)
            return None, None
    else:
        # check current folder for mdcrypto.key.
        if os.path.exists(os.path.join(cur_dir, KEY_FILE)):            
            path = os.path.join(cur_dir, KEY_FILE)
        else:  # get file from system env vars.
            path = os.getenv("KEY_FILE")
            if not path:
                pr_dbg('error, not get KEY_FILE from sys env.')
                return None, None
            if not os.path.exists(path):  # no found.
                pr_dbg('error, not exist sys env KEY_FILE: %s' % path)
                return None, None
    # get passwd and key from file.
    with open(path) as fd:
        passwd_key = fd.read()
    if not passwd_key:
        pr_dbg('error, not get passwd from read file.')
        return None, None
    passwd_md5 = passwd_key[:32]
    key_md5 = passwd_key[32:]
    # return result.
    return passwd_md5, key_md5

def get_key_form_file(path):
    passwd_md5, key_md5 = read_passwd_key_from_file(path)
    if any((not passwd_md5, not key_md5)):
        pr_dbg('get passwd and key of md5 fail.')
        return None
    passwd = getpass.getpass('Input passwd:')
    md5 = hashlib.md5()
    md5.update(passwd.encode())
    passwd_hex = md5.hexdigest()
    # check passwd.
    if passwd_hex != passwd_md5:
        pr_err('passwd invalid!')
        return None
    # decrypto key and return.
    return CryptoHelper(passwd_md5).decrypt(key_md5)


if __name__ == '__main__':
    from pybase.pyinput import get_input_args

    def print_usage(exit_=False):
        print('==================================')
        print('    md5key - %s' % VERSION)
        print('==================================')
        print('usage: python3 md5key.py options')
        print('')
        print('options:')
        print(' -w passwd : set passwd')
        print(' -k key : set key')
        print(' -f path : create key file to path.')
        print(' -v path : display key of path file.')
        if exit_:
            exit()

    passwd = key = None
    opts = dict()
    args = get_input_args('w:k:f:v:h')
    if not args:
        print_usage(True)
    for k, v in args.items():
        if v:
            v = v if isinstance(v, str) else v[0]
        if k == '-w':
            passwd = v
        elif k == '-k':
            key = v
        elif k in ['-f', '-v']:
            opts[k] = v
        else:
            print_usage(True)
    for opt, path in opts.items():
        if opt == '-f':
            if any((not passwd, not key, not path)):
                pr_err('error, passwd or key error.', True)
            write_passwd_key_to_file(passwd, key, path)
        elif opt == '-v':
            if path:
                key = get_key_form_file(path)
                if key:
                    pr_info('get key: %s' % key)
                else:
                    pr_err('no get key!', True)
