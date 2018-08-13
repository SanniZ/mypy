#!/usr/bin/python

# -*- coding: utf-8 -*-
"""
Created on Thu Jul  5 11:17:08 2018

@author: Byng.Zeng
"""

from debug import Debug as d
from input import Input

class CmdProcessing(object):
    def __init__(self):
        self._cmds_list = {}

    def register_cmd_handler(self, handlers):
        if handlers != None and type(handlers) == dict:
            for key in handlers.keys():
                if self._cmds_list.has_key(key):
                    hdrs = list()
                    if type(self._cmds_list[key]) == list:
                        for hdr in self._cmds_list[key]:
                            hdrs.append(hdr)
                    hdrs.append(handlers[key])
                    self._cmds_list[key] = hdrs
                else:
                    self._cmds_list[key] = handlers[key]

    # run input commands
    def run(self, cmds):
        d.dbg('CmdProcessing.run(): %s' % cmds)
        for key in cmds.iterkeys():
            # check help.
            if key == 'help':
                for sub_cmd in cmds[key]:
                    if sub_cmd != 'cfg': # no show while cfg.
                        d.info('help:[help][,cfg]')
                        d.info('  help: show help')
                        d.info('  cfg : show config info')

            if self._cmds_list.has_key(key) == True:
                d.dbg(self._cmds_list[key])
                if type(self._cmds_list[key]) == dict:
                    sub_cmds = self._cmds_list[key]
                    for sub_key in sub_cmds.iterkeys():
                        f = sub_cmds[sub_key]
                        d.dbg(f(cmds[key]))
                else:
                    t = type(self._cmds_list[key])
                    if t == list:
                        for f in self._cmds_list[key]:
                            d.dbg(f(cmds[key]))
                    else:
                        f = self._cmds_list[key]
                        d.dbg(f(cmds[key]))
            else:
                d.err('No handler for: %s' % key)

    # run sys input commands
    def run_sys_input(self):
        self.run(Input().get_input())