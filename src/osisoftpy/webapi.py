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
osisoftpy.webapi
~~~~~~~~~~~~
Some blah blah about what this file is for...
"""
from __future__ import (absolute_import, division, unicode_literals)
from future.builtins import *
from future.utils import iteritems
import logging
import blinker
from osisoftpy.base import Base
from osisoftpy.factory import Factory, create
from osisoftpy.internal import get
from osisoftpy.point import Point
from osisoftpy.points import Points

log = logging.getLogger(__name__)


class WebAPI(Base):
    """

    """
    valid_attr = {'links', 'session', 'debug'}

    def __init__(self, **kwargs):
        super(self.__class__, self).__init__(**kwargs)

        # p = Points(list(), self)
        # self._points = p
        self.signals = {}

    def __str__(self):
        self_str = '<OSIsoft PI Web API [{}]>'
        return self_str.format(self.links.get('Self'))

    @property
    def url(self):
        """Returns the URL of the PI Web API instance.
        :return: str (https://localhost/piwebapi/)
        """
        return self.links.get('Self')

    def points(
            self,
            query,
            scope=None,
            fields=None,
            count=10,
            start=0, ):
        """Sends a request to the PI Web API instance using the provided 
        search query and returned item count. If successful, a list of 
        Points will be returned. 

        :param query: One or many terms, in the form of field:value, 
        like "name:pump". If no field is specfied, like "pump", then the 
        following fields will all be used: name, description, afcategories, 
        afelementtemplate, attributename, attributedescription. 

        The star and question mark wildcards are supported, for example: 
        boil* or boi?er. To perform a fuzzy search, append a tilde to the 
        end of a keyword, like "boilr~" will match "boiler". 

        If multiple terms are entered, they are assumed to be ORed together. 
        If that's not appropriate, you can specify AND, OR, and NOT 
        operators, along with parenthesis to create a complex query. For 
        example "(vibration* AND datatype:float32) OR afelementtemplate:pump" 

        Special characters are used through the keyword syntax, so those 
        characters must be escaped if they are in a literal search term. The 
        following characters must be escaped with a backslash: + - && || ! ( 
        ) { } [ ] ^ " ~ * ? : \ For example, to find a PI point named 
        SI:NUSO.ID specify "q=name:SI\:USO.ID"
        :param scope: List of sources 
        to execute the query against. Specify the sources in string format (
        e.g. pi:mypidataarchive) or in webId format. Multiple scopes (and 
        with different formats) can be specified, separated by semicolons (
        ;).
        :param fields: List of fields to include in each Search Result. 
        If no fields are specified, then the following fields are returned: 
        afcategory; attributes; datatype; description; endtime; haschildren; 
        itemtype; links; matchedfields; name; plottable; starttime; 
        template; uniqueid; uom; webid The following fields are not returned 
        by default: paths; parents; explain (must be paired with the links 
        field)
        :param count: Max number of results to return. The default is 
        10 per page.
        :param start: Index of search result to begin with. The 
        default is to start at index 0.
        :return: :class:`Points <Points>` object containing :class:`Point <Point>` object
        :rtype: osisoftpy.Points
        """
        r = self.request(
            query=query, scope=scope, fields=fields, count=count, start=start)
        p = Points(list([
            create(Factory(Point), x, self.session, self)
            for x in r.json().get('Items', None)
        ]), self)
        # self._points.extend(p)
        # return self._points
        return p

    def request(
            self,
            query,
            scope=None,
            fields=None,
            count=10,
            start=0, ):
        """Sends a request to the PI Web API instance using the provided 
        search query and returned item count. If successful, an APIResponse 
        object will be returned. 

        :param query: One or many terms, in the form of field:value, 
        like "name:pump". If no field is specfied, like "pump", then the 
        following fields will all be used: name, description, afcategories, 
        afelementtemplate, attributename, attributedescription. 

        The star and question mark wildcards are supported, for example: 
        boil* or boi?er. To perform a fuzzy search, append a tilde to the 
        end of a keyword, like "boilr~" will match "boiler". 

        If multiple terms are entered, they are assumed to be ORed together. 
        If that's not appropriate, you can specify AND, OR, and NOT 
        operators, along with parenthesis to create a complex query. For 
        example "(vibration* AND datatype:float32) OR afelementtemplate:pump" 

        Special characters are used through the keyword syntax, so those 
        characters must be escaped if they are in a literal search term. The 
        following characters must be escaped with a backslash: + - && || ! ( 
        ) { } [ ] ^ " ~ * ? : \ For example, to find a PI point named 
        SI:NUSO.ID specify "q=name:SI\:USO.ID"
        :param scope: List of sources 
        to execute the query against. Specify the sources in string format (
        e.g. pi:mypidataarchive) or in webId format. Multiple scopes (and 
        with different formats) can be specified, separated by semicolons (
        ;).
        :param fields: List of fields to include in each Search Result. 
        If no fields are specified, then the following fields are returned: 
        afcategory; attributes; datatype; description; endtime; haschildren; 
        itemtype; links; matchedfields; name; plottable; starttime; 
        template; uniqueid; uom; webid The following fields are not returned 
        by default: paths; parents; explain (must be paired with the links 
        field)
        :param count: Max number of results to return. The default is 
        10 per page.
        :param start: Index of search result to begin with. The 
        default is to start at index 0.
        :return: :class:`APIResponse <APIResponse>` object
        :rtype: osisoftpy.APIResponse
        """
        url = '{}/{}'.format(self.links.get('Search'), 'query')
        params = dict(
            q=query, scope=scope, fields=fields, count=count, start=start)
        try:
            r = get(url, session=self.session, params=params)
            return r.response
        except Exception as e:
            raise e

    def subscribe(self, points, stream, callback=None):
        if not isinstance(points, Points):
            raise TypeError('The object "{}" is not of type "{}"'.format(
                points, Points))
        for p in points:
            signalkey = '{}/{}'.format(p.webid.__str__(), stream)
            if signalkey not in self.signals:
                s = blinker.signal(signalkey)
                self.signals[signalkey] = s
        if callback:
            for (k, signal) in iteritems(self.signals):
                signal.connect(callback)
        return self.signals

    def unsubscribe(self, points, stream):
        if not isinstance(points, Points):
            raise TypeError('The object "{}" is not of type "{}"'.format(
                points, Points))
        for p in points:
            signalkey = '{}/{}'.format(p.webid.__str__(), stream)
            try:
                self.signals.pop(signalkey)
            except KeyError:
                pass
        return self.signals