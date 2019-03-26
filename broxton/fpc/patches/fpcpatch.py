#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 2019-03-19

@author: Byng Zeng
"""

import os

from pybase.pydecorator import get_input_args
from pybase.pysys import print_help
from develop.git import gitpatch as gp

VERSION = '1.1.1'
AUTHOR = 'Byng.Zeng'


# ===============================================================
# ReverFPCtPatch class
# ===============================================================
class FpcRevertPatch(object):

    GITS = {  # git : subject of stop.
        'device/intel/mixins': 'Audio: FW: Update BXT-P to 9.22.03.3662',
        'device/intel/sepolicy': 'recovery: fix sepolicy for access GPU',
        'kernel/bxt': 'i915/fb: use kthread replace async',
        'kernel/config-lts/v4.9':
        'Config: enable ipu4 early device on Gorden peak',
        'packages/services/Car':
        'Decrease the duration of activity transition.',
        'trusty/app/keymaster':
        'Revert "[trusty][app] change KEYMASTER_MAX_BUFFER_LENGTH to 68KB"',
        'trusty/app/sand': '[crypto]remove log in user build',
        'trusty/device/x86/sand': '[device]remove log in user build',
        'trusty/platform/sand':
        '[platform][sand] bypass retrieval of attkb in manufacturing mode',
        'trusty/lk/trusty':
        'Revert "[trusty][lk] change IPC_CHAN_MAX_BUF_SIZE to 68KB"',
        'vendor/intel/fw/evmm':
        'Replace TARGET_PRODUCT with TRUSTY_REF_TARGET',
        'vendor/intel/hardware/fingerprint': 'Initial empty repository',
        # 'vendor/intel/hardware/storage': '',
    }

    SRCS = [
        'kernel/bxt/drivers/fpc',
        'kernel/bxt/include/linux/wakelock.h',
        'trusty/app/sand/fingerprint',
        'trusty/app/sand/fpcfingerprint',
        'vendor/intel/hardware/fingerprint/fingerprint_extension',
        'vendor/intel/hardware/fingerprint/fingerprint_hal',
        'vendor/intel/hardware/fingerprint/fingerprint_libs',
        'vendor/intel/hardware/fingerprint/fingerprint_tac',
        'vendor/intel/hardware/fingerprint/Android.bp',
        'vendor/intel/hardware/fingerprint/Android.mk']


class FpcPatch(object):

    HELP_MENU = (
        '==================================',
        '    FpcPatch - %s' % VERSION,
        '',
        '    @Author: %s' % AUTHOR,
        '    Copyright (c) %s studio' % AUTHOR,
        '==================================',
        '  -a path: apply patches.',
        '    path: path of patches.',
        '  -r path: revert patches.',
        '    path: path of patches.',
        '  -R path: revert patches of xfeng8 version.',
        '    path: path of patches.',
    )

    def __init__(self, root=None, patches=None):
        self._opts = 'ha:r:R:p:'
        self._root = root
        self._patches = patches
        self._src = None
        self._diff = None
        self.update_path_config()

    @get_input_args()
    def process_input_args(self, opts, args=None):
        if '-p' in args:
            self._patches = os.path.abspath(args['-p'])
            self.update_path_config()
        return args

    def update_path_config(self, root=None, patches=None):
        if root:
            self._root = root
        if patches:
            self._patches = patches
            self._diff = os.path.join(self._patches, 'diff')
            self._src = os.path.join(self._patches, 'src')
        if all((self._root, not self._patches)):
            self._patches = os.path.join(
                self._root, 'vendor/intel/hardware/fingerprint/scratch')
            self._diff = os.path.join(self._patches, 'diff')
            self._src = os.path.join(self._patches, 'src')

    def main(self, args=None):
        args = self.process_input_args(self._opts, args=args)
        if all((args, isinstance(args, dict))):
            for key in args.keys():
                if key == '-a':
                    root = os.path.abspath(args['-a'])
                    self.update_path_config(root=root)
                    print('apply patches')
                    gp.apply_patch_files(root, gp.get_patch_files(self._diff))
                    gp.copy_src_files(root, gp.get_src_dirs(self._src))
                    print('apply patches done')
                elif key == '-R':
                    root = os.path.abspath(args['-R'])
                    self.update_path_config(root=root)
                    print('revert patches')
                    gp.revert_gits(root, FpcRevertPatch.GITS)
                    gp.remove_src_files(root, FpcRevertPatch.SRCS)
                    print('revert patches done')
                elif key == '-r':
                    root = os.path.abspath(args['-r'])
                    self.update_path_config(root=root)
                    print('revert patches')
                    gp.revert_patch_files(root, self._diff)
                    gp.remove_src_files(root, FpcRevertPatch.SRCS)
                    print('revert patches done')
                elif key == '-h':
                    print_help(self.HELP_MENU)

# ===============================================================
# main entrance
# ===============================================================
if __name__ == '__main__':
    fpc = FpcPatch()
    fpc.main()
