#!/usr/bin/python

# -*- coding: utf-8 -*-
"""
Created on Thu Jul  5 12:39:24 2018

@author: Byng.Zeng
"""
import subprocess

from debug import Debug as d
from cmdprocessing import CmdProcessing
from code import Code
from linux import HwInfo
from android import Android


class AvbImage(object):
    def __init__(self):
        d.dbg('avbImage init done.')

    def avb_make_image(self, image):
        # copy image to flashfiles folder
        cmd = r'cp {out}/{src}.img {flashfiles}/{tar}.img'.format(\
            out=self._out, src=image, flashfiles=self._flashfiles, tar=image)
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
            self._flashfiles,
            self._flashfiles,
            self._flashfiles,
            self._flashfiles,
            self._flashfiles)
        d.dbg(cmd)
        subprocess.call(cmd, shell=True)

class Broxton(AvbImage, Code):
    make_map = {
        'clean' : 'clean',
        'boot' : 'bootimage',
        'system' : 'systemimage',
        'tos' : 'tosimage',
        'vendor' : 'vendorimage',
        'bootimage' : 'bootimage',
        'systemimage' : 'systemimage',
        'tosimage' : 'tosimage',
        'vendorimage' : 'vendorimage',
        'flashfiles' : 'flashfiles',
        'all' : 'flashfiles',       
    }

    def __init__(self,
                 url=None, pdt=None, opt=None, user=None):
        super(Broxton, self).__init__()
        self._url = url
        self._pdt = pdt
        self._opt = opt
        self._user = user
        self._fw = r'ifwi_gr_mrb_b1.bin'
        self._ioc = r'ioc_firmware_gp_mrb_fab_d_slcan.ias_ioc'
        if self._pdt != None and self._opt != None and self._user!= None:
            self._out = r'out/target/product/{pdt}'.format(pdt=self._pdt)
            self._flashfiles = r'{out}/{pdt}-flashfiles-eng.{user}'.format(\
                                out=self._out, pdt=self._pdt, user=self._user)
        else:
            self._out = None
            self._flashfiles = None

        self._cmdHdrs = CmdProcessing()
        self._cmdHdrs.register_cmd_handler(self.__get_cmd_handlers())
        d.dbg('Broxton init done!')

    def help(self, cmds):
        super(Broxton, self).help(cmds)
        for cmd in cmds:
            if cmd == 'help':
                d.info('make:[option][,option]')
                d.info('  [option]:')
                d.info('  all/flashfiles: make all of images')
                d.info('  boot  : make bootimage')
                d.info('  system: make systemimage')
                d.info('  tos   : make tosimage')
                d.info('  vendor: make vendorimage')
                d.info('flash:[option][,option]')
                d.info('  [option]:')
                d.info('  boot  : flash bootimage')
                d.info('  system: flash systemimage')
                d.info('  tos   : flash tosimage')
                d.info('  vendor: flash vendorimage')
                d.info('  fw    : flash firmware')
                d.info('  ioc   : flash ioc')
                d.info('mmm:xxx')
                d.info('  xxx: mmm xxx dir')
            elif cmd == 'cfg':
                d.info('pdt: {}'.format(self._pdt))
                d.info('opt: {}'.format(self._opt))
                d.info('user: {}'.format(self._user))
                d.info('out: {}'.format(self._out))
                d.info('flashfiles: {}'.format(self._flashfiles))
                d.info('fw: {}'.format(self._fw))
                d.info('ioc: {}'.format(self._ioc))

    def create_make_sh(self, image):
        make_cmds = r'''#!/bin/bash
rm -rf out/.lock
device/intel/mixins/mixin-update
. build/envsetup.sh
lunch {pdt}-{opt}
make {tgt} -j{n}'''.format(pdt=self._pdt, opt=self._opt,\
                        tgt=self.make_map[image], n=HwInfo().get_cups())
        make_sh = r'.make.sh'
        with open(make_sh, 'w') as f:
            f.write(make_cmds)
        return make_sh

    def create_mmm_sh(self, target):
        make_cmds = r'''#!/bin/bash
rm -rf out/.lock
device/intel/mixins/mixin-update
. build/envsetup.sh
lunch {pdt}-{opt}
mmm {tgt}'''.format(pdt=self._pdt, opt=self._opt,tgt=target)
        make_sh = r'.make.sh'
        with open(make_sh, 'w') as f:
            f.write(make_cmds)
        return make_sh

    def make_image(self, images):
        d.dbg('Broxton.make_image: {}'.format(images))
        make_sh = None
        for image in images:
            d.dbg('create makesh for {}'.format(image))
            if image == 'mmm':
                make_sh = 'mmm'
                continue
            elif make_sh == 'mmm':
                make_sh = self.create_mmm_sh(image)
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
        for image in images:
            if image == 'fw':
                self.flash_firmware('{path}/{fw}'.format(path=self._flashfiles, fw=self._fw))
            elif image == 'ioc':
                self.flash_ioc('{path}/{fw}'.format(path=self._flashfiles, fw=self._ioc))
            else:
                # avb make images.
                d.info('update image %s' % image)
                self.avb_make_image(image)
                fimgs.append(image)
        # flash images.
        if len(fimgs) != 0:
            fimgs.append('vbmeta')
            # setup flash env
            ad = Android()
            #ad.adb_wait()
            ad.reboot_bootloader()
            # unlock
            ad.lock(False)
            # flash image now
            for image in fimgs:
                fimage = r'{}/{}.img'.format(self._flashfiles, image)
                #d.info('fastboot flash {} {}'.format(image, fimage))
                ad.flash_image(image, fimage)
            # lock device.
            ad.lock(True)
            ad.fastboot_reboot()

    def flash_firmware(self, fw):
        cmd = r'sudo /opt/intel/platformflashtool/bin/ias-spi-programmer --write {}'.format(fw)
        d.info(cmd)
        subprocess.call(cmd, shell=True)
    
    def flash_ioc(self, ioc):
        cmd = r'sudo /opt/intel/platformflashtool/bin/ioc_flash_server_app -s /dev/ttyUSB2 -grfabc -t {}'.format(ioc)
        d.info(cmd)
        subprocess.call(cmd, shell=True)

    def __get_cmd_handlers(self, cmd=None):
        hdrs = {
            'help': self.help,
            'make': self.make_image,
            'flash' : self.flash_images,
            'url' : self.url_handler,
        }
        if cmd == None:
            return hdrs
        else:
            if hdrs.has_key(cmd) == True:
                return hdrs[cmd]
            else:
                return None

    def run(self):
        self._cmdHdrs.run_sys_input()

if __name__ == '__main__':
    #d.set_debug_level(7)
    URL = r'ssh://android.intel.com/manifests -b android/master -m r0'
    PDT = r'gordon_peak'
    OPT = r'userdebug'
    USR = r'yingbin'

    bxt = Broxton(URL, PDT, OPT, USR)
    bxt.run()