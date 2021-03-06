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
osisoftpy.attribute
~~~~~~~~~~~~
This module contains the class definition for the Attribute class, which
represents an AF Attribute. It's described by the PI Web API.
"""
from osisoftpy.base import Base
from osisoftpy.stream import Stream

class Attribute(Stream):
    """
    An Element object.

    Representation of an AF Element as described by the PI Web API. 
    """

    valid_attr = { 'webid', 'id', 'name', 'description', 'path', 'datatype', 'value',
        'typequalifier', 'defaultunitsname', 'datareferenceplugin', 'configstring',
        'isconfigurationitem', 'isexcluded', 'ishidden', 'ismanualdataentry', 
        'haschildren', 'categories', 'step', 'traitname', 'links', 'session', 'webapi'}
    

    # TODO: update comment doc
    """
    Attributes:
        | webid: Unique GUID for the attribute created by the PI Web API
        | id: Unique GUID for the attribute created by the PI System
        | name: Attribute name
        | description: Description for the AF Attribute
        | path: Path for the AF Attribute
        | type: Data type
        | typequalifier: More specific type (such as enumeration sets)
        | defaultunitsname: Unit of measure
        | datareferenceplugin: Type of data retrieval method
        | configstring: AF attribute configuration string
        | isconfigurationitem: Is configuration attribute
        | isexcluded: Is from template but excluded
        | ishidden: Is hidden in AF
        | ismanualdataentry: Is an attribute that requires manual data entry
        | haschildren: Is this element a parent element of another element
        | categorynames: List of categories that this element belongs to
        | step: Is the value stepped
        | traitname: Specifies the name of the attribute trait
        | links: Direct Link to the PI Web API 
    """

    def __init__(self, **kwargs):
        super(self.__class__, self).__init__(**kwargs)