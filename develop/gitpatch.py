#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 2019-03-15

@author: Byng Zeng
"""

import os
import re
import subprocess

VERSION = '1.1.0'
AUTHOR = 'Byng.Zeng'

subject_pattern = re.compile('^Subject: \[PATCH.*](.*)$')
date_pattern = re.compile('^Date:.*$')


# ===============================================================
# API functions
# ===============================================================
def execute_shell(cmd):
    try:
        res = subprocess.check_output(cmd, shell=True)
    except subprocess.CalledProcessError:
        return -1
    else:
        return res


# ============================================================
# get dirs of patches.
#
# input:
#   path: path of patches.
# output:
#   dict of patch dirs
# ============================================================
def get_git_patches(path):
    dt = {}
    for rt, ds, fs in os.walk(path):
        if fs:
            lt = []
            for f in fs:
                if os.path.splitext(f)[1] == '.patch':
                    lt.append(os.path.join(rt, f))
            if lt:
                dt[rt.replace(path, '').lstrip('/')] = lt
    return dt


def patch_exists(patch):
    result = False
    with open(patch, 'r') as fd:
        logs = list(fd.readlines())
    subject = subject_pattern.findall(logs[3])[0].lstrip()
    res = execute_shell('git log --pretty=format:%s')
    if res != -1:
        res = list(res.decode('utf-8').split('\n'))
        if subject in res:
            result = True
        else:
            for sub in res:
                if sub.startswith(subject):
                    result = True
                    break
    return result


# ============================================================
# apply patch of dirs.
#
# input:
#   root: root path of project.
#   path: path of patches.
#   ds  : list of dirs
# input the list of patch dirs from get_patch_dirs()
# ============================================================
def apply_patches(root, ds):
    for git, lt in ds.items():
        dst = os.path.join(root, git)
        os.chdir(dst)
        for patch in lt:
            if not patch_exists(patch):
                res = execute_shell('git am %s' % (patch))
                if res == -1:
                    print('conflict found : %s - %s' %
                          (git, os.path.basename(patch)[5:-6]))
                    execute_shell('git am --abort')
                else:
                    print('patch appied : %s - %s' %
                          (git, os.path.basename(patch)[5:-6]))
            else:
                print('patch exists : %s - %s' %
                      (git, os.path.basename(patch)[5:-6]))


def get_src_dirs(path):
    dt = {}
    for d in os.listdir(path):
        dt[d] = os.path.join(path, d)
    return dt


# ============================================================
# copy source files.
#
# it will copy all of src files to source code.
# ============================================================
def copy_src_files(root, dirs):
    for dst, src in dirs.items():
        dst = os.path.join(root, dst)
        print('  copy files : %s' % dst)
        execute_shell('cp -rf %s/. %s/' % (src, dst))


# revert all of patch.
def revert_patches(path, gits):
    for git, subject in gits.items():
        git_path = os.path.join(path, git)
        os.chdir(git_path)
        while True:
            # get subject
            res = execute_shell('git log --pretty=format:%s')
            res = list(res.decode('utf-8').split('\n'))[0]
            if res == subject:
                break
            else:
                print('revert patch : %s - %s' % (git, res))
                # reset patch.
                execute_shell('git reset --hard HEAD~')


def remove_src_files(path, srcs):
    for src in srcs:
        p = os.path.join(path, src)
        if os.path.exists(p):
            print('remove files : %s' % src)
            execute_shell('rm -rf %s' % p)
