#!/usr/bin/python
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

import sys
import getopt

from base import MyBase as Base

def print_help():
    print('======================================')
    print('     XunFei FaceID')
    print('======================================')
    print('option: -f path -s path')
    print('  -f:')
    print('    path of the first image')
    print('  -s:')
    print('    path of the second image')
    # exit here
    Base.print_exit()

def get_face_image():
    fid = None
    sid = None
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hf:s:")
    except getopt.GetoptError:
        Base.print_exit('Invalid input, -h for help.')
    # get input
    if len(opts) == 0:
        Base.print_exit('Invalid input, -h for help.')
    else:        
        for name, value in opts:
            if name == '-h':
                print_help()
            elif name == '-f':
                fid = Base.get_abs_path(value)
            elif name == '-s':
                sid = Base.get_abs_path(value)
    return fid, sid

def main():
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
    fid, sid = get_face_image()
    if fid == None or sid == None:
        print('Error, no found id image.')
        return
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

