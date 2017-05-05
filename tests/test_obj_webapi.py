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
osisoftpy.tests.test_int_api.py
~~~~~~~~~~~~
Some blah blah about what this file is for...
"""

import pytest
import requests
from requests.sessions import Session

import osisoftpy
from osisoftpy.webapi import PIWebAPI
from . import utils

params = utils.params


def _get_webapi():
    return osisoftpy.webapi(params.url,
                            authtype=params.authtype,
                            username=params.username,
                            password=params.password)


def test_get_piwebapi_object():
    webapi = _get_webapi()
    assert type(webapi) == PIWebAPI


def test_piwebapi_has_session():
    webapi = _get_webapi()
    print(', '.join("%s: %s" % item for item in vars(webapi).items()))
    assert type(webapi.session) == Session


def test_piwebapi_has_links():
    webapi = _get_webapi()
    print(', '.join("%s: %s" % item for item in vars(webapi).items()))
    assert type(webapi.links) == dict


def test_piwebapi_has_self_url():
    webapi = _get_webapi()
    assert webapi.links.get('Self') == params.url + '/'


def test_piwebapi_has_search_url():
    webapi = _get_webapi()
    assert webapi.links.get('Search') == params.url + '/search'

def test_piwebapi_get_search():
    webapi = _get_webapi()
    r = webapi.search()
    assert r.status_code == requests.codes.ok
    assert r.json().get('Links').get('Self').startswith(
        webapi.links.get('Search'))
