# -*- coding: utf-8 -*-
"""
Created on Thu Jul  5 11:10:22 2018

@author: Byng.Zeng
"""

import subprocess

class Android(object):
    def __init__(self):
        #print('Android init done.')
        pass    
    
    def help(self, cmds=''):
        for cmd in cmds.values():
            if cmd == 'cfg':
                pass
            else:
                print('make:[xxx,[xxx]]    make xxx image')
                print('flash:[xxx,[xxx]]    flash xxx image')
        print 'Android help'
        
    def wait_adb(self):
        cmd = r'adb wait-for-device'
        subprocess.call(cmd, shell=True)
        
    def reboot_bootloader(self):
        cmd = r'adb reboot bootloader'
        subprocess.call(cmd, shell=True)

    def fastboot_reboot(self):
        cmd = r'fastboot reboot'
        subprocess.call(cmd, shell=True)       

    def flash_image(self, pt, image):
        cmd = r'fastboot flash %s %s' % (pt, image)
        print(cmd)
        subprocess.call(cmd, shell=True)

    def unlock(self):
        cmd = r'fastboot flashing unlock'
        print(cmd)
        subprocess.call(cmd, shell=True)        

    def lock(self):
        cmd = r'fastboot flashing lock'
        print(cmd)
        subprocess.call(cmd, shell=True)

    def make_image(self, images):
        print('Android.makeImage: Nothing')
