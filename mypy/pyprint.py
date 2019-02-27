#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 2018-12-26

@author: Byng Zeng
"""


class PyPrint(object):

    PR_LVL_DBG = 0x01
    PR_LVL_INFO = 0x02
    PR_LVL_WARN = 0x04
    PR_LVL_ERR = 0x08
    PR_LVL_ALL = 0x0F

    def __init__(self, tag=None, lvl=0x02 | 0x04 | 0x08):
        self._tag = tag
        self._pr_lvl = lvl

    # decorator pr_fmt
    def __pr_msg(func):
        def fmt_pr_warpper(*args, **kwargs):
            pr = args[0]
            if func(*args, **kwargs):
                msg = ''.join(args[1:])
                if pr._tag:
                    print('[%s] %s' % (pr._tag, msg))
                else:
                    print('%s' % (msg))
        return fmt_pr_warpper

    @__pr_msg
    def pr_dbg(self, *msg):
        return self._pr_lvl & self.PR_LVL_DBG

    @__pr_msg
    def pr_info(self, *msg):
        return self._pr_lvl & self.PR_LVL_INFO

    @__pr_msg
    def pr_warn(self, *msg):
        return self._pr_lvl & self.PR_LVL_WARN

    @__pr_msg
    def pr_err(self, *msg):
        return self._pr_lvl & self.PR_LVL_ERR

    def set_pr_level(self, val):
        self._pr_lvl = val

    def get_pr_level(self):
        return self._pr_lvl
