# -*- coding: utf-8 -*-

#    Copyright 2017 DST Controls
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.
"""
osisoftpy.value
~~~~~~~~~~~~
"""
from __future__ import (absolute_import, division, unicode_literals)
from future.builtins import *
from osisoftpy.base import Base


class Value(Base):
    """
    The Value class provides the response from methods for the available PI points
    """
    valid_attr = {'calculationtype', 'datatype', 'timestamp', 'value',
                  'unitsabbreviation', 'good', 'questionable', 'substituted'}
    """
    Attributes:
        | calculationtype: time or event weighted / summary type
        | datatype: data type
        | timestamp: the time stamp for which the value was queried
        | value: the value of the PI point at the given timestamp
        | unitsabbreviation: abbreviation for the unit of measure for the PI point
        | good: boolean flag indicating whether the value is a “good” or “bad” value in PI
        | questionable: boolean flag indicating whether the value is a questionable value in PI
        | substituted: boolean flag indicating whether the value was substituted
    """

    def __init__(self, **kwargs):
        super(self.__class__, self).__init__(**kwargs)

    def __str__(self):
        self_str = '<OSIsoft PI Value [{} - {}]>'
        return self_str.format(self.timestamp, self.value)

    def __eq__(self, other): 
        return self.__dict__ == other.__dict__