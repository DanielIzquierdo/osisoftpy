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
osisoftpy.tests.test_webapi.py
~~~~~~~~~~~~

Tests for the `osisoftpy.webapi` module.
"""

import re

import osisoftpy
import pytest
import requests
import random
import time

from datetime import datetime, timedelta
from dateutil import parser

from .conftest import query

# https://techsupport.osisoft.com/Troubleshooting/Known-Issues/176830
piserverissue = True

def test_get_webapi_object(webapi):
    assert isinstance(webapi, osisoftpy.WebAPI)


def test_webapi_has_session(webapi):
    print(', '.join("%s: %s" % item for item in vars(webapi).items()))
    assert isinstance(webapi.session, requests.Session)

def test_webapi_has_links(webapi):
    print(', '.join("%s: %s" % item for item in vars(webapi).items()))
    assert isinstance(webapi.links, dict)

def test_webapi_has_str_(webapi, url):
    assert webapi.__str__() == '<OSIsoft PI Web API [{}]>'.format(url+'/')

def test_webapi_has_self_url(webapi, url):
    assert webapi.links.get('Self') == url + '/'

def test_webapi_has_self_url_property(webapi, url):
    assert webapi.url == url+ '/'

def test_webapi_has_search_url(webapi, url):
    assert webapi.links.get('Search') == url + '/search'

def test_webapi_has_dataservers(webapi):
    assert webapi.dataservers.__len__() == 2

def test_webapi_query_sinusoid(webapi):
    tag = 'sinusoid'
    payload = dict(query="name:{}".format(tag), count=10)
    r = webapi.request(**payload)
    assert r.status_code == requests.codes.ok
    assert r.json().get('TotalHits') > 0
    assert r.json().get('Items')[0].get('Name').lower() == 'sinusoid'
    assert bool(
        re.match(r.json().get('Items')[0].get('Name'), tag, re.IGNORECASE))

def test_webapi_points_sinusoid(webapi):
    tag = 'sinusoid'
    payload = dict(query="name:{}".format(tag), count=10, scope='pi:gold')
    r = webapi.points(**payload)
    assert all(isinstance(x, osisoftpy.Point) for x in r)
    assert r.__len__() == 1

@pytest.mark.parametrize('query', query())
def test_webapi_points_query(webapi, query):
    payload = dict(query=query, count=1000)
    points = webapi.points(**payload)
    assert all(isinstance(x, osisoftpy.Point) for x in points)
    msg = '{} points were retrieved with the query "{}"'
    print(msg.format(points.__len__(), query))

def test_webapi_points_scope(webapi):
    points = webapi.points(query='name:SINUSOID*', scope='pi:gold')
    assert points.__len__() == 4

def test_webapi_points_pagination(webapi):
    points = webapi.points(query='name:S*', count=150)
    assert points.__len__() > 151
    assert all(isinstance(point, osisoftpy.Point) for point in points)

def test_webapi_elements_pagination(webapi):
    elements = webapi.elements(query='name:3.*', scope='af:\\\\GOLD\\OSIsoftPy', count=1)
    assert elements.__len__() > 1
    for element in elements:
        assert(isinstance(element, osisoftpy.Element))
        assert(isinstance(element.attributes, dict))

# AF Tests

def test_webapi_has_assetservers_objects(webapi):
    assert all(isinstance(assetserver, osisoftpy.AssetServer) for assetserver in webapi.assetservers)
    assert webapi.assetservers.__len__() > 0

def test_webapi_has_assetdatabases(webapi):
    servers = webapi.assetservers
    for assetserver in servers:
        print('AF Server: {0}'.format(assetserver.name))
        if (assetserver.name == 'GOLD'):
            afdatabases = assetserver.get_databases()
    num_afdatabases = afdatabases.__len__()
    assert num_afdatabases > 2