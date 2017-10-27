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
osisoftpy.element
~~~~~~~~~~~~
This module contains the class definition for the Element class, which
represents an AF Element. It's described by the PI Web API.
"""
from osisoftpy.base import Base

class Element(Base):
    """
    An Element object.

    Representation of an AF Element as described by the PI Web API. 
    """


    valid_attr = { 'webid', 'uniqueid', 'name', 'description', 'path', 'template',
        'haschildren', 'afcategories', 'extendedproperties', 'links', 'attributes'}
    
    #TODO: update comment doc below
    """
    Attributes:
        | webid: Unique GUID for the element created by the PI Web API
        | id: Unique GUID for the element created by the PI System
        | name: Element name
        | description: Description for the AF Element
        | path: Path for the AF Element
        | templatename: Name of template that this element belongs to
        | haschildren: Is this element a parent element of another element
        | categorynames: List of categories that this element belongs to
        | extendedproperties: WebAPI object
        | links: Direct Link to the PI Web API 
    """

    def __init__(self, **kwargs):
        super(self.__class__, self).__init__(**kwargs)

        # self.attributes = []
        self.assetdatabase = None
        # self.categories = {}

    # TODO: Get on Attribute Name instead of Index Number
         