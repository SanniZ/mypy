#!/usr/bin/python

# -*- coding: utf-8 -*-
"""
Created on Thu Jul  5 11:21:29 2018

@author: Byng.Zeng
"""
import subprocess
import socket

from debug import Debug as d

class HwInfo(object):
    def __init__(self):
        d.dbg('HwInfo init done!')

    def help(self, cmds):
        for cmd in cmds:
            if cmd == 'help':
                d.info('hwinfo:[ncpu][,ip]')
                d.info('  ncpu: get number of CPU')
                d.info('  ip: get host IP address')

    def get_cups(self, cmds=None):
        cmd = r'cat /proc/cpuinfo | grep "processor"| wc -l'
        d.dbg(cmd)
        return int(subprocess.check_output(cmd, shell=True))

    def get_host_ip(self, cmds=None):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(('8.8.8.8', 80))
            ip = s.getsockname()[0]
        finally:
            s.close()

        return ip

    def hwif_handler(self, cmds):
        for cmd in cmds:
            if cmd == 'ncpu':
                d.info(self.get_cups())
            elif cmd == 'ip':
                d.info(self.get_host_ip())

    def get_cmd_handlers(self, cmd=None):
        return {
            'help' : self.help,
            'hwinfo' : self.hwif_handler,
        }

class FileOps(object):
    def __init__(self):
        d.dbg('FileOps init done!') 

    def help(self, cmds):
        for cmd in cmds:
            if cmd == 'help':
                d.info('del:[xxx][,xxx]')
                d.info('  xxx: xxx file will be delete.')
                d.info('fdel:[path,]file')
                d.info('  path: path to be find, not set to ./')
                d.info('  file: file to be delete.')
                d.info('find:[path,]file')
                d.info('  path: path to find, not set to ./')
                d.info('  file: file to be find.')

    def delete(self, f):
        cmd = r'rm -rf %s' % f
        d.dbg(cmd)
        return subprocess.call(cmd, shell=True)

    def del_handler(self, cmds):
        for cmd in cmds:
            self.delete(cmd)

    def find(self, path, name):
        cmd = r'find %s -name %s' % (path, name)
        d.dbg(cmd)
        return subprocess.call(cmd, shell=True)

    def find_handler(self, cmds):
        d.dbg('find_handler: {}'.format(cmds))
        try:
            n = len(cmds)
            if n == 1:
                self.find('./', cmds[0])
            elif n >= 2:
                self.find(cmds[0], cmds[1])
        except KeyError as e:
            d.err('Error: %s' % e)

    def find_delete(self, path, name):
        cmd = r'find %s -name %s | xargs rm -rf {}' % (path, name)
        d.dbg(cmd)
        return subprocess.call(cmd, shell=True)

    def fdel_handler(self, cmds):
        d.dbg('fdel_handler: {}'.format(cmds))
        try:
            n = len(cmds)
            if n == 1:
                self.find_delete('./', cmds[0])
            elif n >= 2:
                self.find_delete(cmds[0], cmds[1])
        except KeyError as e:
            d.err('Error: %s' % e)

    def get_cmd_handlers(self, cmd=None):
        hdrs = {
            'help' : self.help,
            'del'  : self.del_handler,
            'fdel' : self.fdel_handler,
            'find' : self.find_handler,
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
    hwif = HwInfo()
    fops = FileOps()
    cmdHdr = CmdProcessing()
    cmdHdr.register_cmd_handler(hwif.get_cmd_handlers())
    cmdHdr.register_cmd_handler(fops.get_cmd_handlers())
    cmdHdr.run_sys_input()