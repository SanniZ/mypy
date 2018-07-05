# -*- coding: utf-8 -*-
"""
Created on Thu Jul  5 12:39:24 2018

@author: Byng.Zeng
"""
import subprocess, os

from Android import Android
from Code import Code
from Linux import Linux
from CmdHandler import CmdHandler

class AvbImage(object):
    def avb_make_image(self, image):
        # copy image to flashfiles folder
        cmd = r'cp {pdt}/{src}.img {flashfiles}/{tar}.img'.format(\
            pdt=self._pdt, src=image, flashfiles=self._flashfiles, tar=image)
        print(cmd)
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
        #print(cmd)
        subprocess.call(cmd, shell=True)        

class Broxton(Android, Code, Linux, CmdHandler, AvbImage):
    support_cmd_list = {
        'help'  : None,
        'url'   : None,
        'flash' : None,
        'make'  : None,
        'rm'    : None,
        'fw'    : None,
        'ioc'   : None,
    }
    
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
                 url='', pdt='gordon_peak', opt='userdebug', user=''):
        super(Broxton, self).__init__()
        self._url = url
        self._pdt = pdt
        self._opt = opt
        self._user = user
        self._out = r'out/target/product/{pdt}'.format(pdt=self._pdt)
        self._flashfiles = r'{out}/{pdt}-flashfiles-eng.{user}'.format(\
                                out=self._out, pdt=self._pdt, user=self._user)
        #print('Broxton init done!')
        
    def help(self, cmds=''):
        super(Android, self).help(cmds)
        super(Code, self).help(cmds)
        super(Linux, self).help(cmds)
        super(CmdHandler, self).help(cmds)
        for cmd in cmds.values():
            if cmd == 'cfg':
                print('pdt: {}'.format(self._pdt))
                print('opt: {}'.format(self._opt))
                print('user: {}'.format(self._user))
                print('out: {}'.format(self._out))
                print('flashfiles: {}'.format(self._flashfiles))

    def check_input(self, cmds):
        for key in cmds.keys():
            if self.support_cmd_list.has_key(key) == False:
                return False
        return True

    def config_handler(self, cmds):
        for key in cmds.iterkeys():
            if key == 'help':
                self.support_cmd_list['help'] = self.help
            elif key == 'make':
                self.support_cmd_list['make'] = self.make_image
            elif key == 'flash':
                self.support_cmd_list['flash'] = self.flash_image
            elif key == 'fw':
                self.support_cmd_list['fw'] = self.flash_fw
            elif key == 'ioc':
                self.support_cmd_list['ioc'] = self.flash_ioc
            elif key == 'url':
                self.support_cmd_list['url'] = self.code_handler
            elif key == 'rm':
                self.support_cmd_list['rm'] = self.delete
                
    def run(self, cmds):
        #print cmds
        for key in cmds.iterkeys():
            if self.support_cmd_list[key] != None:
                f = self.support_cmd_list[key]
                f(cmds[key])
    
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
        for image in images.values():
            #print('make image: {}'.format(image))
            build_sh = self.create_build_script(image)
            cmd = r'./{}'.format(build_sh)
            print(cmd)
            subprocess.call(cmd, shell=True)
            # rm build shell file
            cmd = r'rm -rf {}'.format(build_sh)
            print(cmd)
            subprocess.call(cmd, shell=True)   
            
    def flash_image(self, images):
        # avb make images.
        for image in images.values():
            print('update image %s' % image)
            self.avb_make_image(image)
        # setup flash env
        self.wait_adb()
        self.reboot_bootloader()
        self.unlock()
        # flash image now
        for image in images.values():
            fimage = r'{}/{}.img' % (self._flashfiles, image)
            self.flash_image(image, fimage)
        # lock device.
        self.lock()
        self.fastboot_reboot()

    def flash_firmware(self, fw):
        cmd = r'sudo /opt/intel/platformflashtool/bin/ias-spi-programmer --write {}'.format(fw)
        subprocess.call(cmd, shell=True)
    
    def flash_ioc(self, ioc):
        cmd = r'sudo /opt/intel/platformflashtool/bin/ioc_flash_server_app -s /dev/ttyUSB2 -grfabc -t {}'.format(ioc)
        subprocess.call(cmd, shell=True)

if __name__ == '__main__':
    bxt = Broxton()
    bxt.main()