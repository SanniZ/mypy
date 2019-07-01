#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 13 09:51:42 2018

@author: Byng.Zeng
"""

from develop.android.android import Android
from linux.linux import HwInfo, FileOps
from pyprocess import PyCmdProcess


VERSION='1.0.0'


class PyApp(object):
    def __init__(self):
        self._cmdproc = PyCmdProcess()

    def register_cmd_handlers(self):
        self._cmdproc.register_cmd_handler(Android().get_cmd_handlers())
        self._cmdproc.register_cmd_handler(HwInfo().get_cmd_handlers())
        self._cmdproc.register_cmd_handler(FileOps().get_cmd_handlers())

    def main(self):
        self.register_cmd_handlers()
        self._cmdproc.run_sys_input()

if __name__ == '__main__':
    app = PyApp()
    app.main()
