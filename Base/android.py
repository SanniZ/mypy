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
        self._cmd_handlers = {
            'help' : self.help,
            'adb' : self.adb_handler,
            'fastboot' : self.fastboot_handler,
        }
        d.dbg('Android init done.')    
    
    def help(self, cmds):
        for cmd in cmds.values():
            if cmd == 'help':
                d.info('adb:[option][,option]')
                d.info('option:')
                d.info('  wait: wait for adb device')
                d.info('  device: show adb device')
                d.info('  reboot: reboot device')
                d.info('  rebloader: reboot bootloader')
                d.info('fastboot:[option][,option]')
                d.info('option:')
                d.info('  reboot: reboot device')
                d.info('  lock: lock device')
                d.info('  unlock: unlock device')
                d.info('  xxx: fastboot flash xxx image')

    def adb_wait(self):
        cmd = r'adb wait-for-device'
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

    def get_handler(self, cmd):
        if cmd == 'all':
            return self._cmd_handlers
        elif self._cmd_handlers.has_key(cmd) == True:
            return self._cmd_handlers[cmd]
        else:
            return None


if __name__ == '__main__':
    from input import Input
    from cmdprocessing import CmdProcessing

    #d.set_debug_level('dbg,info,err')
    cmds_list = {} 
    
    ad = Android()
    cmds_list['help'] = ad.get_handler('help')
    cmds_list['adb'] = ad.get_handler('adb')
    cmds_list['fastboot'] = ad.get_handler('fastboot')
   
    cmdHdr = CmdProcessing()
    for key in cmds_list.iterkeys():
        cmdHdr.register_cmd_handler(key, cmds_list[key])
    
    inp = Input()
    input_dict = inp.get_input()
    cmdHdr.run(input_dict)