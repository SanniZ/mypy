#!/usr/bin/env python3

AUTHON = 'Byng Zeng'
VERSION = '1.0.0'

import os

from pybase.pyinput import get_input_args
from pybase.pysys import print_help, execute_shell
from develop.git.git import git_status, git_push_origin_master


# path of mygit.
MYGIT = os.getenv('GIT')


#
# print help for mygit.
#
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
def mygit_status_check(opt):
    tag = None
    excludes = ['__pycache__'] # Exclude files
    gits = mygit_gits()
    for git in gits:
        if opt == '-m':
            opt = 'MOD'
            tag = 'Modified'
        elif opt == '-n':
            opt = 'NEW'
            tag = 'New'
        result = git_status(git, opt)
        if result: # print result
            print("-------%s-------:" % git.replace("%s/" % MYGIT, ''))
            for res in result:
                for f in excludes:
                    if  f not in res:
                        print("[%s]: %s" % (tag, res))


#
# main to options.
#
def main(args=None):
    if not args:
        args = get_input_args('pmnh')
    if args:
        for k in args.keys():
            if k == '-p': # sync to master
                mygit_push_origin_master()
            elif k in ['-m', '-n']: # check files.
                mygit_status_check(k)
            else:
                mygit_help()
    else:
        mygit_help()


#
# entrance.
#
if __name__ == "__main__":
    main()
