#!/usr/bin/env python3

AUTHOR = 'Byng Zeng'
VERSION = '1.0.1'

import os

from pybase.pysys import execute_shell



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
    def git_status_s(path): # get short status.
        if os.path.exists("%s/.git" % path):
            rc, result = execute_shell("cd %s && git status -s" % path)
            if rc == 0:
                return result.decode().splitlines()
            else:
                return None

    opts = {"-m": ["M", "Modified"], "-n": ["??", "New"]}
    if any((not path, not os.path.exists("%s/.git" % path))):  # check path
        print("error, %s is invalid!" % path)
        return None
    if opt not in opts:  # check opt
        print("error, opt %s is not supported!" % opt)
        return None
    # get status list.
    fs = git_status_s(path)
    if not fs:
        return None
    res = []
    for f in fs:  # get files of opt.
        f = f.strip().split()
        if f:
            if f[0] == opts[opt][0]:
                res.append("[%s]: %s" % (opts[opt][1], f[1]))
            else:
                continue
    if all((pr_res, res)):  # print result.
        print("-------%s-------:" % path)
        for f in res:
            print(f)
    return res


#
# run 'git push origin master'.
#
def git_push_origin_master(path):
    if not path:
        print("error, invalid path!")
        return None
    print("-------%s-------" % path)
    rc, result = execute_shell("cd %s && git push origin master" % (path))
    if rc == 0:
        res = result.decode()
    else:
        res = None
    print(res)
    return res


#
# entrance
#
if __name__ == "__main__":
    from pybase.pyinput import get_input_args
    from pybase.pysys import print_help


    def git_help():
        HELPS = (
		"=================================================",
		"    git - %s" % VERSION,
		"=================================================",
		"Usage:    git.py options",
		"  options:",
		"    -p : push to master with 'git push origin master'",
		"    -m : get modified files of path.",
		"    -n : get new files of path.",
        )
        print_help(HELPS)

    args = get_input_args('p:m:n:h')
    if not args:
        git_help()
    for k, v in args.items():
        if k == '-p':
            git_push_origin_master(os.path.abspath(v))
        elif k in ['-m', '-n']:
            git_status(os.path.abspath(v), k, True)
        else:
            git_help()
