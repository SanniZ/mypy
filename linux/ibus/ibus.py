#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 2018-12-05

@author: Byng Zeng
"""

import os

from pybase.pysys import print_help
from pybase.pyinput import get_user_input
from pybase.pydecorator import execute_shell


############################################################################
#              Const Vars
############################################################################

VERSION = '1.1.1'
AUTHOR = 'Byng.Zeng'


WUBI_LOVE98_TXT = '%s/wubi-love98/wubi-love98.txt' % os.getenv('IBus')
WUBI_LOVE98_DB = '%s/wubi-love98/wubi-love98.db' % os.getenv('IBus')
IBUS_LOVE98_DB = '/usr/share/ibus-table/tables/wubi-love98.db'


############################################################################
#              Functions
############################################################################

@execute_shell
def ibus_restart():
    return 'ibus_restart'


@execute_shell
def ibus_list_engine():
    return 'ibus list-engine'


@execute_shell
def ibus_set(engine):
    return 'ibus_setup %s' % engine


@execute_shell
def process_shell_cmd(cmd):
    return cmd


############################################################################
#              IBus class
############################################################################

class IBus(object):

    HELP_MENU = (
        '==================================',
        '    IBus - %s' % VERSION,
        '',
        '    @Author: %s' % AUTHOR,
        '    Copyright (c) %s studio' % AUTHOR,
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
        '  add to dataBase of wubi-love98.db',
        '-u',
        '  update dataBase of wubi-love98.db',
    )

    def ibus_restart(self):
        return ibus_restart()

    def ibus_list_engine(self):
        return ibus_list_engine()

    def ibus_set(self, engine):
        return ibus_set(engine)

    def ibus_add_to_wubi_love98_db(self):
        wd = input('请输入词组：')
        code = input('请输入编码：')
        # get list of txt
        with open(WUBI_LOVE98_TXT, 'r') as fd:
            txt = fd.readlines()
        # add wd to txt
        wd_code = '%s	%s	1\n' % (code, wd)
        txt.insert(len(txt) - 1, wd_code)
        # update txt
        with open(WUBI_LOVE98_TXT, 'w') as fd:
            fd.writelines(txt)

    def ibus_update_wubi_love98_db(self):
        print('update ibus wubi_love98_db...')
        # make temlate love98.db
        cmd = \
            'ibus-table-createdb -s %s -n %s' % \
            (WUBI_LOVE98_TXT, WUBI_LOVE98_DB)
        process_shell_cmd(cmd)
        # backup ibus love98.db
        cmd = 'sudo mv %s %s' % (IBUS_LOVE98_DB, '%s.bak' % IBUS_LOVE98_DB)
        process_shell_cmd(cmd)
        # copy love98.db to ibus.
        cmd = 'sudo mv %s %s' % (WUBI_LOVE98_DB, IBUS_LOVE98_DB)
        process_shell_cmd(cmd)
        # remove love98.db.bak.
        cmd = 'sudo rm -f %s' % ('%s.bak' % IBUS_LOVE98_DB)
        process_shell_cmd(cmd)
        # restart ibus
        cmd = 'killall ibus-daemon && ibus-daemon -d'
        process_shell_cmd(cmd)

    def main(self):
        args = get_user_input('harLPpgSBbu')
        if '-h' in args:
            print_help(self.HELP_MENU)
        if '-a' in args:
            self.ibus_add_to_wubi_love98_db()
        if '-u' in args:
            self.ibus_update_wubi_love98_db()
        if '-r' in args:
            self.ibus_restart()
        if '-L' in args:
            rescode, data = self.ibus_list_engine()
            if rescode < 0:
                print('error, failed to get engine list.')
            else:
                print(str(data, 'utf-8').strip('\n'))
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


############################################################################
#              run IBus instance
############################################################################

if __name__ == '__main__':
    ibus = IBus()
    ibus.main()
