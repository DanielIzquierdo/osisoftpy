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
osisoftpy.tests.attributes.py
~~~~~~~~~~~~
Tests for the `osisoftpy.attributes` module.
"""

import osisoftpy
import pytest
import re

from .conftest import now
from .conftest import pointvalues

@pytest.mark.parametrize('query', ['attributename:SampleInput'])
@pytest.mark.parametrize('keys', [pointvalues().single])
def test_attribute_singlevaluekeys_are_validtypes(webapi, query, keys):
    element = webapi.elements(query)[0]
    attribute = element['SampleInput']
    for k in keys:
        try:
            valuekey = getattr(attribute, k)
            if re.match('int\d{0,2}', attribute.datatype, re.IGNORECASE):
                assert isinstance(valuekey.value, int)
            elif re.match('float\d{0,2}', attribute.datatype, re.IGNORECASE):
                assert isinstance(valuekey.value, float)
        except AttributeError:
            pass

@pytest.mark.parametrize('query', ['attributename:SampleInput'])
@pytest.mark.parametrize('keys', [pointvalues().multi])
def test_attribute_multivaluekeys_are_validtypes(webapi, query, keys):
    element = webapi.elements(query)[0]
    attribute = element['SampleInput']
    for k in keys:
        try:
            valuekey = getattr(attribute, k)
            if re.match('int\d{0,2}', attribute.datatype, re.IGNORECASE):
                assert isinstance(valuekey.value, int)
            elif re.match('float\d{0,2}', attribute.datatype, re.IGNORECASE):
                assert isinstance(valuekey.value, float)
        except AttributeError:
            pass

def test_attribute_only_create_elements(webapi):
    pipoint = 'SINUSOID'
    payload = dict(query="name:{}".format(pipoint), count=10)
    r = webapi.request(**payload)
    assert r.json().get('TotalHits') > 0
    elements = webapi.elements(**payload)
    assert elements.__len__() == 0

@pytest.mark.parametrize('query', ['attributename:SampleInput'])
@pytest.mark.parametrize('key', ['interpolated'])
@pytest.mark.parametrize('params', [
    {'expected_count': 13, 'interval': '2h', },
    {'expected_count': 20161, 'starttime': '2017-10-01 00:00', 'endtime': '2017-10-15 00:00', 'interval': '1m', }
])
def test_attribute_interpolated_return_expected_value_count(
    webapi, query, key, params,
):
    element = webapi.elements(query)[0]
    attribute = element['SampleInput']
    assert isinstance(attribute, osisoftpy.Attribute) 
    expected_count = params.pop('expected_count')
    valuekey = getattr(attribute, key)
    values = valuekey(**params)
    assert values.__len__() == expected_count

@pytest.mark.parametrize('query', ['attributename:SampleInput'])
@pytest.mark.parametrize('key', ['interpolatedattimes'])
@pytest.mark.parametrize('params', [
    {'timestamps': now().format('YYYY-MM-DD HH:mm:ss ZZ'), 'expected_count': 1},
    {'timestamps': [now().format('YYYY-MM-DD HH:mm:ss ZZ'), now().replace(weeks=-1).format('YYYY-MM-DD HH:mm:ss ZZ')], 'expected_count': 2},
    {'timestamps': [
        now().format('YYYY-MM-DD HH:mm:ss ZZ'),
        now().replace(weeks=-1).format('YYYY-MM-DD HH:mm:ss ZZ'),
        now().replace(weeks=-2).format('YYYY-MM-DD HH:mm:ss ZZ'),
        now().replace(weeks=-3).format('YYYY-MM-DD HH:mm:ss ZZ'),
        now().replace(weeks=-4).format('YYYY-MM-DD HH:mm:ss ZZ'),
        now().replace(weeks=-5).format('YYYY-MM-DD HH:mm:ss ZZ'),
        now().replace(weeks=-6).format('YYYY-MM-DD HH:mm:ss ZZ'),

    ], 'expected_count': 7},
])
def test_attribute_interpolatedattimes_return_expected_value_count(
        webapi, query, key, params,
):
    element = webapi.elements(query)[0]
    attribute = element['SampleInput']
    assert isinstance(attribute, osisoftpy.Attribute) 
    expected_count = params.pop('expected_count')
    valuekey = getattr(attribute, key)
    values = valuekey(**params)
    assert values.__len__() == expected_count

@pytest.mark.parametrize('query', ['attributename:SampleInput'])
@pytest.mark.parametrize('key', ['recorded'])
@pytest.mark.parametrize('params', [
    {},
    {'starttime': '*-14d'},
    {'starttime': '*-14d', 'endtime': '*-7d'},
    {'starttime': '*-14d', 'boundarytype': 'inside'},
    {'starttime': '*-14d', 'endtime': '*-7d', 'boundarytype': 'outside'},
])
def test_attribute_recorded_return_values(
        webapi, query, key, params,
):
    element = webapi.elements(query)[0]
    attribute = element['SampleInput']
    assert isinstance(attribute, osisoftpy.Attribute) 
    valuekey = getattr(attribute, key)
    values = valuekey(**params)
    assert values.__len__() > 0


@pytest.mark.parametrize('query', ['attributename:SampleInput'])
@pytest.mark.parametrize('key', ['recordedattime'])
@pytest.mark.parametrize('retrievalmode',['Auto', 'AtOrBefore', 'Before', 'AtOrAfter', 'After','Exact'])
def test_attribute_recorded_returns_one_value(
    webapi, now, query, key, retrievalmode,
):
    element = webapi.elements(query)[0]
    attribute = element['SampleInput']
    assert isinstance(attribute, osisoftpy.Attribute) 
    valuekey = getattr(attribute, key)
    payload = {'time': now.format('YYYY-MM-DD HH:mm:ss ZZ'), 'retrievalmode': retrievalmode}
    value = valuekey(**payload)
    assert isinstance(value, osisoftpy.Value)


@pytest.mark.parametrize('query', ['attributename:SampleConfigItem'])
@pytest.mark.parametrize('key', ['value'])
@pytest.mark.parametrize('params', [{}])
def test_attribute_recorded_return_values_configitem(
        webapi, query, key, params,
):
    element = webapi.elements(query)[0]
    attribute = element['SampleConfigItem']
    assert float(attribute.value) == 24
