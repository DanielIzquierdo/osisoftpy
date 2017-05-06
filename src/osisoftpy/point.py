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
osisoftpy.point
~~~~~~~~~~~~
This module contains the class definition for the Point class, 
which represents a PI System Point it's described by the PI Web API."""

from osisoftpy.base import Base


class Point(Base):
    """An :class:`OSIsoftPy <osisoftpy.dataarchive.Point>` object.
    
    Representation of a PI System Point as described by the PI Web API. 
    
    :param name: Point name
    :param description: Description for the PI Point
    :param webid: Unique GUID for the Point created by the PI Web API
    :param uniqueid: Unique GUID for the Point created by the PI System
    :param datatype: PI Point datatype
    
    :return: :class:`OSIsoftPy <osisoftpy.dataarchive.Point>` object
    :rtype: osisoftpy.dataarchive.Point
    """

    valid_attr = {'name', 'description', 'uniqueid', 'webid', 'datatype'}

    def __init__(self, **kwargs):
        super(self.__class__, self).__init__(**kwargs)

        self.current_value = None
        self.interpolated_values = None
        self.recorded_values = None
        self.plot_values = None
        self.summary_values = None
        self.end_value = None
