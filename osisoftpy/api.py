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
import logging

import requests
import requests_kerberos

from .factory import Factory, create_thing
from .webapi import PIWebAPI

log = logging.getLogger(__name__)


def webapi(url, **kwargs):
    try:
        return _get_webapi(url, **kwargs)
    except Exception as e:
        raise e


def json(url, **kwargs):
    try:
        return _get_json(url, **kwargs)
    except Exception as e:
        raise e


def _get_result(url, **kwargs):
    try:
        with requests.session() as s:
            s.verify = kwargs.get('verifyssl', True)
            s.auth = _get_auth(kwargs.get('authtype', None),
                               kwargs.get('username', None),
                               kwargs.get('password', None))
            return s.get(url)
    except Exception as e:
        raise e


def _get_auth(authtype, username=None, password=None):
    if authtype == 'kerberos':
        return requests_kerberos.HTTPKerberosAuth(
            mutual_authentication=requests_kerberos.OPTIONAL)
    else:
        return requests.auth.HTTPBasicAuth(username, password)


def _get_webapi(url, **kwargs):
    r = _get_result(url, **kwargs)
    factory = Factory(PIWebAPI)
    return create_thing(factory, r.json())


def _get_json(url, **kwargs):
    return _get_result(url, **kwargs)
