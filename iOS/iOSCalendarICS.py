# -*- coding: utf-8 -*-
"""
Created on 2018-11-13

@author: Byng Zeng
"""

import re, sys, getopt

class iOSCalendarICS(object):
    RE_DT_START=r'DTSTART;.+'
    RE_DT_END=r'DTEND;.+'
    RE_DATE=r'\d+'
    RE_TIME_FILTER=r'T\d+'
    RE_TIME=r'\d+'
    RE_LOCATION=r'LOCATION:.+'
    RE_SUMMARY=r'SUMMARY:.+'
    RE_DESCRIPTION=r'DESCRIPTION:.+'
    RE_TITLE=r'X-WR-CALNAME:.+'

    def __init__(self):
        self._src=None
        self._out=None
        self._fmt=None
        self._csvTitle=False

        self._title=None
        self._date_s=None
        self._date_e=None
        self._time_s=None
        self._time_e=None
        self._summary=None
        self._location=None
        self._description=None

        self._re_dt_start=re.compile(iOSCalendarICS.RE_DT_START)
        self._re_dt_end=re.compile(iOSCalendarICS.RE_DT_END)
        self._re_date=re.compile(iOSCalendarICS.RE_DATE)
        self._re_time_filter=re.compile(iOSCalendarICS.RE_TIME_FILTER)
        self._re_time=re.compile(iOSCalendarICS.RE_TIME)
        self._re_loc=re.compile(iOSCalendarICS.RE_LOCATION)
        self._re_sum=re.compile(iOSCalendarICS.RE_SUMMARY)
        self._re_desc=re.compile(iOSCalendarICS.RE_DESCRIPTION)
        self._re_title=re.compile(iOSCalendarICS.RE_TITLE)

        self.getUserOpt()

    def printHelp(self):
        print 'option: -s xxx -o xxx -f xxx'
        print '  -s file:'
        print '    set the file of .ics'
        print '  -o path:'
        print '    set the path of output'
        print '  -f txt/csv:'
        print '    set the format of output'

    def getUserOpt(self):
        try:
            opts, args = getopt.getopt(sys.argv[1:], "hf:o:s:")
        except getopt.GetoptError:
            # print help information and exit:
            self.printHelp()

        # get opt and set values.
        for name, value in opts:
            if name == r'-s':
                self._src=value
            elif name == r'-o':
                self._out=value
            elif name == r'-f':
                self._fmt=value

    # reset all of event values.
    def reset(self):
        self._date_s=None
        self._date_e=None
        self._time_s=None
        self._time_e=None
        self._summary=None
        self._location=None
        self._description=None

    # create Title of csv.
    def createCSVTitle(self):
        # create title if not set.
        if self._csvTitle != True:
            with open(r'%s/%s.csv' % (self._out, self._title), r'a') as w:
                w.write('开始日期,')
                w.write('结束日期,')
                w.write('开始时间,')
                w.write('结束时间,')
                w.write('地点,')
                w.write('事件,')
                w.write('描述\n')

            self._csvTitle=True

    def saveToCSV(self, date_s, date_e, time_s, time_e, location, summary, description):
        with open(r'%s/%s.csv' % (self._out, self._title), r'a') as w:
            w.write('%s-%s-%s,' % (date_s[0:4], date_s[4:6], date_s[6:8]))

            if time_s == None or time_e == None:
                w.write('%s-%s-%s,' % (date_e[0:4], date_e[4:6], date_e[6:8]))
                w.write(',')
                w.write(',')
            else:
                w.write(',')
                w.write('%s:%s,' % (time_s[0:2], time_s[2:4]))
                w.write('%s:%s,' % (time_e[0:2], time_e[2:4]))

            if location == None:
                w.write(',')
            else:
                w.write('%s,' % location[len('LOCATION:'):len(location)-1])

            w.write('%s,' % summary[len('SUMMARY:'):len(summary)-1])

            if description == None:
                w.write('\n')
            else:
                w.write('%s\n' % description[len('DESCRIPTION:'):len(description)-1])

    def saveToTXT(self, date_s, date_e, time_s, time_e, location, summary, description):
        with open(r'%s/%s.txt' % (self._out, self._title), r'a') as w:
            w.write('-----------------------\n')
            if time_s == None or time_e == None:
                w.write('%s/%s/%s-%s/%s/%s\n' % (date_s[0:4], date_s[4:6], date_s[6:8], date_s[0:4], date_s[4:6], date_s[6:8]))
            else:
                w.write('%s/%s/%s %s:%s-%s:%s\n' % (date_s[0:4], date_s[4:6], date_s[6:8], time_s[0:2], time_s[2:4], time_e[0:2], time_e[2:4]))

            if location == None:
                w.write('LOCATION   : \n')
            else:
                w.write('LOCATION   : %s\n' % location[len('LOCATION:'):len(location)-1])

            w.write('SUMMARY    : %s\n' % summary[len('SUMMARY:'):len(summary)-1])

            if self._description == None:
                w.write('DESCRIPTION:\n')
            else:
                w.write('DESCRIPTION: %s\n' % description[len('DESCRIPTION:'):len(description) - 1])

    def printICSContent(self, date_s, date_e, time_s, time_e, location, summary, description):
        print('-----------------------')
        if time_s == None or time_e == None:
            print '%s/%s/%s-%s/%s/%s\n' % (date_s[0:4], date_s[4:6], date_s[6:8], date_s[0:4], date_s[4:6], date_s[6:8])
        else:
            print '%s/%s/%s %s:%s-%s:%s\n' % (date_s[0:4], date_s[4:6], date_s[6:8], time_s[0:2], time_s[2:4], time_e[0:2], time_e[2:4])

        if location == None:
            print 'LOCATION   : \n'
        else:
            print 'LOCATION   : %s\n' % location[len('LOCATION:'):len(location)-1]

        print 'SUMMARY    : %s\n' % summary[len('SUMMARY:'):len(summary)-1]

        if self._description == None:
            print 'DESCRIPTION:\n'
        else:
            print 'DESCRIPTION: %s\n' % description[len('DESCRIPTION:'):len(description) - 1]

    def processICS(self):
        with open(self._src, 'r') as f:
            while True:
                buf=f.readline()
                if len(buf) == 0:
                    break
                # get Title
                title=self._re_title.match(buf)
                if title != None:
                    self._title=title.group()[13:]
                    self._title=self._title[0:len(self._title)-1]
                # get end of date and time
                dt_end=self._re_dt_end.match(buf)
                if dt_end != None:
                    # search date.
                    date_e=self._re_date.search(dt_end.group())
                    if date_e != None:
                        # get date
                        self._date_e=date_e.group()
                        # check time
                        time_f=self._re_time_filter.search(dt_end.group())
                        if time_f == None:
                            self._time_e=None
                        else:
                            time_e=self._re_time.search(time_f.group())
                            self._time_e=time_e.group()

                # get start of date and time
                dt_start=self._re_dt_start.match(buf)
                if dt_start != None:
                    date_s=self._re_date.search(dt_start.group())
                    if date_s != None:
                        self._date_s=date_s.group()
                        time_f=self._re_time_filter.search(dt_start.group())
                        if time_f == None:
                            self._time_s=None
                        else:
                            time_s=self._re_time.search(time_f.group())
                            self._time_s=time_s.group()
                # get summary
                summary=self._re_sum.match(buf)
                if summary != None:
                    self._summary=summary.group()
                    # all of info are ready, process them here.
                    if self._fmt == r'txt':
                        self.saveToTXT(self._date_s, self._date_e, self._time_s, self._time_e, self._location, self._summary, self._description)
                    elif self._fmt == r'csv':
                        self.createCSVTitle()
                        self.saveToCSV(self._date_s, self._date_e, self._time_s, self._time_e, self._location, self._summary, self._description)
                    else:
                        self.printICSContent(self._date_s, self._date_e, self._time_s, self._time_e, self._location, self._summary, self._description)
                    # reset args for next.
                    self.reset()
                # get location
                location=self._re_loc.match(buf)
                if location != None:
                    self._location=location.group()
                # get description
                description=self._re_desc.match(buf)
                if description != None:
                    self._description=description.group()

    def main(self):
        self.processICS()

if __name__ == '__main__':
    iOSCalendarICS().main()