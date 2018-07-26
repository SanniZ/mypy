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
        d.dbg('Code init set url={}'.format(url))

    def help(self, cmds):
        for cmd in cmds:
            if cmd == 'help':
                d.info('url:[init][,sync]')
                d.info('  init: repo init source code')
                d.info('  sync: repo sync source code')
            elif cmd == 'cfg':
                d.info('url: {}'.format(self._url))

    def url_init(self):
        cmd = r'repo init -u %s' % self._url
        d.info(cmd)
        subprocess.call(cmd, shell=True)

    def url_sync(self):
        hw = HwInfo()
        cpus = hw.get_cups()
        if int(cpus) > 5:
            cpus = 5

        cmd = r'repo sync -j{n}'.format(n=cpus)
        d.info(cmd)
        subprocess.call(cmd, shell=True)

    def url_handler(self, cmds):
        d.dbg('url_handler: %s' % cmds)

        for cmd in cmds:
            if  cmd == 'init':
                self.url_init()
            elif  cmd == 'sync':
                self.url_sync()

    def code_get_cmd_handlers(self, cmd=None):
        hdrs = {
            'url' : self.url_handler,
        }
        if cmd == None:
            return hdrs
        else:
            if hdrs.has_key(cmd) == True:
                return hdrs[cmd]
            else:
                return None

if __name__ == '__main__':
    from cmdprocessing import CmdProcessing

    #d.set_debug_level('dbg,info,err')
    code = Code(r'ssh://android.intel.com/h/hypervisor/manifests -b hypervisor/master')
    cmdHdr = CmdProcessing()
    cmdHdr.register_cmd_handler(code.code_get_cmd_handlers())
    cmdHdr.run_sys_input()