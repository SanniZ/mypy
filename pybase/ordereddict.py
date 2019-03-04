#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 2019-03-01

@author: Byng.Zeng
"""

VERSION = '1.2.0'
AUTHOR = 'Byng.Zeng'


############################################################################
#               OrderDict class
############################################################################

class OrderedDict(object):

    __slots__ = ('_keys', '_dt', '_index')

    def __init__(self, dt=None):
        self._keys = []
        self._dt = {}
        self._index = 0
        if dt:
            self.append(dt)

    def __iter__(self):
        return self

    def __next__(self):
        if self._index < len(self._keys):
            key = self._keys[self._index]
            self._index += 1
            return key, self._dt[key]
        else:
            self._index = 0
            raise StopIteration

    def __getitem__(self, item):
        if item in self._dt:
            return self._dt[item]
        elif isinstance(item, int):
            if item < len(self._keys):
                return self._dt[self._keys[item]]
            else:
                raise IndexError('IndexError: invalid index %s' % item)
        else:
            raise KeyError('KeyError: no found key %s' % item)

    def __setitem__(self, item, value):
        if item in self._dt:
            self._dt[item] = value
        elif isinstance(item, int):
            if item < len(self._keys):
                self._dt[self._keys[item]] = value
            else:
                raise IndexError('IndexError: invalid index %s' % item)
        else:
            self.append({item: value})

    def __len__(self):
        return len(self._keys)

    def __add__(self, dt):
        for k, w in dt.items():
            self._dt[k] = w
            self._keys.append(k)
        return self._dt

    def __call__(self):
        return self._dt

    # append a dict
    def append(self, dt):
        return self.__add__(dt)

    # delete from key or index
    def delete(self, key=None, index=None):
        if key:
            if key in self._dt:  # from key
                del self._dt[key]
                for index, k in enumerate(self._keys):
                    if key == k:
                        del self._keys[index]
                        break
            else:
                raise KeyError('KeyError: no found key %s' % key)
        elif index:  # from index
            if index < len(self._keys):
                key = self._keys[index]
                del self._keys[index]
                del self._dt[key]
            else:
                raise IndexError('IndexError: invalid index %s' % index)

    # insert a dt to index position
    def insert(self, index, dt):
        if index <= len(self._keys):
            for k, w in dt.items():
                self._dt[k] = w
                self._keys.insert(index, k)
                index += 1
        else:
            raise IndexError('IndexError: invalid index %s' % index)

    def clear(self):
        return self.__init__()

    def values(self):
        return self._dt

    def keys(self):
        return self._keys

    def count(self):
        return self.__len__()
