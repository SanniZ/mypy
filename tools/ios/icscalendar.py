#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 2018-11-13

@author: Byng Zeng
"""

import re
import os
import subprocess

from pybase.pysys import print_help, print_exit
from pybase.pypath import get_abs_path
from pybase.pyinput import get_input_args
from pybase.pyfile import get_filetype

VERSION = '1.1.0'
AUTHOR = 'Byng.Zeng'

RE_DTSTART = r'DTSTART;.+'
RE_DTEND = r'DTEND;.+'
RE_DATE = r'\d+'
RE_TIME_FILTER = r'T\d+'
RE_TIME = r'\d+'
RE_LOCATION = r'LOCATION:.+'
RE_SUMMARY = r'SUMMARY:.+'
RE_DESCRIPTION = r'DESCRIPTION:.+'
RE_CALNAME = r'X-WR-CALNAME:.+'
RE_END_VEVENT = r'END:VEVENT'

TYPE_ICS = r'ics'
TYPE_CSV = r'csv'
TYPE_TXT = r'txt'


class _ICSCalendarEvent(object):
    def __init__(self):
        self._title = None
        self._date_s = None
        self._date_e = None
        self._time_s = None
        self._time_e = None
        self._summary = None
        self._location = None
        self._description = None
        self._type = ''


class _ICSCalendarRe(object):
    def __init__(self):
        # get all of re_compile.
        self._dt_start = re.compile(RE_DTSTART)
        self._dt_end = re.compile(RE_DTEND)
        self._date = re.compile(RE_DATE)
        self._filter_time = re.compile(RE_TIME_FILTER)
        self._time = re.compile(RE_TIME)
        self._location = re.compile(RE_LOCATION)
        self._summary = re.compile(RE_SUMMARY)
        self._description = re.compile(RE_DESCRIPTION)
        self._end_event = re.compile(RE_END_VEVENT)
        self._cal_name = re.compile(RE_CALNAME)

    def get_cal_name(self, txt):
        return self._cal_name.match(txt)

    def get_location(self, txt):
        return self._location.match(txt)

    def get_description(self, txt):
        return self._description.match(txt)

    def get_dt_end(self, txt):
        return self._dt_end.match(txt)

    def get_date(self, txt):
        return self._date.search(txt)

    def get_time(self, txt):
        time = None
        ftime = self._filter_time.search(txt)
        if ftime:
            time = self._time.search(ftime.group())
        return time

    def get_dt_start(self, txt):
        return self._dt_start.match(txt)

    def get_summary(self, txt):
        return self._summary.match(txt)

    def get_end_event(self, txt):
        return self._end_event.match(txt)


class ICSCalendar(object):

    HELP_MENU = (
        '======================================',
        '     iOS Calender Data Convert',
        '======================================',
        'option:',
        '  -c True/False :',
        '    True is combine all of .ics file together, False is not.',
        '  -f txt/csv :',
        '    format of output file',
        '  -r True/False :',
        '    True is ascending sort, False is descending, default to False.',
        '  -s xxx.ics or xxx/ :',
        '    xxx/ is a path, xxx.ics is a ics file',
        '  -t xxx/ or xxx.xxx :',
        '    xxx/ is is a path, xxx.xxx is the name of target',
    )

    # get all of .ics file under path.
    @staticmethod
    def get_ics_files(path):
        fs = None
        for root, dirs, files in os.walk(path):
            if len(files) != 0:
                for f in files:
                    if get_filetype(f) == TYPE_ICS:
                        if fs is None:
                            fs = list()
                        fs.append(os.path.join(root, f))
        # return all of files.
        return fs

    # get all of .ics with shell find cmd.
    @staticmethod
    def get_ics_files2(path):
        cmd = 'find %s -name *.ics' % path
        try:
            fs = subprocess.check_output(cmd, shell=True)
            fs = list(fs.split())
        except subprocess.CalledProcessError:
            print('No found .ics at %s' % path)
            fs = None
        return fs

    # get all of .ics files.
    @staticmethod
    def get_src_files(path):
        fs = None
        if os.path.exists(path):
            if all((os.path.isfile(path),
                    get_filetype(path) == TYPE_ICS)):
                fs = list()
                fs.append(path)
            elif os.path.isdir(path):
                fs = ICSCalendar.get_ics_files(path)
        # return result.
        return fs

    # make ready for output
    @staticmethod
    def make_output_path(name):
        path = os.path.split(name)[0]
        # make dir for output
        if not os.path.exists(path):
            os.makedirs(path)
        # remove old file.
        if os.path.exists(name):
            os.remove(name)

    # init ICSCalendar
    def __init__(self):
        # init values.
        self._src = None
        self._tgt = None
        self._fmt = None
        self._cal_name = None
        self._events = list()
        self._event_cnt = 0
        self._event = _ICSCalendarEvent()
        # self._sortKey = 'DTSTART'
        self._sort_reverse = False
        self._combine_files = False
        self._re = None

    def get_user_opt(self):
        args = get_input_args('hcf:r:s:t:')
        for k in args.keys():
            if k == r'-h':
                print_help(self.HELP_MENU)
            elif k == r'-c':
                self._combine_files = True
            elif k == r'-f':
                fmt = args['-f'].lower()
                if fmt == TYPE_TXT or fmt == TYPE_CSV:
                    self._fmt = fmt
                else:
                    print_exit("Error, unsupport format!")
            elif k == r'-r':
                if args['-r'] == r'True':
                    self._sort_reverse = True
                else:
                    self._sort_reverse = False
            elif k == r'-s':
                # set _src to list
                if self._src is None:
                    self._src = list()
                # get src files
                fs = self.get_src_files(get_abs_path(args['-s']))
                if fs:
                    # add fs to _src
                    for f in fs:
                        self._src.append(f)
            elif k == r'-t':
                ftype = get_filetype(get_abs_path(args['-t']))
                if ftype in [TYPE_TXT, TYPE_CSV]:
                    self._tgt = get_abs_path(args['-t'])
                    self._combine_files = True
                    self._fmt = ftype
                else:
                    self._tgt = get_abs_path(args['-t'])

    # check input args
    def check_opt_args(self):
        # check src.
        if self._src is None:
            # check current path.
            fs = ICSCalendar.get_ics_files(os.getcwd())
            if fs:
                # set _src to list
                if self._src is None:
                    self._src = list()
                # add fs to _src
                for f in fs:
                    self._src.append(f)

        # check tgt.
        if self._tgt is None:
            self._tgt = os.getcwd()

    # get name of output
    def get_output_name(self, fmt):
        if get_filetype(self._tgt) == fmt:
            name = self._tgt
        elif self._combine_files:
            name = r'%s/%s.%s' % (self._tgt, u'日历', fmt.lower())
        else:
            name = r'%s/%s.%s' % (self._tgt, self._cal_name, fmt.lower())
        # return name of file.
        return name

    # save data to .csv file.
    def save_to_csv(self):
        # get output name
        name = self.get_output_name(TYPE_CSV)
        # ready for write
        ICSCalendar.make_output_path(name)
        # write events.
        with open(name, r'a') as f:
            # create title if not set.
            f.write('开始日期,开始时间,结束日期,结束时间,地点,事件,描述,类型\n')
            # start to write events.
            for event in self._events:
                # start of date.
                f.write('%s-%s-%s,' % (event._date_s[0:4], event._date_s[4:6],
                                       event._date_s[6:8]))
                # start of time
                if event._time_s is None:
                    f.write(',')
                else:
                    f.write('%s:%s,' % (event._time_s[0:2],
                                        event._time_s[2:4]))
                # end of date
                if event._date_e == event._date_s:
                    f.write(',')
                else:
                    f.write('%s-%s-%s,' % (event._date_e[0:4],
                                           event._date_e[4:6],
                                           event._date_e[6:8]))
                # end of time
                if event._time_e is None:
                    f.write(',')
                else:
                    f.write('%s:%s,' % (event._time_e[0:2],
                                        event._time_e[2:4]))
                # write location.
                if event._location is None:
                    f.write(',')
                else:
                    f.write('%s,' % event._location[
                            len('LOCATION:'): len(event._location)-1])
                # write summary.
                f.write('%s,' % event._summary[
                                len('SUMMARY:'):len(event._summary)-1])
                # write description.
                if event._description is None:
                    f.write(',')
                else:
                    f.write('%s,' % event._description[
                            len('DESCRIPTION:'):len(event._description)-1])
                # write type of data.
                f.write('%s\n' % event._type)
        print('output: %s' % name)

    # save data to .txt file.
    def save_to_txt(self):
        # get output name
        name = self.get_output_name(TYPE_TXT)
        # ready for write
        ICSCalendar.make_output_path(name)
        # write events.
        with open(name, r'a') as f:
            for event in self._events:
                f.write('----------------------------------------------\n')
                # date and time.
                if event._date_e == event._date_s:  # at the same day.
                    if event._time_s is None or event._time_e is None:
                        f.write('%s/%s/%s %s\n' % (
                            event._date_s[0:4], event._date_s[4:6],
                            event._date_s[6:8], event._type))
                    else:  # day event: xxxx/xx/xx xx:xx-xx:xx
                        f.write('%s/%s/%s %s:%s-%s:%s %s\n' % (
                            event._date_s[0:4], event._date_s[4:6],
                            event._date_s[6:8],
                            event._time_s[0:2], event._time_s[2:4],
                            event._time_e[0:2], event._time_e[2:4],
                            event._type))
                else:
                    if event._time_s is None or event._time_e is None:
                        f.write('%s/%s/%s-%s/%s/%s %s\n' % (
                            event._date_s[0:4], event._date_s[4:6],
                            event._date_s[6:8], event._date_e[0:4],
                            event._date_e[4:6], event._date_e[6:8],
                            event._type))
                    else:  # day event: xxxx/xx/xx xx:xx-xx:xx
                        f.write('%s/%s/%s %s:%s-%s/%s/%s %s:%s %s\n' % (
                            event._date_s[0:4], event._date_s[4:6],
                            event._date_s[6:8], event._time_s[0:2],
                            event._time_s[2:4], event._date_e[0:4],
                            event._date_e[4:6], event._date_e[6:8],
                            event._time_e[0:2], event._time_e[2:4],
                            event._type))
                # location
                if event._location is None:
                    f.write('LOCATION   : \n')
                else:
                    f.write('LOCATION   : %s\n' % event._location[
                        len('LOCATION:'):len(event._location)-1])
                # summary
                f.write('SUMMARY    : %s\n' % event._summary[
                    len('SUMMARY:'):len(event._summary)-1])
                # description
                if event._description is None:
                    f.write('DESCRIPTION:\n')
                else:
                    f.write('DESCRIPTION: %s\n' % event._description[
                        len('DESCRIPTION:'):len(event._description) - 1])
        print('output: %s' % name)

    # print all of data.
    def print_ics_contents(self):
        for event in self._events:
            print('----------------------------------------------\n')
            # date and time.
            if event._date_e == event._date_s:  # at the same day.
                if event._time_s is None or event._time_e is None:
                    print('%s/%s/%s %s\n' % (
                        event._date_s[0:4], event._date_s[4:6],
                        event._date_s[6:8], event._type))
                else:  # day event: xxxx/xx/xx xx:xx-xx:xx
                    print('%s/%s/%s %s:%s-%s:%s %s\n' % (
                        event._date_s[0:4], event._date_s[4:6],
                        event._date_s[6:8], event._time_s[0:2],
                        event._time_s[2:4], event._time_e[0:2],
                        event._time_e[2:4], event._type))
            else:
                if event._time_s is None or event._time_e is None:
                    print('%s/%s/%s-%s/%s/%s %s\n' % (
                        event._date_s[0:4], event._date_s[4:6],
                        event._date_s[6:8], event._date_e[0:4],
                        event._date_e[4:6], event._date_e[6:8],
                        event._type))
                else:  # day event: xxxx/xx/xx xx:xx-xx:xx
                    print('%s/%s/%s %s:%s-%s/%s/%s %s:%s %s\n' % (
                        event._date_s[0:4], event._date_s[4:6],
                        event._date_s[6:8], event._time_s[0:2],
                        event._time_s[2:4], event._date_e[0:4],
                        event._date_e[4:6], event._date_e[6:8],
                        event._time_e[0:2], event._time_e[2:4],
                        event._type))
            # location
            if event._location is None:
                print('LOCATION   : \n')
            else:
                print('LOCATION   : %s\n' % event._location[
                        len('LOCATION:'):len(event._location)-1])
            # summary
            print('SUMMARY    : %s\n' % event._summary[
                        len('SUMMARY:'):len(event._summary)-1])
            # description
            if event._description is None:
                print('DESCRIPTION:\n')
            else:
                print('DESCRIPTION: %s\n' % event._description[
                        len('DESCRIPTION:'):len(event._description) - 1])

    # call function to output data.
    def format_output(self):
        if len(self._events) == 0:
            return
        # sort all of events.
        self._events.sort(key=lambda event: event._date_s,
                          reverse=self._sort_reverse)
        # output
        if self._fmt == TYPE_TXT:
            self.save_to_txt()
        elif self._fmt == TYPE_CSV:
            self.save_to_csv()
        elif self._fmt is None:
            self.print_ics_contents()
        else:
            print('Error, use -f txt/csv to set format output\n')
            print_help(self.HELP_MENU)

        # clear all of events.
        self._events = list()

    # insert event to evevnt_list.
    def insert_event(self):
        self._events.append(self._event)
        # update for next event.
        self._event = _ICSCalendarEvent()

    # process ics file data.
    def process_ics(self, ics):
        if not os.path.isfile(ics):
            print('Error, no found %s' % ics)
            return False

        with open(ics, 'r') as f:
            while True:
                buf = f.readline()
                if len(buf) == 0:
                    break
                # create _ICSCalendarRe
                if self._re is None:
                    self._re = _ICSCalendarRe()
                # get ICSCalendar Name
                calName = self._re.get_cal_name(buf)
                if calName:
                    self._cal_name = calName.group()[len('X-WR-CALNAME:'):]
                # get location
                location = self._re.get_location(buf)
                if location:
                    self._event._location = location.group()
                # get description
                description = self._re.get_description(buf)
                if description:
                    self._event._description = description.group()
                # get end of date and time
                dt_end = self._re.get_dt_end(buf)
                if dt_end:
                    # search date.
                    date_e = self._re.get_date(dt_end.group())
                    if date_e:
                        # get date of end
                        self._event._date_e = date_e.group()
                        # get time of end
                        time_e = self._re.get_time(dt_end.group())
                        if time_e:
                            self._event._time_e = time_e.group()
                # get start of date and time
                dt_start = self._re.get_dt_start(buf)
                if dt_start:
                    date_s = self._re.get_date(dt_start.group())
                    if date_s:
                        # get date of start
                        self._event._date_s = date_s.group()
                        # get time of start
                        time_s = self._re.get_time(dt_start.group())
                        if time_s:
                            self._event._time_s = time_s.group()
                # get summary
                summary = self._re.get_summary(buf)
                if summary:
                    self._event._summary = summary.group()
                    self._event._type = self._cal_name

                # event is ready, insert to list now.
                end_event = self._re.get_end_event(buf)
                if end_event:
                    self.insert_event()

    # handler for dir files.
    def fs_handler(self):
        # loop for all of files.
        for f in self._src:
            self.process_ics(f)
            # output a .ics data.
            self.format_output()

    # handler for combine dir files.
    def combine_fs_handler(self):
        # loop for all of files.
        for f in self._src:
            self.process_ics(f)
        # output all of data.
        self.format_output()

    # entrance of ICSCalendar
    def main(self):
        # get user options.
        self.get_user_opt()
        # check args.
        self.check_opt_args()
        # start to process data.
        if self._src is None or len(self._src) == 0:
            print_exit('No found .ics, do nothing.')
        elif self._combine_files:
            self.combine_fs_handler()
        else:
            self.fs_handler()


if __name__ == '__main__':
    cal = ICSCalendar()
    cal.main()
