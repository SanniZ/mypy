#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on 2018-11-13

@author: Byng Zeng
"""

import re, sys, os, getopt


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

class ICSCalendarEvent(object):
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


class ICSCalendarRe(object):
    def __init__(self):
        # get all of re_compile.
        self._DTStart=re.compile(RE_DTSTART)
        self._DTEnd=re.compile(RE_DTEND)
        self._Date=re.compile(RE_DATE)
        self._filterTime=re.compile(RE_TIME_FILTER)
        self._Time=re.compile(RE_TIME)
        self._Location=re.compile(RE_LOCATION)
        self._Summay=re.compile(RE_SUMMARY)
        self._Description=re.compile(RE_DESCRIPTION)
        self._CalName=re.compile(RE_CALNAME)

    def getCalName(self, txt):
        return self._CalName.match(txt)


    def getLocation(self, txt):
        return self._Location.match(txt)


    def getDescription(self, txt):
        return self._Description.match(txt)


    def getDTEnd(self, txt):
        return self._DTEnd.match(txt)


    def getDate(self, txt):
        return self._Date.search(txt)


    def getTime(self, txt):
        time=None
        ftime=self._filterTime.search(txt)
        if ftime != None:
            time=self._Time.search(ftime.group())
        return time


    def getDTStart(self, txt):
        return self._DTStart.match(txt)


    def getSummary(self, txt):
        return self._Summay.match(txt)




class ICSCalendar(object):
    # print help menu.
    @classmethod
    def printHelp(cls):
        print '======================================'
        print '     iOS Calender Data Convert'
        print '======================================'
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
        ICSCalendar.errorExit()


    # print msg and exit
    @classmethod
    def errorExit(cls, msg=None):
        if msg != None:
            print msg
        # stop runing and exit.
        exit()


    # get abs path.
    @classmethod
    def getAbsPath(cls, path):
        if path[0:1] == r'.':
             path=path.replace(r'.', os.getcwd(), 1)
        return path


    # get external name of file.
    @classmethod
    def getExtName(cls, f):
        return os.path.splitext(f)[1][1:].upper()


    # get all of .ics file under path.
    @classmethod
    def getICSFiles(cls, path):
        fs=None
        for root, dirs, files in os.walk(path):
            if len(files) != 0:
                for f in files:
                    if ICSCalendar.getExtName(f) == TYPE_ICS:
                        if fs == None:
                            fs=list()
                        fs.append(os.path.join(root, f))
        # return all of files.
        return fs


    # get all of .ics files.
    @classmethod
    def getSrcFiles(cls, path):
        fs=None
        if os.path.exists(path) == True:
            if os.path.isfile(path) == True and ICSCalendar.getExtName(path) == TYPE_ICS:
                fs=list()
                fs.append(path)
            elif os.path.isdir(path) == True:
                fs=ICSCalendar.getICSFiles(path)
        # return result.
        return fs


    # make ready for output
    @classmethod
    def makeOutputPath(cls, name):
        path=os.path.split(name)[0]
        # make dir for output
        if os.path.exists(path) == False:
            os.makedirs(path)
        # remove old file.
        if os.path.exists(name) == True:
            os.remove(name)


    # init ICSCalendar
    def __init__(self):
        # init values.
        self._src=None
        self._tgt=None
        self._fmt=None
        self._calName=None
        self._listEvents=list()
        self._listCnt=0
        self._event=ICSCalendarEvent()
        #self._sortKey='DTSTART'
        self._sortReverse=False
        self._combineFiles=False
        self._re=None


    def getUserOpt(self):
        try:
            opts, args = getopt.getopt(sys.argv[1:], "hcf:s:t:r:")
        except getopt.GetoptError:
            ICSCalendar.errorExit('Invalid input, -h for help.')
        # process input value
	if len(opts) == 0 and len(args) != 0:
            ICSCalendar.errorExit('Invalid input, -h for help.')
	else:
            for name, value in opts:
                if name == r'-h':
                    ICSCalendar.printHelp()
                elif name == r'-c':
                    self._combineFiles=True
                elif name == r'-f':
                    fmt=value.upper()
                    if fmt == TYPE_TXT or fmt == TYPE_CSV:
                        self._fmt=fmt
                    else:
                        ICSCalendar.errorExit("Error, unsupport format!")
                elif name == r'-r':
                    if value == r'True':
                        self._sortReverse=True
                    else:
                        self._sortReverse=False
                elif name == r'-s':
                    # set _src to list
                    if self._src == None:
                        self._src=list()
                    # get src files
                    fs=self.getSrcFiles(ICSCalendar.getAbsPath(value))
                    if fs != None:
                       # add fs to _src
                       for f in fs:
                           self._src.append(f)
                elif name == r'-t':
                    extName=ICSCalendar.getExtName(ICSCalendar.getAbsPath(value))
                    if extName == TYPE_TXT or extName == TYPE_CSV:
                        self._tgt=ICSCalendar.getAbsPath(value)
                        self._combineFiles=True
                        self._fmt=extName
                    else:
                        self._tgt=ICSCalendar.getAbsPath(value)
                else:
                    ICSCalendar.errorExit('Error, unknown %s %s' % (name, value))


    # check input args
    def checkOptArgs(self):
        # check src.
        if self._src == None:
            # check current path.
            fs=ICSCalendar.getICSFiles(os.getcwd())
            if fs != None:
                # set _src to list
                if self._src == None:
                    self._src=list()
                # add fs to _src
                for f in fs:
                    self._src.append(f)

        # check tgt.
        if self._tgt == None:
            self._tgt=os.getcwd()


    # get name of output
    def getOutputFileName(self, fmt):
        if ICSCalendar.getExtName(self._tgt) == fmt:
                name=self._tgt
        elif self._combineFiles == True:
	    name=r'%s/%s.%s' % (self._tgt, r'日历', fmt.lower())
        else:
	    name=r'%s/%s.%s' % (self._tgt, self._calName, fmt.lower())
        # return name of file.
        return name


    # save data to .csv file.
    def saveToCSV(self):
        # get output name
        name=self.getOutputFileName(TYPE_CSV)
        # ready for write
        ICSCalendar.makeOutputPath(name)
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
        name=self.getOutputFileName(TYPE_TXT)
        # ready for write
        ICSCalendar.makeOutputPath(name)
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


    # call function to output data.
    def formatOutput(self):
        if len(self._listEvents) == 0:
            return
        # sort all of events.
        self._listEvents.sort(key=lambda event: event._date_s, reverse=self._sortReverse)
        # output
        if self._fmt == TYPE_TXT:
            self.saveToTXT()
        elif self._fmt == TYPE_CSV:
            self.saveToCSV()
        elif self._fmt == None:
            self.printICSContent()
        else:
            print 'Error, use -f txt/csv to set format output\n'
            printHelp()

        # clear all of events.
        self._listEvents=list()


    # insert event to evevnt_list.
    def insertEvent(self):
        self._listEvents.append(self._event)
        # update for next event.
        self._event=ICSCalendarEvent()


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
                # create ICSCalendarRe
                if self._re == None:
                    self._re=ICSCalendarRe()
                # get ICSCalendar Name
                calName=self._re.getCalName(buf)
                if calName != None:
                    self._calName=calName.group()[len('X-WR-CALNAME:'):len(calName.group())-1]
                # get location
                location=self._re.getLocation(buf)
                if location != None:
                    self._event._location=location.group()
                # get description
                description=self._re.getDescription(buf)
                if description != None:
                    self._event._description=description.group()
                # get end of date and time
                dt_end=self._re.getDTEnd(buf)
                if dt_end != None:
                    # search date.
                    date_e=self._re.getDate(dt_end.group())
                    if date_e != None:
                        # get date of end
                        self._event._date_e=date_e.group()
                        # get time of end
                        time_e=self._re.getTime(dt_end.group())
                        if time_e != None:
                            self._event._time_e=time_e.group()
                # get start of date and time
                dt_start=self._re.getDTStart(buf)
                if dt_start != None:
                    date_s=self._re.getDate(dt_start.group())
                    if date_s != None:
                        # get date of start
                        self._event._date_s=date_s.group()
                        # get time of start
                        time_s=self._re.getTime(dt_start.group())
                        if time_s != None:
                            self._event._time_s=time_s.group()
                # get summary
                summary=self._re.getSummary(buf)
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


    # entrance of ICSCalendar
    def main(self):
        # get user options.
        self.getUserOpt()
        # check args.
        self.checkOptArgs()
        # start to process data.
        if self._src == None or len(self._src) == 0:
            ICSCalendar.errorExit('No found .ics, do nothing.')
        elif self._combineFiles == True:
            self.CombineICSHandler()
        else:
            self.ICSHandler()



if __name__ == '__main__':
    cal=ICSCalendar()
    cal.main()
