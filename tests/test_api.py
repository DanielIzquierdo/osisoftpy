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
osisoftpy.tests.test_api.py
~~~~~~~~~~~~

Tests for the `osisoftpy.api` module.
"""
import pytest
import requests
from .conftest import credentials

import osisoftpy

skip = False

@pytest.mark.skipif(skip, reason="Takes an extra 3s...")
def test_api_get_request(url, authtype, username, password):
    r = osisoftpy.request(url, authtype=authtype, username=username,
                      password=password)
    assert r.status_code == requests.codes.ok
    assert r.json().get('Links').get('Self').startswith(url)


@pytest.mark.skipif(skip, reason="Takes an extra 3s...")
@pytest.mark.parametrize('url', ['BLANK', 'fizz', '%^$@^%#$!&', 'http', None])
def test_api_get_webapi_with_urls(url):
    if url == 'BLANK':
        with pytest.raises(TypeError) as e:
            osisoftpy.request()
        e.match('argument')
    else:
        with pytest.raises(requests.exceptions.MissingSchema) as e:
            osisoftpy.webapi(url)
        e.match('Invalid')


@pytest.mark.skipif(skip, reason="Takes an extra 5s...")
@pytest.mark.parametrize('a', ['kerberos', 'basic', None])
@pytest.mark.parametrize('u', ['albertxu', 'andrew', None])
@pytest.mark.parametrize('s', ['Welcome2pi', 'p@ssw0rd', None])
def test_api_get_webapi_with_credentials(url, a, u, s):

    if (a, u, s) in credentials().valid:
        webapi = osisoftpy.webapi(url, authtype=a, username=u, password=s)
        assert isinstance(webapi, osisoftpy.WebAPI)
        assert webapi.links.get('Self').startswith(url)
    else:
        with pytest.raises(osisoftpy.exceptions.Unauthorized) as e:
            osisoftpy.webapi(url, authtype=a, username=u, password=s)
        assert 'Server rejected request' in str(e.value)


