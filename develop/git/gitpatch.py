#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 2019-03-15

@author: Byng Zeng
"""

import os
import re
import subprocess


VERSION = '1.2.0'
AUTHOR = 'Byng.Zeng'

subject_pattern = re.compile('^Subject: \[PATCH.*\](.*)')


# ===============================================================
# execute shell command
# ===============================================================
def execute_shell(cmd):
    try:
        res = subprocess.check_output(cmd, shell=True)
    except subprocess.CalledProcessError:
        return -1
    else:
        return res


# ============================================================
# get subjects of git
#
# input:
#  path: path of git.
#  depth: depth of subjects.
# output:
#   subjects of git.
# ============================================================
def get_git_subjects(path, depth=None):
    os.chdir(path)
    res = execute_shell('git log --pretty=format:%s')
    if res != -1:
        subjects = list(res.decode('utf-8').split('\n'))
        if not depth:
            return subjects
        elif len(subjects) > depth:
            return subjects[:depth]
        else:
            return subjects
    else:
        return None


# ============================================================
# get dirs of patches.
#
# input:
#   path: path of patches.
# output:
#   dict of patch dirs
# ============================================================
def get_patch_files(path):
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


# ============================================================
# get subject of .patch file
#
# input:
#   patch: file of patch.
# output:
#   subject of patch
# ============================================================
def get_patch_subject(patch):
    with open(patch, 'r') as fd:
        logs = list(fd.readlines())
    return subject_pattern.findall(logs[3])[0].lstrip()


# ============================================================
# check patch is exist in git.
#
# input:
#   path: path of git.
#   patch: file of patch
# output:
#   return True if exist, otherwise is False
# ============================================================
def patch_exists(path, patch):
    result = False
    with open(patch, 'r') as fd:
        logs = list(fd.readlines())
    subject = subject_pattern.findall(logs[3])[0].lstrip()
    git_subjects = get_git_subjects(path)
    if git_subjects:
        if subject in git_subjects:
            result = True
        else:
            for sub in git_subjects:
                if sub.startswith(subject):
                    result = True
                    break
    return result


# ============================================================
# check subject is exist at git_subjects.
#
# input:
#   subject: subject to check.
#   git_subjects: all of subjects in git.
#   path: path of git.
# output:
#   return True if exist, otherwise is False
# ============================================================
def subject_exists(subject, git_subjects=None, path=None):
    result = False
    # get sujects of git.
    if not git_subjects:
        if path:
            git_subjects = get_git_subjects(path)
        else:
            return False  # no subject of git
    # check subject
    if subject in git_subjects:
        result = True
    else:
        for sub in git_subjects:
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
def apply_patch_files(root, git_patches):
    for git, patches in git_patches.items():
        dst_git = os.path.join(root, git)
        for patch in patches:
            if patch_exists(dst_git, patch):
                print('patch exists : %s - %s' % (
                      git, os.path.basename(patch)[5:-6]))
            else:
                os.chdir(dst_git)
                res = execute_shell('git am %s' % patch)
                if res == -1:
                    print('conflict found : %s' %
                          os.path.basename(patch)[5:-6])
                    execute_shell('git am --abort')
                else:
                    print('patch appied : %s - %s' % (
                          git, os.path.basename(patch)[5:-6]))


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
def revert_gits(path, gits):
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
                execute_shell('git reset --hard HEAD~')
                print('revert patch : %s - %s' % (git, res))


# ============================================================
# reset patches.
#
# git_path: abs path of git.
# git : ref path of git
# reset_depth : depth to reset
# ============================================================
def reset_patches(git_path, git, reset_depth):
    os.chdir(git_path)
    for index in range(reset_depth):
        res = execute_shell('git log --pretty=format:%s')
        res = list(res.decode('utf-8').split('\n'))[0]
        print('revert patch : %s - %s' % (git, res))
        execute_shell('git reset --hard HEAD~')


# ============================================================
# revert all of patch.
#
# path: root path of project.
# gits: dict of gits, {git_path, [subjects1, subject2, ...]}
# ============================================================
def revert_patch_files(root, path):
    files = get_patch_files(path)
    for git, fs in files.items():
        # get subjects of git.
        git_path = os.path.join(root, git)
        git_subjects = get_git_subjects(git_path)
        # get invalid subjects.
        check_subjects = []
        for f in fs:
            sub = get_patch_subject(f)
            if sub:
                if subject_exists(sub, git_subjects=git_subjects):
                    check_subjects.append(sub)
        # get revert depth
        reset_depth = 0
        for check_sub in check_subjects:
            for index, sub in enumerate(git_subjects):
                if any((sub == check_sub, sub.startswith(check_sub))):
                    if index >= reset_depth:
                        reset_depth = index + 1
        reset_patches(git_path, git, reset_depth)


# ============================================================
# remove all of src files.
#
# path: root path of project.
# srcs: all of srcs ref to remove
# ============================================================
def remove_src_files(path, srcs):
    for src in srcs:
        p = os.path.join(path, src)
        if os.path.exists(p):
            print('remove files :', src)
            execute_shell('rm -rf %s' % p)
