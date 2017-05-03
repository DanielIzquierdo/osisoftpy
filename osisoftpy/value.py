# -*- coding: utf-8 -*-

from __future__ import print_function
from __future__ import unicode_literals

from .base import Base


class Value(Base):
    """The Value class provides methods for the available PI points"""

    def __init__(self, calculationtype=None, datatype=None, timestamp=None,
                 value=None, unitsabbreviation=None, good=False,
                 questionable=False, substituted=False):
        # type: (str, str, str, str, bool, bool, bool) -> object

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
        self.calculationtype = calculationtype
        self.datatype = datatype
        self.timestamp = timestamp
        self.value = value
        self.unitsabbreviation = unitsabbreviation
        self.good = good
        self.questionable = questionable
        self.substituted = substituted

    def __repr__(self):
        representation = 'Point("{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}"'
        return representation.format(self.calculationtype, self.datatype,
                                     self.timestamp, self.value,
                                     self.unitsabbreviation, self.good,
                                     self.questionable, self.substituted)
