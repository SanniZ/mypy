#!/usr/bin/env python
# -*- coding: UTF-8 -*-

AUTHOR  = 'Byng.Zeng'
VERSION = '1.0.0'

import os
import sys
import getopt


# ===========================================
# usage
# ===========================================
def print_usage():
    USAGES = [
        '=====================================================',
        '    %s  - %s' % (os.path.splitext(os.path.basename(__file__))[0], VERSION),
        '=====================================================',
        'merge widgets.',
        '',
        'usage:  python %s option' % os.path.basename(__file__),
        '',
        'option:',
        ' -w module | --widget=module : module name',
        ' -f name   | --file=name   : name of file to be saved.',
        '',
        'Sample:',
        '  python %s -w mic1.py -w audio-record.py -f d:/mic1-record.py' % os.path.basename(__file__),
    ]
    for txt in USAGES:
        print(txt)


# ===========================================
# function APIs
# ===========================================
def write(widgets, file):
    with open(file, 'w') as fd:
        fd.write("widgets = {\n")
        fd.write("    'widgets': [\n")
        for w in widgets['widgets']:
            fd.write("        '%s',\n" % w)
        fd.write("               ],\n")
        fd.write("\n")

        fd.write("    'enable': [\n")
        for w in widgets['enable']:
            fd.write("        '%s',\n" % w)
        fd.write("     ],\n")
        fd.write("\n")

        fd.write("    'disable': [\n")
        for w in widgets['disable']:
            fd.write("        '%s',\n" % w)
        fd.write("    ],\n")
        fd.write("}")


def join(widgets):
    ws = None
    for w in widgets:
        if not ws:
            ws = w
            continue
        for i in range(len(w['widgets'])):
            ws['widgets'].append(''.join("%s" % w['widgets'][i]))
            ws['enable'].append(''.join("%s" % w['enable'][i]))
            ws['disable'].append(''.join("%s" % w['disable'][i]))
    return ws


def main(opts=None):
    # check opts.
    if not opts:  # get opts.
        try:
            opts, args = getopt.getopt(sys.argv[1:], 'hw:o:', ['help', 'widget=', 'file='])
        except getopt.GetoptError as e:
            print(str(e))
            print_usage()
            return False
        # if args:
        #     print('unknown %s, -h for help' % args)
        #     return False
    widgets = list()
    fname = None
    if not opts:
        print_usage()
        return False
    else:
        for opt in opts:
            if opt[0] in ['-w', '--widget']:  # load widgets.
                sys.path.append(os.path.dirname(opt[1]))  # append path of module.
                try:
                    module = __import__(os.path.basename(opt[1]).replace('.py', ''))  # import module
                except ModuleNotFoundError as e:
                    print(str(e))
                    return False
                widgets.append(module.widgets)  # set widgets
            elif opt[0] in ['-f', '--file']:  # set debug mode
                fname = os.path.abspath(opt[1])
            else:
                print_usage()
                return False
    if not fname:
        for opt in opts:
            if opt[0] in ['-w', '--widget']:
                if not fname:
                    fname = os.path.basename(opt[1]).replace('.py', '')
                else:
                    fname += '-' + os.path.basename(opt[1]).replace('.py', '')
        fname += '.py'
    if all(widgets):
        write(join(widgets), fname)
        print("output: %s" % fname)
    return True


# ===========================================
# entrance
# ===========================================
if __name__ == '__main__':
    main()