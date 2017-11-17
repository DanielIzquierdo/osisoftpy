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
from dateutil import parser
from datetime import datetime
import logging
import blinker
import re
from osisoftpy.base import Base
from osisoftpy.factory import Factory, create
from osisoftpy.internal import get
from osisoftpy.point import Point
from osisoftpy.points import Points
from osisoftpy.element import Element
from osisoftpy.elements import Elements
from osisoftpy.attribute import Attribute

log = logging.getLogger(__name__)


class WebAPI(Base):
    valid_attr = {'links', 'session', 'debug'}
    dataservers = []
    assetservers = []

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
            count=100,
            start=0, ):
        """Sends a request to the PI Web API instance using the provided 
        search query and returned item count. If successful, a Points object 
        will be returned. 
        
        :param query: One or many terms, in the form of field:value,
            like 'name:pump'. If no field is specfied, like 'pump', then the 
            following fields will all be used: name, description, afcategories, 
            afelementtemplate, attributename, attributedescription. 
        
            The star and question mark wildcards are supported, for example: 
            boil* or boi?er. To perform a fuzzy search, append a tilde to the 
            end of a keyword, like 'boilr~' will match 'boiler'. 
        
            If multiple terms are entered, they are assumed to be ORed together. 
            If that's not appropriate, you can specify AND, OR, and NOT (must be
            capitalized) operators, along with parenthesis to create a complex query. 
            For example '(vibration* AND datatype:float32) OR afelementtemplate:pump' 
            Special characters are used through the keyword syntax, so those 
            characters must be escaped if they are in a literal search term. The 
            following characters must be escaped with a backslash: + - && || ! ( 
            ) { } [ ] ^ " ~ * ? : \ For example, to find a PI point named 
            SI:NUSO.ID specify 'q=name:SI\:USO.ID'
            
        :param scope: List of sources to execute the 
            query against. Specify the sources in string format (
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
            100 per page.
        :param start: Index of search result to begin with. The 
            default is to start at index 0.
        :return: :class:`osisoftpy.Points` object containing :class:`osisoftpy.Point`
        :rtype: osisoftpy.Points
        """

        totalitems = 0
        totalhits = None
        points = Points([], self)

        r = self.request(
                query=query, scope=scope, fields=fields, count=count, start=start)
        items = r.json().get('Items', [])
        totalhits = r.json().get('TotalHits', 0)
        points = Points(points.list + list([
                create(Factory(Point), x, self.session, self)
                for x in items if x['ItemType'] == 'pipoint'
            ]), self)
        # ceiling division
        expectedloop = -(-totalhits // count)
        for x in range(1, expectedloop):
            start += count
            r = self.request(
                query=query, scope=scope, fields=fields, count=count, start=start)
            items = r.json().get('Items', [])
            totalhits = r.json().get('TotalHits', 0)
            points = Points(points.list + list([
                    create(Factory(Point), x, self.session, self)
                    for x in items if x['ItemType'] == 'pipoint'
                ]), self)

        [self._map_dataserver_to_point(point) for point in points]
        return points

    # added default value to fields so it also returns paths and parents
    def elements(
            self,
            query,
            scope=None,
            fields='afcategory;attributes;datatype;description;endtime;haschildren;itemtype;'
                +'links;matchedfields;name;starttime;plottable;template;uniqueid;uom;webid;paths;parents;',
            count=100,
            start=0, ):
        #TODO: Update Comment Block
        """Sends a request to the PI Web API instance using the provided 
        search query and returned item count. If successful, a Points object 
        will be returned. 
        
        :param query: One or many terms, in the form of field:value,
            like 'name:pump'. If no field is specfied, like 'pump', then the 
            following fields will all be used: name, description, afcategories, 
            afelementtemplate, attributename, attributedescription. 
        
            The star and question mark wildcards are supported, for example: 
            boil* or boi?er. To perform a fuzzy search, append a tilde to the 
            end of a keyword, like 'boilr~' will match 'boiler'. 
        
            If multiple terms are entered, they are assumed to be ORed together. 
            If that's not appropriate, you can specify AND, OR, and NOT (must be
            capitalized) operators, along with parenthesis to create a complex query. 
            For example '(vibration* AND datatype:float32) OR afelementtemplate:pump' 
            Special characters are used through the keyword syntax, so those 
            characters must be escaped if they are in a literal search term. The 
            following characters must be escaped with a backslash: + - && || ! ( 
            ) { } [ ] ^ " ~ * ? : \ For example, to find a PI point named 
            SI:NUSO.ID specify 'q=name:SI\:USO.ID'
            
        :param scope: List of sources to execute the 
            query against. Specify the sources in string format (
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
            100 per page.
        :param start: Index of search result to begin with. The 
            default is to start at index 0.
        :return: :class:`osisoftpy.Points` object containing :class:`osisoftpy.Point`
        :rtype: osisoftpy.Points
        """

        totalitems = 0
        totalhits = None
        elements = Elements([], self)

        #inital call
        r = self.request(
                query=query, scope=scope, fields=fields, count=count, start=start)
        items = r.json().get('Items', [])
        totalhits = r.json().get('TotalHits', 0)

        preAttributeList = list([
                 create(Factory(Element), x, self.session, self)
                 for x in items if x['ItemType'] == 'afelement'
            ])
        for element in preAttributeList:
            if element.attributes:
                #list implementation
                # attributes = list([
                #     create(Factory(Attribute), attribute, self.session, self) 
                #     for attribute in element.attributes
                # ])
                #dict implementation
                attributes = { 
                    attribute['Name']: create(Factory(Attribute), attribute, self.session, self)
                    for attribute in element.attributes 
                }
                
            else:
                attributes = []
            element.attributes = attributes

        elements = Elements(elements.list + preAttributeList, self)
        
        # repeating call when all elements are retrieved
        # ceiling division
        expectedloop = -(-totalhits // count)
        for i in range(1, expectedloop):
            start += count
            r = self.request(   
                query=query, scope=scope, fields=fields, count=count, start=start)
            items = r.json().get('Items', [])
            totalhits = r.json().get('TotalHits', 0)
            
            preAttributeList = list([
                 create(Factory(Element), x, self.session, self)
                 for x in items if x['ItemType'] == 'afelement'
            ])
            for element in preAttributeList:
                if element.attributes:
                    #list implementation
                    # attributes = list([
                    #     create(Factory(Attribute), attribute, self.session, self) 
                    #     for attribute in element.attributes
                    # ])
                    #dict implementation
                    attributes = { 
                        attribute['Name']: create(Factory(Attribute), attribute, self.session, self)
                        for attribute in element.attributes 
                    }
                    
                else:
                    attributes = []
                element.attributes = attributes

            elements = Elements(elements.list + preAttributeList, self)

        # [self._map_dataserver_to_point(point) for point in points]
        return elements

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
            SI:NUSO.ID specify 'q=name:SI\:USO.ID'

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

    def subscribe(self, points, stream, startdatetime=None, enddatetime=None, callback=None):
        """Monitor whenever the PI point is read and an update has occurred. 
        Trigger the callback function when the value changes

        :param Points points: List of Point objects to start monitoring
        :param string stream: Name of the reading method used for monitoring the point. 
            Options are current, interpolatedattimes, recordedattime, end
        :param string startdatetime: Optional – Timestamp for when to start monitoring
        :param string enddatetime: Optional – Timestamp for when to stop monitoring
        :param func callback: Reference to the function to trigger when an update occurs
        """
        if not isinstance(points, Points):
            raise TypeError('The object "{}" is not of type "{}"'.format(
                points, Points))
        for p in points:
            formattedstartdate = self._parse_timestamp(startdatetime)
            formattedenddate = self._parse_timestamp(enddatetime)

            signalkey = '{}/{}/{}{}'.format(p.webid.__str__(), stream, formattedstartdate or '', formattedenddate or '')
            if signalkey not in self.signals:
                s = blinker.signal(signalkey)
                self.signals[signalkey] = s
                if callback:
                    self.signals[signalkey].connect(callback)
        return self.signals

    def unsubscribe(self, points, stream, startdatetime=None, enddatetime=None):
        """Stop monitoring a given list of PI Points for updates

        :param Points points: List of Point objects to stop monitoring
        :param string stream: Name of the reading method used for monitoring the point. 
            Options are current, interpolatedattimes, recordedattime, end
        :param string startdatetime: Optional – Timestamp for when to start monitoring
        :param string enddatetime: Optional – Timestamp for when to stop monitoring
        """
        if not isinstance(points, Points):
            raise TypeError('The object "{}" is not of type "{}"'.format(
                points, Points))
        for p in points:
            formattedstartdate = self._parse_timestamp(startdatetime)
            formattedenddate = self._parse_timestamp(enddatetime)
            signalkey = '{}/{}/{}{}'.format(p.webid.__str__(), stream, formattedstartdate or '', formattedenddate or '')
            try:
                self.signals.pop(signalkey)
            except KeyError:
                pass
        return self.signals

    def piservers(self):
        for dataserver in self.dataservers:
            print('pi:' + dataserver.name)

    def afservers(self):
        for assetserver in self.assetservers:
            print('af:' + assetserver.name)

    def _map_dataserver_to_point(self, point):
        uniqueid = point.uniqueid
        serverid = re.search('{(.*?)}', uniqueid).group(1)
        point.dataserver = next((dataserver for dataserver in self.dataservers if dataserver.id == serverid), None)

    # can't use this
    def _map_assetserver_to_element(self, element):
        uniqueid = element.uniqueid
        serverid = re.search('{(.*?)}', uniqueid).group(1)
        point.dataserver = next((dataserver for dataserver in self.dataservers if dataserver.id == serverid), None)

    def _parse_timestamp(self, datetime):
        if datetime:
            parseddatetime = parser.parse(datetime)
            formatteddatetime = None if parseddatetime == None else parseddatetime.strftime('%Y%m%d%H%M%S')
        else:  
            formatteddatetime = None
        return formatteddatetime
    