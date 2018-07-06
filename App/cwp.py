#!/usr/bin/python

# -*- coding: utf-8 -*-
"""
Created on Thu Jul  5 15:18:47 2018

@author: Byng.Zeng
"""

import subprocess

from CmdHandler import CmdHandler

class Cwp(CmdHandler):
    url = r'ssh://android.intel.com/h/hypervisor/manifests -b hypervisor/master'

    def __init__(self,url):
        super(Cwp, self).__init__()
        self._url = url
        self.support_cmd_list['make'] = None
        #self.set_debug_level('dbg,info,err')
        self.dbg('Cwp init done!')

    def help(self, cmds=''):
        super(Cwp, self).help(cmds)
        for cmd in cmds.values():
            if cmd == 'help':
                self.info('make:[all][,sos][,sos_dm][sos_kernel][,uos][,uos_kernel][,flash][,flash_sos][,flash_uos][,flash_data]')
                self.info('  all: make all of images')
                self.info('  sos: make sos image')
                self.info('  sos_dm: make sos_dm image')
                self.info('  sos_kernel: make sos_kernel image')
                self.info('  uos: make uos image')
                self.info('  uos_kernel: make uos_kernel image')
                self.info('  flash: flash all of image')
                self.info('  flash_sos: flash sos image')
                self.info('  flash_uos: flash uos image')
                self.info('  flash_data: flash data image')
            elif cmd == 'cfg':
                self.info('url: {}'.format(self._url))

    def make_image(self, images):
        self.dbg('_make_image: get input {}'.format(images))
        for image in images.values():
            self.dbg('_make_image: make {}'.format(image))
            cmd=r'make {}'.format(image)
            subprocess.call(cmd, shell=True)

    def config_handler(self, cmds):
        super(Cwp, self).config_handler(cmds)
        for key in cmds.iterkeys():
            if key == 'make':
                self.support_cmd_list['make'] = self.make_image

if __name__ == '__main__':
    cwp = Cwp(Cwp.url)
    cwp.main()