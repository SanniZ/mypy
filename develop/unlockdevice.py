#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on: 2018-12-28

@author: Byng Zeng
"""

import sys
import getopt
import subprocess
import time

VERSION = '1.1.1'
AUTHOR = 'Byng.Zeng'


class UnlockDevice(object):

    HELP_MENU = (
        '============================================',
        '    UnlockDevice - %s' % VERSION,
        '',
        '    @Author: %s' % AUTHOR,
        '    Copyright (c) %s studio' % AUTHOR,
        '============================================',
        'options: -t num [-k num,num] [-s n]',
        '  -t num: set times of test',
        '  -k num,num: set position of unlock key',
        '  -s n: current power state: 1 or 0',
    )

    def execute_shell(self, cmd):
        try:
            data = subprocess.check_output(cmd, shell=True)
        except subprocess.CalledProcessError as e:
            return -1, str(e)
        else:
            return 0, data

    def __init__(self):
        self._unlock_times = 0  # test times.
        self._power_on = 1  # power on.
        self._key_pos = (620, 920)  # key position (620, 920) ,(500, 600)

    def send_power(self):
        cmd = 'adb shell input keyevent 26'
        rescode, data = self.execute_shell(cmd)
        if rescode < 0:
            print('stop, send power failed.')
            sys.exit()

    def send_unlock(self):
        cmd = 'adb shell input tap %s %s' % (
                self._key_pos[0], self._key_pos[1])
        rescode, data = self.execute_shell(cmd)
        if rescode < 0:
            print('stop, send unlock failed.')
            sys.exit()

    def get_input_args(self):
        try:
            opts, args = getopt.getopt(sys.argv[1:], 'ht:k:s:')
        except getopt.GetoptError as e:
            print(str(e))
            opts = None
        else:
            for name, value in opts:
                if name == '-h':
                    for usage in self.HELP_MENU:
                        print(usage)
                    print('\ndefault set: -k %s,%s -s %s' % (
                        self._key_pos[0], self._key_pos[1], self._power_on))
                    sys.exit()
                if name == '-t':
                    self._unlock_times = int(value)
                if name == '-k':
                    pos = value.split(',')
                    self._key_pos = tuple(pos)
                if name == '-s':
                    self._power_on = int(value)
        return opts

    def lock_device(self):
        if self._power_on:
            # power down
            self.send_power()
            time.sleep(2)

    def run_unlock_test(self):
        # first to lock device.
        self.lock_device()
        # start to test unlock device.
        for index in range(self._unlock_times):
            print('Test: %d/%d' % (index + 1, self._unlock_times))
            print('power up')
            self.send_power()  # power up
            time.sleep(3)
            # unlock device.
            print('unlock')
            self.send_unlock()  # unlock
            time.sleep(4)
            # power off to lock device.
            if index < self._unlock_times - 1:
                # print('power off')
                self.send_power()  # power down
                time.sleep(1)
        print('all of %d times test done!\n' % self._unlock_times)


if __name__ == '__main__':
    unlock = UnlockDevice()
    # get input args.
    args = unlock.get_input_args()
    if args:
        if unlock._unlock_times:
            unlock.run_unlock_test()
