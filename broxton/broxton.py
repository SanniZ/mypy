#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul  5 12:39:24 2018

@author: Byng.Zeng
"""
import os
import subprocess

from develop.debug import Debug as d
from pybase.pyprocess.pyprocess import PyCmdProcess
from develop.repo.repohelper import RepoHelper
from develop.android.android import Android
try:
    from broxton.make.makesh import MakeSH
except ImportError as e:
    from make.makesh import MakeSH


VERSION = '1.1.3'


class AvbImage(object):
    def avb_make_image(self, image, broxton):
        # copy image to flashfiles folder
        cmd = r'cp {out}/{src}.img {flashfiles}/{tar}.img'.format(
                out=broxton._out, src=image, flashfiles=broxton._flashfiles,
                tar=image)
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
        subprocess.call(cmd, shell=True)


class Broxton(object):
    URL = 'ssh://xfeng8-ubuntu2.sh.intel.com:29418/manifests -b master'
    PDT = 'gordon_peak'
    OPT = 'userdebug'
    USR = os.getenv('USER')

    def __init__(self, url=URL, pdt=PDT, opt=OPT, user=USR):
        self._url = url
        self._pdt = pdt
        self._opt = opt
        self._user = user
        self._fw = r'ifwi_gr_mrb_b1.bin'
        self._ioc = r'ioc_firmware_gp_mrb_fab_e.ias_ioc'
        if all((self._pdt, self._opt, self._user)):
            self._out = r'out/target/product/{pdt}'.format(pdt=self._pdt)
            self._flashfiles = r'{out}/{pdt}-flashfiles-eng.{user}'.format(
                                out=self._out, pdt=self._pdt, user=self._user)
        else:
            self._out = None
            self._flashfiles = None
        # register cmd handlers.
        self.__register_cmd_handlers()

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

    def make_image(self, images):
        d.dbg('Broxton.make_image: {}'.format(images))
        make_sh = MakeSH(pdt=self._pdt, opt=self._opt, user=self._user)
        sh = None
        pre_delete = False
        for image in images:
            # pre delete.
            if image in ['clear', 'clr', 'delete', 'del']:
                pre_delete = True
                continue
            elif image in ['noclear', 'noclr', 'nodelete', 'nodel']:
                pre_delete = False
                continue
            # create and excute make shell
            d.dbg('create makesh for {}'.format(image))
            if type(image) is dict:
                if 'mmm' in image:
                    sh = MakeSH(
                        pdt=self._pdt, opt=self._opt,
                        user=self._user).create_mmm_sh(image['mmm'])
                else:
                    d.err('Not support: %s' % str(image))
                    exit()
            else:
                sh = make_sh.create_make_sh(image, pre_delete)
            # run makesh to build images.
            make_sh.execute_make_sh(sh)

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
        tool = '/opt/intel/platformflashtool/bin/ias-spi-programmer'
        cmd = r'sudo {} --write {}'.format(tool, fw)
        d.info(cmd)
        subprocess.call(cmd, shell=True)

    def flash_ioc(self, ioc):
        tool = '/opt/intel/platformflashtool/bin/ioc_flash_server_app'
        cmd = r'sudo {} -s /dev/ttyUSB2 -grfabc -t {}'.format(tool, ioc)
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
        self._cmdproc = PyCmdProcess()
        self._repo = RepoHelper(self._url)
        self._cmdproc.register_cmd_handler(self._repo.get_cmd_handlers())
        self._cmdproc.register_cmd_handler(self.get_cmd_handlers())

    def run_sys_input(self):
        self._cmdproc.run_sys_input()

if __name__ == '__main__':
    bxt = Broxton(r'ssh://android.intel.com/manifests -b android/master -m r0',
                  r'gordon_peak',
                  r'userdebug',
                  os.getenv('USER'))

    bxt.run_sys_input()
