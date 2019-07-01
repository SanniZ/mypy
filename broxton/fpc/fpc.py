#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul  5 14:33:36 2018

@author: Byng.Zeng
"""
import os

from broxton.broxton import Broxton
from develop.debug import Debug as d
import subprocess

VERSION = '1.0.1'


class Fpc(Broxton):
    URL = 'ssh://xfeng8-ubuntu2.sh.intel.com:29418/manifests -b master'
    PDT = 'gordon_peak'
    OPT = 'userdebug'
    USR = os.getenv('USER')

    def __init__(self, url=URL, pdt=PDT, opt=OPT, user=USR):
        super(Fpc, self).__init__(url=url, pdt=pdt, opt=opt, user=user)
        self._cmdproc.register_cmd_handler(self.__get_cmd_handlers())

    def help(self, cmds):
        super(Fpc, self).help(cmds)
        for cmd in cmds:
            if cmd == 'help':
                d.info('ftest:[make][,push][,xxx]')
                d.info('  make: build fingerprint test binary')
                d.info('  push: push ftest to /data/')
                d.info('  xxx : run ftest xxx test')

    def ftest_handlers(self, cmds):
        for cmd in cmds:
            if cmd == 'make':
                l = list()
                l.append(
                    'vendor/intel/hardware/fingerprint/fingerprint_tac/normal')
                d = dict()
                d['mmm'] = l
                image = list()
                image.append(d)
                self.make_image(image)
            elif cmd == 'push':
                sh = r'adb push {out}/vendor/bin/fpc_tee_test /data/ftest'\
                    .format(out=self._out)
                subprocess.call(sh, shell=True)
                sh = r'adb shell chmod a+x /data/ftest'
                subprocess.call(sh, shell=True)
            elif cmd == 'help':
                sh = r'adb shell ./data/ftest'
                subprocess.call(sh, shell=True)
            else:
                sh = r'adb shell ./data/ftest %s' % cmd
                subprocess.call(sh, shell=True)

    def __get_cmd_handlers(self):
        hdrs = {
            'ftest': self.ftest_handlers,
        }
        return hdrs


if __name__ == '__main__':
    fpc = Fpc()
    fpc.run_sys_input()
