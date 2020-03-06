#!/usr/bin/env python
# -*- coding: UTF-8 -*-

AUTHOR  = 'Byng.Zeng'
VERSION = '1.0.1'

import os
import sys
import getopt
import subprocess

JOIN_WIDGETS=False

# ===========================================
# usage
# ===========================================
def print_usage():
    USAGES = [
        '=====================================================',
        '    %s  - %s' % (os.path.splitext(os.path.basename(__file__))[0], VERSION),
        '=====================================================',
        'execute tinymix widgets.',
        '',
        'usage:  python %s option' % os.path.basename(__file__),
        '',
        'option:',
        '  -e | --enable  : enable widgets',
        '  -d | --disable : disable widgets',
        '  -c | --check   : check widgets',
        '  -C | --CHECK   : check short widgets',
        '  -s | --shell   : run shell commands',
        ' [-w module | --widget=module] : module name',
        '',
        'Note:',
        '  put module.py and %s under the same path, or',
        '  run tinymix.py under path of module.py ',
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
        pr_dbg('execute: %s' % cmd)
        try:
            result = subprocess.check_output(cmd, shell=True)
        except subprocess.CalledProcessError as e:
            rc = False
            result = str(e)
    return rc, result.decode()


# -----------------------------------------------
# set widgets
#
# widgets : dict of widgets,
#           contains keys of 'widgets' , 'enable'/'disable'
# key     : 'enable' or 'disable'
#
# No retrun value.
# -----------------------------------------------
def set(widgets, key):
    if not widgets:  # no widgets.
        pr_err('error, no set widgets ')
        return False, None
    result = list()
    #if TINYWIDGET:
    #    w = tinywidget.join_widgets(widgets)
    #    widgets = list()
    #    widgets.append(w)
    for widget in widgets:
        if key not in widget: # no key at widgets.
            pr_err('set(): no key %s ' % (key))
            continue
        for i, w in enumerate(widget['widgets']):  # run widgets.
            if key == 'widgets':
                cmd = "adb shell tinymix '%s'" % w
            else:
                cmd = "adb shell tinymix '%s' %s" % (w, widget[key][i])
            # run tinymix cmd
            rc, data = execute_shell(cmd)
            if rc:
                result.append(data)
    return True, result


# -----------------------------------------------
# check widgets
#
# widgets : dict of widgets, contains key of 'widgets'
#
# print values of widgets.
# -----------------------------------------------
def check(widgets):
    rc, result = execute_shell('adb shell tinymix')
    if not rc:
        pr_err('check(): tinymix fail!')
        return False
    # decode to string
    if not widgets:  # print all of widgets.
        pr_info(result)
    result = result.split('\n')  # list.
    for widget in widgets:
        for w in widget['widgets']:  # check widget.
            for val in result:
                if val.find(w) != -1:  # found and print
                    pr_info(val)
    return True


# -----------------------------------------------
# shell
#
# cmd : shell command
#
# print result of result.
# -----------------------------------------------
def shell(cmd):
    rc, result = execute_shell('adb shell tinymix %s' % cmd)
    if (rc):
        print(result)


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
            opts, args = getopt.getopt(sys.argv[1:], 'hcCdesw:v',
                ['help', 'check', 'CHECK', 'disable', 'enable', '--shell', 'widget=', 'verbose'])
        except getopt.GetoptError as e:
            pr_err(str(e))
            print_usage()
            return False
        # if args:
        #     pr_err('unknown %s, -h for help' % args)
        #     return False

    widgets = list()
    options = list()
    shell_cmd = ''

    # run tinymix while no opts and args.
    if all((not opts, not args)):
        rc, result = execute_shell('adb shell tinymix')
        print(result)
        return True
    elif opts:
        # config opts.
        for opt in opts:
            if opt[0] in ['-w', '--widget']:  # load widgets.
                sys.path.append(os.path.dirname(opt[1]))  # append path of module.
                try:
                    module = __import__(os.path.basename(opt[1]).replace('.py', ''))  # import module
                except ModuleNotFoundError as e:
                    pr_err(str(e))
                    return False
                widgets.append(module.widgets)  # set widgets
            elif opt[0] in ['-s', '--shell']:  # set shell mode.
                options.append(opt[0])
                for v in args:
                    if v.isdigit():
                        shell_cmd = shell_cmd + ' ' + ' '.join(v)
                    else:
                        shell_cmd = shell_cmd + ' ' + ''.join("'%s'" % v)
            elif opt[0] in ['-v', '--verbose']:  # set debug mode
                pr_lvl.append('dbg')
            else:  # options.
                options.append(opt[0])  # set options
    elif args:
        for v in args:
            if v.isdigit():
                shell_cmd = shell_cmd + ' ' + ' '.join(v)
            else:
                shell_cmd = shell_cmd + ' ' + ''.join("'%s'" % v)
        options.append('--shell')
    # join widgets together.
    if JOIN_WIDGETS:
        sys.path.append(os.path.dirname('tinywidget.py'))
        tw = __import__('tinywidget')
        ws = tw.join(widgets)
        widgets = list()
        widgets.append(ws)
    # execute options.
    if options:  # execute options.
        for opt in options:
            if opt in ['-c', '--check']:  # check status of widgets
                check(widgets)
            elif opt in ['-C', '--CHECK']:  # check status and range of widgets
                rc, result = set(widgets, 'widgets')
                if rc:
                    for data in result:
                        print(data)
            elif opt in ['-d', '--disable']:  # disable widgets
                set(widgets, 'disable')
            elif opt in ['-e', '--enable']:  # enable widgets
                set(widgets, 'enable')
            elif opt in ['-s', '--shell']:  # shell widgets
                shell(shell_cmd)
            else:  # print usage.
                print_usage()
                return True
    elif all((not shell_cmd, args)):  # unknown args while no option.
        pr_info('unknown args: %s' % args)
    # return 
    return True


# ===========================================
# entrance
# ===========================================
if __name__ == '__main__':
    main()