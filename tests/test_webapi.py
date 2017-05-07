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

Tests for the `osisoftpy.webapi` module.
"""

import re

import osisoftpy
import pytest
import requests

from .conftest import query


def test_get_webapi_object(webapi):
    assert type(webapi) == osisoftpy.WebAPI


def test_webapi_has_session(webapi):
    print(', '.join("%s: %s" % item for item in vars(webapi).items()))
    assert type(webapi.session) == requests.Session


def test_webapi_has_links(webapi):
    print(', '.join("%s: %s" % item for item in vars(webapi).items()))
    assert type(webapi.links) == dict


def test_webapi_has_self_url(webapi, url):
    assert webapi.links.get('Self') == url + '/'


def test_webapi_has_search_url(webapi, url):
    assert webapi.links.get('Search') == url + '/search'


def test_webapi_search_method(webapi):
    r = webapi.search()
    assert r.status_code == requests.codes.ok
    assert r.json().get('Links').get('Self').startswith(
        webapi.links.get('Search'))


def test_webapi_query_method(webapi):
    with pytest.raises(osisoftpy.exceptions.PIWebAPIError) as e:
        r = webapi.query()
        assert r.status_code == requests.codes.ok
    assert e.match('Query parameter must be specified')


def test_webapi_query_sinusoid(webapi):
    tag = 'sinusoid'
    payload = {"q": "name:{}".format(tag), "count": 10}
    r = webapi.query(params=payload)
    assert r.status_code == requests.codes.ok
    assert r.json().get('TotalHits') > 0
    assert r.json().get('Items')[0].get('Name').lower() == 'sinusoid'
    assert bool(
        re.match(r.json().get('Items')[0].get('Name'), tag, re.IGNORECASE))


def test_webapi_points_sinusoid(webapi):
    tag = 'sinusoid'
    payload = {"q": "name:{}".format(tag), "count": 10}
    r = webapi.points(params=payload)
    assert all(isinstance(x, osisoftpy.Point) for x in r)
    assert r.__len__() == 1


@pytest.mark.parametrize('query', query())
def test_webapi_points_query(webapi, query):
    payload = {"q": query, "count": 1000}
    points = webapi.points(params=payload)
    assert all(isinstance(x, osisoftpy.Point) for x in points)
    msg = '{} points were retrieved with the query "{}"'
    print(msg.format(points.__len__(), query))
