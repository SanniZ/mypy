#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul  5 11:25:54 2018

@author: Byng.Zeng
"""

import subprocess
from linux.linux import HwInfo
from develop.debug import Debug as d


class RepoHelper(object):
    def __init__(self, url):
        self._url = url
        d.dbg('RepoHelper init set url={}'.format(url))

    def help(self, cmds):
        for cmd in cmds:
            if cmd == 'help':
                d.info('repo:[init][,sync|fsync]')
                d.info('  init : repo init source code')
                d.info('  sync : repo sync source code')
                d.info('  fsync: repo sync source code with -f')
            elif cmd == 'cfg':
                d.info('url: {}'.format(self._url))

    def repo_init(self):
        cmd = r'repo init -u %s' % self._url
        d.info(cmd)
        subprocess.call(cmd, shell=True)

    def repo_sync(self, force=False):
        hw = HwInfo()
        cpus = hw.get_cups()
        if int(cpus) > 5:
            cpus = 5

        if force:
            cmd = r'repo sync -c -j{n} -f'.format(n=cpus)
        else:
            cmd = r'repo sync -c -j{n}'.format(n=cpus)
        d.info(cmd)
        subprocess.call(cmd, shell=True)

    def url_handler(self, cmds):
        d.dbg('url_handler: %s' % cmds)

        for cmd in cmds:
            if cmd == 'init':
                self.repo_init()
            elif cmd == 'sync':
                self.repo_sync()
            elif cmd == 'fsync':
                self.repo_sync(True)

    def get_cmd_handlers(self, cmd=None):
        hdrs = {
            'help': self.help,
            'repo': self.url_handler,
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
    helper = RepoHelper(
        r'ssh://android.intel.com/h/hypervisor/manifests -b hypervisor/master')

    from cmdprocess.cmdprocessing import CmdProcessing
    cmdHdr = CmdProcessing()
    cmdHdr.register_cmd_handler(helper.get_cmd_handlers())
    cmdHdr.run_sys_input()
