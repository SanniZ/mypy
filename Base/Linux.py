# -*- coding: utf-8 -*-
"""
Created on Thu Jul  5 11:21:29 2018

@author: Byng.Zeng
"""

import commands

class Linux(object):
    def __init__(self):
        #print('Linux init done.')
        pass       
    
    def help(self, cmds=''):
        for cmd in cmds.values():
            if cmd == 'cfg':
                pass
            else:
                print('rm:[xxx,[xxx]]    remove xxx file')
    
    def get_cups(self):
        cmd = r'cat /proc/cpuinfo | grep "processor"| wc -l'
        return commands.getoutput(cmd)
   
    def delete(self, f):
        cmd = r'rm -rf %s' % f
        return commands.getoutput(cmd)
        
if __name__ == '__main__':
    linux = Linux()
    print linux.get_cups()