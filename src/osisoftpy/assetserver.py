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
osisoftpy.assetserver
~~~~~~~~~~~~
This module contains the class definition for the AssetServer class, which
represents an AF Server. It's described by the PI Web API.
"""
from osisoftpy.base import Base
from osisoftpy.factory import Factory
from osisoftpy.factory import create
from osisoftpy.internal import get
from osisoftpy.assetdatabase import AssetDatabase

class AssetServer(Base):
    """
    An AssetServer object.

    Representation of an AF Server as described by the PI Web API. 
    """

    valid_attr = { 'webid', 'id', 'name', 'description', 'path', 'isconnected', 
        'serverversion', 'extendedproperties', 'links', 'session', 'webapi'}
    databases = []
    
    """
    Attributes:
        | webid: Unique GUID for the Point created by the PI Web API
        | id: Unique GUID for the Point created by the PI System
        | name: Server name
        | description: Description for the AF Server
        | path: Path for the AF Server
        | isconnected: Boolean that indicates whether the server is connected 
        | serverversion: AF Server version
        | extendedproperties: WebAPI object
        | links: Direct Link to the PI Web API 
        | session: PI Web API Connection session
        | webapi: WebAPI object
    """

    def __init__(self, **kwargs):
        super(self.__class__, self).__init__(**kwargs)

    def __str__(self):
        self_str = '<OSIsoft PI AF Server [{} - {}]>'
        return self_str.format(self.name, self.description)

    def get_databases(self, **kwargs):
        """
        Retrieves all databases within the current server and returns
        a collection of AssetDatabase objects
        """
        payload = {
            'namefilter': None,
            'selectedfields': None,
        }
        url = '{}/{}/{}/{}'.format(
            self.webapi.links.get('Self'), 'assetservers', self.webid, 'assetdatabases')
        r = get(url, self.session, params=payload, **kwargs)
        print(r.response.json)

        databases = list([create(Factory(AssetDatabase), r.response.json(), self.session,
                       self.webapi)])
        return databases