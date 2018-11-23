#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on 2018-11-22

@author: Byng Zeng
"""

import re, os, sys, getopt
import subprocess
import shutil

class fingerprintPatch(object):
    def __init__(self):
        self._source=None
        self._patch=None
        self._opt=None

    def printHelp(self):
        print '======================================'
        print '     For fingerprint Patch'
        print '======================================'
        print 'option: -s xxx -p xxx -o am|ghal|gta'
        print '  -s xxx'
        print '    if -o am: set root path of source code'
        print '    if -o ghal or -o gta: set out/target/product/xxx of source code'
        print '  -p xxx'
        print '    set root path of patch.'
        print '  -o am|ghal|gta'
        print '    am  : run git am to apply all of patch.'
        print '    ghal: get prebuild files of fingerprint HAL'
        print '    gta : get prebuild files of fingerprint TA'


    # print msg and exit
    def errorExit(self, msg=None):
        if msg != None:
            print msg
        # stop runing and exit.
        exit()


    # get user input.
    def getUserInput(self):
        try:
            opts, args = getopt.getopt(sys.argv[1:], "hs:p:o:")
        except getopt.GetoptError:
            self.printHelp()
        # process input value
        for name, value in opts:
            if name == r'-h':
                self.printHelp()
                self.errorExit()
            elif name == r'-s':
                self._source=self.getAbsPath(value)
            elif name == r'-p':
                self._patch=self.getAbsPath(value)
            elif name == r'-o':
                self._opt=value


    # get abs path.
    def getAbsPath(self, path):
        if path[0:1] == r'.':
             path=path.replace(r'.', os.getcwd(), 1)
        return path


    # get dirs of patch path.
    def getDirsOfPatch(self):
        dirs=[]
        for rt, ds, fs in os.walk(self._patch):
            if len(fs) != 0 :
                for f in fs:
                    if os.path.splitext(f)[1] == r'.patch':
                        rt=rt.replace(self._patch, '')
                        dirs.append(rt)
                        break
        if len(dirs) != 0:
            return sorted(dirs)
        else:
            return None


    # run git am to apply all of .patch
    def applyDirsPatch(self, dirs):
        if dirs == None:
            print 'Error, no dir!'
        else:
            for d in dirs:
                print '--------------------------------------------------'
                print 'apply patch: %s\n' % os.path.join(self._source, d)
                cmd='cd %s && git am %s/*.patch' % (os.path.join(self._source, d), os.path.join(self._patch, d))
                subprocess.call(cmd, shell=True)


    # get all of fingerprint HAL prebuild files.
    def getHalPrebuildFiles(self):
        files_of_prebuild=[
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
            src=os.path.join(self._source, f)
            tgt=os.path.join(self._patch, f)
            # create dir
            dt=os.path.split(tgt)[0]
            if os.path.exists(dt) != True:
                os.makedirs(dt)
            # copy file here
            shutil.copy(src, tgt)


    # get all of TA prebuild files.
    def getTaPrebuildFiles(self):
        files_of_prebuild=[
            'obj/trusty/build-sand-x86-64/user_tasks/sand/fpcfingerprint/build/build.elf',
        ]
        # copy files.
        for f in files_of_prebuild:
            src=os.path.join(self._source, f)
            tgt=os.path.join(self._patch, 'fingerprint/fingerprint.elf')
            # create dir
            dt=os.path.split(tgt)[0]
            if os.path.exists(dt) != True:
                os.makedirs(dt)
            # copy file here
            shutil.copy(src, tgt)


    # enterance of app
    def main(self):
        # get user input
        self.getUserInput()

        if self._source == None or self._patch == None or self._opt == None:
            self.errorExit('Error, invalid input, run -h to get help!')

        if self._opt == r'am':
            # get dirs of patch.
            dirs=self.getDirsOfPatch()
            if dirs != None:
                self.applyDirsPatch(dirs)
            else:
                print 'No found .patch file!'
        elif self._opt == r'ghal':
            self.getHalPrebuildFiles()
        elif self._opt == r'gta':
            self.getTaPrebuildFiles()
        else:
            self.errorExit('Error, unsupport %s' % self._opt)

if __name__ == '__main__':
    patch=fingerprintPatch()
    patch.main()
