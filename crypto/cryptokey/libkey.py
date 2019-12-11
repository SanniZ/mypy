
import os
import getpass
from ctypes import cdll, c_char_p, create_string_buffer

def get_key_from_libkey():

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