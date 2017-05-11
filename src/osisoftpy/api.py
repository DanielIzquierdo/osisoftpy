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
osisoftpy.api
~~~~~~~~~~~~
This module implements the OSIsoftPy API.
"""

from osisoftpy.factory import Factory, create
from osisoftpy.internal import get
from osisoftpy.webapi import WebAPI

def webapi(url, authtype='kerberos', username=None, password=None, verifyssl=False):
    """Sends a request to the provided url and authentication configuration. 
    If successfully, a WebAPI object will be constructed from the response 
    and returned. 

    :param url: The URL of the PI Web API server.
    :param authtype: Optional - Options are Basic and Kerberos.
        Default authtype is kerberos.
    :param username: Optional username - Only used for basic auth.
    :param password: Optional password - Only used for basic auth.
    :param verifyssl: Optional SSL verification. If set to False, then
        InsecureRequestWarning will be disabled.
    :return: :class:`WebAPI <WebAPI>` object
    :rtype: osisoftpy.WebAPI
    """
    r = get(url, authtype=authtype, username=username, password=password, verifyssl=verifyssl)
    return create(Factory(WebAPI), r.response.json(), r.session)

