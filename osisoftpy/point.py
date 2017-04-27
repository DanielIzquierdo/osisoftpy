# -*- coding: utf-8 -*-

from __future__ import print_function
from __future__ import unicode_literals


class Point(object):
    """The Point class provides methods for the available PI points"""

    def __init__(self, name=None, description=None, uniqueid=None, webid=None,
                 datatype=None):
        # type: (str, str, str, str, str) -> object

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
        self._current_value = None
        self._interpolated_values = None
        self._recorded_values = None
        self._plot_values = None
        self._summary_values = None
        self._end_value = None

    def __repr__(self):
        representation = 'Point("{}", "{}", "{}", "{}", "{}", "{}")'
        return representation.format(self._name, self._description,
                                     self._uniqueid, self._webid,
                                     self._datatype, self._current_value)

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, description):
        self._description = description

    @property
    def uniqueid(self):
        return self._uniqueid

    @uniqueid.setter
    def uniqueid(self, uniqueid):
        self._uniqueid = uniqueid

    @property
    def webid(self):
        return self._webid

    @webid.setter
    def webid(self, webid):
        self._webid = webid

    @property
    def datatype(self):
        return self._datatype

    @datatype.setter
    def datatype(self, datatype):
        self._datatype = datatype

    @property
    def current_value(self):
        return self._current_value

    @current_value.setter
    def current_value(self, current_value):
        self._current_value = current_value

    # TODO: NOT IMPLEMENTED
    @property
    def interpolated_values(self):
        # raise NotImplementedError()
        return self._interpolated_values

    @property
    def recorded_values(self): return self._recorded_values

    @property
    def plot_values(self): return self._plot_values

    @property
    def summary_values(self): return self._summary_values

    @property
    def end_value(self): return self._end_value
