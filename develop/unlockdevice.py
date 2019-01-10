#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Created on: 2018-12-28

@author: Zbyng Zeng
"""

import sys
import getopt
import subprocess
import time

class UnlockDevice(object):

    HELP_MENU = (
        '============================================',
        '    UnlockDeviceTest',
        '============================================',
        'options: -t num [-k num,num] [-s n]',
        '  -t num: set times of test',
        '  -k num,num: set position of unlock key',
        '  -s n: current power state: 1 or 0',
    )

    def __init__(self):
        self._unlock_times = 0  # test times.
        self._state = 1 # power on.
        self._key_pos = (620, 920) # key position (620, 920) ,(500, 600)

    def send_power(self):
        cmd = 'adb shell input keyevent 26'
        subprocess.call(cmd, shell=True)

    def send_unlock(self):
        cmd = 'adb shell input tap %s %s' % (self._key_pos[0], self._key_pos[1])
        subprocess.call(cmd, shell=True)


    def get_input_opts(self):
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
                    print('\ndefault set: -k %s,%s -s %s' %
                            (self._key_pos[0], self._key_pos[1], self._state))
                    sys.exit()
                if name == '-t':
                    self._unlock_times = int(value)
                if name == '-k':
                    pos = value.split(',')
                    self._key_pos = tuple(pos)
                if name == '-s':
                    self._state = int(value)
        return opts

    def lock_device(self):
        if self._state:
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
            self.send_power() # power up
            time.sleep(3)
            # unlock device.
            print('unlock')
            self.send_unlock() # unlock
            time.sleep(4)
            # power off to lock device.
            if index < self._unlock_times - 1:
                #print('power off')
                self.send_power() # power down
                time.sleep(1)
        print('all of %d times test done!\n' % self._unlock_times)


if __name__ == '__main__':
    unlock = UnlockDevice()
    # get input args.
    opts = unlock.get_input_opts()
    if not opts:
        sys.exit()
    # run test.
    if unlock._unlock_times:
        # start to test unlock
        unlock.run_unlock_test()
