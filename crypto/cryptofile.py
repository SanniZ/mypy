#!/usr/bin/env python3

AUTHOR='Byng Zeng'
VERSION='1.0.0'

import os
import sys

from crypto.cryptohelper import CryptoHelper
from pybase.pyfile import find

#
# return list of type files.
# 
# path: dir of path to find.
# ftype: type of file, example: txt, md.
#
def get_type_files(path, ftype):
    return find(path, ftype=ftype)



#
# encrypt files of path.
#
# key: key to encrypto.
# src: path of source.
# dst: path of output.
#
def encrypto_path_files(key, src, dst, ftype, cipher='AES', mode='CBC'):
    fs = get_type_files(src, ftype)
    if fs:
        enc=CryptoHelper(key, cipher=cipher, mode=mode)
        for k, v in fs.items():
            with open(os.path.join(v, k), 'r') as fd:
                f = fd.read()
            f = enc.encrypt(f)
            if not f:
                print('stop, encrypto %s failed!' % os.path.join(v,k))
                return False
            dr = v.replace(src, '')
            if not os.path.exists(os.path.join(dst, dr)):
                os.makedirs(os.path.join(dst, dr))
            with open(os.path.join(dst, dr, k), 'w') as fd:
                fd.write(f.decode())
    return True



#
# decrypt files of path.
#
# key: key to decrypto.
# src: path of source.
# dst: path of output.
#
def decrypto_path_files(key, src, dst, ftype, cipher='AES', mode='CBC'):
    fs = get_type_files(src, ftype)
    if fs:
        dec=CryptoHelper(key=key, cipher=cipher, mode=mode)
        for k, v in fs.items():
            with open(os.path.join(v, k), 'r') as fd:
                f = fd.read()
            f = dec.decrypt(f.encode())
            if not f:
                print('stop, decrypto %s failed' % os.path.join(v, k))
                return False
            dr = v.replace(src, '')
            if not os.path.exists(os.path.join(dst, dr)):
                os.makedirs(os.path.join(dst, dr))
            with open(os.path.join(dst, dr, k), 'w') as fd:
                fd.write(f)
    return True


class CryptoFile(object):
    def __init__(self, key, src, dst, ftype):
        self._key = key
        self._src = os.path.abspath(src) + '/'
        self._dst = os.path.abspath(dst) + '/'
        self._ftype = ftype


    def encrypto_files(self):
        encrypto_path_files(self._key, self._src, self._dst, self._ftype)

    def decrypto_files(self):
        decrypto_path_files(self._key, self._src, self._dst, self._ftype)
