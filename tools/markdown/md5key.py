#!/usr/bin/env python3

AUTHOR = 'Byng Zeng'
VERSION = '1.0.0'

import hashlib 

from crypto.cryptohelper import CryptoHelper

def encrypto_md5_key(passwd, key):
    if any((not passwd, not key)):
        return None, None
    md5 = hashlib.md5()
    md5.update(passwd.encode())
    passwd_md5 = md5.hexdigest()
    key_md5 = CryptoHelper(passwd_md5).encrypt(key)
    return passwd_md5, key_md5


def create_md5_key_file(passwd, key, path=None):
    out = 'md5.key'
    passwd_md5, key_md5 = encrypto_md5_key(passwd, key)
    if any((not passwd_md5, not key_md5)):
        print('error, passwd and key invalid!')
        return False
    if path:
        out = path
    with open(out, 'w') as fd:
        fd.write("passwd: %s\n" % passwd_md5)
        fd.write("key: %s\n" % key_md5.decode())
    return True

if __name__ == '__main__':
    from pybase.pyinput import get_input_args

    def print_usage():
        print('==================================')
        print('    md5key - %s' % VERSION)
        print('==================================')
        print('usage: python3 md5key.py -w passwd -k key')
        print(' -w passwd : set passwd')
        print(' -k key : set key')

    passwd = None
    key = None
    md5_key_path = None
    args = get_input_args('w:k:o:h')
    if not args:
        print_usage()
        exit()
    for k, v in args.items():
        if v:
            v = v if isinstance(v, str) else v[0]
        if k == '-w':
            passwd = v
        elif k == '-k':
            key = v
        elif k == '-o':
            md5_key_path = v
        else:
            print_usage()
    if any((not passwd, not key)):
        print('error, -h for help.')
        exit()
    create_md5_key_file(passwd, key, md5_key_path)