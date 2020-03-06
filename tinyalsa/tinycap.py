#!/usr/bin/env python
# -*- coding: UTF-8 -*-

AUTHOR  = 'Byng.Zeng'
VERSION = '1.0.0'


import os
import sys
import getopt
import subprocess


# ===========================================
# usage
# ===========================================
def print_usage():
    USAGES = [
        '=====================================================',
        '    %s  - %s' % (os.path.splitext(os.path.basename(__file__))[0], VERSION),
        '=====================================================',
        'execute tinycap.',
        '',
        'usage:  python %s option' % os.path.basename(__file__),
        '',
        'option:',
        '  -p xxx | --path=xxx : path to save',
        '  -D xxx | --card=xxx : number of card',
        '  -d xxx | --device=xxx : number of device',
        '  -c xxx | --channel=xxx : number of channel',
        '  -r xxx | --resample=xxx : number of resample',
        ' [-b xxx | --bits=xxx] : number of bits',
        '',
        'Note:',
        '  default settings:',
        '  -D 0 -d 0 -c 2 -r 44100 -b 16',
    ]
    for txt in USAGES:
        print(txt)


# ===========================================
# print msg
# ===========================================
pr_lvl = ['err', 'info']

def pr_dbg(msg):
    if 'dbg' in pr_lvl:
        print(msg)

def pr_info(msg):
    if 'info' in pr_lvl:
        print(msg)

def pr_err(msg):
    if 'err' in pr_lvl:
        print(msg)


# ===========================================
# function APIs
# ===========================================
# -----------------------------------------------
# execute shell command
#
# cmd: the comand of shell will be execute.
#
# return rc(True/False), result(data of shell)
# -----------------------------------------------
def execute_shell(cmd):
    rc = True
    result = None
    if cmd:
        pr_dbg('%s' % cmd)
        try:
            result = subprocess.check_output(cmd, shell=True)
        except subprocess.CalledProcessError as e:
            rc = False
            result = str(e)


# -----------------------------------------------
# tinycap to record.
##
# No retrun value.
# -----------------------------------------------
def tinycap(file, card=0, device=0, channel=2, resample=44100, bits=16):
    cmd = "adb shell tinycap %s -D %d -d %d -c %d -r %d -b %d" % (
                file, card, device, channel, resample, bits)
    execute_shell(cmd)


# -----------------------------------------------
# main.
#
# opts: options of cmd.
#
# No retrun value.
# -----------------------------------------------
def main(opts=None):
    # check opts.
    if not opts:  # get opts.
        try:
            opts, args = getopt.getopt(sys.argv[1:], 'hf:D:d:c:r:b:',
                ['help', 'file=', 'card=', 'device=', 'channel=', 'resample=', 'bits='])
        except getopt.GetoptError as e:
            pr_err(str(e))
            print_usage()
            return False
        if args:
            pr_err('unknown %s, -h for help' % args)
            return False
    if not opts:
        print_usage()
        exit()

    # config opts.
    file = None
    card = 0
    device = 0
    channel = 2
    resample = 44100
    bits = 16
    for opt in opts:
        if opt[0] in ['-f', '--file']:
            file = opt[1]
        elif opt[0] in ['-D', '--card']:
            card = opt[1]
        elif opt[0] in ['-d', '--device']:
            device = opt[1]
        elif opt[0] in ['-c', '--channel']:
            channel = opt[1]
        elif opt[0] in ['-r', '--resample']:
            resample = opt[1]
        elif opt[0] in ['-b', '--bits']:
            bits = opt[1]
        elif opt[0] in ['-v', '--verbose']:
            pr_lvl.append('dbg')
        else:
            options.append(opt[0])  # set options
    if not file:
        pr_err('error, no file, -h for help!')
    tinycap(file, card, device, channel, resample, bits)


# ===========================================
# entrance
# ===========================================
if __name__ == '__main__':
    main()