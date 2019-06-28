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

VERSION = '2.0.1'
AUTHOR = 'Byng.Zeng'


############################################################################
#            Function APIs
############################################################################

def execute_shell(cmd):
    try:
        data = subprocess.check_output(cmd, shell=True)
    except subprocess.CalledProcessError as e:
        return -1, str(e)
    else:
        return 0, data


def send_power_key():
    cmd = 'adb shell input keyevent 26'
    rescode, data = execute_shell(cmd)
    if rescode < 0:
        print('stop, send power failed.')
        sys.exit()


def send_unlock_tap(key_pos):
    cmd = 'adb shell input tap %s %s' % (
            key_pos[0], key_pos[1])
    rescode, data = execute_shell(cmd)
    if rescode < 0:
        print('stop, send unlock failed.')
        sys.exit()


def lock_device(nsleep=1):
    send_power_key()
    time.sleep(nsleep)


############################################################################
#            UnlockDevice class
############################################################################

class UnlockDeviceTest(object):
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
        '  -u 1/0: send key to unlock device.',
        '  -w n,m,j: power on, off and unlock waitting time.'
    )

    def __init__(self):
        self._unlock_times = 0  # test times.
        self._power_on = 1  # power on.
        self._key_pos = (620, 920)  # key position (620, 920) ,(500, 600)
        self._auto_unlock = False
        self._power_up_time = 3
        self._power_off_time = 1
        self._unlock_time = 4

    def get_input_args(self):
        try:
            opts, args = getopt.getopt(sys.argv[1:], 'ht:k:s:u:w:')
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
                elif name == '-t':
                    self._unlock_times = int(value)
                elif name == '-k':
                    pos = value.split(',')
                    self._key_pos = tuple(pos)
                elif name == '-s':
                    self._power_on = int(value)
                elif name == '-u':
                    if value.upper() in ['1', 'TRUE']:
                        self._auto_unlock = True
                    else:
                        self._auto_unlock = False
                elif name == '-w':
                    data = value.split(',')
                    if len(data) >= 3:
                        self._power_up_time = int(data[0])
                        self._power_off_time = int(data[1])
                        self._unlock_time = int(data[2])
                    else:
                        inp = input(
                         '-w error, set default (%d, %d, %d) to run(Y/N)?' %
                         (self._power_up_time,
                          self._power_off_time, self._unlock_time))
                        if inp.upper() != 'Y':
                            sys.exit()
        return opts

    def run_unlock_test(self):
        # first to lock device.
        if self._power_on:
            lock_device(self._power_off_time)
        # start to test unlock device.
        for index in range(self._unlock_times):
            print('Test: %d/%d' % (index + 1, self._unlock_times))
            print('power up')
            send_power_key()  # power up
            time.sleep(self._power_up_time)
            # unlock device.
            print('unlock')
            if self._auto_unlock:
                send_unlock_tap(self._key_pos)  # unlock
            time.sleep(self._unlock_time)
            # power off to lock device.
            if index < self._unlock_times - 1:
                # print('power off')
                send_power_key()  # power off
                time.sleep(self._power_off_time)
        print('all of %d times test done!\n' % self._unlock_times)

    def main(self):
        # get input args.
        args = self.get_input_args()
        if args:
            if self._unlock_times:
                self.run_unlock_test()


############################################################################
#               main entrance
############################################################################

if __name__ == '__main__':
    unlock_test = UnlockDeviceTest()
    unlock_test.main()
