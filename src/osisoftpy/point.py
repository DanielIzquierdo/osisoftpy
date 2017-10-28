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
This module contains the class definition for the Point class, which
represents a PI System Point. It's described by the PI Web API.
"""
import logging

from osisoftpy.stream import Stream
from osisoftpy.internal import _stringify

log = logging.getLogger(__name__)


class Point(Stream):
    """
    A Point object.

    Representation of a PI System Point as described by the PI Web API. 
    """

    valid_attr = {'name', 'description', 'uniqueid', 'webid', 'datatype',
                  'links', 'session', 'webapi'}
    dataserver = None
    
    """
    Attributes:
        | name: Point name
        | description: Description for the PI Point
        | uniqueid: Unique GUID for the Point created by the PI System
        | webid: Unique GUID for the Point created by the PI Web API
        | datatype: PI Point datatype
        | links: Direct Link to the PI Web API 
        | session: PI Web API Connection session
        | webapi: WebAPI object
    """

    def __init__(self, **kwargs):
        super(self.__class__, self).__init__(**kwargs)

    def __str__(self):
        self_str = '<OSIsoft PI Point [{} - {}]>'
        return self_str.format(self.name, self.description)

    def attributes(self, namefilter=None, selectedfields=None):
        payload = {
            'namefilter': namefilter,
            'selectedfields': selectedfields,
        }
        return self._get_values(
            payload=payload, endpoint='attributes', controller='points')

    