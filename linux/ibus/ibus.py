#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on 2018-12-05

@author: Byng Zeng
"""

import re
import os
import sys
import getopt
import subprocess
import shutil

from base import MyBase as Base

WUBI_LOVE98_TXT = '%s/linux/ibus/ibus-love98.txt' % Base.get_mypy_path()
WUBI_LOVE98_DB = '%s/linux/ibus/ibus-love98.db' % Base.get_mypy_path()
IBUS_LOVE98_DB = '/usr/share/ibus-table/tables/wubi-love98.db'

class IBus(object):

    @classmethod
    def print_help(cls):
        help_menu = (
            '==================================',
            '    IBus command set',
            '==================================',
            '-r',
            '  restart',
            '-L',
            '  list engine',
            '-P',
            '  setup sunpinyin',
            '-p',
            '  setup pinyin',
            '-g',
            '  setup googlepinyin',
            '-S',
            '  setup wubi98',
            '-B',
            '  setup wubi-haifeng86',
            '-b',
            '  setup wubi-jidian86',
            '-a',
            '  add to database of wubi-love98.db',
            '-u',
            '  update database of wubi-love98.db',
        )
        # print
        for txt in help_menu:
            print(txt)
        Base.print_exit()

    def ibus_restart(self):
        cmd = 'ibus_restart'
        subprocess.call(cmd, shell=True)

    def ibus_list_engine(self):
        cmd = 'ibus list-engine'
        subprocess.call(cmd, shell=True)

    def ibus_set(self, engine):
        cmd = 'ibus_setup %s' % engine
        subprocess.call(cmd, shell=True)

    def ibus_add_to_wubi_love98_db(self):
        wd = raw_input('请输入词组：')
        code = raw_input('请输入编码：')
        # get list of txt
        with open(WUBI_LOVE98_TXT, 'r') as f:
            txt = f.readlines()
        # add wd to txt
        wd_code = '%s	%s	1\n' % (code, wd)
        txt.insert(len(txt) - 1, wd_code)
        # update txt
        with open(WUBI_LOVE98_TXT, 'w') as f:
            f.writelines(txt)

    def ibus_update_wubi_love98_db(self):
        print('update ibus wubi_love98_db...')
        # make temlate love98.db
        cmd = 'ibus-table-createdb -s %s -n %s' % (WUBI_LOVE98_TXT, WUBI_LOVE98_DB)
        subprocess.call(cmd, shell=True)
        # backup ibus love98.db
        cmd = 'sudo mv %s %s' % (IBUS_LOVE98_DB, '%s.bak' % IBUS_LOVE98_DB)
        subprocess.call(cmd, shell=True)
        # copy love98.db to ibus.
        cmd = 'sudo mv %s %s' % (WUBI_LOVE98_DB, IBUS_LOVE98_DB)
        subprocess.call(cmd, shell=True)
        # remove love98.db.bak.
        cmd = 'sudo rm -f %s' % ('%s.bak' % IBUS_LOVE98_DB)
        subprocess.call(cmd, shell=True)
        # restart ibus
        cmd = 'killall ibus-daemon && ibus-daemon -d'
        subprocess.call(cmd, shell=True)

    def main(self):
        args = Base.get_user_input('harLPpgSBbu')
        if '-h' in args:
            self.print_help()
        if '-a' in args:
            self.ibus_add_to_wubi_love98_db()
        if '-r' in args:
            self.ibus_restart()
        if '-L' in args:
            self.ibus_list_engine()
        if '-P' in args:
            self.ibus_set('sunpinyin')
        if '-p' in args:
            self.ibus_set('pinyin')
        if '-g' in args:
            self.ibus_set('googlepinyin')
        if '-S' in args:
            self.ibus_set('wubi98')
        if '-B' in args:
            self.ibus_set('wubi-haifeng86')
        if '-b' in args:
            self.ibus_set('wubi-jingdian86')
        if '-u' in args:
            self.ibus_update_wubi_love98_db()

if __name__ == '__main__':
    ibus = IBus()
    ibus.main()
