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
        re_dict = re.compile(r'^([\w]+):([\w,\.\/\*\|#-]+)$')
        re_args = re.compile(r'[\w\.\/\*\|#-]+')
        re_argv = re.compile('^([\w]+)#([\w,\.\/\*\|-]+)$')
        output = dict()

        if len(cmds) == 0:
            cmds=['help:help']

        for cmd in cmds:
            dict_cmds = re_dict.match(cmd)
            if dict_cmds != None: # dict type
                k, v = dict_cmds.groups()
                d.dbg((k,v))
                if k in output:
                    for x in re_args.findall(v):
                        output[k].append(x)
                else:
                    output[k] = re_args.findall(v)
            else:
                k = None
                if k in output:
                    for x in re_args.findall(cmd):
                        output[k].append(x)
                else:
                    output[k] = re_args.findall(cmd)

            # parse # argv
            list_argv = output[k]
            for index in range(len(list_argv)):
                find_argv = re_argv.match(list_argv[index])
                if find_argv != None:
                    dict_argv = dict()
                    argv = find_argv.groups()
                    dict_argv[argv[0]] = list(argv[1:])
                    list_argv[index] = dict_argv

        d.dbg('parser_cmd_args(): %s' % output)
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
