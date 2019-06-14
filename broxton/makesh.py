#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 2019-06-12

@author: Byng.Zeng
"""

import os
import sys
import subprocess

from linux.linux import HwInfo


VERSION = '1.1.0'


IMAGE_MAP = {
    'clean': 'clean',
    'boot': 'bootimage',
    'system': 'systemimage',
    'tos': 'tosimage',
    'vendor': 'vendorimage',
    'all': 'flashfiles',
    'bootimage': 'bootimage',
    'systemimage': 'systemimage',
    'tosimage': 'tosimage',
    'vendorimage': 'vendorimage',
    'flashfiles': 'flashfiles',
}


def create_make_sh(image,
                   pdt='gordon_peak', opt='userdebug', image_files=None):
    if image not in IMAGE_MAP:
        print('error, found unknown image: %s' % image)
        return None

    img = IMAGE_MAP[image]
    if img in ['clean']:
        make_sh = create_clean_sh()
    else:
        make_sh = r'.make.sh'
        with open(make_sh, 'w') as fd:
            fd.write("#!/bin/bash\n")
            if image_files:
                for f in image_files:
                    fd.write("rm -rf {f}\n".format(f=f))
            fd.write("rm -rf out/.lock\n")
            fd.write("device/intel/mixins/mixin-update\n")
            fd.write(". build/envsetup.sh\n")
            fd.write("lunch {pdt}-{opt}\n".format(pdt=pdt, opt=opt))
            if os.path.exists('build.log'):
                os.rename('build.log', 'build.log.old')
            ncpu = HwInfo().get_cups()
            fd.write("make {tgt} -j{n} 2>&1 | tee build.log\n".format(
                tgt=img, n=(ncpu if ncpu < 8 else ncpu - 4)))
    return make_sh


def create_mmm_sh(target, pdt='gordon_peak', opt='userdebug'):
    # convert to string
    t = type(target)
    if t == list:
        tgt = str(target[0])  # only support first arg.
    else:
        tgt = target

    make_sh = r'.make.sh'
    with open(make_sh, 'w') as f:
        f.write("#!/bin/bash\n")
        f.write("rm -rf out/.lock\n")
        f.write("device/intel/mixins/mixin-update\n")
        f.write(". build/envsetup.sh\n")
        f.write("lunch {pdt}-{opt}\n".format(pdt=pdt, opt=opt))
        f.write("mmm {tgt}\n".format(tgt=tgt))
    return make_sh


def create_clean_sh():
    make_sh = r'.make.sh'
    with open(make_sh, 'w') as f:
        f.write("#!/bin/bash\n")
        f.write("rm -rf out\n")
    return make_sh


def execute_make_sh(make_sh):
    cmd = r'chmod a+x {}'.format(make_sh)
    subprocess.call(cmd, shell=True)
    # run make sh
    cmd = r'./{}'.format(make_sh)
    subprocess.call(cmd, shell=True)
    # delete make sh
    cmd = r'rm -rf {}'.format(make_sh)
    subprocess.call(cmd, shell=True)


class MakeSH(object):

    def __init__(self, pdt, opt, user=os.getenv('USER')):
        self._pdt = pdt
        self._opt = opt
        self._user = user
        self._out = 'out/target/product/{pdt}'.format(pdt=self._pdt)
        self._flashfiles = '{out}/{pdt}-flashfiles-eng.{user}'.format(
                            out=self._out, pdt=self._pdt, user=self._user)

    def create_make_sh(self, image):
        return create_make_sh(image, self._pdt, self._opt,
                              self.image_pre_delete_files(image))

    def execute_make_sh(self, make_sh):
        execute_make_sh(make_sh)

    def execute_make_image(self, image):
        execute_make_sh(self.create_make_sh(image))

    def create_mmm_sh(self, target):
        return create_mmm_sh(target, self._pdt, self._opt)

    def image_pre_delete_files(self, image):
        image_files = {
            'bootimage': ['boot.img', 'obj/kernel'],
            'systemimage': ['system.img', 'system', 'obj/JAVA_LIBRARY'],
            'vendorimage': ['vendor.img', 'vendor'],
            'tosimage': ['tos.img', 'obj/trusty'],
            'flashfiles': ['*.img', 'obj/kernel', 'obj/trusty',
                           '{pdt}-flashfiles-eng.{user}*'.format(
                               pdt=self._pdt, user=self._user)],
        }
        fs = []
        if image in IMAGE_MAP:
            img = IMAGE_MAP[image]
            if img in image_files:
                for f in image_files[img]:
                    fs.append('{out}/{f}'.format(out=self._out, f=f))
                return fs
        return fs


if __name__ == '__main__':
    makesh = MakeSH(pdt='gordon_peak', opt='userdebug')
    for image in sys.argv[1:]:
        if image in ['clean', 'clear', 'clr']:
            sh = create_clean_sh()
        else:
            sh = makesh.create_make_sh(image)
        execute_make_sh(sh)
