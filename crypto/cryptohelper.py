#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 2018-02-25

@author: Byng.Zeng
"""
import os
import sys

try:
    from Crypto.Cipher import AES, DES
except ImportError:
    print("run 'pip3 install pycrypto' to install Crypto module.")
    sys.exit()

import base64

import rsa

'''
Note:
    run 'pip3 install pycrypto' to install Crypto module.
'''

VERSION = '1.1.2'


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
        text += '\0'.encode() * (length - n)
    return text


def encode_text(text):
    return text.encode() if type(text) == str else text


# create rsa keys.
#
# return values: pubkey, prikey.
#
def RSA_create_keys(n=256):
    return rsa.newkeys(n)


def RSA_get_msg_space(key, decrypt=0):
    SPACES = {77: [21, 44], 78: [21, 44],
              154: [53, 88], 155: [53, 88],
              308: [117, 172], 309: [117, 172],
              617: [245, 344], 618: [245, 344]}
    key = str(key)
    if key.startswith('PublicKey'):
        key = key[len('PublicKey'):]
    elif key.startswith('PrivateKey'):
        key = key[len('PrivateKey'):]
    else:
        print('RSA error: not get msg space!')
        return None
    key = key[1:-1].split(',')[0]
    n = len(key)
    if n in SPACES:
        return SPACES[n][decrypt]
    else:
        return None


def RSA_encrypt(pubkey, text, keylenght=None):
    msg_space = RSA_get_msg_space(pubkey)
    if not msg_space:
        return None
    text = encode_text(text)
    result = bytes()
    n = len(text)
    while n:
        if n > msg_space:
            txt = text[:msg_space]
            text = text[msg_space:]
            n = len(text)
        else:
            txt = text
            n = 0
        result += base64.urlsafe_b64encode(rsa.encrypt(txt, pubkey))
    return result


def RSA_decrypt(prikey, text):
    msg_space = RSA_get_msg_space(prikey, 1)
    if not msg_space:
        return None
    result = None
    n = len(text)
    result = bytes()
    rsa.decrypt(base64.urlsafe_b64decode(text), prikey)
    while n:
        if n > msg_space:
            txt = text[:msg_space]
            text = text[msg_space:]
            n = len(text)
        else:
            txt = text
            n = 0
        result += rsa.decrypt(base64.urlsafe_b64decode(txt), prikey)
    return result.decode() if type(result) == bytes else result


def DES_encrypt(key, text, iv=DES_IV, mode='ECB'):
    text = encode_text(text)
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
    if len(key) not in[16, 24,32]:
        print("key length %d is invalid!" % len(key))
        return None
    text = encode_text(text)
    mode = get_cipher_mode('AES', mode)
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
    if any((not key, not text, not iv, not mode, len(key) not in [16, 24, 32])):
        print('AES_encrypt error, found None input.')
        return None
    mode = get_cipher_mode('AES', mode)
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

    def __init__(self, key, pubkey=None, iv=None, cipher='AES', mode='CBC'):
        self._key = key
        self._pubkey = pubkey
        self._cipher = cipher
        self._mode = mode
        if iv:
            self._iv = iv
        elif cipher in self.IVS:
            self._iv = self.IVS[cipher]

    def encrypt(self, text):
        if self._cipher == 'AES':
            return AES_encrypt(self._key, text, self._iv, self._mode)
        elif self._cipher == 'DES':
            return DES_encrypt(self._key, text, self._iv, self._mode)
        elif self._cipher == 'RSA':
            return RSA_encrypt(self._pubkey, text)

    def decrypt(self, text):
        if self._cipher == 'AES':
            return AES_decrypt(self._key, text, self._iv, self._mode)
        elif self._cipher == 'DES':
            return DES_decrypt(self._key, text, self._iv, self._mode)
        elif self._cipher == 'RSA':
            return RSA_decrypt(self._key, text)
