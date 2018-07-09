#!/usr/bin/python

# -*- coding: utf-8 -*-
"""
Created on Thu Jul  5 15:18:47 2018

@author: Byng.Zeng
"""

import subprocess

from code import Code
from debug import Debug as d

class Cwp(Code):
    URL = r'ssh://android.intel.com/h/hypervisor/manifests -b hypervisor/master'

    def __init__(self,url):
        super(Cwp, self).__init__(url)
        self._url = url
        self._cmd_handlers = {
            'make': self.make_image,
            'flash' : self.make_image,
            'url' : self.url_handler,
            'help' : self.help,
        }
        #self.set_debug_level('dbg,info,err')
        d.dbg('Cwp init done!')

    def help(self, cmds):
        super(Cwp, self).help(cmds)
        for cmd in cmds.values():
            if cmd == 'help':
                d.info('make:[option][,option]')
                d.info('option:')
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
            cmd=r'make {}'.format(image)
            subprocess.call(cmd, shell=True)

    def get_handler(self, cmd):
        if self._cmd_handlers.has_key(cmd) == True:
            return self._cmd_handlers[cmd]
        else:
            return None

if __name__ == '__main__':
    from input import Input
    from cmdprocessing import CmdProcessing

    #d.set_debug_level('dbg,info,err')
    cmds_list = {} 

    cwp = Cwp(Cwp.URL)
    cmds_list['help'] = cwp.get_handler('help')    
    cmds_list['url'] = cwp.get_handler('url')
    cmds_list['make'] = cwp.get_handler('make')
    cmds_list['flash'] = cwp.get_handler('flash')

    cmdHdr = CmdProcessing()
    for key in cmds_list.iterkeys():
        cmdHdr.register_cmd_handler(key, cmds_list[key])

    inp = Input()
    input_dict = inp.get_input()
    cmdHdr.run(input_dict)