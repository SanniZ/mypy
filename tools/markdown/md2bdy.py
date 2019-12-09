#!/usr/bin/env python3

AUTHOR = 'Byng Zeng'
VERSION = '1.0.0'


import os

from pybase.pyinput import get_input_args
from tools.baiduyun.baiduyun import BaiduYun
from tools.markdown.mdcrypto import markdown



def crypto_markdown(path, key=None, encrypto=False):
    if not os.path.exists(path): # check path
        return False
    if key:
        args = {'-k': key, '-s': path}
    else:
        args = {"-K": os.path.join(os.getenv('HBINPY'), "markdown.key"),
                "-s": path}
    if encrypto:
        args['-e'] = None  # encrypto
    else:
        args['-d'] = None  # decrypto
    markdown(args)
    return True


def main(args=None):
    if not args:
        args = get_input_args('l:y:k:e')
    if args:
        src_path = None
        src_enc  = False
        key = None
        bdy_args = {'-f': '.md', '-v': None, '-c': 'upload'}
        for k, v in args.items():
            if v:
                v = v if isinstance(v, str) else v[0]
            if k == '-l':  # local path
                src_path = os.path.abspath(v)
                bdy_args["-l"] = src_path
            elif k == '-y':  # yun path.
                bdy_args['-y'] = v
            elif k == '-k':
                key = v
            elif k == '-e':  # encrypto
                src_enc = True
        if any(('-l' not in bdy_args, '-y' not in bdy_args)):
            print("Pls set -l and -y")
            return False
        if bdy_args:
            if src_enc:  # decrypto, upload and encrypto
                if crypto_markdown(src_path, key, False):  # decrypto files.
                    BaiduYun(view=True).main(bdy_args)  # upload to baiduyun.
                    crypto_markdown(src_path, key, True)  # re-encrypto.
                else:  # error
                    print('error, decrypto failed!')
                    return False
            else:  # upload to yun.
                BaiduYun(view=True).main(bdy_args)  # upload to baiduyun.
    return True


if __name__ == "__main__":
    main()
