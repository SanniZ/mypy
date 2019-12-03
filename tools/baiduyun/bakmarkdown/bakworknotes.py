
import os

from pybase.pyinput import get_input_args
from tools.baiduyun.baiduyun import BaiduYun
from tools.markdown.mdcrypto import markdown

bdy_path = "myMarkdown/worknotes"
loc_path = os.path.join(os.getenv('MYGIT'), 'worknotes')


def decrypto_files(path):
    if not os.path.exists(path):
        return False
    argd = {"-K": os.path.join(os.getenv('HBINPY'), "mdcrypto.key"),
            "-s": loc_path,
            "-d": None}
    markdown(argd)
    return True

def encrypto_files(path):
    if not os.path.exists(path):
        return False
    argd = {"-K": os.path.join(os.getenv('HBINPY'), "mdcrypto.key"),
            "-s": loc_path,
            "-e": None}
    markdown(argd)
    return True


def main(args=None):
    if not args:
        args = get_input_args('u')
    if args:
        bdy_args = None
        for k in args.keys():
            if k == '-u':
                bdy_args = {"-y": bdy_path,
                            "-l": loc_path,
                            "-f": ".md",
                            "-v": None,
                            "-c": "upload"}
        if bdy_args:
            if decrypto_files(loc_path):  # decrypto files.
                BaiduYun(view=True).main(bdy_args)  # upload to baiduyun.
                encrypto_files(loc_path)  # re-encrypto.

if __name__ == "__main__":
    main()
