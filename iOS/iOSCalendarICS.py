#!/usr/bin/python

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

    TYPE_ICS=r'ICS'
    TYPE_CSV=r'CSV'
    TYPE_TXT=r'TXT'

    # init Calendar
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
        self._sortReverse=False
        self._combineFiles=False

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


    # print help menu.
    def printHelp(self):
        print 'option: -s xxx -t xxx [-f xxx] [-r xxx] [-c]'
        print '  -c:'
        print '    True is combine all of .ics file together, False is not.'
        print '  -f txt/csv:'
        print '    format of output file'
        print '  -r True/False:'
        print '    True is ascending sort, False is descending, default to False.'
        print '  -s xxx.ics or xxx/:'
        print '    xxx/ is a path, xxx.ics is a ics file'
        print '  -t xxx/ or xxx.xxx:'
        print '    xxx/ is is a path, xxx.xxx is the name of target'
        # exit here
        self.stopAndExit()


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
                self._combineFiles=True
            elif name == r'-f':
                self._fmt=value.upper()
                if self._fmt != Calendar.TYPE_TXT or self._fmt != Calendar.TYPE_CSV:
                    self.stopAndExit("Error, unsupport format!")
            elif name == r'-r':
                if value == r'True':
                    self._sortReverse=True
                else:
                    self._sortReverse=False
            elif name == r'-s':
                # set _src to list
                if self._src == None:
                    self._src=[]
                # get src files
                fs=self.getSrcFiles(self.getAbsPath(value))
                if fs != None:
                    # add fs to _src
                    for f in fs:
                        self._src.append(f)
            elif name == r'-t':
                extName=self.getExtName(self.getAbsPath(value))
                if extName == Calendar.TYPE_TXT or extName == Calendar.TYPE_CSV:
                    self._tgt=self.getAbsPath(value)
                    self._combineFiles=True
                    self._fmt=extName
                else:
                    self._tgt=self.getAbsPath(value)


    # check input args
    def checkOptArgs(self):
        # check src.
        if self._src == None:
            # check current path.
            fs=self.getICSFiles(os.getcwd())
            if fs != None:
                # set _src to list
                if self._src == None:
                    self._src=[]
                # add fs to _src
                for f in fs:
                    self._src.append(f)

        # check tgt.
        if self._tgt == None:
            self._tgt=os.getcwd()


    # print error msg and exit
    def stopAndExit(self, msg=None):
        if msg != None:
            print msg
        # stop runing and exit.
        exit()


    # get abs path.
    def getAbsPath(self, path):
        if path[0:1] == r'.':
             path=path.replace(r'.', os.getcwd(), 1)
        return path


    # get external name of file.
    def getExtName(self, f):
        return os.path.splitext(f)[1][1:].upper()

    # get all of .ics file under path.
    def getICSFiles(self, path):
        fs=None
        flist=os.listdir(path)
        for f in flist:
            if self.getExtName(f) == Calendar.TYPE_ICS:
                if fs == None:
                    fs=[]
                fs.append(f)
        # return all of files.
        return fs


    def getSrcFiles(self, path):
        fs=None
        if os.path.exists(path) == True:
            if os.path.isfile(path) == True and self.getExtName(path) == Calendar.TYPE_ICS:
                fs=[]
                fs.append(path)
            elif os.path.isdir(path) == True:
                fs=self.getICSFiles(path)
        # return result.
        return fs

    # get name of output
    def getOutputFileName(self, fmt):
        if self.getExtName(self._tgt) == fmt:
                name=self._tgt
        elif self._combineFiles == True:
	    name=r'%s/%s.%s' % (self._tgt, r'日历', fmt.lower())
        else:
	    name=r'%s/%s.%s' % (self._tgt, self._calName, fmt.lower())
        # return name of file.
        return name


    # make ready for output
    def readyForOutput(self, name):
        path=os.path.split(name)[0]
        if os.path.exists(path) == False:
            os.mkdir(path)
        if os.path.exists(name) == True:
            os.remove(name)


    # save data to .csv file.
    def saveToCSV(self):
        # get output name
        name=self.getOutputFileName(Calendar.TYPE_CSV)
        # ready for write
        self.readyForOutput(name)
        # write events.
        with open(name, r'a') as f:
            # create title if not set.
            f.write('开始日期,开始时间,结束日期,结束时间,地点,事件,描述,类型\n')
            # start to write events.
            for event in self._listEvents:
                # start of date.
                f.write('%s-%s-%s,' % (event._date_s[0:4], event._date_s[4:6], event._date_s[6:8]))
                # start of time
                if event._time_s == None:
                    f.write(',')
                else:
                    f.write('%s:%s,' % (event._time_s[0:2], event._time_s[2:4]))
                # end of date
                if event._date_e == event._date_s:
                    f.write(',')
                else:
                    f.write('%s-%s-%s,' % (event._date_e[0:4], event._date_e[4:6], event._date_e[6:8]))
                # end of time
                if event._time_e == None:
                    f.write(',')
                else:
                    f.write('%s:%s,' % (event._time_e[0:2], event._time_e[2:4]))
                # write location.
                if event._location == None:
                    f.write(',')
                else:
                    f.write('%s,' % event._location[len('LOCATION:'):len(event._location)-1])
                # write summary.
                f.write('%s,' % event._summary[len('SUMMARY:'):len(event._summary)-1])
                # write description.
                if event._description == None:
                    f.write(',')
                else:
                    f.write('%s,' % event._description[len('DESCRIPTION:'):len(event._description)-1])
                # write type of data.
                f.write('%s\n' % event._type)
        print 'output: %s' % name


    # save data to .txt file.
    def saveToTXT(self):
        # get output name
        name=self.getOutputFileName(Calendar.TYPE_TXT)
        # ready for write
        self.readyForOutput(name)
        # write events.
        with open(name, r'a') as f:
            for event in self._listEvents:
                f.write('----------------------------------------------\n')
                # date and time.
                if event._date_e == event._date_s: # at the same day.
                    if event._time_s == None or event._time_e == None: # days event: xxxx/xx/xx
                        f.write('%s/%s/%s %s\n' % (event._date_s[0:4], event._date_s[4:6], event._date_s[6:8], event._type))
                    else: # day event: xxxx/xx/xx xx:xx-xx:xx
                        f.write('%s/%s/%s %s:%s-%s:%s %s\n' % (event._date_s[0:4], event._date_s[4:6], event._date_s[6:8],
                                                               event._time_s[0:2], event._time_s[2:4], event._time_e[0:2], event._time_e[2:4], event._type))
                else:
                    if event._time_s == None or event._time_e == None: # days event: xxxx/xx/xx-xxxx/xx/xx
                        f.write('%s/%s/%s-%s/%s/%s %s\n' % (event._date_s[0:4], event._date_s[4:6], event._date_s[6:8],
                                                            event._date_e[0:4], event._date_e[4:6], event._date_e[6:8], event._type))
                    else: # day event: xxxx/xx/xx xx:xx-xx:xx
                        f.write('%s/%s/%s %s:%s-%s/%s/%s %s:%s %s\n' % (event._date_s[0:4], event._date_s[4:6], event._date_s[6:8], event._time_s[0:2], event._time_s[2:4], 
                                                                        event._date_e[0:4], event._date_e[4:6], event._date_e[6:8], event._time_e[0:2], event._time_e[2:4], event._type))
                # location
                if event._location == None:
                    f.write('LOCATION   : \n')
                else:
                    f.write('LOCATION   : %s\n' % event._location[len('LOCATION:'):len(event._location)-1])
                # summary
                f.write('SUMMARY    : %s\n' % event._summary[len('SUMMARY:'):len(event._summary)-1])
                # description
                if event._description == None:
                    f.write('DESCRIPTION:\n')
                else:
                    f.write('DESCRIPTION: %s\n' % event._description[len('DESCRIPTION:'):len(event._description) - 1])
        print 'output: %s' % name


    # print all of data.
    def printICSContent(self):
        for event in self._listEvents:
            print('----------------------------------------------\n')
            # date and time.
            if event._date_e == event._date_s: # at the same day.
                if event._time_s == None or event._time_e == None: # days event: xxxx/xx/xx
                    print '%s/%s/%s %s\n' % (event._date_s[0:4], event._date_s[4:6], event._date_s[6:8], event._type)
                else: # day event: xxxx/xx/xx xx:xx-xx:xx
                    print '%s/%s/%s %s:%s-%s:%s %s\n' % (event._date_s[0:4], event._date_s[4:6], event._date_s[6:8],
                                                         event._time_s[0:2], event._time_s[2:4], event._time_e[0:2], event._time_e[2:4], event._type)
            else:
                if event._time_s == None or event._time_e == None: # days event: xxxx/xx/xx-xxxx/xx/xx
                    print '%s/%s/%s-%s/%s/%s %s\n' % (event._date_s[0:4], event._date_s[4:6], event._date_s[6:8],
                                                      event._date_e[0:4], event._date_e[4:6], event._date_e[6:8], event._type)
                else: # day event: xxxx/xx/xx xx:xx-xx:xx
                    print '%s/%s/%s %s:%s-%s/%s/%s %s:%s %s\n' % (event._date_s[0:4], event._date_s[4:6], event._date_s[6:8], event._time_s[0:2], event._time_s[2:4],
                                                                  event._date_e[0:4], event._date_e[4:6], event._date_e[6:8], event._time_e[0:2], event._time_e[2:4], event._type)
            # location
            if event._location == None:
                print 'LOCATION   : \n'
            else:
                print 'LOCATION   : %s\n' % event._location[len('LOCATION:'):len(event._location)-1]
            # summary
            print 'SUMMARY    : %s\n' % event._summary[len('SUMMARY:'):len(event._summary)-1]
            # description
            if event._description == None:
                print 'DESCRIPTION:\n'
            else:
                print 'DESCRIPTION: %s\n' % event._description[len('DESCRIPTION:'):len(event._description) - 1]


    # set sort data.
    def sortEvent(self, event):
        return event._date_s


    # call function to output data.
    def formatOutput(self):
        if len(self._listEvents) == 0:
            return
        # sort all of events.
        self._listEvents.sort(key=self.sortEvent, reverse=self._sortReverse)
        # output
        if self._fmt == Calendar.TYPE_TXT:
            self.saveToTXT()
        elif self._fmt == Calendar.TYPE_CSV:
            self.saveToCSV()
        elif self._fmt == None:
            self.printICSContent()
        else:
            print 'Error, use -f txt/csv to set format output\n'
            self.printHelp()

        # clear all of events.
        self._listEvents=[]


    # insert event to evevnt_list.
    def insertEvent(self):
        self._listEvents.append(self._event)
        # update for next event.
        self._event=CalendarEvent()


    # process ics file data.
    def processICS(self, ics):
        if os.path.isfile(ics) != True:
            print 'Error, no found %s' % ics
            return False

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
                    self._event._type=self._calName
                    # event is ready, insert to list now.
                    self.insertEvent()


    # handler for dir files.
    def ICSHandler(self):
        # loop for all of files.
        for f in self._src:
            self.processICS(f)
            # output a .ics data.
            self.formatOutput()


    # handler for combine dir files.
    def CombineICSHandler(self):
        # loop for all of files.
        for f in self._src:
            self.processICS(f)
        # output all of data.
        self.formatOutput()


    # entrance of Calendar
    def main(self):
        # get user options.
        self.getUserOpt()
        # check args.
        self.checkOptArgs()
        # start to process data.
        if self._src == None or len(self._src) == 0:
            self.stopAndExit('No found .ics, do nothing.')
        elif self._combineFiles == True:
            self.CombineICSHandler()
        else:
            self.ICSHandler()



if __name__ == '__main__':
    cal=Calendar()
    cal.main()
