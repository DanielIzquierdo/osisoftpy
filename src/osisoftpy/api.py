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
from __future__ import (absolute_import, division, unicode_literals)

import requests
import requests_kerberos
from requests_kerberos import HTTPKerberosAuth
import logging
from requests.packages.urllib3 import disable_warnings
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from osisoftpy.structures import APIResponse
from osisoftpy.exceptions import (PIWebAPIError, Unauthorized, HTTPError)
from osisoftpy.factory import Factory, create
from osisoftpy.webapi import WebAPI

log = logging.getLogger(__name__)


def webapi(
        url,
        hostname_override=None,
        principal=None,
        authtype='kerberos',
        username=None,
        password=None,
        verifyssl=False):
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
    try:
        s = requests.session()
        s.verify = verifyssl
        if not s.verify:
            disable_warnings(InsecureRequestWarning)
        if authtype == 'kerberos':
            s.auth = HTTPKerberosAuth(
                mutual_authentication=requests_kerberos.OPTIONAL,
                sanitize_mutual_error_response=False,
                hostname_override=hostname_override,
                force_preemptive=True,
                principal=principal)
        else:
            s.auth = requests.auth.HTTPBasicAuth(username, password)
        r = APIResponse(s.get(url), s)
        if r.response.status_code == 401:
            raise Unauthorized(
                'Authorization denied - incorrect username or password.')
        if r.response.status_code != 200:
            raise HTTPError('Wrong server response: %s %s' %
                            (r.response.status_code, r.response.reason))
        json = r.response.json()
        if 'Errors' in json and json.get('Errors').__len__() > 0:
            msg = 'PI Web API returned an error: {}'
            raise PIWebAPIError(msg.format(json.get('Errors')))
        return create(Factory(WebAPI), json, r.session)
    except:
        raise
