#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 2019-07-25

@author: Byng.Zeng
"""

VERSION='1.0.0'

import os
import sys
import subprocess
import shutil

from collections import OrderedDict

# default home of zephyr
ZEPHYR_HOME=os.path.join(os.getenv('HOME'), "workspace/zephyr/master")


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
        cmake=os.path.join(os.getenv('CMAKE'), 'cmake')
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


# main 
#
def main(args=None):
    if args:
        cmds = OrderedDict()
        cmd_pending = None
        home = ZEPHYR_HOME
        # get args of cmd.
        for index, cmd in enumerate(args):
            if cmd in ['-b', 'build']:
                cmds['build'] = []
                cmd_pending = 'build'
            elif cmd in ['-r', 'run']:
                cmd_pending = 'run'
                cmds['run'] = []
            elif cmd in ['-h', 'home']:
                cmd_pending = 'home'
            elif cmd_pending == 'build':
                cmds['build'].append(cmd)
            elif cmd_pending == 'run':
                cmds['run'].append(cmd)
            elif cmd_pending == 'home':
                home = cmd
                cmd_pending = None
            else:
               usage_help()
    else:
        usage_help()
    # run cmds.
    for key, value in cmds.items():
        if key == 'build':  # build
            if len(value) >= 2:  # build(name, src)
                build(name=values[0], src=values[1], home=home)
            elif len(value) == 1:  # build(name)
                build(name=value[0], home=home)
        elif key == 'run':  # run
            if len(value) > 0:  # run(name)
                run(value[0], home)
            else:
                usage_help()
    return 0



if __name__ == '__main__':
    main(sys.argv[1:])
