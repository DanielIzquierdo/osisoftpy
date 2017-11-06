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
osisoftpy.tests.test_point.py
~~~~~~~~~~~~

Tests for the `osisoftpy.point` module.
"""

import re

import osisoftpy
import pytest

from .conftest import now
from .conftest import pointvalues

skip = True


# TODO: add tests for docstrings
# TODO: consider if still worth testing
# @pytest.mark.parametrize('query', [(query())])
# @pytest.mark.parametrize('count', [10])
# @pytest.mark.parametrize('key', pointvalues().single)
# def test_points_singlevaluekeys_are_immutable(webapi, query, count, key):
#     payload = dict(query=query, count=count)
#     points = webapi.points(**payload)
#     assert all(isinstance(x, osisoftpy.Point) for x in points)
#     for point in points:
#         with pytest.raises(AttributeError) as e:
#             print(point, key, 'foo')
#             setattr(point, key, 'foo')
#         e.match('can\'t set attribute')
#         assert isinstance(point.current, osisoftpy.Value)


@pytest.mark.parametrize('query', ['name:sinusoid'])
@pytest.mark.parametrize('count', [10])
@pytest.mark.parametrize('keys', [pointvalues().single])
def test_points_singlevaluekeys_are_validtypes(webapi, query, count, keys):
    payload = dict(query=query, count=count)
    points = webapi.points(**payload)
    assert all(isinstance(x, osisoftpy.Point) for x in points)
    for point in points:
        for k in keys:
            try:
                valuekey = getattr(point, k)
                if re.match('int\d{0,2}', point.datatype, re.IGNORECASE):
                    assert type(valuekey.value) is int
                elif re.match('float\d{0,2}', point.datatype, re.IGNORECASE):
                    assert type(valuekey.value) is float
            except AttributeError:
                pass


@pytest.mark.parametrize('query', ['name:sinusoid'])
@pytest.mark.parametrize('count', [10])
@pytest.mark.parametrize('keys', [pointvalues().multi])
def test_points_multivaluekeys_are_validtypes(webapi, query, count, keys):
    payload = dict(query=query, count=count)
    points = webapi.points(**payload)
    assert all(isinstance(x, osisoftpy.Point) for x in points)
    for point in points:
        for k in keys:
            try:
                valuekey = getattr(point, k)
                if re.match('int\d{0,2}', point.datatype, re.IGNORECASE):
                    assert type(valuekey.value) is int
                elif re.match('float\d{0,2}', point.datatype, re.IGNORECASE):
                    assert type(valuekey.value) is float
            except AttributeError:
                pass

def test_points_only_create_pipoints(webapi):
    afelement='PythonElement'
    payload = dict(query="name:{}".format(afelement), count=10)
    r = webapi.request(**payload)
    assert r.json().get('TotalHits') > 0
    points = webapi.points(**payload)
    assert points.__len__() == 0

# TODO: Currently failing cuz of daylight savings
@pytest.mark.parametrize('query', ['name:sinusoid'])
@pytest.mark.parametrize('count', [10])
@pytest.mark.parametrize('key', ['interpolated'])
@pytest.mark.parametrize('params', [
    {'expected_count': 13, 'interval': '2h', },
    {'expected_count': 20161, 'starttime': '*-14d', 'interval': '1m', }
])
def test_points_interpolated_return_expected_value_count(
    webapi, query, count, key, params,
):
    payload = dict(query=query, count=count)
    points = webapi.points(**payload)
    assert all(isinstance(x, osisoftpy.Point) for x in points)
    expected_count = params.pop('expected_count')
    for point in points:
        valuekey = getattr(point, key)
        values = valuekey(**params)
        assert values.__len__() == expected_count


@pytest.mark.parametrize('query', ['name:sinusoid'])
@pytest.mark.parametrize('count', [10])
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
def test_points_interpolatedattimes_return_expected_value_count(
        webapi, query, count, key, params,
):
    payload = dict(query=query, count=count)
    points = webapi.points(**payload)
    assert all(isinstance(x, osisoftpy.Point) for x in points)
    expected_count = params.pop('expected_count')
    for point in points:
        valuekey = getattr(point, key)
        values = valuekey(**params)
        assert values.__len__() == expected_count


# TODO : figure out how to calculate the expected number of recorded values
@pytest.mark.parametrize('query', ['name:sinusoid'])
@pytest.mark.parametrize('count', [10])
@pytest.mark.parametrize('key', ['recorded'])
@pytest.mark.parametrize('params', [
    {},
    {'starttime': '*-14d'},
    {'starttime': '*-14d', 'endtime': '*-7d'},
    {'starttime': '*-14d', 'boundarytype': 'inside'},
    {'starttime': '*-14d', 'endtime': '*-7d', 'boundarytype': 'outside'},

])
def test_points_recorded_return_values(
        webapi, query, count, key, params,
):
    payload = dict(query=query, count=count)
    points = webapi.points(**payload)
    assert all(isinstance(x, osisoftpy.Point) for x in points)
    for point in points:
        valuekey = getattr(point, key)
        values = valuekey(**params)
        assert values.__len__() > 0


@pytest.mark.parametrize('query', ['name:sinusoid'])
@pytest.mark.parametrize('count', [10])
@pytest.mark.parametrize('key', ['recordedattime'])
@pytest.mark.parametrize('retrievalmode',['Auto', 'AtOrBefore', 'Before', 'AtOrAfter', 'After','Exact'])
def test_points_recorded_returns_one_value(
    webapi, now, query, count, key, retrievalmode,
):
    payload = dict(query=query, count=count)
    points = webapi.points(**payload)
    assert all(isinstance(x, osisoftpy.Point) for x in points)
    for point in points:
        valuekey = getattr(point, key)
        payload = {'time': now.format('YYYY-MM-DD HH:mm:ss ZZ'), 'retrievalmode': retrievalmode}
        value = valuekey(**payload)
        assert isinstance(value, osisoftpy.Value)
        # for value in values:
        #     print('Point {}, recorded value {} {}: {}'.format(
        #         point.name, retrievalmode, now, value.value))

@pytest.mark.parametrize('query', ['name:sinusoid'])
def test_point_contains_dataserver(
    webapi, query
):
    payload = dict(query=query)
    points = webapi.points(**payload)
    assert all(isinstance(x.dataserver, osisoftpy.DataServer) for x in points)

def test_webapi_dispalys_dataserver_helper(
    webapi, capfd
):
    webapi.piservers()
    out, err = capfd.readouterr()
    assert 'pi:' in out