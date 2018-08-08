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
                d.info('log:logcat/dmesg/kmsg[,xxx]')
                d.info('  logcat: get logcat debug info')
                d.info('  dmesg : get dmesg debug info')
                d.info('  kmsg  : get kmsg debug info')
                d.info('  xxx   : grep xxx debug info')

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

    def print_log(self, log_type, text=None):
        if log_type == 'logcat':
            cmd = 'adb logcat'
        elif log_type == 'dmesg':
            cmd = 'adb shell dmesg'
        elif log_type == 'kmsg':
            cmd = 'adb shell cat /proc/kmsg'
        else:
            d.err('unknown type!')
            return

        if text != None and len(text) != 0:
            filter_cnt=0
            for i in range(len(text)):
                if text[i] == 'all':
                    cmd = r' {}'.format(cmd)
                    break;
                elif text[i] == 'root':
                    subprocess.call(r'adb root', shell=True)
                    continue
                elif text[i] == 'reset':
                    subprocess.call(r'reset', shell=True)
                    continue
                elif text[i] == 'clear' or text[i] == 'clr':
                    subprocess.call(r'clear', shell=True)
                    continue
                else:
                    if filter_cnt == 0:
                        txt = text[i]
                    else:
                        txt=r'{}|{}'.format(txt, text[i])
                    filter_cnt+=1

            cmd = r'{} | grep --color -iE "{}"'.format(cmd, txt)
            d.info(cmd)
            #self.adb_root()
            subprocess.call(cmd, shell=True)

    def logcat_handlers(self,cmds):
        self.print_log('logcat', cmds)

    def dmesg_handlers(self,cmds):
        self.print_log('dmesg', cmds)

    def kmsg_handlers(self,cmds):
        self.print_log('kmsg', cmds)

    def get_cmd_handlers(self, cmd=None):
        hdrs = {
            'help' : self.help,
            'adb' : self.adb_handler,
            'fastboot' : self.fastboot_handler,
            'logcat' : self.logcat_handlers,
            'dmesg'  : self.dmesg_handlers,
            'kmsg'   : self.kmsg_handlers,
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
