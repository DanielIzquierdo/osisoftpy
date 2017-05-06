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

def test_get_webapi_without_url():
    with pytest.raises(TypeError) as e:
        osisoftpy.response()
    e.match('argument')

@pytest.mark.parametrize('url', ['fizz', 'buzz', 'localhst', 'http'])
def test_get_webapi_with_invalid_url(url):
    with pytest.raises(requests.exceptions.MissingSchema) as e:
        osisoftpy.response(url)
    e.match('Invalid URL')

@pytest.mark.parametrize('authtype, username, password', credentials().unknown)
def test_get_webapi_with_credentials(url, authtype, username, password):
    cred = authtype, username, password
    r = osisoftpy.response(url, authtype=cred[0],
                           username=cred[1],
                           password=cred[2])
    if cred in credentials().valid:
        assert r.status_code == requests.codes.ok
        assert r.json().get('Links').get('Self').startswith(url)
    else:
        assert r.status_code == requests.codes.unauthorized

def test_get_webapi_valid_url_basic_missing_credentials(url, authtype):
    r = osisoftpy.response(url, authtype=authtype)
    assert r.status_code == requests.codes.unauthorized


def test_get_webapi_valid_url_basic_missing_password(url, authtype, username):
    r = osisoftpy.response(url, authtype=authtype,
                           username=username)
    assert r.status_code == requests.codes.unauthorized


def test_get_webapi_valid_url_basic_missing_username(url, authtype, password):
    r = osisoftpy.response(url, authtype=authtype,
                           password=password)
    assert r.status_code == requests.codes.unauthorized


def test_get_webapi_valid_url_basic_valid_credentials(url, authtype,
                                                      username, password):
    r = osisoftpy.response(url, authtype=authtype,
                           username=username,
                           password=password)
    assert r.status_code == requests.codes.ok
    assert r.json().get('Links').get('Self').startswith(url)
