#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul  5 15:18:47 2018

@author: Byng.Zeng
"""

import subprocess

from develop.repo.repohelper import RepoHelper
from develop.debug import Debug as d
from cmdprocess.cmdprocessing import CmdProcessing


class Cwp(RepoHelper):

    URL = \
        r'ssh://android.intel.com/h/hypervisor/manifests -b hypervisor/master'

    def __init__(self, url=URL):
        super(Cwp, self).__init__(url)
        self._url = url

        # create cmd process
        self._cmdHdrs = CmdProcessing()
        self._cmdHdrs.register_cmd_handler(self.get_cmd_handlers())
        d.dbg('Cwp init done!')

    def help(self, cmds):
        super(Cwp, self).help(cmds)
        for cmd in cmds:
            if cmd == 'help':
                d.info('make:[option][,option]')
                d.info('  [option]:')
                d.info('  all: make all of images')
                d.info('  sos: make sos image')
                d.info('  sos_dm: make sos_dm image')
                d.info('  sos_kernel: make sos_kernel image')
                d.info('  uos: make uos image')
                d.info('  uos_kernel: make uos_kernel image')
                d.info('  flash: flash all of image')
                d.info('  flash_sos: flash sos image')
                d.info('  flash_uos: flash uos image')
                d.info('  flash_data: flash data image')
            elif cmd == 'cfg':
                d.info('url: {}'.format(self._url))

    def make_image(self, images):
        d.dbg('_make_image: get input {}'.format(images))
        for image in images.values():
            d.dbg('_make_image: make {}'.format(image))
            cmd = r'make {}'.format(image)
            subprocess.call(cmd, shell=True)

    def get_cmd_handlers(self, cmd=None):
        hdrs = {
            'make': self.make_image,
            'flash': self.make_image,
            'url': self.url_handler,
            'help': self.help,
        }
        if not cmd:
            return hdrs
        else:
            if cmd in hdrs:
                return hdrs[cmd]
            else:
                return None


if __name__ == '__main__':
    # d.set_debug_level('dbg,info,err')
    cwp = Cwp()
    cwp._cmdHdrs.run_sys_input()
