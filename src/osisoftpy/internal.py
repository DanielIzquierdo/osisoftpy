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
osisoftpy.internal
~~~~~~~~~~~~
Some blah blah about what this file is for...
"""
from collections import namedtuple
import logging
import requests
import requests_kerberos

log = logging.getLogger(__name__)


def stringify(**kwargs):
    """
    Return a concatenated string of the keys and values of the kwargs
    Source: http://stackoverflow.com/a/39623935
    :param kwargs: kwargs to be combined into a single string
    :return: String representation of the kwargs
    """
    return (','.join('{0}={1!r}'.format(k, v)
                     for k, v in kwargs.items()))


def _get_auth(authtype, username=None, password=None):
    if authtype == 'kerberos':
        return requests_kerberos.HTTPKerberosAuth(
            mutual_authentication=requests_kerberos.OPTIONAL)
    else:
        return requests.auth.HTTPBasicAuth(username, password)


def get(url, session=None, **kwargs):
    try:
        s = session or requests.session()
        log.debug(s)
        with s:
            s.verify = kwargs.get('verifyssl', True)
            log.debug(s.auth)
            s.auth = s.auth or _get_auth(kwargs.get('authtype', None),
                                         kwargs.get('username', None),
                                         kwargs.get('password', None))
            Response = namedtuple('Response', ['response', 'session'])
            r = Response(s.get(url, params=kwargs.get('params', None)), s)

            log.debug(r.response.json())
            return r
    except Exception as e:
        raise e
