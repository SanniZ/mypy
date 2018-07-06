# -*- coding: utf-8 -*-
"""
Created on Thu Jul  5 11:10:22 2018

@author: Byng.Zeng
"""

import subprocess
from Debug import Debug

class Android(Debug):
    def __init__(self):
        super(Android, self).__init__()
        self.dbg('Android init done.')    
    
    def help(self, cmds=''):
        self.dbg('Android help.')
        
    def adb_wait(self):
        cmd = r'adb wait-for-device'
        self.info(cmd)
        subprocess.call(cmd, shell=True)

    def adb_device(self):
        cmd = r'adb devices'
        self.info(cmd)
        subprocess.call(cmd, shell=True)
        
    def reboot(self):
        cmd = r'adb wait-for-device'
        self.info(cmd)
        subprocess.call(cmd, shell=True)   
        
    def reboot_bootloader(self):
        cmd = r'adb reboot bootloader'
        self.info(cmd)
        subprocess.call(cmd, shell=True)

    def adb_handlers(self, cmds=''):
        self.dbg('adb_handlers: %s' % cmds)
        for cmd in cmds.values():
            if cmd == 'wait':
                self.adb_wait()
            elif cmd == 'device':
                self.adb_device()
            elif cmd == 'reboot':
                self.reboot()
            elif cmd == 'rebloader':
                self.reboot_bootloader()
                
    def fastboot_reboot(self):
        cmd = r'fastboot reboot'
        self.info(cmd)
        subprocess.call(cmd, shell=True)       

    def flash_image(self, pt, image):
        cmd = r'fastboot flash %s %s' % (pt, image)
        self.info(cmd)
        subprocess.call(cmd, shell=True)

    def lock(self, lock=True):
        if lock == True: 
            cmd = r'fastboot flashing lock'
            self.info(cmd)
        else:
            cmd = r'fastboot flashing unlock'
            self.info(cmd)     
        subprocess.call(cmd, shell=True)

    def fastboot_handlers(self, cmds=''):
        for cmd in cmds.values():
            if cmd == 'reboot':
                self.fastboot_reboot()
            elif cmd == 'lock':
                self.lock(True)
            elif cmd == 'unlock':
                self.lock(False)
            else:
                image=r''
                self.flash_image(cmd, cmd, image)

if __name__ == '__main__':
    ad = Android()
    ad.help()