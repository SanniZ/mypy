#!/usr/bin/env python3

AUTHOR='Byng Zeng'
VERSION='1.0.1'

import os

from crypto.cryptofile.cryptofile import CryptoFile
from pybase.pyinput import get_input_args
from pybase.pysys import print_help
from pybase.pyfile import remove_type_file


key = 'CryptoFileHelper'
src = os.getcwd()
dst = src
cipher = 'AES'
mode = 'CBC'
ftype = None  # file type will be crypto.
xtype = ftype  # file type will be saved.
rtype = False  # remove ftype after encrytpo/decrypto.


#######################################################
# Function APIs
#######################################################

def cryptofile_help():
    help_menus = (
        "=====================================",
        "    cryptofile - %s" % VERSION,
        "=====================================",
        " options: [-k xxx] [-s xxx] [-o xxx] -d/-e"
        " -k: 16, 24, 32 Bytes key password",
        " -s: path of source",
        " -o: path of output",
        " -d: decrypto and remove ftype files",
        " -D: decrytpo ftype files",
        " -e: encrypto and remove ftype files",
        " -E: encrytpo ftype files",
        " -t: type name of file will be crypto",
        " -x: type name of file will be saved",
        " -c: set cipher and mode: AES/DES/RSA [,CBC/ECB]",
        " -m: set mode of cipher: CBC, ECB",
        " -r: remove ftype files after encrypto/decrypto",
        " -v: print information",
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
        args = get_input_args('dDeEk:s:o:c:m:t:rvh')
    if args:
        # set vars.
        global key, src, dst, cipher, mode, ftype, xtype, rtype
        pr = False
        opts = []
        for k, v in args.items():
            if k == '-k':
                key = v
            elif k == '-s':
                src = os.path.abspath(v)
            elif k == '-o':
                dst = os.path.abspath(v)
            elif k == '-c':
                if len(v) < 2:
                    cipher = v
                else:
                    cipher = v[0]
                    mode = v[1]
            elif k == '-m':
                mode = v
            elif k == '-t':
                ftype = v
            elif k == '-x':
                xtype = v
            elif k == '-v':
                pr = True
            elif k == '-r':
                rtype = True
            elif k in ['-d', '-D', '-e', '-E']:
                opts.append(k)
                if k in ['-d', '-e']:  # remove ftype files.
                    rtype = True
            elif k == '-h':
                cryptofile_help()
        # set dst = src if src is None.
        if not dst:
            dst = src
        if opts:
            cf = CryptoFile(key, src, dst, ftype, xtype, cipher, mode)
            cf.set_pr(pr)
            # run opts.
            for opt in opts:
                if opt in ['-d', '-D']:
                    if all((cf.decrypto_files(), rtype)):
                        remove_type_file(src, ftype)
                elif opt in ['-e', '-E']:
                    if all((cf.encrypto_files(), rtype)):
                        remove_type_file(src, ftype)
                    

#######################################################
# Entrance.
#######################################################
if __name__ == '__main__':
    main()
