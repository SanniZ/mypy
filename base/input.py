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
        re_dict = re.compile(r'^([\w]+):([\w,\.\/\*]+)$')
        re_argv = re.compile(r'[\w\.\/\*]+')
        output = dict()

        if len(cmds) == 0:
            cmds=['help:help']

        for cmd in cmds:
            if re.search(':', cmd) != None: # dict type
                k, v = re_dict.match(cmd).groups()
                d.dbg((k,v))
                if output.has_key(k):
                    for x in re_argv.findall(v):
                        output[k].append(x)
                else:
                    output[k]= re_argv.findall(v)
            else:
                if output.has_key(None):
                    for x in re_argv.findall(cmd):
                        output[None].append(x)
                else:
                    output[None] = re_argv.findall(cmd)

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