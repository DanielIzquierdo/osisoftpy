# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from __future__ import print_function

import collections


class Point(object):
    """The Point class provides methods for the available PI points"""

    def __init__(self, name=None, description=None,
                 uniqueid=None, webid=None, datatype=None):
        # type: (string, string, string, string, string) -> object

        """

        :rtype: Point object
        :param name: 
        :param description: 
        :param uniqueid: 
        :param webid: 
        :param datatype: 
        """
        self._name = name
        self._description = description
        self._uniqueid = uniqueid
        self._webid = webid
        self._datatype = datatype

    @property
    def name(self): return self._name

    @property
    def description(self): return self._description

    @property
    def uniqueid(self): return self._uniqueid

    @property
    def webid(self): return self._webid

    @property
    def datatype(self): return self._datatype


class Points(collections.MutableSequence):
    def __init__(self, types, *args):
        self.types = types
        self.list = list()
        self.extend(list(args))

    def check(self, v):
        if not isinstance(v, self.types):
            raise TypeError, v

    def __len__(self): return len(self.list)

    def __getitem__(self, i): return self.list[i]

    def __delitem__(self, i): del self.list[i]

    def __setitem__(self, i, v):
        self.check(v)
        self.list[i] = v

    def insert(self, i, v):
        self.check(v)
        self.list.insert(i, v)

    def __str__(self):
        return str(self.list)

