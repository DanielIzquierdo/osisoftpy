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
osisoftpy.dataserver
~~~~~~~~~~~~
This module contains the class definition for the DataServer class, which
represents a PI Server. It's described by the PI Web API.
"""
from osisoftpy.base import Base

class DataServer(Base):
    """
    A PI Server object.

    Representation of a PI System Server as described by the PI Web API. 
    """

    valid_attr = { 'webid', 'id', 'name', 'path', 'isconnected', 
        'serverversion' , 'links'}

    def __init__(self, **kwargs):
        super(self.__class__, self).__init__(**kwargs)