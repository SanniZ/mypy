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


VERSION = '1.0.1'


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
def build(name=None, src=None, home=ZEPHYR_HOME):
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
              "&& {cmake} -B {out} -DBOARD=qemu_x86 {src}".format(home=home,
                                                                  cmake=cmake,
                                                                  out=out,
                                                                  src=src)
        subprocess.call(cmd, shell=True, executable="/bin/bash")
    return 0


# run name of application
#
def run(name=None, home=ZEPHYR_HOME):
    if name:
        src = os.path.join('out', name)
        if not os.path.exists(os.path.join(home, src)):
            print('No found application of %s' % name)
            return -1
        # run shell command to run target
        cmd = "cd {home} && make run".format(home=os.path.join(home, src))
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
        if key == 'build':  # build
            if len(value) >= 2:  # build(name, src)
                build(name=value[0], src=value[1], home=home)
            elif len(value) == 1:  # build(name)
                build(name=value[0], home=home)
        elif key == 'run':  # run
            if len(value) > 0:  # run(name)
                run(value[0], home)
            elif 'build' in cmds:
                run(cmds['build'][0], home)
            else:
                usage_help()
    return 0


# main
#
def main(args=None):
    cmds = get_cmds(args)
    if cmds:
        run_cmds(cmds)
    return 0


if __name__ == '__main__':
    main(sys.argv[1:])
