#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul  5 11:21:29 2018

@author: Byng.Zeng
"""

import subprocess
import socket
import re

from develop.debug import Debug as d


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
        hdrs = {
            'help': self.help,
            'hwinfo': self.hwif_handler,
        }
        if not cmd:
            return hdrs
        else:
            if cmd in hdrs:
                return hdrs[cmd]
            else:
                return None


class PSTool(object):

    def help(self, cmds):
        for cmd in cmds:
            if cmd == 'help':
                d.info('ps:kw[,list/kill]')
                d.info('  kw: the keyword will be search.')
                d.info('  list/kill: list/kill the ps.')

    def ps_handler(self, cmds):
        l = len(cmds)
        if l >= 2:
            kw = cmds[0]
            opt = cmds[1]
        else:
            kw = cmds[0]
            opt = 'list'
        # configs
        grep_kw_cmd = 'ps -ax | grep %s' % kw
        pattern_ps = re.compile('(\d+) (pts|\?)')
        # get ps
        while 1:
            output = subprocess.check_output(grep_kw_cmd, shell=True)
            output = output.decode()
            # show pids of keyword.
            if opt in ['list', 'kill']:
                print(output)
                if opt == 'list':
                    break
            # kill pids
            if opt == 'kill':
                result = pattern_ps.findall(output)
                pids = list(map(lambda x: x[0], result))
                print('*****************************************************')
                print(pids)
                opt_k = input('Kill all of Ps(Y/N/O/L):').upper()
                if opt_k == 'Y':  # kill all of pids
                    ps = ''
                    for p in pids:
                        ps += ' %s' % p
                    cmd = 'sudo kill -9 %s' % ps
                    # print(cmd)
                    subprocess.call(cmd, shell=True)
                elif opt_k == 'O':  # options of pids.
                    opt_pids = input('You want to kill(xxx,xxx):')
                    opt_pids = opt_pids.split(',')
                    ps = ''
                    for p in opt_pids:
                        if p in pids:
                            ps += ' %s' % p
                    cmd = 'sudo kill -9 %s' % ps
                    # print(cmd)
                    subprocess.call(cmd, shell=True)
                elif opt_k == 'N':  # cancel.
                    break

    def get_cmd_handlers(self, cmd=None):
        hdrs = {
            'help': self.help,
            'ps': self.ps_handler,
        }
        if not cmd:
            return hdrs
        else:
            if cmd in hdrs:
                return hdrs[cmd]
            else:
                return None


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
            'help': self.help,
            'del': self.del_handler,
            'fdel': self.fdel_handler,
            'find': self.find_handler,
        }
        if not cmd:
            return hdrs
        else:
            if cmd in hdrs:
                return hdrs[cmd]
            else:
                return None

if __name__ == '__main__':
    from cmdprocess.cmdprocessing import CmdProcessing

    # d.set_debug_level('dbg,info,err')
    hwif = HwInfo()
    fops = FileOps()
    ps = PSTool()
    cmdHdr = CmdProcessing()
    cmdHdr.register_cmd_handler(hwif.get_cmd_handlers())
    cmdHdr.register_cmd_handler(fops.get_cmd_handlers())
    cmdHdr.register_cmd_handler(ps.get_cmd_handlers())
    cmdHdr.run_sys_input()
