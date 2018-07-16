#!/usr/bin/python

# -*- coding: utf-8 -*-
"""
Created on Thu Jul  5 11:10:22 2018

@author: Byng.Zeng
"""

import subprocess
from debug import Debug as d

class Android(object):
    def __init__(self):
        d.dbg('Android init done.')    
    
    def help(self, cmds):
        for cmd in cmds:
            if cmd == 'help':
                d.info('adb:[option][,option]')
                d.info('  [option]:')
                d.info('  wait: wait for adb device')
                d.info('  root: run adb root')
                d.info('  device: show adb device')
                d.info('  reboot: reboot device')
                d.info('  rebloader: reboot bootloader')
                d.info('fastboot:[option][,option]')
                d.info('  [option]:')
                d.info('  reboot: reboot device')
                d.info('  lock: lock device')
                d.info('  unlock: unlock device')
                d.info('  xxx: fastboot flash xxx image')

    def adb_wait(self):
        cmd = r'adb wait-for-device'
        d.info(cmd)
        subprocess.call(cmd, shell=True)

    def adb_root(self):
        cmd = r'adb root'
        d.dbg(cmd)
        subprocess.call(cmd, shell=True)

    def adb_device(self):
        cmd = r'adb devices'
        d.dbg(cmd)
        subprocess.call(cmd, shell=True)
        
    def reboot(self):
        cmd = r'adb reboot'
        d.dbg(cmd)
        subprocess.call(cmd, shell=True)   
        
    def reboot_bootloader(self):
        cmd = r'adb reboot bootloader'
        d.info(cmd)
        subprocess.call(cmd, shell=True)

    def adb_handler(self, cmds):
        d.dbg('adb_handlers: %s' % cmds)
        for cmd in cmds:
            if cmd == 'wait':
                self.adb_wait()
            elif cmd == 'root':
                self.adb_root()
            elif cmd == 'device':
                self.adb_device()
            elif cmd == 'reboot':
                self.reboot()
            elif cmd == 'rebloader':
                self.reboot_bootloader()
                
    def fastboot_reboot(self):
        cmd = r'fastboot reboot'
        d.info(cmd)
        subprocess.call(cmd, shell=True)       

    def flash_image(self, pt, image):
        cmd = r'fastboot flash %s %s' % (pt, image)
        d.info(cmd)
        subprocess.call(cmd, shell=True)

    def lock(self, lock=True):
        if lock == True: 
            cmd = r'fastboot flashing lock'
            d.info(cmd)
        else:
            cmd = r'fastboot flashing unlock'
            d.info(cmd)     
        subprocess.call(cmd, shell=True)

    def fastboot_handler(self, cmds):
        for cmd in cmds:
            if cmd == 'reboot':
                self.fastboot_reboot()
            elif cmd == 'lock':
                self.lock(True)
            elif cmd == 'unlock':
                self.lock(False)
            else:
                image=r''
                self.flash_image(cmd, cmd, image)

    def get_cmd_handlers(self, cmd=None):
        hdrs = {
            'help' : self.help,
            'adb' : self.adb_handler,
            'fastboot' : self.fastboot_handler,
        }
        if cmd == None:
            return hdrs
        else:
            if hdrs.has_key(cmd) == True:
                return hdrs[cmd]
            else:
                return None


if __name__ == '__main__':
    from cmdprocessing import CmdProcessing

    #d.set_debug_level('dbg,info,err')
    ad = Android()
    cmdHdr = CmdProcessing()
    cmdHdr.register_cmd_handler(ad.get_cmd_handlers())
    cmdHdr.run_sys_input()
