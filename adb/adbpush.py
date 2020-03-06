#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import subprocess


# files of src.
srcs = ['sc8811.z02',
        'sc8811.z03',
        'sc8811.zip']
# path of tgt
tgt = 'storage/80B6-586E/Morningcore/sc8811/zip'

# push srcs
def push(srcs=srcs, tgt=tgt):
    for src in srcs:
        cmd = 'adb push %s %s' % (src, tgt)
        print("%s -> %s" % (src, tgt))
        subprocess.call(cmd, shell=True)
        print("done!")


if __name__ == '__main__':
    push()

