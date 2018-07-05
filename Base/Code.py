# -*- coding: utf-8 -*-
"""
Created on Thu Jul  5 11:25:54 2018

@author: Byng.Zeng
"""

import subprocess
from Linux import Linux

class Code(object):
    def __init__(self, url=''):
        #print('Code init url={}'.format(url))
        self._url = url

    def help(self, cmds=''):
        #print('Class Code help.')
        for cmd in cmds.values():
            if cmd == 'cfg':
                print('url: {}'.format(self._url))
            else:
                print('url:init/sync    init or sync code')

    def code_init(self):
        cmd = r'repo init -u %s' % self._url
        print(cmd)
        subprocess.call(cmd, shell=True)

    def code_sync(self):
        linux = Linux()
        cpus = linux.get_cpus()
        if cpus > 5:
            cpus = 5
        
        cmd = r'repo sync -j{num}'.format(num=cpus)
        print(cmd)
        subprocess.call(cmd, shell=True)
        
    def code_handler(self, cmds=''):
        t = type(cmds)
        if t == dict:
            for cmd in cmds.values():
                if cmd == 'init':
                    self.init()
                elif cmd == 'sync':
                    self.sync()
        elif t == list:
            for i in range(cmds):
                if cmds[i] == 'init':
                    self.init()
                elif cmds[i] == 'sync':
                    self.sync()
        elif t == str:
            if cmds == 'init':
                self.init()
            elif cmds == 'sync':
                self.sync()


if __name__ == '__main__':
    code = Code()
    code.handler()