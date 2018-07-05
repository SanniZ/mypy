# -*- coding: utf-8 -*-
"""
Created on Thu Jul  5 11:17:08 2018

@author: Byng.Zeng
"""

import re, sys

class Parser(object):
    def __init__(self):
        #print('Parser init done.')
        pass
    
    def help(self, cmds=''):
        for cmd in cmds.values():
            if cmd == 'cfg':
                pass
            else:
                pass
        
    def parser_cmd_args(self, cmds):
        re_dict = re.compile(r'^([a-z0-9]{1,8}):([a-z,_0-9]{0,32})$')
        output = {}
        
        for cmd in cmds:
            if re.search(':', cmd) != None: # dict type
                k, v = re_dict.match(cmd).groups()
                #print k,v
                output[k]= self.parser_args(v)
            elif re.search(',', cmd) != None: # str type
                output = self.parser_args(cmd)
            else:
                output = self.parser_args(cmd)

        #print(output)
        return output
        
    def parser_args(self, argv):
        reArgv = re.compile(r'^([a-z]{1,8}),([a-z,_]{0,32})$')
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

class CmdHandler(Parser):
    # list of support cmd, value: function.
    supportCmds = {
        'help'  : None,
        'url'   : None,
        'flash' : None,
        'make'  : None,
        'rm'    : None,
        'fw'    : None,
        'ioc'   : None,
    }

    def __init__(self):
        super(CmdHandler, self).__init__()
        #print('CmdHandler init done.')
        pass

    def help(self, cmds=''):
        for cmd in cmds.values():
            if cmd == 'cfg':
                pass
            else:
                pass

    def get_input(self):
        parser = Parser()
        return parser.parser_cmd_args(sys.argv[1:])   

    def check_input(self, cmds):
        #print(cmds)
        return True

    def config_handler(self, cmds):
        #print(cmds)
        pass
                
    def run(self, cmds):
        #print(cmds)
        pass

    def main(self):
        inp = self.get_input()
        if inp == None:
            print('Error, input invalid!')
            exit()
            
        if self.check_input(inp) == False:
            print('Error, check input fail!')
            exit()

        self.config_handler(inp)
        self.run(inp)


if __name__ == '__main__':
    hdr = CmdHandler()
    hdr.main(sys.argv[1:])