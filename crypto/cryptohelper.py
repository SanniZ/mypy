#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 2018-02-19

@author: Zbyng.Zeng
"""

from Crypto.Cipher import AES
import base64

'''
Note:
    run 'sudo pip3 install pycrypto'' to install Crypto module.
    key must be 16B（AES-128）, 24B（AES-192） or 32B（AES-256）
'''

VERSION = '1.0.0'

ALIGN_LENGTH = 16

IV = '@CryptoHelper-IV'


class CryptoHelper(object):

    @classmethod
    def __align_length(cls, text):
        n = len(text) % ALIGN_LENGTH
        if n:
            text += '\0' * (ALIGN_LENGTH - n)
        return text

    @classmethod
    def AES_encrypt(cls, key, paintext, iv=IV, mode=AES.MODE_CBC):
        key = cls.__align_length(key)
        iv = cls.__align_length(iv)
        try:
            cipher = AES.new(key, mode, iv)
        except ValueError as e:
            print('AES_encrypt error: ', str(e))
            return None
        else:
            paintext = cls.__align_length(paintext)
            ciphertext = base64.b64encode(cipher.encrypt(paintext))
            return ciphertext

    @classmethod
    def AES_decrypt(cls, key, ciphertext, iv=IV, mode=AES.MODE_CBC):
        key = cls.__align_length(key)
        iv = cls.__align_length(iv)
        try:
            cipher = AES.new(key, mode, iv)
        except ValueError as e:
            print('AES_decrypt error: ', str(e))
            return None
        else:
            paintext = cipher.decrypt(base64.b64decode(ciphertext))
            return paintext.decode().rstrip('\0')

    @classmethod
    def encrypt(cls, key, paintext, iv=IV, cipher='AES', mode=AES.MODE_CBC):
        if cipher == 'AES':
            return cls.AES_encrypt(key, paintext, iv, mode)

    @classmethod
    def decrypt(cls, key, ciphertext, iv=IV, cipher='AES', mode=AES.MODE_CBC):
        if cipher == 'AES':
            return cls.AES_decrypt(key, ciphertext, iv, mode)
