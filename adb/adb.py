#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os
import sys
import getopt
import subprocess


VERSION = '1.0.0'
AUTHOR  = 'Byng.Zeng'

local_path = os.getcwd()

# ===========================================
# usage
# ===========================================
#
def print_usage():
    USAGES = [
        '=====================================================',
        '    %s  - %s' % (os.path.splitext(os.path.basename(__file__))[0], VERSION),
        '=====================================================',
        'usage:   python %s option' % os.path.basename(__file__),
        '',
        'option:',
        '  [-s xxx | --src=xxx] : source path',
        '   -t xxx | --tgt=xxx : target path, it is xxx/xxx',
        '   -f xxx | --ftype=xxx : file type, example .md',
        '   -o xxx | --option=xxx : xxx=push/cmdline',
        '  [-v | --verbose] : print debug info',
    ]
    for txt in USAGES:
        print(txt)


# ===========================================
# print interface
# ===========================================
#
pr_lvl = ['info', 'warn', 'err']

def pr_dbg(*msg):
    if 'dbg' in pr_lvl:
        print(*msg)

def pr_info(*msg):
    if 'info' in pr_lvl:
        print(*msg)

def pr_warn(*msg):
    if 'warn' in pr_lvl:
        print(*msg)

def pr_err(*msg):
    if 'err' in pr_lvl:
        print(*msg)


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
#  get type files
#
# path: path of files.
# ftype: type of files.
#
# return None or list
#
# -----------------------------------------------
def get_type_files(path, ftype):
    if not check_args(path, 'path'):
        return None
    lt = list()
    for rt, ds, fs in os.walk(path):  #walk for path
        if fs:  # get file list
            for f in fs:
                if not ftype:
                    lt.append(os.path.join(rt, f))
                elif os.path.splitext(f)[1] in ftype:
                    lt.append(os.path.join(rt, f))
    return lt


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
        pr_dbg('%s' % cmd)
        try:
            result = subprocess.check_output(cmd, shell=True)
        except subprocess.CalledProcessError as e:
            rc = False
            result = pr_err(str(e))
    return rc, result


# -----------------------------------------------
# push src files to tgt of device.
#
# src: local path of src.
# tgt: path of device will be saved.
# ftype: file type, example: .md, .pdf.
#
# return dict of files result.
#
# -----------------------------------------------
def push_files(src, tgt, ftype):
    # check args.
    if not check_args(src, 'src', tgt, 'tgt'):
        return None
    fs = get_type_files(src, ftype)
    result = dict()
    if fs:
        for f in fs:
            dname = os.path.join(tgt,
                os.path.dirname(f).replace('%s\\' % local_path, '')).replace('\\', '/')
            fname = os.path.join(dname, os.path.basename(f)).replace('\\', '/')
            pr_info('%s -> %s' % (f, fname))
            rc, result = execute_shell('adb shell mkdir -p %s' % dname)
            if not rc:  # mkdir is successful, and push file next.
                rc, result = execute_shell('adb push %s %s' % (f, fname))
                result[f] = rc
    return result


# -----------------------------------------------
# loop for comand line.
#
# devname: name of device will be process.
#
# return if cmd is 'exit' or 'quit'.
#
# -----------------------------------------------
def loop_cmdline():
    while(True):
        cmd = input('(exit/-e/quit/-q to exit): ')
        if not cmd:
            continue
        if cmd in ['exit', 'quit', '-q', '-e']:
            break
        else:
            if not 'adb' in cmd:
                cmd = 'adb shell %s' % cmd
            rc, result = execute_shell(cmd)
            if rc:
                print(result.decode('utf-8'))


# -----------------------------------------------
# main.
#
# opts: options of cmd.
#
# -----------------------------------------------
def main(opts=None):
    if not opts:  # get opts.
        try:
            opts, args = getopt.getopt(sys.argv[1:], 'hs:t:f:o:v',
                ['src=', 'tgt=', 'ftype=', 'device=', '--option=', '--verbose'])
        except getopt.GetoptError as e:
            pr_warn(str(e))
            print_usage()
            exit()
    # check opts.
    if not opts:
        print_usage()
        exit()
    # config args.
    src = os.getcwd()
    tgt = None
    ftype = None
    option = None
    for opt in opts:
        if opt[0] in ['-s', '--src']:
            src = os.path.abspath(opt[1])
        elif opt[0] in ['-t', '--tgt']:
            tgt = opt[1]
        elif opt[0] in ['-f', '--ftype']:
            ftype = opt[1]
        elif opt[0] in ['-o', '--opt=']:
            option = opt[1]
        elif opt[0] in ['-v', '--verbose']:
            pr_lvl.append('dbg')
        elif opt[0] in ['-h', '--help']:
            print_usage()
            exit()
    # execute option
    if not option:
        print('no option, -h for help')
        exit()
    if option in ['push']:
        push_files(src, tgt, ftype)
    elif option in ['cmdline']:
        loop_cmdline()


# ===========================================
# entrance
# ===========================================
#
if __name__ == '__main__':
    main()

