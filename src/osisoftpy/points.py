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
osisoftpy.points
~~~~~~~~~~~~
Some blah blah about what this file is for...
"""

from osisoftpy.internal import wrapt_handle_exceptions


class Points(list):
    def __init__(self, **kwargs):
        super(self.__class__, self).__init__(**kwargs)

        self._session = kwargs.get('session', None)
        self._webapi = kwargs.get('webapi', None)

    @property
    def session(self):
        return self._session

    @property
    def webapi(self):
        return self._session

    @wrapt_handle_exceptions
    def current(
            self,
            time=None,
            namefilter=None,
            categoryname=None,
            templatename=None,
            showexcluded=False,
            showhidden=False,
            showfullhierarchy=False,
            selectedfields=None,
    ):
        """
        Returns values of the attributes for an Element, Event Frame or 
        Attribute at the specified time. 

        :param time: An optional time. The default time context is 
            determined from the owning object - for example, the time range of 
            the event frame or transfer which holds this attribute. Otherwise, 
            the implementation of the Data Reference determines the meaning of 
            no context. For Points or simply configured PI Point Data 
            References, this means the snapshot value of the PI Point on the 
            Data Server.
        :return: :class:`OSIsoftPy <osisoftpy.Point>` object
        :rtype: osisoftpy.Point
        """
        payload = dict(
            time=time,
            namefilter=namefilter,
            categoryname=categoryname,
            templatename=templatename,
            showexcluded=showexcluded,
            showhidden=showhidden,
            showfullhierarchy=showfullhierarchy,
            action='current',
            points = self
        )

        return self.webapi.streamset(**payload)
