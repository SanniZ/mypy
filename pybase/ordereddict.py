#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 2019-03-01

@author: Byng.Zeng
"""

VERSION = '1.2.3'
AUTHOR = 'Byng.Zeng'


############################################################################
#               OrderedDict class
############################################################################

class OrderedDict(object):

    __slots__ = ('_keys', '_dt', '_index')

    def __init__(self, dt=None):
        self._keys = []
        self._dt = {}
        self._index = 0
        if all((dt, isinstance(dt, dict))):
            self.append(dt)

    def __call__(self):
        lt = []
        for k in self._keys:
            lt.append((k, self._dt[k]))
        return lt

    def __iter__(self):
        return self

    def __next__(self):
        if self._index < len(self._keys):
            key = self._keys[self._index]
            self._index += 1
            return key
        else:
            self._index = 0
            raise StopIteration

    def __getitem__(self, key):
        if key in self._dt:
            return self._dt[key]
        else:
            raise KeyError('no found key %s' % key)

    def __setitem__(self, item, value):
        if item in self._dt:
            self._dt[item] = value
        else:
            self.__add__({item: value})

    def __len__(self):
        return len(self._keys)

    def __add__(self, dt):
        if isinstance(dt, dict):
            for k, w in dt.items():
                if k not in self._keys:
                    self._keys.append(k)
                self._dt[k] = w
        else:
            raise TypeError('%s in not dict type' % dt)

    def __delitem__(self, key):
        if key in self._keys:
            del self._dt[key]
            del self._keys[self._keys.index(key)]
        else:
            raise KeyError('no found key %s' % key)

    # append a dict
    def append(self, dt):
        self.__add__(dt)

    # delete from key or index
    def delete(self, key):
        self.__delitem__(key)

    # insert a dt to index position
    def insert(self, index, dt):
        if index <= len(self._keys):
            for k, w in dt.items():
                self._dt[k] = w
                self._keys.insert(index, k)
                index += 1
        else:
            raise IndexError('overflow index %s' % index)

    def items(self):
        for key in self._keys:
            yield key, self._dt[key]

    def clear(self):
        self.__init__()

    def values(self):
        values = []
        for k in self._keys:
            values.append(self._dt[k])
        return values

    def keys(self):
        return self._keys

    def index(self, key):
        if key in self._keys:
            return self._keys.index(key)
        else:
            raise KeyError('no found key %s' % key)

    def count(self):
        return self.__len__()

    def get_index(self, index):
        if index >= len(self._keys):
            return IndexError('overflow index %s' % index)
        else:
            key = self._keys[index]
            return key, self._dt[key]
