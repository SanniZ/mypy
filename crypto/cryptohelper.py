#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 2018-02-25

@author: Zbyng.Zeng
"""

from Crypto.Cipher import AES, DES
import base64

'''
Note:
    run 'sudo pip3 install pycrypto' to install Crypto module.
'''

VERSION = '1.1.0'


DES_ALIGN_LENGTH = 8
DES_IV = 'Crypt-IV'


AES_ALIGN_LENGTH = 16
AES_IV = '~CryptoHelper-IV'


CRYPTO_MODES = {
    'DES': {'CBC': DES.MODE_CBC, 'ECB': DES.MODE_ECB},
    'AES': {'CBC': AES.MODE_CBC, 'ECB': AES.MODE_ECB},
}


def get_cipher_mode(cipher, mode):
    result = None
    if any((not cipher, not mode)):
        return None
    cipher = cipher.upper()
    mode = mode.upper()
    if cipher in CRYPTO_MODES:
        modes = CRYPTO_MODES[cipher]
        if mode in modes:
            result = modes[mode]
    return result


def align_length(text, length):
    n = len(text) % length
    if n:
        text += '\0' * (length - n)
    return text


def DES_encrypt(key, text, iv=DES_IV, mode='ECB'):
    if any((not key, not text, not iv, not mode)):
        print('AES_encrypt error, found None input.')
        return None
    mode = get_cipher_mode('DES', mode)
    if not mode:
        print('DES_encrypt error, found invalid mode.')
        return None
    try:
        cipher = DES.new(key, mode, iv)
    except ValueError as e:
        print('DES_encrypt error: ', str(e))
        return None
    else:
        text = align_length(text, DES_ALIGN_LENGTH)
        result = base64.b64encode(cipher.encrypt(text))
        return result


def DES_decrypt(key, text, iv=DES_IV, mode='ECB'):
    if any((not key, not text, not iv, not mode)):
        print('AES_encrypt error, found None input.')
        return None
    mode = get_cipher_mode('DES', mode)
    if not mode:
        print('DES_decrypt error, found invalid mode.')
        return None
    try:
        cipher = DES.new(key, mode, iv)
    except ValueError as e:
        print('DES_decrypt error: ', str(e))
        return None
    else:
        result = cipher.decrypt(base64.b64decode(text))
        return result.decode().rstrip('\0')


def AES_encrypt(key, text, iv=AES_IV, mode=AES.MODE_CBC):
    if any((not key, not text, not iv, not mode)):
        print('AES_encrypt error, found None input.')
        return None
    mode = get_cipher_mode('DES', mode)
    if not mode:
        print('AES_encrypt error, found invalid mode.')
        return None
    try:
        cipher = AES.new(key, mode, iv)
    except ValueError as e:
        print('AES_encrypt error: ', str(e))
        return None
    else:
        text = align_length(text, AES_ALIGN_LENGTH)
        result = base64.b64encode(cipher.encrypt(text))
        return result


def AES_decrypt(key, text, iv=AES_IV, mode=AES.MODE_CBC):
    if any((not key, not text, not iv, not mode)):
        print('AES_encrypt error, found None input.')
        return None
    mode = get_cipher_mode('DES', mode)
    if not mode:
        print('AES_decrypt error, found invalid mode.')
        return None
    try:
        cipher = AES.new(key, mode, iv)
    except ValueError as e:
        print('AES_decrypt error: ', str(e))
        return None
    else:
        result = cipher.decrypt(base64.b64decode(text))
        return result.decode().rstrip('\0')


############################################################################
#               CryptoHelper Class
############################################################################

class CryptoHelper(object):

    IVS = {'AES': AES_IV, 'DES': DES_IV}

    def __init__(self, key, iv=None, cipher='AES', mode='CBC'):
        self._key = key
        self._cipher = cipher
        self._mode = mode
        if iv:
            self._iv = iv
        elif cipher in self.IVS:
            self._iv = self.IVS[cipher]

    def encrypt(self, data):
        if self._cipher == 'AES':
            return AES_encrypt(self._key, data, self._iv, self._mode)
        elif self._cipher == 'DES':
            return DES_encrypt(self._key, data, self._iv, self._mode)

    def decrypt(self, data):
        if self._cipher == 'AES':
            return AES_decrypt(self._key, data, self._iv, self._mode)
        elif self._cipher == 'DES':
            return DES_decrypt(self._key, data, self._iv, self._mode)
