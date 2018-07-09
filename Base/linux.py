#!/usr/bin/python

# -*- coding: utf-8 -*-
"""
Created on Thu Jul  5 11:21:29 2018

@author: Byng.Zeng
"""

import commands
from debug import Debug as d

class HwInfo(object):
    def __init__(self):
        self._cmd_handlers = {
            'help' : self.help,
            'hwinfo' : self.get_cups,
        }

    def help(self, cmds=''):
        for cmd in cmds.values():
            if cmd == 'help':
                d.info('hwinfo:[ncpu]')
                d.info('  ncpu: get number of CPU')

    def get_cups(self, cmds=None):
        cmd = r'cat /proc/cpuinfo | grep "processor"| wc -l'
        d.dbg(cmd)
        return commands.getoutput(cmd)

    def hwinfo_handler(self, cmds):
        for cmd in cmds.values():
            if cmd == 'ncpu':
                d.info(self.get_cups())

    def get_handler(self, cmd):
        if cmd == 'all':
            return self._cmd_handlers
        elif self._cmd_handlers.has_key(cmd) == True:
            return self._cmd_handlers[cmd]
        else:
            return None

class FileOps(object):
    def __init__(self):
        self._cmd_handlers = {
            'help' : self.help,
            'del'  : self.del_handler,
            'fdel' : self.fdel_handler,
        }

    def help(self, cmds=''):
        for cmd in cmds.values():
            if cmd == 'help':
                d.info('del:[xxx][,xxx]')
                d.info('  xxx: xxx file will be delete.')
                d.info('fdel:path,file')
                d.info('  path: which path to find.')
                d.info('  file: which file be delete.')

    def delete(self, f):
        cmd = r'rm -rf %s' % f
        d.info(cmd)
        return commands.getoutput(cmd)

    def del_handler(self, cmds=''):
        for cmd in cmds.values():
            self.delete(cmd)

    def find_delete(self, path, name):
        cmd = r'find %s -name %s | xargs rm -rf {}\;' % (path, name)
        d.info(cmd)
        return commands.getoutput(cmd)

    def fdel_handler(self, cmds=''):
        d.dbg('fdel_handler: {}'.format(cmds))
        try:
            self.find_delete(cmds[0], cmds[1])
        except KeyError as e:
            d.err('Error: %s' % e)

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

    hw = HwInfo()
    cmds_list['help'] = hw.get_handler('help')
    cmds_list['hwinfo'] = hw.get_handler('hwinfo')

    fops = FileOps()
    cmds_list['help'] = fops.get_handler('help')
    cmds_list['del'] = fops.get_handler('del')
    cmds_list['fdel'] = fops.get_handler('fdel')

    cmdHdr = CmdProcessing()
    for key in cmds_list.iterkeys():
        cmdHdr.register_cmd_handler(key, cmds_list[key])

    inp = Input()
    input_dict = inp.get_input()
    cmdHdr.run(input_dict)