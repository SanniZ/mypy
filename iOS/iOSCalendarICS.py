# -*- coding: utf-8 -*-
"""
Created on 2018-11-13

@author: Byng Zeng
"""

import re

RE_DT_START=r'DTSTART;TZID=Asia/Shanghai:\d{,8}T\d{,4}'
RE_DT_END=r'DTEND;TZID=Asia/Shanghai:\d{,8}T\d{,4}'
RE_DATE=r'\d+'
RE_TIME_FILTER=r'T\d+'
RE_TIME=r'\d+'
RE_LOCATION=r'LOCATION:.+'
RE_SUMMARY=r'SUMMARY:.+'
RE_DESCRIPTION=r'DESCRIPTION:.+'

re_dt_start=re.compile(RE_DT_START)
re_dt_end=re.compile(RE_DT_END)
re_date=re.compile(RE_DATE)
re_time_filter=re.compile(RE_TIME_FILTER)
re_time=re.compile(RE_TIME)
re_loc=re.compile(RE_LOCATION)
re_sum=re.compile(RE_SUMMARY)
re_desc=re.compile(RE_DESCRIPTION)


g_date=None
g_time_s=None
g_time_e=None

g_summary=None
g_location=None
g_description=None

with open(r'Byng.ics', 'r') as f:
    while True:
        buf=f.readline()
        if len(buf) == 0:
            break

        dt_end=re_dt_end.match(buf)
        if dt_end != None:
            date_e=re_date.search(dt_end.group())
            if date_e != None:
                time_f=re_time_filter.search(dt_end.group())
                time_e=re_time.search(time_f.group())
                g_time_e=time_e.group()

        dt_start=re_dt_start.match(buf)
        if dt_start != None:
            date_s=re_date.search(dt_start.group())
            if date_s != None:
                time_f=re_time_filter.search(dt_start.group())
                time_s=re_time.search(time_f.group())
                g_time_s=time_s.group()
                g_date=date_s.group()

        summary=re_sum.match(buf)
        if summary != None:
            g_summary=summary.group()
            print('-----------------------')
            print '%s-%s-%s %s:%s-%s:%s' % (g_date[0:4], g_date[4:6], g_date[6:8], g_time_s[0:2], g_time_s[2:4], g_time_e[0:2], g_time_e[2:4])
            print('LOCATION   : %s' % g_location[9:])
            print('SUMMARY    : %s' % g_summary[8:])
            if g_description == None:
                print(r'DESCRIPTION:')
            else:
                print(r'DESCRIPTION: %s' % g_description[12:])            
        
        location=re_loc.match(buf)
        if location != None:
            g_location=location.group()

        description=re_desc.match(buf)        
        if description != None:
            g_description=description.group()

