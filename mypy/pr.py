#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Created on 2018-12-26

@author: Byng Zeng
"""


class Print(object):

    PR_LVL_DBG = 0x01
    PR_LVL_WARN = 0x02
    PR_LVL_INFO = 0x04
    PR_LVL_ERR = 0x08
    PR_LVL_ALL = 0x0F

    def __init__(self, tag=None, lvl=0x04 | 0x08):
        self._tag = tag
        self._pr_lvl = lvl

    def pr_dbg(self, fmt):
        if all((self._pr_lvl & self.PR_LVL_DBG, fmt)):
            if self._tag:
                print('[%s] %s' % (self._tag, fmt))
            else:
                print('%s' % (fmt))

    def pr_info(self, fmt):
        if all((self._pr_lvl & self.PR_LVL_INFO, fmt)):
            if self._tag:
                print('[%s] %s' % (self._tag, fmt))
            else:
                print('%s' % (fmt))

    def pr_warn(self, fmt):
        if all((self._pr_lvl & self.PR_LVL_WARN, fmt)):
            if self._tag:
                print('[%s] %s' % (self._tag, fmt))
            else:
                print('%s' % (fmt))

    def pr_err(self, fmt):
        if all((self._pr_lvl & self.PR_LVL_ERR, fmt)):
            if self._tag:
                print('[%s] %s' % (self._tag, fmt))
            else:
                print('%s' % (fmt))

    def set_pr_level(self, val):
        self._pr_lvl = val

    def get_pr_level(self):
        return self._pr_lvl
