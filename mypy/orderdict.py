#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 2019-03-01

@author: Zbyng.Zeng
"""

VERSION = '1.0.0'


############################################################################
#               OrderDict class
############################################################################

class OrderDict(object):

    def __init__(self, dt=None):
        self._lt = []
        self._max = 0
        self._dt = {}
        self._index = 0
        if dt:
            self.append(dt)

    def __iter__(self):
        return self

    def __next__(self):
        if self._index < self._max:
            key = self._lt[self._index]
            self._index += 1
            return key, self._dt[key]
        else:
            self._index = 0
            raise StopIteration

    def __getitem__(self, item):
        if item in self._dt:
            return self._dt[item]
        elif isinstance(item, int):
            if item < self._max:
                return self._dt[self._lt[item]]

    def __setitem__(self, item, value):
        if item in self._dt:
            self._dt[item] = value
        elif isinstance(item, int):
            if item < self._max:
                self._dt[self._lt[item]] = value
        else:
            self.append({item: value})

    # append a dict
    def append(self, dt):
        for k, w in dt.items():
            self._dt[k] = w
            self._lt.append(k)
            self._max += 1

    # delete from key or index
    def delete(self, key=None, index=None):
        if key:
            if key in self._dt:  # from key
                del self._dt[key]
                self._max -= 1
                for index, k in enumerate(self._lt):
                    if key == k:
                        del self._lt[index]
                        break
        elif index:  # from index
            if index < self._max:
                key = self._lt[index]
                del self._lt[index]
                del self._dt[key]
                self._max -= 1

    # insert a dt to index position
    def insert(self, index, dt):
        if index <= self._max:
            for k, w in dt.items():
                self._dt[k] = w
                self._lt.insert(index, k)
                self._max += 1
                index += 1

    def clear(self):
        return self.__init__()

    def values(self):
        return self._dt

    def keys(self):
        return self._lt

    def count(self):
        return self._max
