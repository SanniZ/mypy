#!/usr/bin/env python3

AUTHOR='Byng Zeng'
VERSION='1.0.2'

import os

from crypto.cryptohelper import CryptoHelper
from pybase.pyfile import find


#######################################################
# Function APIs
#######################################################

_pr = False

#
# set print msg
#
def set_pr(pr):
    global _pr
    _pr = pr

#
# print msg
#
def pr_info(msg):
    global _pr
    if _pr:
        print(msg)


#
# return list of type files.
# 
# path: dir of path to find.
# ftype: type of file, example: txt, md.
#
# return None or list.
#
def get_type_files(path, ftype):
    if any((not path, not ftype)):
        return None
    else:
        return find(path, ftype=ftype)



#
# encrypt files of path.
#
# key: key to encrypto.
# src: path of source.
# dst: path of output.
#
# return None or list.
#
def encrypto_path_files(key, src, dst, ftype, xtype=None, cipher='AES', mode='CBC'):
    fs = get_type_files(src, ftype)
    if fs:
        enc=CryptoHelper(key, cipher=cipher, mode=mode)
        res = []
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
            if xtype:
                k = k.replace(ftype, xtype)
            else:
                k = k.replace(ftype, "%sx" % ftype)
            fx = os.path.join(dst, dr, k)
            res.append(fx)
            pr_info("out: %s" % fx)
            with open(fx, 'w') as fd:
                fd.write(f.decode())
        # return res list.
        return res
    else:
        return None



#
# decrypt files of path.
#
# key: key to decrypto.
# src: path of source.
# dst: path of output.
#
# return None or list.
#
def decrypto_path_files(key, src, dst, ftype, xtype=None, cipher='AES', mode='CBC'):
    fs = get_type_files(src, ftype)
    if fs:
        dec=CryptoHelper(key=key, cipher=cipher, mode=mode)
        res = []
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
            if xtype:
                k = k.replace(ftype, xtype)
            else:
                k = k.replace(ftype, ftype[:-1])
            fdx = os.path.join(dst, dr, k)
            res.append(fdx)
            pr_info("out: %s" % fdx)
            with open(fdx, 'w') as fd:
                fd.write(f)
        # reutrn res list.
        return res
    else:
        return None


#######################################################
# class:  CryptoFile
#######################################################

class CryptoFile(object):
    def __init__(self, key, src, dst, ftype, xtype=None, cipher='AES', mode='CBC'):
        self._key = key
        self._src = os.path.abspath(src) + '/'
        self._dst = os.path.abspath(dst) + '/'
        self._ftype = ftype
        self._xtype = xtype
        self._cipher = cipher
        self._mode = mode

    def encrypto_files(self):
        return encrypto_path_files(self._key, self._src, self._dst, self._ftype, self._xtype, self._cipher, self._mode)

    def decrypto_files(self):
        return decrypto_path_files(self._key, self._src, self._dst, self._ftype, self._xtype, self._cipher, self._mode)

    def set_pr(self, pr):
        if pr:
            set_pr(True)
        else:
            set_pr(False)
