#!/usr/bin/env python3

AUTHON = 'Byng Zeng'
VERSION = '1.0.1'

import os

from pybase.pysys import execute_shell
from develop.git.git import git_status, git_push_origin_master


# path of mygit.
MYGIT = os.getenv('GIT')


#
# get all gits of mygit.
#
def mygit_gits():
    lt = []
    for rt, ds, fs in os.walk(MYGIT):
        if '.git' in ds:
            lt.append(rt)
    return lt


#
# sync to master
#
def mygit_push_origin_master():
    gits = mygit_gits()
    for git in gits:
        git_push_origin_master(git)


#
# check status files of modified or new.
#
def mygit_status(opt):
    def is_exclude_file(f):
        excludes = ['__pycache__', "pyc"] # Exclude files
        for ex in excludes:
            if ex in f:
                return True
        return False

    gits = mygit_gits()
    for git in gits:
        result = git_status(git, opt)
        if result: # print result
            fs = []
            for res in result:
                if not is_exclude_file(res):
                    fs.append(res)
            if fs:
                print("-------%s-------:" % git.replace("%s/" % MYGIT, ''))
                for f in fs:
                    print("%s" % (f))


#
# entrance.
#
if __name__ == "__main__":
    from pybase.pyinput import get_input_args
    from pybase.pysys import print_help

    def mygit_help():
        HELPS = (
		"==============================================",
		"     mygit - %s" % VERSION,
		"==============================================",
		"Usage:  mygit option",
		"option:",
		"  -p : push origin master.",
		"  -m : check all of modified files.",
		"  -n : check all of new files",
        )
        print_help(HELPS, True)


    args = get_input_args('pmnh')
    if not args:
        mygit_help()
    for k in args.keys():
        if k == '-p': # sync to master
            mygit_push_origin_master()
        elif k in ['-m', '-n']: # check files.
            mygit_status(k)
        else:
            mygit_help()
