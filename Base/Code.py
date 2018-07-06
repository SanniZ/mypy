# -*- coding: utf-8 -*-
"""
Created on Thu Jul  5 11:25:54 2018

@author: Byng.Zeng
"""

import subprocess
from Linux import Linux
from Debug import Debug


class Code(Debug):
    def __init__(self, url=''):
        super(Code, self).__init__()
        self._url = url
        self.dbg('Code init set url={}'.format(url))
        
    def help(self, cmds=''):
        self.dbg('Class Code help.')
        super(Code, self).help(cmds)
        for cmd in cmds.values():
            if cmd == 'help':
                self.info('url:[init][,sync]')
                self.info('  init: repo init source code')
                self.info('  sync: repo sync source code')
            elif cmd == 'cfg':
                self.info('url: {}'.format(self._url))

    def code_init(self):
        cmd = r'repo init -u %s' % self._url
        self.info(cmd)
        subprocess.call(cmd, shell=True)

    def code_sync(self):
        linux = Linux()
        cpus = linux.get_cpus()
        if cpus > 5:
            cpus = 5
        
        cmd = r'repo sync -j{num}'.format(num=cpus)
        self.info(cmd)
        subprocess.call(cmd, shell=True)
        
    def code_handler(self, cmds=''):
        self.dbg('code_handler: %s' % cmds)
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


if __name__ == '__main__':
    code = Code()
    code.handler()