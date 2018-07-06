# -*- coding: utf-8 -*-
"""
Created on Thu Jul  5 11:21:29 2018

@author: Byng.Zeng
"""

import commands
from Debug import Debug

class Linux(Debug):
    def __init__(self):
        super(Linux, self).__init__()
        self.dbg('Linux init done!')     
    
    def help(self, cmds=''):
        self.dbg('Linux help.')
    
    def get_cups(self):
        cmd = r'cat /proc/cpuinfo | grep "processor"| wc -l'
        self.dbg(cmd)
        return commands.getoutput(cmd)


    def pc_handlers(self, cmds=''):
        self.dbg('pc_handlers: {}'.format(cmds))
        for cmd in cmds.values():
            if cmd == 'cpu':
                self.info(self.get_cups())
   
    def delete(self, f):
        cmd = r'rm -rf %s' % f
        self.info(cmd)
        return commands.getoutput(cmd)
        
    def find_delete(self, path, name):
        cmd = r'find %s -name %s | xargs rm -rf {}\;' % (path, name)
        self.info(cmd)
        return commands.getoutput(cmd)

    def del_handlers(self, cmds=''):
        for cmd in cmds.values():
            self.delete(cmd)

    def fdel_handlers(self, cmds=''):
        self.dbg('fdel_handler: {}'.format(cmds))
        self.find_delete(cmds[0], cmds[1])

if __name__ == '__main__':
    linux = Linux()
    linux.info(linux.get_cups())