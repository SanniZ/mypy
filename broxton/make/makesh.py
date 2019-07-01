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


VERSION = '1.1.1'


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
    def set_make_ncpu():
        ncpu = HwInfo().get_cups()
        if ncpu <= 8:
            return ncpu - 1
        elif ncpu <= 16:
            return ncpu - 2
        else:
            return ncpu - 4


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
            if image_files:  # pre delete files.
                for f in image_files:
                    fd.write("rm -rf {f}\n".format(f=f))
            fd.write("rm -rf out/.lock\n")
            fd.write("device/intel/mixins/mixin-update\n")
            fd.write(". build/envsetup.sh\n")
            fd.write("lunch {pdt}-{opt}\n".format(pdt=pdt, opt=opt))
            if os.path.exists('build.log'):
                os.rename('build.log', 'build.log.old')
            fd.write("make {tgt} -j{n} 2>&1 | tee build.log\n".format(
                tgt=img, n=set_make_ncpu()))
    return make_sh


def create_mmm_sh(target, pdt='gordon_peak', opt='userdebug'):
    # convert to string
    t = type(target)
    if t == list:
        tgt = str(target[0])  # only support first arg.
    else:
        tgt = target

    make_sh = r'.make.sh'
    with open(make_sh, 'w') as fd:
        fd.write("#!/bin/bash\n")
        fd.write("rm -rf out/.lock\n")
        fd.write("device/intel/mixins/mixin-update\n")
        fd.write(". build/envsetup.sh\n")
        fd.write("lunch {pdt}-{opt}\n".format(pdt=pdt, opt=opt))
        fd.write("mmm {tgt}\n".format(tgt=tgt))
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

    def create_make_sh(self, image, pre_delete=False):
        return create_make_sh(
                  image, self._pdt, self._opt,
                  self.image_pre_delete_files(image) if pre_delete else None)

    def execute_make_sh(self, make_sh):
        execute_make_sh(make_sh)

    def execute_make_image(self, image):
        execute_make_sh(self.create_make_sh(image))

    def create_mmm_sh(self, target):
        return create_mmm_sh(target, self._pdt, self._opt)

    def image_pre_delete_files(self, image):
        image_files = {  # image : [files]
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
    pre_delete = False
    for image in sys.argv[1:]:
        # pre delete.
        if image in ['clear', 'clr', 'delete', 'del']:
            pre_delete = True
            continue
        elif image in ['noclear', 'noclr', 'nodelete', 'nodel']:
            pre_delete = False
            continue
        # create and excute make shell.
        if image in ['clean', 'cln']:
            sh = create_clean_sh()
        else:
            sh = makesh.create_make_sh(image, pre_delete)
        execute_make_sh(sh)
