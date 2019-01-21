#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 13 09:51:42 2018

@author: Byng.Zeng
"""


from cmdprocessing import CmdProcessing
from android import Android
from linux import HwInfo, FileOps


class Tools(object):
    def __init__(self):
        self._cmd_prc = CmdProcessing()

    def register_cmd_handlers(self):
        self._cmd_prc.register_cmd_handler(Android().get_cmd_handlers())
        self._cmd_prc.register_cmd_handler(HwInfo().get_cmd_handlers())
        self._cmd_prc.register_cmd_handler(FileOps().get_cmd_handlers())

    def main(self):
        self.register_cmd_handlers()
        self._cmd_prc.run_sys_input()

if __name__ == '__main__':
    ts = Tools()
    ts.main()
