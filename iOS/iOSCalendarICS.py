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

    TYPE_FILE=r'FILE'
    TYPE_DIR=r'DIR'
    TYPE_DIR_COMBINE=r'DIR_COMBINE'

    def __init__(self):
        # init values.
        self._src=None
        self._srcType=None
        self._tgt=None
        self._tgtType=None
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
                self._combineFiles=True
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


    # check user args
    def checkOptArgs(self):
        # check src.
        if self._src == None:
            self._src=os.getcwd()
            self._srcType=Calendar.TYPE_DIR
        elif os.path.exists(self._src) == False:
            print 'Error no found %s, pls use -s xxx to set source: xxx/xxx.ics or xxx/\n' % self._src
            self.printHelp()
        elif os.path.isfile(self._src) == True:
            # check external name
            if os.path.splitext(self._src)[1] != r'.ics':
                print 'Error, %s is not ics file!\n' % self._src
                self.printHelp()
            else:
                self._srcType=Calendar.TYPE_FILE
        elif os.path.isdir(self._src) == True:
            self._srcType=Calendar.TYPE_DIR
        else:
            print 'Error, pls use -s xxx to set source: xxx/xxx.ics or xxx/'
            self.printHelp()

        # check tgt.
        if self._fmt != None:
            if self._tgt == None:
                self._tgt=os.getcwd()
                self._tgtType=Calendar.TYPE_DIR
                #print 'No set target dir, default set to current path: %s.\n' % self._tgt
            else:
                extName=os.path.splitext(self._tgt)[1][1:]
                if extName == r'':
                    self._tgtType=Calendar.TYPE_DIR
                    if self._tgt[len(self._tgt)-1] == r'/':
                        self._tgt=self._tgt[:len(self._tgt)-1]
                elif extName == self._fmt:
                    if self._srcType == Calendar.TYPE_DIR:
                        if self._combineFiles == False:
                            opt=raw_input(r'Do you want to output all of data to %s(y/n)?' % os.path.basename(self._tgt))
                            if opt.upper() == r'Y':
                                self._combineFiles=True
                                self._tgtType=Calendar.TYPE_FILE
                            else:
                                self._tgt=os.path.split(self._tgt)[0]
                                self._tgtType=Calendar.TYPE_DIR
                    else:
                        self._tgtType=Calendar.TYPE_FILE
                else:
                    self._tgtType=Calendar.TYPE_DIR


    # get all of .ics file under folder.
    def getFilesOfPath(self):
        #self._src=os.path.dirname(self._src)
        return os.listdir(self._src)


    def getOutputFileName(self, fmt):
        if self._tgtType == Calendar.TYPE_FILE:
            # tgt is match fmt external name.
            if self._fmt == os.path.splitext(self._tgt)[1][1:]:
                name=self._tgt
            else: # tgt is not match fmt external name, set name=%tgt.%fmt
                name=r'%s.%s' % (self._tgt, self._fmt)
        elif self._tgtType == Calendar.TYPE_DIR:
            if self._combineFiles == True:
	        name=r'%s/%s.%s' % (self._tgt, r'Combine', fmt)
            else:
	        name=r'%s/%s.%s' % (self._tgt, self._calName, fmt)
        else:
            print 'Error, unknown output format.'
            self.printHelp()
        # return name of file.
        return name


    def readyForOutput(self, name):
        path=os.path.split(name)[0]
        if os.path.exists(path) == False:
            os.mkdir(path)
        if os.path.exists(name) == True:
            os.remove(name)


    def getOptType(self):
        if self._srcType == Calendar.TYPE_FILE:
            result=Calendar.TYPE_FILE
        elif self._srcType == Calendar.TYPE_DIR:
            if self._combineFiles == True:
                result=Calendar.TYPE_DIR_COMBINE
            else:
                result=Calendar.TYPE_DIR
        #print 'operation type: %s' % result
        # return result.
        return result


    # save data to .csv file.
    def saveToCSV(self):
        # get output name
        name=self.getOutputFileName(r'csv')
        # ready for write
        self.readyForOutput(name)
        # write events.
        with open(name, r'a') as f:
            # create title if not set.
            if self._combineFiles == True:
                f.write('开始日期,结束日期,开始时间,结束时间,地点,事件,描述,类型\n')
            else:
                f.write('开始日期,结束日期,开始时间,结束时间,地点,事件,描述\n')
            # start to write events.
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
                if self._combineFiles == True:
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
        print 'output: %s' % name

    # save data to .txt file.
    def saveToTXT(self):
        # get output name
        name=self.getOutputFileName(r'txt')
        # ready for write
        self.readyForOutput(name)
        # write events.
        with open(name, r'a') as f:
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
        print 'output: %s' % name

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
            self.saveToCSV()
        elif self._fmt == None:
            self.printICSContent()
        else:
            print 'Error, use -f txt/csv to set format output\n'
            self.printHelp()

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
                    if self._combineFiles == True or self._fmt == None:
                        self._event._type=self._calName
                    # event is ready, insert to list now.
                    self.insertEvent()


    def singleFileHandler(self, f):
        self.processICS(f)
        # output
        self.formatOutput()


    def dirFilesHandler(self):
        fs=self.getFilesOfPath()
        # loop for all of files.
        for f in fs:
            self.singleFileHandler(f)


    def CombineDIRHandler(self):
        fs=self.getFilesOfPath()
        # loop for all of files.
        for f in fs:
            self.processICS(f)
        # output
        self.formatOutput()


    def main(self):
        # get user options.
        self.getUserOpt()
        # check args.
        self.checkOptArgs()
        # get operation type.
        optType=self.getOptType()
        if optType == Calendar.TYPE_FILE:
            self.singleFileHandler(self._src)
        elif optType == Calendar.TYPE_DIR:
            self.dirFilesHandler()
        elif optType == Calendar.TYPE_DIR_COMBINE:
            self.CombineDIRHandler()



if __name__ == '__main__':
    cal=Calendar()
    cal.main()
