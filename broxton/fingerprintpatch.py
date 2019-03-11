#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 2018-11-22

@author: Byng Zeng
"""

import sys
import os
import getopt
import subprocess
import shutil

VERSION = '1.0.0'
AUTHOR = 'Byng.Zeng'


# print msg and exit
def stop_and_exit(msg=None):
    if msg:
        print(msg)
    # stop runing and exit.
    exit()


# get abs path.
def get_abs_path(path):
    if path[0:1] == r'.':
        path = path.replace(r'.', os.getcwd(), 1)
    return path


# get external name of file.
def get_ext_name(f):
    return os.path.splitext(f)[1].lower()


class FingerprintPatch(object):
    def __init__(self):
        self._source = None
        self._patch = None
        self._opt = None

    def print_help(self):
        HELP_MENU = (
            '======================================',
            '    FingerprintPatch - %s' % VERSION,
            '',
            '    @Author: %s' % AUTHOR,
            '    Copyright (c) %s studio' % AUTHOR,
            '======================================'
            'option: -s xxx -p xxx -o am|ghal|gta',
            '  -s path: set source path',
            '    if -o am: set root path of source code',
            '    if -o ghal/gta: set out/target/product/xxx of source code',
            '  -p path: set root path of patch',
            '    path: path of patch.',
            '  -o am|ghal|gta',
            '    am: run git am to apply all of patch.',
            '    ghal: get prebuild files of fingerprint HAL',
            '    gta: get prebuild files of fingerprint TA',
            '    grh: revert all of patches.',
        )
        for help in HELP_MENU:
            print(help)

    # get user input.
    def process_input(self):
        try:
            opts, args = getopt.getopt(sys.argv[1:], "hs:p:o:")
        except getopt.GetoptError:
            self.print_help()
        # process input value
        for name, value in opts:
            if name == r'-h':
                self.print_help()
                stop_and_exit()
            elif name == r'-s':
                self._source = get_abs_path(value)
            elif name == r'-p':
                self._patch = get_abs_path(value)
            elif name == r'-o':
                self._opt = value

    # get dirs of patch path.
    def get_dirs_of_patch(self):
        dirs = list()
        for rt, ds, fs in os.walk(self._patch):
            if len(fs) != 0:
                for f in fs:
                    if get_ext_name(f) == r'.patch':
                        rt = rt.replace(self._patch, '')
                        dirs.append(rt)
                        break
        if len(dirs) != 0:
            return sorted(dirs)
        else:
            return None

    # run git am to apply all of .patch
    def apply_patch_of_dirs(self, dirs):
        if not dirs:
            print('Error, no dir!')
        else:
            for d in dirs:
                print('--------------------------------------------------')
                print('apply patch: %s\n' % os.path.join(self._source, d))
                cmd = 'cd %s && git am %s/*.patch' % (
                    os.path.join(self._source, d),
                    os.path.join(self._patch, d))
                subprocess.call(cmd, shell=True)

    # get all of fingerprint HAL prebuild files.
    def get_hal_prebuild_files(self):
        files_of_prebuild = [
            'system/etc/permissions/android.hardware.fingerprint.xml',
            'system/framework/android.hardware.biometrics.fingerprint-V2.1-java.jar',
            'system/framework/com.fingerprints.extension-V1.0-java.jar',
            'system/framework/com.fingerprints.fmi.jar',
            'system/framework/oat/x86/android.hardware.biometrics.fingerprint-V2.1-java.odex',
            'system/framework/oat/x86/android.hardware.biometrics.fingerprint-V2.1-java.vdex',
            'system/framework/oat/x86/com.fingerprints.extension-V1.0-java.odex',
            'system/framework/oat/x86/com.fingerprints.extension-V1.0-java.vdex',
            'system/framework/oat/x86_64/android.hardware.biometrics.fingerprint-V2.1-java.odex',
            'system/framework/oat/x86_64/android.hardware.biometrics.fingerprint-V2.1-java.vdex',
            'system/framework/oat/x86_64/com.fingerprints.extension-V1.0-java.odex',
            'system/framework/oat/x86_64/com.fingerprints.extension-V1.0-java.vdex',
            'system/lib/android.hardware.biometrics.fingerprint@2.1.so',
            'system/lib/com.fingerprints.extension@1.0.so',
            'system/lib/vndk/android.hardware.biometrics.fingerprint@2.1.so',
            'system/lib/vndk/com.fingerprints.extension@1.0.so',
            'system/lib64/android.hardware.biometrics.fingerprint@2.1.so',
            'system/lib64/com.fingerprints.extension@1.0.so',
            'system/lib64/vndk/android.hardware.biometrics.fingerprint@2.1.so',
            'system/lib64/vndk/com.fingerprints.extension@1.0.so',
            'vendor/bin/hw/android.hardware.biometrics.fpcfingerprint@2.1-service',
            'vendor/etc/init/android.hardware.biometrics.fpcfingerprint@2.1-service.rc',
            'vendor/etc/permissions/com.fingerprints.extension.xml',
            'vendor/framework/com.fingerprints.extension.jar',
            'vendor/lib/hw/com.fingerprints.extension@1.0-impl.so',
            'vendor/lib64/hw/com.fingerprints.extension@1.0-impl.so'
        ]
        # copy files.
        for f in files_of_prebuild:
            src = os.path.join(self._source, f)
            tgt = os.path.join(self._patch, f)
            # create dir
            dt = os.path.split(tgt)[0]
            if not os.path.exists(dt):
                os.makedirs(dt)
            # copy file here
            shutil.copy(src, tgt)

    # get all of TA prebuild files.
    def get_ta_prebuild_files(self):
        files_of_prebuild = [
            'obj/trusty/build-sand-x86-64/user_tasks/sand/fpcfingerprint/build/build.elf',
        ]
        # copy files.
        for f in files_of_prebuild:
            src = os.path.join(self._source, f)
            tgt = os.path.join(self._patch, 'fingerprint/fingerprint.elf')
            # create dir
            dt = os.path.split(tgt)[0]
            if not os.path.exists(dt):
                os.makedirs(dt)
            # copy file here
            shutil.copy(src, tgt)

    # revert all of patch.
    def revert_patches(self, source_path):
        patch_paths = {
            'device/intel/mixins': 8,
            'device/intel/sepolicy': 1,
            'kernel/bxt': 2,
            'kernel/config-lts/v4.9': 1,
            'packages/services/Car': 1,
            'trusty/app/keymaster': 1,
            'trusty/app/sand': 23,
            'trusty/device/x86/sand': 1,
            'trusty/platform/sand': 7,
            'trusty/lk/trusty': 1,
            'vendor/intel/fw/evmm': 2,
            'vendor/intel/hardware/fingerprint': 18,
            'vendor/intel/hardware/storage': 1,
        }
        for path, num in patch_paths.items():
            for i in range(num):
                cmd = 'cd %s/%s && git reset --hard HEAD~' % (source_path,
                                                              path)
                print(cmd)
                subprocess.call(cmd, shell=True)

    # enterance of app
    def main(self):
        # get user input
        self.process_input()

        if any((not self._source, not self._patch, not self._opt)):
            stop_and_exit('Error, invalid input, run -h to get help!')

        if self._opt == r'am':
            # get dirs of patch.
            dirs = self.get_dirs_of_patch()
            if dirs:
                self.apply_patch_of_dirs(dirs)
            else:
                print('No found .patch file!')
        elif self._opt == r'ghal':
            self.get_hal_prebuild_files()
        elif self._opt == r'gta':
            self.get_ta_prebuild_files()
        elif self._opt == r'grh':
            self.revert_patches(self._source)
        else:
            stop_and_exit('Error, unsupport %s' % self._opt)

if __name__ == '__main__':
    patch = FingerprintPatch()
    patch.main()
