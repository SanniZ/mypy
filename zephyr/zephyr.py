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


VERSION = '1.0.3'


# default home of zephyr
ZEPHYR_HOME = os.getenv('ZEPHYR_SRC_HOME')


def print_msg(msg, exit_=False):
    t = type(msg)
    if t == str:
        print(msg)
    elif t in [dict, tuple]:
        for m in msg:
            print(m)
    if exit_:
        sys.exit()


# build name of application.
#
# set default src to samples/ if src=None.
def build(args):
    def build_help():
        HELPS = (
            '',
            'usage: zephyr build name [src] [board] [home]',
            '',
            'name or name=xxx:',
            '  name of application to build',
            'src or src=xxx',
            '  path of src of application.',
            'board or board=xxx',
            '  board platform to build, default qemu_x86',
        )
        print_msg(HELPS, 1)

    home = ZEPHYR_HOME
    name = src = None
    board = 'qemu_x86'

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
                elif cv[0] in ['-h', '--help']:
                    build_help()
                else:
                    print_msg('Error, unknown %s to build' % cv[0], -1)
            else:
                if val in ['-h', '--help']:
                    build_help()
                if not name:
                    name = val
                elif not src:
                    src = val
                elif not board:
                    board = val

    if name:
        if not src:  # set default src to samples.
            ds = [home, 'samples']
            found_app = False
            for d in ds:
                src = os.path.join(d, name)
                if os.path.exists(src):
                    found_app = True
                    break
        # check source code.
        if not found_app:
            print_msg('No found source code of %s' % name, -1)
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
            'usage: zephyr run name [path]',
            '',
            'name or name=xxx:',
            '  name of application to build',
            'path or path=xxx',
            '  build path of application.',
        )
        print_msg(HELPS, 1)

    home = ZEPHYR_HOME
    name = path = None

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
                elif cv[0] in ['-h', '--help']:
                    run_help()
                else:
                    print_msg('Error, unknown %s to run' % cv[0], -1)
            else:
                if val in ['-h', '--help']:
                    run_help()
                if not name:
                    name = val
    if not name:
        print_msg('Error, unknown name to run!', -1)

    if not path:
        path = os.path.join(home, 'out', name)

    if not os.path.exists(path):
        print_msg('No found application of %s' % name, -1)
    # run shell command to run target
    cmd = "cd {path} && make run".format(path=path)
    subprocess.call(cmd, shell=True, executable="/bin/bash")
    return 0


# usage help
#
def usage_help(args=None):
    USAGE = (
        "---------------------------------------------",
        "    Zephyr Tools  - %s" % VERSION,
        "---------------------------------------------",
        "",
        "  usage: zephyr cmd [options]",
        "",
        "-b | build : name | src [board]",
        "  build application of zephyr.",
        "-r | run   : name | path",
        "  run application of zephyr.",
        "-H | home  : path",
        "  set home of zephyr.",
        "",
        "--help for cmd help",
    )
    print_msg(USAGE, 1)


# format:        name  : [min_args, [args], function]
support_cmds = {
    'build': [1, ['-b', 'build'], build],
    'run': [1, ['-r', 'run'], run],
    'home': [1, ['-H', 'home'], None],
    'help': [0, ['-help', 'help'], usage_help],
}


# get cmds.
#
def get_cmds(args):
    cmds = OrderedDict()
    cmd_pending = None
    cmd_found = None
    # get args of cmd.
    for cmd in args:
        for key, values in support_cmds.items():
            if cmd in values[1]:  # found supported cmd.
                cmd_pending = key
                cmds[cmd_pending] = []
                cmd_found = key
                break
        if cmd_found:  # get next cmd.
            cmd_found = None
            continue
        # get args for cmd.
        if cmd_pending:
            cmds[cmd_pending].append(cmd)
    # check cmd args.
    for cmd in cmds:
        if len(cmds[cmd]) < support_cmds[cmd][0]:
            print_msg('Error, no args for %s, --help for help' % cmd, -1)
    return cmds


# run cmds
#
def run_cmds(cmds):
    rc = 0
    if cmds:
        # set home
        if 'home' in cmds:
            if len(cmds['home']):
                home = cmds['home'][0]
            else:
                print_msg('Error, no args for home!', -1)
            del cmds['home']  # remove home from cmds.
        else:
            if ZEPHYR_HOME:
                home = ZEPHYR_HOME
            else:
                print_msg('Error, no get home value, '
                          'or set default home "export ZEPHYR_SRC_HOME=xxx"',
                          -1)
        # run cmds.
        for key, value in cmds.items():
            if key in support_cmds:
                args = {}
                args['home'] = home
                args['args'] = value
                rc = support_cmds[key][2](args)
    return rc


# main
#
def main(args=None):
    if not args:
        usage_help()
    # get cmd and args.
    cmds = get_cmds(args)
    if cmds:
        run_cmds(cmds)
    else:
        usage_help()


# entrance.
if __name__ == '__main__':
    main(sys.argv[1:])
