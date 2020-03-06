#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os
import sys
import getopt
import subprocess


VERSION = '1.0.0'
AUTHOR  = 'Byng.Zeng'

# ===========================================
# usage
# ===========================================
#
def print_usage():
    USAGES = [
        '=====================================================',
        '    %s  - %s' % (os.path.splitext(os.path.basename(__file__))[0], VERSION),
        '=====================================================',
        'It is a side tone loopback test of headset.',
        '',
        'usage:   python %s option' % os.path.basename(__file__),
        '',
        'option:',
        '  [-t | --test] : test loopback',
        '  [-s | --stop] : stop loopback',
    ]
    for txt in USAGES:
        print(txt)

# ===========================================
# function APIs
# ===========================================
#
# -----------------------------------------------
#  check args
#
# arg1, arg2: the arg to check.
# txt1, txt2: print the info which is None.
#
# return True if not None,
#        otherwise is False and print invald arg.
# -----------------------------------------------
def check_args(*args):
    for i, value in enumerate(args):
        if i % 2 == 0:
            if not value:
                pr_err('error, %s is invalid' % args[i+1])
                return False
    return True

# -----------------------------------------------
# execute shell command
#
# cmd: the comand of shell will be execute.
#
# return rc(True/False), result(data of shell)
#
# -----------------------------------------------
def execute_shell(cmd):
    rc = True
    result = None
    if cmd:
        print('%s' % cmd)
        try:
            result = subprocess.check_output(cmd, shell=True)
        except subprocess.CalledProcessError as e:
            rc = False
            result = str(e)
    return rc, result


# -----------------------------------------------
# open loopback
# -----------------------------------------------
def test_loopback():
    #cmds = ['5 124', '9 35', '16 1', '63 1', '67 1', '72 1']
    cmds = ["'ADC1 MIXER Mic1 Input Switch' 1",
            "'MIC1 Gain' 35",
            "'ADC1 Gain' 124",
            "'MIC1 HPMIC Switch' 1",
            "'HPR MIXER Side Tone Switch' 1",
            "'HPL MIXER Side Tone Switch' 1"]
    for cmd in cmds:
        execute_shell('adb shell tinymix %s' % cmd)

# -----------------------------------------------
# stop loopback
# -----------------------------------------------
def stop_loopback():
    #cmds = ['5 0', '9 0', '16 0', '63 0', '67 0', '72 0']
    cmds = ["'ADC1 MIXER Mic1 Input Switch' 0",
            "'MIC1 Gain' 0",
            "'ADC1 Gain' 0",
            "'MIC1 HPMIC Switch' 0",
            "'HPR MIXER Side Tone Switch' 0",
            "'HPL MIXER Side Tone Switch' 0"]
    for cmd in cmds:
        execute_shell('adb shell tinymix %s' % cmd)

# -----------------------------------------------
# main.
#
# opts: options of cmd.
#
# -----------------------------------------------
def main(opts=None):
    if not opts:  # get opts.
        try:
            opts, args = getopt.getopt(sys.argv[1:], 'hts', ['run', 'stop'])
        except getopt.GetoptError as e:
            print(str(e))
            print_usage()
            exit()
    # check opts.
    if not opts:
        print_usage()
        exit()
    # execute opts.
    for opt in opts:
        if opt[0] in ['-t', '--test']:
            test_loopback()
        elif opt[0] in ['-s', '--stop']:
            stop_loopback()


# ===========================================
# entrance
# ===========================================
#
if __name__ == '__main__':
    main()