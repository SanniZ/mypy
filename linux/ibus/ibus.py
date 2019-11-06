#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 2018-12-05

@author: Byng Zeng
"""

import os

from pybase.pysys import print_help
from pybase.pyinput import get_input_args
from pybase.pydecorator import execute_shell


############################################################################
#              Const Vars
############################################################################

VERSION = '1.1.2'
AUTHOR = 'Byng Zeng'

IBUS_TABLES_DIR = '/usr/share/ibus-table/tables'
IBUS_ICONS_DIR = '/usr/share/ibus-table/icons'

WUBI_LOVE98_TXT = '%s/wubi-love98/wubi-love98.txt' % os.getenv('IBUS')
WUBI_LOVE98_DB = '%s/wubi-love98/wubi-love98.db' % os.getenv('IBUS')
IBUS_LOVE98_DB = "%s/wubi-love98.db" % (IBUS_TABLES_DIR)


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
        '  set sunpinyin',
        '-p',
        '  set pinyin',
        '-g',
        '  set googlepinyin',
        '-w',
        '  set wubi-love98',
        '-S',
        '  setup wubi-love98',
        '-a',
        '  add new keyword to wubi-love98.db',
        '-u',
        '  update wubi-love98.db',
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
        if os.path.exists(IBUS_LOVE98_DB):
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

    def ibus_setup(self):
        cmd = 'sudo cp wubi98.svg %s/wubi98.svg' % (IBUS_ICONS_DIR)
        process_shell_cmd(cmd)
        self.ibus_update_wubi_love98_db()

    def main(self):
        args = get_input_args('harLPpgSBbu', True)
        if not args:
            print_help(self.HELP_MENU)
            sys.exit()
        else:
            for k in args.keys():
                if k == '-a':
                    self.ibus_add_to_wubi_love98_db()
                elif k == '-u':
                    self.ibus_update_wubi_love98_db()
                elif k == '-r':
                    self.ibus_restart()
                elif k == '-L':
                    rescode, data = self.ibus_list_engine()
                    if rescode < 0:
                        print('error, failed to get engine list.')
                    else:
                        print(str(data, 'utf-8').strip('\n'))
                elif k == '-P':
                    self.ibus_set('sunpinyin')
                elif k == '-p':
                    self.ibus_set('pinyin')
                elif k == '-g':
                    self.ibus_set('googlepinyin')
                elif k == '-w':
                    self.ibus_set('wubi98')
                elif k == '-S':
                    self.ibus_setup()
                elif k == '-B':
                    self.ibus_set('wubi-haifeng86')
                elif k == '-b':
                    self.ibus_set('wubi-jingdian86')
                elif k == '-h':
                    print_help(self.HELP_MENU)
                    sys.exit()
                else:
                    print_help(self.HELP_MENU)
                    sys.exit()

############################################################################
#              run IBus instance
############################################################################

if __name__ == '__main__':
    ibus = IBus()
    ibus.main()
