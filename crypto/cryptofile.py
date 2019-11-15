#!/usr/bin/env python3

AUTHOR='Byng Zeng'
VERSION='1.0.1'

import os
import sys

from crypto.cryptohelper import CryptoHelper
from pybase.pyfile import find

_pr = False

#
# set print msg
#
def pr_set(pr):
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

# entrance.
if __name__ == '__main__':
    from pybase.pyinput import get_input_args
    from pybase.pysys import print_help, print_exit
    from pybase.pyfile import remove_type_file


    key = 'CryptoFile*-00-*'
    src = os.getcwd()
    dst = src
    cipher = 'AES'
    mode = 'CBC'
    ftype = None
    xtype = ftype

    def cryptofile_help():
        help_menus = (
            "=====================================",
            "    cryptofile - %s" % VERSION,
            "=====================================",
            " options: [-k xxx] [-s xxx] [-o xxx] -d/-e"
            " -h: print help",
            " -k: 16, 24, 32 Bytes key password",
            " -s: path of source",
            " -o: path of output",
            " -d: decrypto files",
            " -e: encrypto files",
            " -t: type name of file will be crypto",
            " -x: type name of file will be saved",
            " -c: set cipher: AES, DES, RSA",
            " -m: set mode of cipher: CBC, ECB",
            " -r: remove ftype files after encrypto/decrypto",
            " -i: print information",
            "",
            "defualt:",
            "  key=%s, cipher=%s, mode=%s" % (key, cipher, mode),
            "  src=%s, dst=%s" % (src, dst),
            "  ftype=%s, xtype=%s" % (ftype, xtype),
            "",
            "Note: when xtype=None",
            "   xtype will be {ftype}+x while run -e, e.g: txt -> txtx",
            "   xtype will be {ftype}-x while run -e, e.g: txtx -> txt",
        )
        print_help(help_menus, True)

    def main(args=None):
        if not args:
            args = get_input_args('dek:s:o:c:m:t:rih')
        if args:
            # set vars.
            global key, src, dst, cipher, mode, ftype, xtype
            opts = []
            for k, v in args.items():
                if k == '-k':
                    key = v
                elif k == '-s':
                    src = os.path.abspath(v)
                elif k == '-o':
                    dst = os.path.abspath(v)
                elif k == '-c':
                    cipher = v
                elif k == '-m':
                    mode = v
                elif k == '-t':
                    ftype = v
                elif k == '-x':
                    xtype = v
                elif k == '-i':
                    pr_set(True)
                elif k in ['-d', '-e', '-r']:
                    opts.append(k)
                elif k == '-h':
                    cryptofile_help()
            # set dst = src if src is None.
            if not dst:
                dst = src
            if opts:
                cf = CryptoFile(key, src, dst, ftype, xtype, cipher, mode)
                # run opts.
                for opt in opts:
                    if opt == '-d':
                        cf.decrypto_files()
                    elif opt == '-e':
                        cf.encrypto_files()
                    elif opt == '-r':
                        remove_type_file(src, ftype)
    # run main.
    main()
