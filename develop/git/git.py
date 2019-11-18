#!/usr/bin/env python3

AUTHOR = 'Byng Zeng'
VERSION = '1.0.0'

import os
import subprocess

from pybase.pyinput import get_input_args
from pybase.pyprint import PyPrint 
from pybase.pysys import print_help, execute_shell


pr = PyPrint()


def git_help():
    HELPS = (
	"=================================================",
	"    git - %s" % VERSION,
	"=================================================",
	"Usage:    git.py options",
	"  options:",
	"    -p : push to master with 'git push origin master'",
	"    -s [path,][new/mod] : get status of path",
	"",
	"git.py -s new/mod : get list of new/modified files of current path",
	"git.py -s path    : get list of new and modified of path",
	"git path,new/mod  : get list of new/modified files of path",
    )
    print_help(HELPS)

#
# run 'git status -s' to get short status.
#
# parameter:
#   path: path of git reposition.
#
# return values:
#   status of git reposition.
#
def git_status_s(path):
    if os.path.exists("%s/.git" % path):
        rc, result = execute_shell("cd %s && git status -s" % path)
        if rc == 0:
            return result.decode().splitlines()
        else:
            return None


ST_NEW = 'NEW'
ST_MOD = 'MOD'

def status_opt_is_valid(opt):
    if opt.upper() in [ST_NEW, ST_MOD]:
        return True
    else:
        return False

#
# get file list of status.
#
# parameters:
#   path: path to git reposition.
#   status: 'new', 'modified' of status.
#
# return values:
#   None of file list.
#
def git_status(path, opt, pr_res=False):
    if not path:
        pr.pr_err("error, path is invalid!")
    status = opt.upper()
    if not status_opt_is_valid(status):
        pr.pr_err("error, status should be %s or %s!" % (ST_NEW, ST_MOD))
        return None
    fs = git_status_s(path)
    if not fs:
        return None
    if pr_res:
        pr.pr_info("-------%s-------:" % path)
    res = []
    for f in fs:
        f = f.strip().split()
        if f:
            if all((ST_NEW == status, f[0] == '??')):
                res.append("[New]: %s" % f[1])
            elif all((ST_MOD == status, f[0] == 'M')):
                res.append("[Modified]: %s" % f[1])
            if all((pr_res, res)):
                pr.pr_info(res)
    return res


def git_push_origin_master(path):
    if not path:
        pr.pr_err("error, invalid path!")
        return None
    pr.pr_info("-------%s-------" % path)
    rc, result = execute_shell("cd %s && git push origin master" % (path))
    if rc == 0:
        res = result.decode()
    else:
        res = "None"
    pr.pr_info(res)


#
# main for options.
#
def main(args=None):
    if not args:
        args = get_input_args('p:s:h')
    if args:
        for k, v in args.items():
            if k in ['-s']:
                v = v.split(',')
                opts = []
                if len(v) > 1: # vars: path and opt
                    path = v[0]
                    opts.append(v[1])
                else:  # vars: opt
                    path = os.path.abspath(v[0])
                    if os.path.exists(path):
                        opts.append('NEW')
                        opts.append('MOD')
                    else:
                        path = os.path.abspath(os.path.curdir)
                        opts.append(v[0])
                pr.pr_info("-------%s-------" % path)
                for opt in opts:
                    result = git_status(path, opt)
                    if result:
                        for res in result:
                            pr.pr_info(res)
            elif k == '-p':
                path = os.path.abspath(v)
                git_push_origin_master(path)
            else:
                git_help()


#
# entrance
#
if __name__ == '__main__':
    main()
