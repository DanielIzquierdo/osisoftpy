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
osisoftpy.assetdatabase
~~~~~~~~~~~~
This module contains the class definition for the AssetDatabase class, which
represents an AF Database. It's described by the PI Web API.
"""
from osisoftpy.base import Base

class AssetDatabase(Base):
    """
    An AssetDatabase object.

    Representation of an AF Database as described by the PI Web API. 
    """

    valid_attr = { 'webid', 'id', 'name', 'description', 'path', 'extendedproperties', 'links', 'session', 'webapi'}
    
    """
    Attributes:
        | webid: Unique GUID for the Point created by the PI Web API
        | id: Unique GUID for the Point created by the PI System
        | name: Database name
        | description: Description for the database
        | path: Path for the AF database
        | extendedproperties: WebAPI object
        | links: Direct Link to the PI Web API 
    """

    def __init__(self, **kwargs):
        super(self.__class__, self).__init__(**kwargs)

        self.elements = {}
        self.elementtemplates = {}
        self.assetserver = None
        self.elementcategories = {}
        self.attributecategories = {}
