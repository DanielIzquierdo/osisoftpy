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
"""This module contains the class definition for the DataArchive class, 
which represents a PI System Data Archive server as it's described by the PI 
Web API. """

from .base import Base


class DataArchive(Base):
    """An :class:`OSIsoftPy <osisoftpy.dataarchive.DataArchive>` object.

    Representation of a PI System Data Archive server as described by the PI 
    Web API. 

    :param name: PI server name
    :param name: PI Data Archive server name
    :param webid: PI Data Archive Web ID
    :param serverversion: PI Data Archive software version
    :param isconnected: Connection status with the PI Web API
    :param id: PI Data Archive ID
    
    :return: :class:`OSIsoftPy <osisoftpy.dataarchive.DataArchive>` object
    :rtype: osisoftpy.dataarchive.DataArchive
    """

    valid_attr = {'name', 'serverversion', 'webid', 'isconnected', 'id'}

    def __init__(self, **kwargs):
        super(self.__class__, self).__init__(**kwargs)

    def __str__(self):
        return '<OSIsoft PI Data Archive Server [{} - {}]>'.format(self.name,
                                                    self.serverversion)
