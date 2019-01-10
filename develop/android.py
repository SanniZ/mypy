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
                d.info('  wait: wait for adb device')
                d.info('  root: run adb root')
                d.info('  device: show adb device')
                d.info('  reboot: reboot device')
                d.info('  rebloader: reboot bootloader')
                d.info('  power: sent power on/off key')
                d.info('  back: sent back key')
                d.info('  unlock: sent tap to unlock device')
                d.info('fastboot:[option][,option]')
                d.info('  reboot: reboot device')
                d.info('  lock: lock device')
                d.info('  unlock: unlock device')
                d.info('  xxx: fastboot flash xxx image')
                d.info('logcat: [wait][,root][,clr][,xxx]')
                d.info('  wait: wait for adb device')
                d.info('  root: run adb root')
                d.info('  clr : clear screen display')
                d.info('  xxx : grep xxx')
                d.info('dmesg : [wait][,root][,clr][,xxx]')
                d.info('  wait: wait for adb device')
                d.info('  root: run adb root')
                d.info('  clr : clear screen display')
                d.info('  xxx : grep xxx')
                d.info('kmsg  : [wait][,root][,clr][,xxx]')
                d.info('  wait: wait for adb device')
                d.info('  root: run adb root')
                d.info('  clr : clear screen display')
                d.info('  xxx : grep xxx')


    ADB_FUNCTIONS = {
        'wait' : 'adb wait-for-device',
        'root' : 'adb root',
        'devices' : 'adb devices',
        'reboot' : 'adb reboot',
        'rebloader' : 'adb reboot bootloader',
        'power' : 'adb shell input keyevent 26',
        'back' : 'adb shell input keyevent 4',
        'unlock' : 'adb shell input tap 500 600',
        #'unlock' : 'adb shell input swipe 500 50 500 700',
    }


    def adb_handler(self, cmds):
        d.dbg('adb_handlers: %s' % cmds)
        for cmd in cmds:
            if cmd in self.ADB_FUNCTIONS.keys():
                subprocess.call(self.ADB_FUNCTIONS[cmd], shell=True)

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
                elif text[i] == 'wait':
                    subprocess.call(r'adb wait-for-device', shell=True)
                    continue
                elif text[i] == 'root':
                    subprocess.call(r'adb root', shell=True)
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
