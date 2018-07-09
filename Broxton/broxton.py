#!/usr/bin/python

# -*- coding: utf-8 -*-
"""
Created on Thu Jul  5 12:39:24 2018

@author: Byng.Zeng
"""
import subprocess, os

from debug import Debug as d
from input import Input
from cmdprocessing import CmdProcessing
from code import Code

class AvbImage(object):
    def __init__(self):
        d.dbg('AvbImage init done!')

    def avb_make_image(self, image):
        # copy image to flashfiles folder
        cmd = r'cp {pdt}/{src}.img {flashfiles}/{tar}.img'.format(\
            pdt=self._pdt, src=image, flashfiles=self._flashfiles, tar=image)
        d.dbg(cmd)
        subprocess.call(cmd, shell=True)

        # uses avbtool to build image
        cmd = r'''
            out/host/linux-x86/bin/avbtool make_vbmeta_image --output %s/vbmeta.img \
            --include_descriptors_from_image %s/boot.img \
            --include_descriptors_from_image %s/system.img \
            --include_descriptors_from_image %s/vendor.img \
            --include_descriptors_from_image %s/tos.img \
            --key $TEST_KEY_PATH/testkey_rsa4096.pem --algorithm SHA256_RSA4096
            ''' % (self._flashfiles,
                   self._flashfiles,
                   self._flashfiles,
                   self._flashfiles,
                   self._flashfiles)
        d.dbg(cmd)
        subprocess.call(cmd, shell=True)        

class Broxton(AvbImage, Code):
    images_map = {
        'boot' : 'bootimage',
        'system' : 'bootimage',
        'tos' : 'bootimage',
        'bootimage' : 'bootimage',
        'systemimage' : 'bootimage',
        'tosimage' : 'bootimage',
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
        self._ioc = r'ioc_firmware_gp_mrb_fab_e_slcan.ias_ioc'
        if self._pdt != None and self._opt != None and self._user!= None:
            self._out = r'out/target/product/{pdt}'.format(pdt=self._pdt)
            self._flashfiles = r'{out}/{pdt}-flashfiles-eng.{user}'.format(\
                                out=self._out, pdt=self._pdt, user=self._user)
        else:
            self._out = None
            self._flashfiles = None
        
        self._cmd_handlers = {
            'help': self.help,
            'make': self.make_image,
            'flash' : self.flash_image,
            'url' : self.url_handler,
        }

        d.info(self._cmd_handlers)
        d.dbg('Broxton init done!')

    def help(self, cmds=''):
        #super(Code, self).help(cmds)
        super(Broxton, self).help(cmds)
        for cmd in cmds.values():
            if cmd == 'help':
                d.info('make:[option][,option]')
                d.info('option:')
                d.info('  all/flashfiles: make all of images')
                d.info('  boot  : make bootimage')
                d.info('  system: make systemimage')
                d.info('  tos   : make tosimage')
                d.info('  vendor: make vendorimage')
                d.info('flash:[option][,option]')
                d.info('option:')
                d.info('  boot  : flash bootimage')
                d.info('  system: flash systemimage')
                d.info('  tos   : flash tosimage')
                d.info('  vendor: flash vendorimage')
                d.info('  fw    : flash firmware')
                d.info('  ioc   : flash ioc')
            elif cmd == 'cfg':
                d.info('url: {}'.format(self._url))
                d.info('pdt: {}'.format(self._pdt))
                d.info('opt: {}'.format(self._opt))
                d.info('user: {}'.format(self._user))
                d.info('out: {}'.format(self._out))
                d.info('flashfiles: {}'.format(self._flashfiles))
                d.info('fw: {}'.format(self._fw))
                d.info('ioc: {}'.format(self._ioc))

    def create_build_script(self, image):
        builds = r'''#!/bin/bash
rm -rf out/.lock
device/intel/mixins/mixin-update
. build/envsetup.sh
lunch {pdt}-{opt}
make {tgt} -j{n}'''.format(pdt=self._pdt, opt=self._opt,\
                            tgt=self.images_map[image], n=self.get_cups())
        build_sh = r'.build_image.sh'
        with open(build_sh, 'w') as f:
            f.write(builds)
        # run buildImage.sh
        os.system(r'chmod a+x {}'.format(build_sh))
        return build_sh

    def make_image(self, images):
        d.dbg('Broxton.make_image: images {}'.format(images))
        for image in images.values():
            d.info('create makesh for {}'.format(image))
            build_sh = self.create_build_script(image)
            cmd = r'./{}'.format(build_sh)
            d.info(cmd)
            subprocess.call(cmd, shell=True)
            # rm build shell file
            cmd = r'rm -rf {}'.format(build_sh)
            d.info(cmd)
            subprocess.call(cmd, shell=True)   

    def flash_image(self, images):
        for image in images.values():
            if image == 'fw':
                self.flash_firmware('{path}/{fw}'.format(path=self._flashfiles, fw=self._fw))
            elif image == 'ioc':
                self.flash_ioc('{path}/{fw}'.format(path=self._flashfiles, fw=self._ioc))
            else:
                # avb make images.
                for image in images.values():
                    d.info('update image %s' % image)
                    self.avb_make_image(image)
                # setup flash env
                self.wait_adb()
                self.reboot_bootloader()
                # unlock
                self.lock(False)
                # flash image now
                for image in images.values():
                    fimage = r'{}/{}.img' % (self._flashfiles, image)
                    self.flash_image(image, fimage)
                # lock device.
                self.lock(True)
                self.fastboot_reboot()

    def flash_firmware(self, fw):
        cmd = r'sudo /opt/intel/platformflashtool/bin/ias-spi-programmer --write {}'.format(fw)
        d.info(cmd)
        subprocess.call(cmd, shell=True)
    
    def flash_ioc(self, ioc):
        cmd = r'sudo /opt/intel/platformflashtool/bin/ioc_flash_server_app -s /dev/ttyUSB2 -grfabc -t {}'.format(ioc)
        d.info(cmd)
        subprocess.call(cmd, shell=True)

    def get_handler(self, cmd):
        if self._cmd_handlers.has_key(cmd) == True:
            return self._cmd_handlers[cmd]
        else:
            return None

    def run(self):
        cmds_list = {} 

        cmds_list['help'] = self.get_handler('help')
        cmds_list['url'] = self.get_handler('url')
        cmds_list['make'] = self.get_handler('make')
        cmds_list['flash'] = self.get_handler('flash')

        cmdHdr = CmdProcessing()
        for key in cmds_list.iterkeys():
            cmdHdr.register_cmd_handler(key, cmds_list[key])

        inp = Input()
        input_dict = inp.get_input()
        cmdHdr.run(input_dict)

if __name__ == '__main__':
    #d.set_debug_level('dbg,info,err')
    bxt = Broxton(r'ssh://android.intel.com/manifests -b android/master -m r0',
                  'gordon_peak', 'userdebug', 'yingbin')
    bxt.run()