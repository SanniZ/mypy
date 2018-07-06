# -*- coding: utf-8 -*-
"""
Created on Thu Jul  5 11:17:08 2018

@author: Byng.Zeng
"""

import re, sys
#import subprocess
from Debug import Debug
from Android import Android
from Linux import Linux
from Code import Code

class Parser(Debug):
    def __init__(self):
        super(Parser, self).__init__()
        self.dbg('Parser init done.')
        pass

    def help(self, cmds=''):
        pass

    def parser_cmd_args(self, cmds):
        re_dict = re.compile(r'^([a-z0-9]{1,8}):([a-z,_0-9./*]{0,32})$')
        output = {}
        
        if len(cmds) == 0:
            cmds=['help:help']
        
        for cmd in cmds:
            if re.search(':', cmd) != None: # dict type
                k, v = re_dict.match(cmd).groups()
                self.dbg((k,v))
                output[k]= self.parser_args(v)
            elif re.search(',', cmd) != None: # str type
                output = self.parser_args(cmd)
            else:
                output = self.parser_args(cmd)

        self.dbg(output)
        return output
        
    def parser_args(self, argv):
        reArgv = re.compile(r'^([a-z,_0-9./*]{0,32}),([a-z,_0-9./*]{0,32})$')
        index = 0
        output = {}
        while argv:
            if re.search(',', argv) == None:
                output[index] = argv
                argv = 0
            else:
                k, v = reArgv.match(argv).groups()
                argv = v
                output[index] = k
            index += 1

        return output 

class CmdHandler(Parser, Android, Linux, Code):
    # list of support cmd, value: function.
    support_cmd_list = {
        'help'     : None,
        'adb'      : None,
        'fastboot' : None,
        'del'      : None,
        'fdel'     : None,
        'pc'       : None,
        'url'      : None,
    }

    def __init__(self):
        super(CmdHandler, self).__init__()
        self.dbg('CmdHandler init done.')
        pass

    def help(self, cmds=''):
        super(CmdHandler, self).help(cmds)
        for cmd in cmds.values():
            if cmd == 'help':
                self.info('help:help')
                self.info('  help: show help.')
                self.info('adb:[wait][,reboot][,rebloader]')
                self.info('  wait     : wait for adb.')
                self.info('  device   : show adb device.')
                self.info('  reboot   : reboot device')
                self.info('  rebloader: reboot bootloader')
                self.info('fastboot:[reboot][,xxx]')
                self.info('  reboot: reboot device.')
                self.info('  lock  : lock device.')
                self.info('  unlock: unlock device.')
                self.info('  xxx   : fastboot flash xxx')
                self.info('del:xxx[,xxx]')
                self.info('  xxx: delete xxx file.')
                self.info('fdel:path,xxx')
                self.info('  path: path of file will be deleted.')
                self.info('  xxx : file will be delete')
                self.info('pc:cpu')
                self.info('  cpu: get the number of CPU.')
                self.info('url:init/sync')
                self.info('  init: repo init code.')
                self.info('  sync: repo sync code.')
                

    def get_input(self):
        parser = Parser()
        return parser.parser_cmd_args(sys.argv[1:])   

    def check_input(self, cmds):
        self.dbg(cmds)
        for key in cmds.keys():
            if self.support_cmd_list.has_key(key) == False:
                return False
        return True

    def config_handler(self, cmds):
        for key in cmds.iterkeys():
            if key == 'help':
                self.support_cmd_list['help'] = self.help
            elif key == 'adb':
                self.support_cmd_list['adb'] = self.adb_handlers
            elif key == 'fastboot':
                self.support_cmd_list['fastboot'] = self.fastboot_handlers
            elif key == 'del':
                self.support_cmd_list['del'] = self.del_handlers
            elif key == 'fdel':
                self.support_cmd_list['fdel'] = self.fdel_handlers
            elif key == 'pc':
                self.support_cmd_list['pc'] = self.pc_handlers
            elif key == 'url':
                self.support_cmd_list['url'] = self.code_handler
                
    def run(self, cmds):
        self.dbg('CmdHandler.run: {}'.format(cmds))
        for key in cmds.iterkeys():
            if self.support_cmd_list[key] != None:
                f = self.support_cmd_list[key]
                f(cmds[key])

    def main(self):
        inp = self.get_input()
        if inp == None:
            self.err('Error, input invalid!')
            exit()
            
        if self.check_input(inp) == False:
            self.err('Error, check input fail!')
            exit()

        self.config_handler(inp)
        self.run(inp)


if __name__ == '__main__':
    hdr = CmdHandler()
    hdr.main()