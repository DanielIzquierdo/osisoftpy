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

import osisoftpy


def test_get_webapi_without_url():
    with pytest.raises(TypeError) as e:
        osisoftpy.response()
    e.match('argument')


def test_get_webapi_with_invalid_url():
    with pytest.raises(requests.exceptions.MissingSchema) as e:
        osisoftpy.response('foobar')
    e.match('Invalid URL')


def test_get_webapi_with_valid_url_no_credentials(url):
    r = osisoftpy.response(url)
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
