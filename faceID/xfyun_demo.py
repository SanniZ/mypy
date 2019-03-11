#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 2018-12-04

@author: Byng Zeng
"""

import requests
import time
import json
import hashlib
import base64

from pybase.pysys import print_help, print_exit
from pybase.pyinput import get_input_args
from pybase.pypath import get_abs_path

VERSION = '0.1.0'
AUTHOR = 'Byng.Zeng'


HELP_MENU = (
    '======================================',
    '    XunFei FaceID - %s' % VERSION,
    '',
    '    @Author: %s' % AUTHOR,
    '    Copyright (c) %s studio' % AUTHOR,
    '======================================',
    'option:',
    '  -f path: set first image',
    '    path: the path of the first image',
    '  -s path: set the second image',
    '    path: path of the second image',
)


def get_face_image():
    fid = None
    sid = None
    args = get_input_args('hf:s:')
    for k in args.keys():
        if k == '-f':
            fid = get_abs_path(args['-f'])
        elif k == '-s':
            sid = get_abs_path(args['-s'])
        elif k == '-h':
            print_help(HELP_MENU)
    return fid, sid


def main():
    fid, sid = get_face_image()
    if any((not fid, not sid)):
        print_exit('Error, no found id image.')

    x_appid = 'wsr00030d4d@ch407c0f6177e2477400'
    api_key = ''
    url = 'http://api.xfyun.cn/v1/service/v1/image_identify/face_verification'
    x_time = str(int(time.time()))
    param = {'auto_rotate': True}
    param = json.dumps(param)
    x_param = base64.b64encode(param.encode('utf-8'))
    m2 = hashlib.md5()
    m2.update(str(api_key + x_time + str(x_param)))
    x_checksum = m2.hexdigest()
    x_header = {
        'X-Appid': x_appid,
        'X-CurTime': x_time,
        'X-CheckSum': x_checksum,
        'X-Param': x_param,
    }
    with open(fid, 'rb') as f:
        f1 = f.read()
    with open(sid, 'rb') as f:
        f2 = f.read()
    f1_base64 = str(base64.b64encode(f1))
    f2_base64 = str(base64.b64encode(f2))
    data = {
        'first_image': f1_base64,
        'second_image': f2_base64,
    }
    req = requests.post(url, data=data, headers=x_header)
    result = str(req.content)
    print(result)
    return


if __name__ == '__main__':
    main()
