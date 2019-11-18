#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 2018-12-26

@author: Byng Zeng
"""
import inspect


############################################################################
#               Const Vars
############################################################################

VERSION = '1.1.0'

PR_LVL_DBG = 0x01
PR_LVL_INFO = 0x02
PR_LVL_WARN = 0x04
PR_LVL_ERR = 0x08
PR_LVL_ALL = PR_LVL_DBG | PR_LVL_INFO | PR_LVL_WARN | PR_LVL_ERR

PR_LVL_DEFAULT = PR_LVL_INFO | PR_LVL_WARN | PR_LVL_ERR


############################################################################
#               PyPrint class
############################################################################

class PyPrint(object):

    def __init__(self, tag=None, lvl=PR_LVL_DEFAULT, funcname=False):
        self._tag = tag
        self._lvl = lvl
        self._funcname = funcname

    @property
    def tag(self):
        return self._tag

    @property
    def level(self):
        return self._lvl

    @level.setter
    def level(self, lvl):
        self._lvl = lvl
        return self._lvl

    @property
    def config(self):
        return self._tag, self._lvl, self._funcname

    # decorator pr_fmt
    def __pr_msg(func):
        def fmt_pr_warpper(*args, **kwargs):
            pr = args[0]
            if func(*args, **kwargs):
                msg = ''
                if pr._tag:
                    msg += '[%s]' % pr._tag
                if pr._funcname:
                    msg += ' %s()' % inspect.stack()[1][3] \
                        if msg else '%s()' % inspect.stack()[1][3]
                msg += ': ' if msg else ''
                for m in args[1:]:
                    if m:
                        msg += \
                            ''.join(str(m)) if isinstance(m, dict) else ''.join(m)
                print(msg)
        return fmt_pr_warpper

    @__pr_msg
    def pr_dbg(self, *msg):
        return self._lvl & PR_LVL_DBG

    @__pr_msg
    def pr_info(self, *msg):
        return self._lvl & PR_LVL_INFO

    @__pr_msg
    def pr_warn(self, *msg):
        return self._lvl & PR_LVL_WARN

    @__pr_msg
    def pr_err(self, *msg):
        return self._lvl & PR_LVL_ERR

    def get_config(self):
        return self._tag, self._lvl, self._funcname

    def set_level(self, lvl):
        self._lvl = lvl

    def get_level(self):
        return self._lvl

    def add_level(self, lvl):
        self._lvl = self._lvl | lvl

    def clear_level(self, lvl):
        self._lvl = self._lvl & ~lvl

    def set_funcname(self, funcname=True):
        self._funcname = funcname

    def get_funcname(self):
        return self._funcname
