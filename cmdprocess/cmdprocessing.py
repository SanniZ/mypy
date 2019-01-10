# -*- coding: utf-8 -*-
"""
Created on Thu Jul  5 11:17:08 2018

@author: Byng.Zeng
"""

from debug import Debug as d
from input import Input

class CmdProcessing(object):
    def __init__(self):
        self._cmd_dict = dict()

    def register_cmd_handler(self, handlers):
        if handlers != None and type(handlers) == dict:
            for key in handlers.keys():
                if key in self._cmd_dict:
                    hdrs = list()
                    if type(self._cmd_dict[key]) == list:
                        for hdr in self._cmd_dict[key]:
                            hdrs.append(hdr)
                    hdrs.append(handlers[key])
                    self._cmd_dict[key] = hdrs
                else:
                    self._cmd_dict[key] = handlers[key]

    # run input commands
    def run(self, cmds):
        d.dbg('CmdProcessing.run(): %s' % cmds)
        for key in cmds.keys():
            # check help.
            if key == 'help':
                for sub_cmd in cmds[key]:
                    if sub_cmd != 'cfg': # no show while cfg.
                        d.info('help:[help][,cfg]')
                        d.info('  help: show help')
                        d.info('  cfg : show config info')

            if key in self._cmd_dict:
                d.dbg(self._cmd_dict[key])
                if type(self._cmd_dict[key]) == dict:
                    sub_cmds = self._cmd_dict[key]
                    for sub_key in sub_cmds.iterkeys():
                        f = sub_cmds[sub_key]
                        d.dbg(f(cmds[key]))
                else:
                    t = type(self._cmd_dict[key])
                    if t == list:
                        for f in self._cmd_dict[key]:
                            d.dbg(f(cmds[key]))
                    else:
                        f = self._cmd_dict[key]
                        d.dbg(f(cmds[key]))
            else:
                d.err('No handler for: %s' % key)

    # run sys input commands
    def run_sys_input(self):
        self.run(Input().get_input())
