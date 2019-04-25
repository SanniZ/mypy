#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul  5 12:39:24 2018

@author: Byng.Zeng
"""

import os
import subprocess

from develop.debug import Debug as d
from cmdprocess.cmdprocessing import CmdProcessing
from develop.repo.repohelper import RepoHelper
from linux.linux import HwInfo
from develop.android.android import Android


class AvbImage(object):
    def avb_make_image(self, image, broxton):
        # copy image to flashfiles folder
        cmd = r'cp {out}/{src}.img {flashfiles}/{tar}.img'.format(
                out=broxton._out, src=image, flashfiles=broxton._flashfiles,
                tar=image)
        d.dbg(cmd)
        subprocess.call(cmd, shell=True)

        d.dbg('avb make image now.')
        cmd = r'''out/host/linux-x86/bin/avbtool make_vbmeta_image \
                    --output {}/vbmeta.img \
                    --include_descriptors_from_image {}/boot.img \
                    --include_descriptors_from_image {}/system.img \
                    --include_descriptors_from_image {}/vendor.img \
                    --include_descriptors_from_image {}/tos.img \
                    --key external/avb/test/data/testkey_rsa4096.pem \
                    --algorithm SHA256_RSA4096'''.format(
            broxton._flashfiles,
            broxton._flashfiles,
            broxton._flashfiles,
            broxton._flashfiles,
            broxton._flashfiles)
        d.dbg(cmd)
        subprocess.call(cmd, shell=True)


class Broxton(object):
    make_map = {
        'clean': 'clean',
        'boot': 'bootimage',
        'system': 'systemimage',
        'tos': 'tosimage',
        'vendor': 'vendorimage',
        'bootimage': 'bootimage',
        'systemimage': 'systemimage',
        'tosimage': 'tosimage',
        'vendorimage': 'vendorimage',
        'flashfiles': 'flashfiles',
        'all': 'flashfiles',
    }

    rmdir_map = {
        'bootimage': 'out/target/product/gordon_peak/obj/kernel',
        'tosimage': 'out/target/product/gordon_peak/obj/trusty',
        'vendorimage': 'out/target/product/gordon_peak/vendor',
        'systemimage': 'out/target/product/gordon_peak/system',
    }

    def __init__(self,
                 url=None, pdt=None, opt=None, user=None):
        super(Broxton, self).__init__()
        self._url = url
        self._pdt = pdt
        self._opt = opt
        self._user = user
        self._fw = r'ifwi_gr_mrb_b1.bin'
        self._ioc = r'ioc_firmware_gp_mrb_fab_e_slcan.ias_ioc'
        if all((self._pdt, self._opt, self._user)):
            self._out = r'out/target/product/{pdt}'.format(pdt=self._pdt)
            self._flashfiles = r'{out}/{pdt}-flashfiles-eng.{user}'.format(
                                out=self._out, pdt=self._pdt, user=self._user)
        else:
            self._out = None
            self._flashfiles = None

        self.__register_cmd_handlers()
        d.dbg('Broxton init done!')

    def help(self, cmds):
        for cmd in cmds:
            if cmd == 'help':
                d.info('make:[option][,option]')
                d.info('  [option]:')
                d.info('  all/flashfiles: make all of images')
                d.info('  boot  : make bootimage')
                d.info('  system: make systemimage')
                d.info('  tos   : make tosimage')
                d.info('  vendor: make vendorimage')
                d.info('  mmm#xxx: make xxx dir')
                d.info('flash:[option][,option]')
                d.info('  [option]:')
                d.info('  boot  : flash bootimage')
                d.info('  system: flash systemimage')
                d.info('  tos   : flash tosimage')
                d.info('  vendor: flash vendorimage')
                d.info('  fw    : flash firmware')
                d.info('  ioc   : flash ioc')
            elif cmd == 'cfg':
                d.info('pdt: {}'.format(self._pdt))
                d.info('opt: {}'.format(self._opt))
                d.info('user: {}'.format(self._user))
                d.info('out: {}'.format(self._out))
                d.info('flashfiles: {}'.format(self._flashfiles))
                d.info('fw: {}'.format(self._fw))
                d.info('ioc: {}'.format(self._ioc))

    def create_make_sh(self, image):
        make_sh = r'.make.sh'
        img = self.make_map[image]
        with open(make_sh, 'w') as f:
            f.write("#!/bin/bash\n")
            if img in self.rmdir_map.keys():
                f.write('rm -rf %s\n' % self.rmdir_map[img])
            f.write("rm -rf out/.lock\n")
            f.write("device/intel/mixins/mixin-update\n")
            f.write(". build/envsetup.sh\n")
            f.write("lunch {pdt}-{opt}\n".format(pdt=self._pdt, opt=self._opt))
            if os.path.exists('build.log'):
                os.rename('build.log', 'build.log.old')
            f.write("make {tgt} -j{n} 2>&1 | tee build.log\n".format(
                    tgt=self.make_map[image], n=HwInfo().get_cups()))
        return make_sh

    def create_mmm_sh(self, target):
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
            f.write("lunch {pdt}-{opt}\n".format(pdt=self._pdt, opt=self._opt))
            f.write("mmm {tgt}\n".format(tgt=tgt))

        return make_sh

    def make_image(self, images):
        d.dbg('Broxton.make_image: {}'.format(images))
        make_sh = None
        for image in images:
            d.dbg('create makesh for {}'.format(image))
            if type(image) is dict:
                if 'mmm' in image:
                    make_sh = self.create_mmm_sh(image['mmm'])
                else:
                    d.err('Not support: %s' % str(image))
                    exit()
            else:
                make_sh = self.create_make_sh(image)

            # set run right
            cmd = r'chmod a+x {}'.format(make_sh)
            subprocess.call(cmd, shell=True)
            # run make sh
            cmd = r'./{}'.format(make_sh)
            d.dbg(cmd)
            subprocess.call(cmd, shell=True)
            # delete make sh
            cmd = r'rm -rf {}'.format(make_sh)
            d.dbg(cmd)
            subprocess.call(cmd, shell=True)

    def flash_images(self, images):
        fimgs = list()
        avb = None
        for image in images:
            if image == 'fw':
                self.flash_firmware(
                    '{path}/{fw}'.format(path=self._flashfiles, fw=self._fw))
            elif image == 'ioc':
                self.flash_ioc('{path}/{fw}'.format(
                                path=self._flashfiles, fw=self._ioc))
            else:
                # avb make images.
                d.info('update %s image' % image)
                if not avb:
                    avb = AvbImage()
                avb.avb_make_image(image, self)
                fimgs.append(image)
        # flash images.
        if len(fimgs) != 0:
            fimgs.append('vbmeta')
            # setup flash env
            ad = Android()
            # ad.adb_wait()
            # enter bootloader mode.
            ad.run_cmd_handler(['rebootloader'])
            # unlock
            ad.run_cmd_handler(['deviceunlock'])
            # flash image now
            for image in fimgs:
                fimage = r'{}/{}.img'.format(self._flashfiles, image)
                d.info('fastboot flash {} {}'.format(image, fimage))
                ad.flash_image(image, fimage)
            # lock device.
            ad.run_cmd_handler(['devicelock'])
            # reboot
            ad.run_cmd_handler(['fastreboot'])

    def flash_firmware(self, fw):
        cmd = \
            r'sudo /opt/intel/platformflashtool/bin/ias-spi-programmer --write %s'.format(fw)
        d.info(cmd)
        subprocess.call(cmd, shell=True)

    def flash_ioc(self, ioc):
        cmd = r'sudo /opt/intel/platformflashtool/bin/ioc_flash_server_app -s /dev/ttyUSB2 -grfabc -t {}'.format(ioc)
        d.info(cmd)
        subprocess.call(cmd, shell=True)

    def get_cmd_handlers(self, cmd=None):
        hdrs = {
            'help': self.help,
            'make': self.make_image,
            'flash': self.flash_images,
        }

        if not cmd:
            return hdrs
        else:
            if cmd in hdrs:
                return hdrs[cmd]
            else:
                return None

    def __register_cmd_handlers(self):
        self._cmdHdrs = CmdProcessing()
        self._repo = RepoHelper(self._url)
        self._cmdHdrs.register_cmd_handler(self._repo.get_cmd_handlers())
        self._cmdHdrs.register_cmd_handler(self.get_cmd_handlers())

    def run_sys_input(self):
        self._cmdHdrs.run_sys_input()

if __name__ == '__main__':
    bxt = Broxton(r'ssh://android.intel.com/manifests -b android/master -m r0',
                  r'gordon_peak',
                  r'userdebug',
                  r'yingbin')

    bxt.run_sys_input()
