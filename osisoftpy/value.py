# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from __future__ import print_function

import collections


class Value(object):
    """The Point class provides methods for the available PI points"""

    def __init__(self, calculationtype=None, datatype=None, timestamp=None,
                 value=None,
                 unitsabbreviation=None, good=False, questionable=False,
                 substituted=False):
        # type: (string, string, string, string, bool, bool, bool) -> None

        """

        :param type: 
        :param timestamp: 
        :param value: 
        :param unitsabbreviation: 
        :param good: 
        :param questionable: 
        :param substituted: 
        :rtype: None
        """
        self._calculationtype = calculationtype
        self._timestamp = timestamp
        self._value = value
        self._unitsabbreviation = unitsabbreviation
        self._good = good
        self._questionable = questionable
        self._substituted = substituted

    def __repr__(self):
        representation = 'Point("{}", "{}", "{}", "{}", "{}", "{}", "{}")'
        return representation.format(self._calculationtype, self._timestamp,
                                     self._value, self._unitsabbreviation,
                                     self._good, self._questionable,
                                     self._substituted)

    @property
    def calculationtype(self): return self._calculationtype

    @property
    def datatype(self): return self._datatype

    @property
    def timestamp(self): return self._timestamp

    @property
    def value(self): return self._value

    @property
    def unitsabbreviation(self): return self._unitsabbreviation

    @property
    def good(self): return self._good

    @property
    def questionable(self): return self._questionable

    @property
    def substituted(self): return self._substituted