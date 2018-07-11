# -*- coding: utf-8 -*-
"""
Created on Mon Jul  9 09:41:13 2018

@author: Byng.Zeng
"""

import re, sys
from debug import Debug as d

class Parser(object):
    def __init__(self):
        d.dbg('Parser init done.')   

    def parser_cmd_args(self, cmds):
        re_dict = re.compile(r'^([a-z0-9]{1,8}):([a-z,_0-9./*]{0,32})$')
        output = {}

        if len(cmds) == 0:
            cmds=['help:help']

        for cmd in cmds:
            if re.search(':', cmd) != None: # dict type
                k, v = re_dict.match(cmd).groups()
                d.dbg((k,v))
                output[k]= self.parser_args(v)
            elif re.search(',', cmd) != None: # str type
                output = self.parser_args(cmd)
            else:
                output = self.parser_args(cmd)

        d.dbg(output)
        return output

    def parser_args(self, argv):
        reArgv = re.compile(r'^([a-z,_0-9./*]{0,32}),([a-z,_0-9./*]{0,32})$')
        output = []
        while argv:
            if re.search(',', argv) == None:
                output.append(argv)
                argv = 0
            else:
                k, v = reArgv.match(argv).groups()
                argv = v
                output.append(k)

        d.dbg(output)
        return output 

class Input(Parser):
    def __init__(self):
        d.dbg('Input init done.')
        pass

    # input: xxx:xxx,xxx
    # output: xxx:[xxx, xxx, xxx]
    def get_input(self):
        parser = Parser()
        return parser.parser_cmd_args(sys.argv[1:])