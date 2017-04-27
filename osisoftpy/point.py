# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from __future__ import print_function

from .value import Value
from .collection import Collection


class Point(object):
    """The Point class provides methods for the available PI points"""

    def __init__(self, name=None, description=None, uniqueid=None, webid=None,
                 datatype=None):
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
        self._values = Collection(Value)

    def __repr__(self):
        representation = 'Point("{}", "{}", "{}", "{}", "{}", "{}")'
        return representation.format(self._name, self._description,
                                     self._uniqueid, self._webid,
                                     self._datatype, self._values)

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

    @property
    def values(self): return self._values
