#!/usr/bin/env python3

AUTHOR = 'Byng.Zeng'
VERSION = '1.0.0'

import os
import sys
import getopt
import collections
import subprocess
import shutil



# ============================================
# print msg
# ============================================
#
PR_LVL = ['info', 'warn', 'err']

def pr_msg(msg, lvl, flag):
    if lvl in PR_LVL:
        if flag:
            print('[%s] %s' % (flag, msg))
        else:
            print('%s' % msg)


def pr_dbg(msg, flag='debug'):
    pr_msg(msg, 'dbg', flag)        


def pr_info(msg, flag='info'):
    pr_msg(msg, 'info', flag)        


def pr_warn(msg, flag='warning'):
    pr_msg(msg, 'warn', flag)        


def pr_err(msg, flag='error'):
    pr_msg(msg, 'err', flag)        


# =====================================================
# API functions
# =====================================================
#

def get_input_args(opts):

    dt = collections.OrderedDict()
    try:
        opts, args = getopt.getopt(sys.argv[1:], opts)
    except getopt.GetoptError as e:
        pr_err('%s, -h for help.' % str(e))
        sys.exit()
    else:
        if opts:
            for key, value in opts:
                dt[key] = value
    return dt


def get_py_files(path):
    if not path:
        return None
    result = list()
    for rt, ds, fs in os.walk(path):
        if fs:
            for f in fs:
                if os.path.splitext(f)[1] in ['.py', '.PY']:
                    result.append(os.path.join(rt, f))
    pr_dbg('get py files: %s' % result)
    return result


def create_setup_py(src, py):
    if any((not src, not py)):
        pr_err('create_setup_py() src=%s, py=%s' % (src, py))
        return -1
    if os.path.basename(py) == '__init__.py':
        pr_dbg('found %s' % py)
        return 1
    name = None
    name = py.replace(src + '/', '').replace('.py', '').replace('/', '_')
    if not name:
        pr_err('create_setup_py() name = %s, py=%s' % (name, py))
        return -1
    with open('setup.py', 'w') as fd:
        fd.write('from distutils.core import setup\n')
        fd.write('from Cython.Build import cythonize\n')
        fd.write("setup(name='%s.so', ext_modules=cythonize('%s'))\n" % (name, py))
    return 0


def package_dist(src, tgt, py):
    if any((not src, not tgt, not py)):
        pr_err('src: %s and tgt: %s, package dist fail!' % (src, tgt))
        return None
    pyso = None
    pyname = os.path.splitext(os.path.basename(py))[0]
    if pyname == '__init__':
        if os.path.dirname(py) == src:
            pyso = os.path.basename(py)
        else:
            pyso = os.path.join(os.path.relpath(os.path.dirname(py), src), os.path.basename(py))
    else:
        # check .so
        all_path = [os.getcwd(), src]
        path_so = None
        for path in all_path:
            if path_so:
                break
            pr_dbg('check .so under %s' % src)
            for rt, ds, fs in os.walk(path):
                if fs:
                    for f in fs:
                        if os.path.splitext(f)[1] == '.so':
                            pr_dbg('package_dist() f=%s, pyname=%s' % (f, pyname))
                            if not f.startswith(pyname):
                                continue
                            if rt == path:
                                pyso = f
                            else:
                                pyso = os.path.join(rt.replace(path + '/', ''), f)
                            path_so = path
                            pr_dbg('update %s->%s' % (f, pyso))
                            break
    # check pyso
    if not pyso:
        pr_dbg('no found .so')
        return None
    src_pyso = os.path.join(path_so, pyso)
    tgt_pyso = os.path.join(tgt, pyso)
    pr_dbg('src_pyso: %s, tgt_pyso: %s' % (src_pyso, tgt_pyso))
    if not os.path.exists(src_pyso):
        pr_err('package_dist(): not found %s' % src_pyso) 
        return None
    try:
        os.makedirs(os.path.dirname(tgt_pyso))
    except FileExistsError:
        pr_warn('dir %s exist!' % os.path.dirname(tgt_pyso))
    try:
        shutil.copyfile(src_pyso, tgt_pyso)
    except shutil.SameFileError:
        pr_warn('file %s exist!')
    pr_dbg('package dist: %s' % tgt_pyso)
    return tgt_pyso

def clean_build_files(path):
    if not path:
        pr_err('clean_temp_files() path=%s' % path)
        return False
    build_files = ['.c', '.so']
    # check temp files of path and cwd.
    for p in [path, os.getcwd()]:
        for rt, ds, fs in os.walk(p):
            if fs:
                for f in fs:
                    subfix = os.path.splitext(f)[1]
                    if subfix in build_files:
                        f = os.path.join(rt, f)
                        os.remove(f)
                        pr_dbg('delete %s' % f, False )
    # delete setup.py
    # pr_dbg('setup: %s' % (os.path.join(os.getcwd(), 'setup')))
    # pr_dbg('build: %s' % (os.path.join(os.getcwd(), 'build')))
    if os.path.exists(os.path.join(os.getcwd(), 'setup.py')):
        os.remove(os.path.join(os.getcwd(), 'setup.py'))
        pr_dbg('delete setup.py', False)
    # delete build folder
    if os.path.exists(os.path.join(os.getcwd(), 'build')):
        shutil.rmtree(os.path.join(os.getcwd(), 'build'))
        pr_dbg('delete build', False)
    return True

def build_py_so(src, tgt):
    if any((not src, not tgt)):
        pr_err('build_py_so() not found src and tgt!')
        return None
    # get all of .py
    py_files = get_py_files(src)
    if not py_files:
        pr_err('build_py_so() not get py file.')
        return None
    # build, package and clean
    result = list()
    for py in py_files:
        setup_py = create_setup_py(src, py)
        if setup_py < 0:  # error, create setup.py 
            pr_warn('failed to create setup.py for %s!' % py)
            continue
        elif setup_py > 0:  # __init__.py
            package_dist(src, tgt, py)
            continue
        ret = subprocess.check_output('python3 setup.py build_ext --inplace', shell=True)
        pr_info(ret)
        # package .so to tgt
        dist = package_dist(src, tgt, py)
        if dist:
            result.append(dist)
        # clean temp files.
        clean_build_files(src)
    return result


def main():
    args = get_input_args('ds:t:o:h')
    if not args:
        pr_err('not found args!')
        return None
    src = tgt = opt = None
    # config vars
    for k, v in args.items():
        if k == '-s':
            src = os.path.abspath(v)
        elif k == '-t':
            tgt = os.path.abspath(v)
        elif k == '-o':
            opt = v
        elif k == '-d':
            PR_LVL.append('dbg')
    # set current path to src.
    if not src:
        src = os.getcwd()
    # set src path to tgt if no tgt.
    if not tgt:
        tgt = src
    # run command options.
    if opt == 'clean':  # clean build.
        clean_build_files(src)
    elif opt == 'build':  # build .py to .so
        result = build_py_so(src, tgt)
        if result:
            pr_info('--------------------dist-----------------------', False)
            for pyso in result:
                pr_info('output: %s' % pyso, False)


# ======================================
# entrance.
# ======================================
if __name__ == '__main__':
    main()
