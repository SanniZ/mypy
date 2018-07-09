#!/usr/bin/python

# -*- coding: utf-8 -*-
"""
Created on Thu Jul  5 11:17:08 2018

@author: Byng.Zeng
"""

from debug import Debug as d

class CmdProcessing(object):
    def __init__(self):
        self._cmds_list = {}

    def register_cmd_handler(self, cmd, handler):
        d.dbg('register: {}'.format(cmd, handler))
        self._cmds_list[cmd] = handler

    def run(self, cmds):
        d.dbg('CmdProcessing.run(): %s' % cmds)
        for key in cmds.iterkeys():
            if key == 'help':
                d.info('help:[help][,cfg]')
                d.info('  help: show help')
                d.info('  cfg : show config info')

            if self._cmds_list.has_key(key) == True:
                f = self._cmds_list[key]
                return f(cmds[key])
            else:
                d.err('No handler for: %s' % key)


if __name__ == '__main__':
    from input import Input
    from linux import HwInfo

    #d.set_debug_level('dbg,info,err')
    cmds_list = {} 

    hw = HwInfo()
    cmds_list['hwinfo'] = hw.get_handler('hwinfo')

    cmdHdr = CmdProcessing()
    for key in cmds_list.iterkeys():
        cmdHdr.register_cmd_handler(key, cmds_list[key])

    inp = Input()
    input_dict = inp.get_input()
    cmdHdr.run(input_dict)