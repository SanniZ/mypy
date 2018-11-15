# -*- coding: utf-8 -*-
"""
Created on 2018-11-13

@author: Byng Zeng
"""

import re, sys, os, getopt


class CalendarEvent(object):
    def __init__(self):
        self._title=None
        self._date_s=None
        self._date_e=None
        self._time_s=None
        self._time_e=None
        self._summary=None
        self._location=None
        self._description=None
        self._type=''

class Calendar(object):
    RE_DTSTART=r'DTSTART;.+'
    RE_DTEND=r'DTEND;.+'
    RE_DATE=r'\d+'
    RE_TIME_FILTER=r'T\d+'
    RE_TIME=r'\d+'
    RE_LOCATION=r'LOCATION:.+'
    RE_SUMMARY=r'SUMMARY:.+'
    RE_DESCRIPTION=r'DESCRIPTION:.+'
    RE_CALNAME=r'X-WR-CALNAME:.+'

    def __init__(self):
        # init values.
        self._src=None
        self._tgt=None
        self._fmt=None
        self._calName=None
        self._listEvents=[]
        self._listCnt=0
        self._event=CalendarEvent()
        #self._sortKey='DTSTART'
        self._sortReverse=True
        self._multiCombine=False

        # get all of re_compile.
        self._re_dtstart=re.compile(Calendar.RE_DTSTART)
        self._re_dtend=re.compile(Calendar.RE_DTEND)
        self._re_date=re.compile(Calendar.RE_DATE)
        self._re_time_filter=re.compile(Calendar.RE_TIME_FILTER)
        self._re_time=re.compile(Calendar.RE_TIME)
        self._re_location=re.compile(Calendar.RE_LOCATION)
        self._re_sum=re.compile(Calendar.RE_SUMMARY)
        self._re_desc=re.compile(Calendar.RE_DESCRIPTION)
        self._re_calname=re.compile(Calendar.RE_CALNAME)
        # get user options.
        self.getUserOpt()

    def printHelp(self):
        print 'option: -s xxx -t xxx [-f xxx] [-r xxx] [-c]'
        print '  -c:'
        print '    True is combine all of .ics file together, False is not.'
        print '  -f txt/csv:'
        print '    format of output file'
        print '  -r True/False:'
        print '    True is ascending sort, False is descending, default to True.'
        print '  -s xxx.ics or xxx/:'
        print '    xxx/ is a path, xxx.ics is a ics file'
        print '  -t xxx/ or xxx.xxx:'
        print '    xxx/ is is a path, xxx.xxx is the name of target'
        # stop and exit.
        exit()

    def getUserOpt(self):
        try:
            opts, args = getopt.getopt(sys.argv[1:], "hcf:s:t:R:")
        except getopt.GetoptError:
            self.printHelp()
        # process input value
        for name, value in opts:
            if name == r'-h':
                self.printHelp()
            elif name == r'-c':
                self._multiCombine=True
            elif name == r'-f':
                self._fmt=value
            elif name == r'-r':
                if value == r'True':
                    self._sortReverse=True
                else:
                    self._sortReverse=False
            elif name == r'-s':
                self._src=value
            elif name == r'-t':
                self._tgt=value
        # check args.
        if self._src == None or self._tgt == None:
            self.printHelp()

    # get all of .ics file under folder.
    def getFilesOfPath(self):
        self._src=os.path.dirname(self._src)
        return os.listdir(self._src)

    def getOutputFileName(self, fmt):
        if self._tgt.find(r'.%s' % fmt) == -1:
            name=r'%s/%s.%s' % (os.path.dirname(self._tgt), self._calName, fmt)
        else:
            name=r'%s/%s' % (os.path.dirname(self._tgt), self._calName)
        # remove old file.
        if os.path.exists(name) == True:
            os.remove(name)
        # return name of file.
        return name

    # create table header
    def createCSVTitle(self):
        # create title if not set.
        with open(self.getOutputFileName(r'csv'), r'a') as f:
            if self._multiCombine == True:
                f.write('开始日期,结束日期,开始时间,结束时间,地点,事件,描述,类型\n')
            else:
                f.write('开始日期,结束日期,开始时间,结束时间,地点,事件,描述\n')

    # save data to .csv file.
    def saveToCSV(self):
        with open(self.getOutputFileName(r'csv'), r'a') as f:
            for event in self._listEvents:
                # write start of date.
                f.write('%s-%s-%s,' % (event._date_s[0:4], event._date_s[4:6], event._date_s[6:8]))
                # write end of date,start of time,end of time.
                if event._time_s == None or event._time_e == None: # days event: xxxx/xx/xx-xxxx/xx/xx
                    f.write('%s-%s-%s,' % (event._date_e[0:4], event._date_e[4:6], event._date_e[6:8]))
                    f.write(',')
                    f.write(',')
                else: # day event: xxxx/xx/xx xx:xx-xx:xx
                    f.write(',')
                    f.write('%s:%s,' % (event._time_s[0:2], event._time_s[2:4]))
                    f.write('%s:%s,' % (event._time_e[0:2], event._time_e[2:4]))
                # write location.
                if event._location == None:
                    f.write(',')
                else:
                    f.write('%s,' % event._location[len('LOCATION:'):len(event._location)-1])
                # write summary.
                f.write('%s,' % event._summary[len('SUMMARY:'):len(event._summary)-1])
                # write type if it is combine option.
                if self._multiCombine == True:
                    # write description.
                    if event._description == None:
                        f.write(',')
                    else:
                        f.write('%s,' % event._description[len('DESCRIPTION:'):len(event._description)-1])
                    # write type of data.
                    f.write('%s\n' % event._type)
                else:
                    # write description.
                    if event._description == None:
                        f.write('\n')
                    else:
                        f.write('%s\n' % event._description[len('DESCRIPTION:'):len(event._description)-1])

    # save data to .txt file.
    def saveToTXT(self):
        with open(self.getOutputFileName(r'txt'), r'a') as f:
            for event in self._listEvents:
                # write new event.
                f.write('----------------------------------------------\n')
                # write start of date,end of date,start of time,end of time.
                if event._time_s == None or event._time_e == None: # days event: xxxx/xx/xx-xxxx/xx/xx
                    f.write('%s/%s/%s-%s/%s/%s %s\n' % (event._date_s[0:4], event._date_s[4:6], event._date_s[6:8], event._date_s[0:4], event._date_s[4:6], event._date_s[6:8], event._type))
                else: # day event: xxxx/xx/xx xx:xx-xx:xx
                    f.write('%s/%s/%s %s:%s-%s:%s %s\n' % (event._date_s[0:4], event._date_s[4:6], event._date_s[6:8], event._time_s[0:2], event._time_s[2:4], event._time_e[0:2], event._time_e[2:4], event._type))
                # write location.
                if event._location == None:
                    f.write('LOCATION   : \n')
                else:
                    f.write('LOCATION   : %s\n' % event._location[len('LOCATION:'):len(event._location)-1])
                # write summary
                f.write('SUMMARY    : %s\n' % event._summary[len('SUMMARY:'):len(event._summary)-1])
                # write description.
                if event._description == None:
                    f.write('DESCRIPTION:\n')
                else:
                    f.write('DESCRIPTION: %s\n' % event._description[len('DESCRIPTION:'):len(event._description) - 1])

    def printICSContent(self):
        for event in self._listEvents:
            print('----------------------------------------------\n')
            if event._time_s == None or event._time_e == None: # days event: xxxx/xx/xx-xxxx/xx/xx
                print '%s/%s/%s-%s/%s/%s %s\n' % (event._date_s[0:4], event._date_s[4:6], event._date_s[6:8], event._date_s[0:4], event._date_s[4:6], event._date_s[6:8], event._type)
            else: # day event: xxxx/xx/xx xx:xx-xx:xx
                print '%s/%s/%s %s:%s-%s:%s %s\n' % (event._date_s[0:4], event._date_s[4:6], event._date_s[6:8], event._time_s[0:2], event._time_s[2:4], event._time_e[0:2], event._time_e[2:4], event._type)

            if event._location == None:
                print 'LOCATION   : \n'
            else:
                print 'LOCATION   : %s\n' % event._location[len('LOCATION:'):len(event._location)-1]

            print 'SUMMARY    : %s\n' % event._summary[len('SUMMARY:'):len(event._summary)-1]

            if event._description == None:
                print 'DESCRIPTION:\n'
            else:
                print 'DESCRIPTION: %s\n' % event._description[len('DESCRIPTION:'):len(event._description) - 1]

    def sortEvent(self, event):
        return event._date_s

    def formatOutput(self):
        if len(self._listEvents) == 0:
            return
        # sort all of events.
        self._listEvents.sort(key=self.sortEvent, reverse=self._sortReverse)
        # output
        if self._fmt == r'txt':
            self.saveToTXT()
        elif self._fmt == r'csv':
            self.createCSVTitle()
            self.saveToCSV()
        else:
            self.printICSContent()
        # clear all of events.
        self._listEvents=[]

    def insertEvent(self):
        self._listEvents.append(self._event)
        # update for next event.
        self._event=CalendarEvent()

    def processICS(self, ics):
        if os.path.isfile(ics) != True:
            print 'Error, no found %s' % ics
            return

        with open(ics, 'r') as f:
            while True:
                buf=f.readline()
                if len(buf) == 0:
                    break
                # get Calendar Name
                calName=self._re_calname.match(buf)
                if calName != None:
                    self._calName=calName.group()[len('X-WR-CALNAME:'):len(calName.group())-1]
                # get location
                location=self._re_location.match(buf)
                if location != None:
                    self._event._location=location.group()
                # get description
                description=self._re_desc.match(buf)
                if description != None:
                    self._event._description=description.group()
                # get end of date and time
                dt_end=self._re_dtend.match(buf)
                if dt_end != None:
                    # search date.
                    date_e=self._re_date.search(dt_end.group())
                    if date_e != None:
                        # get date
                        self._event._date_e=date_e.group()
                        # check time
                        time_f=self._re_time_filter.search(dt_end.group())
                        if time_f != None:
                            time_e=self._re_time.search(time_f.group())
                            if time_e != None:
                                self._event._time_e=time_e.group()
                # get start of date and time
                dt_start=self._re_dtstart.match(buf)
                if dt_start != None:
                    date_s=self._re_date.search(dt_start.group())
                    if date_s != None:
                        self._event._date_s=date_s.group()
                        # check time
                        time_f=self._re_time_filter.search(dt_start.group())
                        if time_f != None:
                            time_s=self._re_time.search(time_f.group())
                            if time_s != None:
                                self._event._time_s=time_s.group()
                # get summary
                summary=self._re_sum.match(buf)
                if summary != None:
                    self._event._summary=summary.group()
                    # add type of data
                    if self._multiCombine == True:
                        self._event._type=self._calName
                    # event is ready, insert to list now.
                    self.insertEvent()

    def main(self):
        # no .ics, it is a path.
        if self._src.find(r'.ics') != -1:
            self.processICS(self._src)
            self.formatOutput()
        else:
            fs=self.getFilesOfPath()
            for f in fs:
                if self._multiCombine == True:
                    self.processICS(r'%s/%s' % (self._src, f))
                else:
                    self.processICS(r'%s/%s' % (self._src, f))
                    self.formatOutput()
            # get name of tgt
            name=os.path.basename(self._tgt)
            if name == '':
                self._calName=r'Combine'
            else:
                self._calName=name
            # output files.
            self.formatOutput()

if __name__ == '__main__':
    cal=Calendar()
    cal.main()
