#!/usr/bin/python

# -*- coding: utf-8 -*-
"""
Created on Thu Jul  5 11:25:54 2018

@author: Byng.Zeng
"""

import subprocess
from linux import HwInfo
from debug import Debug as d

class Code(object):
    def __init__(self, url):
        self._url = url

        self._cmd_handlers = {
            'url' : self.url_handler,
        }
        d.dbg('Code init set url={}'.format(url))

    def help(self, cmds=''):
        for cmd in cmds.values():
            if cmd == 'help':
                d.info('url:[init][,sync]')
                d.info('  init: repo init source code')
                d.info('  sync: repo sync source code')
            elif cmd == 'cfg':
                d.info('url: {}'.format(self._url))

    def code_init(self):
        cmd = r'repo init -u %s' % self._url
        d.info(cmd)
        subprocess.call(cmd, shell=True)

    def code_sync(self):
        hw = HwInfo()
        cpus = hw.get_cups()
        if int(cpus) > 5:
            cpus = 5

        cmd = r'repo sync -j{}'.format(cpus)
        d.info(cmd)
        subprocess.call(cmd, shell=True)

    def url_handler(self, cmds):
        d.dbg('url_handler: %s' % cmds)
        t = type(cmds)
        if t == dict:
            for cmd in cmds.values():
                if cmd == 'init':
                    self.code_init()
                elif cmd == 'sync':
                    self.code_sync()
        elif t == list:
            for i in range(cmds):
                if cmds[i] == 'init':
                    self.code_init()
                elif cmds[i] == 'sync':
                    self.code_sync()
        elif t == str:
            if cmds == 'init':
                self.code_init()
            elif cmds == 'sync':
                self.code_sync()

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

    code = Code(r'ssh://android.intel.com/h/hypervisor/manifests -b hypervisor/master')
    cmds_list['url'] = code.get_handler('url')

    cmdHdr = CmdProcessing()
    for key in cmds_list.iterkeys():
        cmdHdr.register_cmd_handler(key, cmds_list[key])

    inp = Input()
    input_dict = inp.get_input()
    cmdHdr.run(input_dict)