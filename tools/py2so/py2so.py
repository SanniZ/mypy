#!/usr/bin/env python3

AUTHOR = 'Byng.Zeng'
VERSION = '1.0.1'

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
    name = os.path.splitext(os.path.basename(py))[0]
    if not name:
        pr_err('create_setup_py() name = %s, py=%s' % (name, py))
        return -1
    with open('setup.py', 'w') as fd:
        fd.write('from distutils.core import setup\n')
        fd.write('from Cython.Build import cythonize\n')
        fd.write("setup(name='%s.so', ext_modules=cythonize('%s'))\n" % (name, py))
        pr_dbg('create setup.py: name=%s.so, cythonize=%s' % (name, py))
    return 0


def package_dist(src, tgt):
    if any((not src, not tgt)):
        pr_err('src: %s and tgt: %s, package dist fail!' % (src, tgt))
        return None
    # search all of .so and __init__.py
    result = list()
    for rt, ds, fs in os.walk(src):
        if fs:
            for f in fs:
                srcso = os.path.join(rt,f)
                if rt == src:
                    distso = os.path.join(tgt, f)
                else:
                    distso = os.path.join(tgt, os.path.relpath(rt, src), f)
                pr_dbg('rt=%s, src=%s, f=%s' % (rt, src, f))
                pr_dbg('packaege_dist() srcso: %s, distso: %s' % (srcso, distso))
                if os.path.basename(distso) == '__init__.py':
                    if not os.path.exists(os.path.dirname(distso)):
                        os.makedirs(os.path.dirname(distso))
                    shutil.copyfile(srcso, distso)
                    result.append(distso)
                elif os.path.splitext(os.path.basename(distso))[1] == '.so':
                    if not os.path.exists(os.path.dirname(distso)):
                        os.makedirs(os.path.dirname(distso))
                    shutil.move(srcso, distso)
                    result.append(distso)
    # check real path of .so of current path.
    for f in os.listdir(os.getcwd()):
        if os.path.splitext(f)[1] == '.so':  # .so
            for rt, ds, fs in os.walk(src):  # check src for path dir.
                if fs:
                    for f2 in fs:
                        if f.startswith(os.path.splitext(f2)[0]):
                            distso = os.path.join(tgt, os.path.relpath(rt, src), f)
                            if not os.path.exists(os.path.dirname(distso)):
                                os.makedirs(os.path.dirname(distso))
                            shutil.move(os.path.join(os.getcwd(), f), distso)
                            result.append(distso)
    return result


def clean_build_files(path):
    if not path:
        pr_err('clean_build_files() path=%s' % path)
        return False
    build_files = ['.c']
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
        if setup_py != 0:  # error, create setup.py 
            continue
        try:
            ret = subprocess.check_output('python3 setup.py build_ext --inplace', shell=True)
        except subprocess.CalledProcessError:
            pr_warn('build setup.py for %s fail!' % py)
            continue
        pr_info(ret, False)
    # clean temp files.
    clean_build_files(src)
    # package .so to tgt
    dist = package_dist(src, tgt)
    return dist


def usage_help():
    USAGES = (
	"===========================================================  ", 
	"    py2so - %s" % VERSION,
	"===========================================================  ", 
	"Build .py to share library .so",
	"",
	"Usage:   python3 pyso.py options",
	"options:",
	"  -s path : set path of .py",
	"  -t path : set path of .so",
	"  -o build/clean :  build .py / clean build files.",
    )
    for usage in USAGES:
        print(usage)


def main():
    args = get_input_args('ds:t:o:h')
    if not args:
        usage_help()
        exit()
    # config vars
    src = tgt = opt = None
    for k, v in args.items():
        if k == '-s':
            src = os.path.abspath(v)
        elif k == '-t':
            tgt = os.path.abspath(v)
        elif k == '-o':
            opt = v
        elif k == '-d':
            PR_LVL.append('dbg')
        else:
            usage_help()
            exit()
    # set current path to src.
    if not src:
        src = os.getcwd()
    # set src path to tgt if no tgt.
    if not tgt:
        tgt = os.path.join(os.getcwd(), 'dist')
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
