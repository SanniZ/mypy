# -*- coding: utf-8 -*-
"""
Created on Thu Jul  5 12:39:24 2018

@author: Byng.Zeng
"""
import subprocess, os

#from Android import Android
#from Code import Code
#from Linux import Linux
from CmdHandler import CmdHandler
from Debug import Debug

class AvbImage(Debug):
    def __init__(self):
        super(AvbImage, self).__init__()
        self.dbg('AvbImage init done!')
    
    def avb_make_image(self, image):
        # copy image to flashfiles folder
        cmd = r'cp {pdt}/{src}.img {flashfiles}/{tar}.img'.format(\
            pdt=self._pdt, src=image, flashfiles=self._flashfiles, tar=image)
        self.dbg(cmd)
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
        self.dbg(cmd)
        subprocess.call(cmd, shell=True)        

class Broxton(CmdHandler, AvbImage):
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
        
        self.support_cmd_list['url'] = None   
        self.support_cmd_list['make'] = None 
        self.support_cmd_list['flash'] = None
        #self.support_cmd_list['fw'] = None
        #self.support_cmd_list['ioc'] = None

        self.dbg('Broxton init done!')
        
    def help(self, cmds=''):
        #super(Code, self).help(cmds)
        super(Broxton, self).help(cmds)
        for cmd in cmds.values():
            if cmd == 'help':
                self.info('make:[all/flashfiles][,boot][,system][,tos][,vendor]')
                self.info('  all/flashfiles: make all of images')
                self.info('  boot  : make bootimage')
                self.info('  system: make systemimage')
                self.info('  tos   : make tosimage')
                self.info('  vendor: make vendorimage')
                self.info('flash:[boot][,system][,tos][,vendor]')
                self.info('  boot  : flash bootimage')
                self.info('  system: flash systemimage')
                self.info('  tos   : flash tosimage')
                self.info('  vendor: flash vendorimage')
                self.info('  fw    : flash firmware')
                self.info('  ioc   : flash ioc')
            elif cmd == 'cfg':
                self.info('url: {}'.format(self._url))
                self.info('pdt: {}'.format(self._pdt))
                self.info('opt: {}'.format(self._opt))
                self.info('user: {}'.format(self._user))
                self.info('out: {}'.format(self._out))
                self.info('flashfiles: {}'.format(self._flashfiles))
                self.info('fw: {}'.format(self._fw))
                self.info('ioc: {}'.format(self._ioc))

    def config_handler(self, cmds):
        super(Broxton, self).config_handler(cmds)
        for key in cmds.iterkeys():
            if key == 'help':
                self.support_cmd_list['help'] = self.help
            elif key == 'url':
                self.support_cmd_list['url'] = self.code_handler
            elif key == 'make':
                self.support_cmd_list['make'] = self.make_image
            elif key == 'flash':
                self.support_cmd_list['flash'] = self.flash_image
            #elif key == 'fw':
            #    self.support_cmd_list['fw'] = self.flash_firmware
            #elif key == 'ioc':
            #    self.support_cmd_list['ioc'] = self.flash_ioc
    
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
        self.dbg('Broxton.make_image: images {}'.format(images))
        pass
        for image in images.values():
            self.info('create makesh for {}'.format(image))
            build_sh = self.create_build_script(image)
            cmd = r'./{}'.format(build_sh)
            self.info(cmd)
            subprocess.call(cmd, shell=True)
            # rm build shell file
            cmd = r'rm -rf {}'.format(build_sh)
            self.info(cmd)
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
                    self.info('update image %s' % image)
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
        self.info(cmd)
        subprocess.call(cmd, shell=True)
    
    def flash_ioc(self, ioc):
        cmd = r'sudo /opt/intel/platformflashtool/bin/ioc_flash_server_app -s /dev/ttyUSB2 -grfabc -t {}'.format(ioc)
        self.info(cmd)
        subprocess.call(cmd, shell=True)

if __name__ == '__main__':
    bxt = Broxton()
    bxt.main()