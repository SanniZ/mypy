#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 2019-07-25

@author: Byng.Zeng
"""

import os
import sys
import subprocess
import shutil

from collections import OrderedDict


VERSION = '1.0.2'


# default home of zephyr
ZEPHYR_HOME = os.path.join(os.getenv('HOME'), "workspace/zephyr/master")


# usage help
#
def usage_help():
    USAGE = (
        "---------------------------------------------",
        "    Zephyr Tools  - %s" % VERSION,
        "---------------------------------------------",
        "",
        "  usage: zephyr options",
        "",
        "options:",
        "  -b | build  name,[path]:",
        "    build application of zephyr.",
        "  -r | run  name:",
        "    run application of zephyr.",
        "  -h | home  path",
        "    set path of zephyr.",
    )
    for help in USAGE:
        print(help)
    sys.exit()


# build name of application.
#
# set default src to samples/ if src=None.
def build(args):
    def build_help():
        HELPS = (
            '',
            '  usage: zephyr build name [src] [board] [home]',
            '',
            'name or name=xxx:',
            '  name of application to build',
            'src or src=xxx',
            '  path of src of application.',
            'board or board=xxx',
            '  board platform to build, default qemu_x86',
            'home or home=xxx',
            '  path of project',
        )
        for help in HELPS:
            print(help)
        sys.exit()

    home = ZEPHYR_HOME
    name = src = None
    board = 'qemu_x86'

    if not args:
        print("Error, no found build args!")
        return 0
    # update home.
    if 'home' in args:
        home = args['home']
    # build args.
    if 'args' in args:
        for val in args['args']:
            cv = val.split('=')
            if len(cv) > 1:
                if cv[0] == 'name':
                    name = cv[1]
                elif cv[0] == 'src':
                    src = cv[1]
                elif cv[0] == 'board':
                    board = cv[1]
                elif cv[0] == 'help':
                    build_help()
                else:
                    print('Error, unknown %s to build' % cv[0])
                    sys.exit()
            else:
                if val in ['-h', 'help', '--help']:
                    build_help()
                if not name:
                    name = val
                elif not src:
                    src = val
                elif not board:
                    board = val

    if name:
        if not src:  # set default src to samples.
            src = os.path.join('samples', name)
        # check source code.
        if not os.path.exists(os.path.join(home, src)):
            print('No found source code of %s' % name)
            return -1
        # remove old out
        out = os.path.join('out', name)
        if os.path.exists(os.path.join(home, out)):
            shutil.rmtree(os.path.join(home, out))
        # get cmake
        cmake = os.path.join(os.getenv('CMAKE'), 'cmake')
        # run shell command to make target.
        cmd = "cd {home} && source zephyr-env.sh " \
              "&& {cmake} -B {out} -DBOARD={board} {src} 2>&1 " \
              "| tee build.log".format(home=home,
                                       cmake=cmake,
                                       out=out,
                                       board=board,
                                       src=src)
        subprocess.call(cmd, shell=True, executable="/bin/bash")
    return 0


# run name of application
#
def run(args):
    def run_help():
        HELPS = (
            '',
            '  usage: zephyr run name [path]',
            '',
            'name or name=xxx:',
            '  name of application to build',
            'path or path=xxx',
            '  build path of application.',
        )
        for help in HELPS:
            print(help)
        sys.exit()

    home = ZEPHYR_HOME
    name = path = None

    if not args:
        print("Error, no found build args!")
        return 0
    # update home.
    if 'home' in args:
        home = args['home']
    # build args.
    if 'args' in args:
        for val in args['args']:
            cv = val.split('=')
            if len(cv) > 1:
                if cv[0] == 'name':
                    name = cv[1]
                elif cv[0] == 'path':
                    path = cv[1]
                elif cv[0] == 'help':
                    run_help()
                else:
                    print('Error, unknown %s to run' % cv[0])
                    sys.exit()
            else:
                if val in ['-h', 'help', '--help']:
                    run_help()
                if not name:
                    name = val

    if (not path) and name:
        path = os.path.join(home, 'out', name)

    if not os.path.exists(path):
        print('No found application of %s' % name)
        return -1
    # run shell command to run target
    cmd = "cd {path} && make run".format(path=path)
    subprocess.call(cmd, shell=True, executable="/bin/bash")
    return 0


# get cmds.
#
def get_cmds(args):
    if not args:
        usage_help()

    support_cmds = {'build': ['-b', 'build'],
                    'run': ['-r', 'run'],
                    'home': ['-h', 'home'],
                    }

    cmds = OrderedDict()
    cmd_pending = None
    cmd_found = 0
    # get args of cmd.
    for cmd in args:
        if not cmd_found:  # check new cmd.
            for key, values in support_cmds.items():
                if cmd in values:  # found supported cmd.
                    cmd_pending = key
                    cmds[cmd_pending] = []
                    cmd_found = 1
                    break
            if cmd_found:  # get next cmd.
                continue
        # get args for cmd.
        if cmd_pending:
            cmds[cmd_pending].append(cmd)
            cmd_found = 0
    return cmds


# run cmds
#
def run_cmds(cmds):
    support_cmds = {'build': build,
                    'run': run,
                    }

    if not cmds:
        usage_help()
        return -1

    home = ZEPHYR_HOME
    # check home
    if 'home' in cmds:
        if len(cmds['home']):
            home = cmds['home'][0]
        else:
            print('Error, no args for home!')
            return -1
        del cmds['home']  # remove home from cmds.
    # run cmds.
    for key, value in cmds.items():
        if key in support_cmds:
            args = {}
            args['home'] = home
            args['args'] = value
            support_cmds[key](args)
    return 0


# main
#
def main(args=None):
    cmds = get_cmds(args)
    run_cmds(cmds)
    return 0


if __name__ == '__main__':
    main(sys.argv[1:])
