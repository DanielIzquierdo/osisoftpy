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
max values = 2147483647
"""
from __future__ import (absolute_import, division, unicode_literals)
from future.builtins import *

import collections
import logging

from osisoftpy.factory import Factory
from osisoftpy.factory import create
from osisoftpy.internal import get_batch
from osisoftpy.value import Value

log = logging.getLogger(__name__)


class Points(collections.MutableSequence):
    def __init__(self, iterable, webapi):
        self.list = list()
        self.webapi = webapi
        self.extend(list(iterable))

    def __getitem__(self, key):
        return self.list[key]

    def __setitem__(self, key, value):
        self.list[key] = value

    def __delitem__(self, key):
        del self.list[key]

    def __len__(self):
        return len(self.list)

    def insert(self, key, value):
        self.list.insert(key, value)

    def __str__(self):
        return str(self.list)

    @property
    def session(self):
        return self.webapi.session

    def current(
            self,
            time = None,
            namefilter = None,
            categoryname = None,
            templatename = None,
            showexcluded = False,
            showhidden = False,
            showfullhierarchy = False,
            selectedfields = None,
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
            selectedfields=selectedfields
        )

        r = get_batch('GET', self.webapi, self, 'value', params=payload)
        json = r.response.json()

        # The Web API returns a tuple for each request given to it via batch.
        # in this case, the key is the name of the tag.
        # maybe use webid instead?
        # point[0] is the index given (name in this case)
        # point[1] is the content (the current value in this case)
        for p in json.items():
            point = next((x for x in self if x.name == p[0]), None)
            v = create(Factory(Value), p[1].get('Content'), self.session,
                       self.webapi)
            point.current_value = v
        return self
