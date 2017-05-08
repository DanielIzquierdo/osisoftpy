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

import pytest
import osisoftpy

from .conftest import pointvalues
from .conftest import query
from .conftest import now

skip = False



# TODO: add tests for docstrings


@pytest.mark.parametrize('query', [(query())])
@pytest.mark.parametrize('count', [10])
@pytest.mark.parametrize('key', pointvalues().single)
def test_points_singlevaluekeys_are_immutable(webapi, query, count, key):
    points = webapi.points(params=dict(q=query, count=count))
    assert all(isinstance(x, osisoftpy.Point) for x in points)
    for point in points:
        with pytest.raises(AttributeError) as e:
            print(point, key, 'foo')
            setattr(point, key, 'foo')
        e.match('can\'t set attribute')
        assert isinstance(point.current, osisoftpy.Value)


@pytest.mark.parametrize('query', ['name:sinusoid'])
@pytest.mark.parametrize('count', [10])
@pytest.mark.parametrize('keys', [pointvalues().single])
def test_points_singlevaluekeys_are_validtypes(webapi, query, count, keys):
    payload = dict(q=query, count=count)
    points = webapi.points(params=payload)
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
    payload = dict(q=query, count=count)
    points = webapi.points(params=payload)
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
@pytest.mark.parametrize('key', ['interpolated'])
@pytest.mark.parametrize('params', [
    {'expected_count': 13, 'interval': '2h', },
    {'expected_count': 20161, 'starttime': '*-14d', 'interval': '1m', }
])
def test_points_interpolated_return_expected_value_count(
        webapi, query, count, key, params,
):
    payload = dict(q=query, count=count)
    points = webapi.points(params=payload)
    assert all(isinstance(x, osisoftpy.Point) for x in points)
    for point in points:
        valuekey = getattr(point, key)
        expected_count = params.pop('expected_count')
        values = valuekey(**params)
        assert values.__len__() == expected_count


@pytest.mark.parametrize('query', ['name:sinusoid'])
@pytest.mark.parametrize('count', [10])
@pytest.mark.parametrize('key', ['interpolatedattimes'])
@pytest.mark.parametrize('params', [
    {'time': now(), 'expected_count': 1},
    {'time': [now(), now().replace(weeks=-1)], 'expected_count': 2},
    {'time': [
        now(),
        now().replace(weeks=-1),
        now().replace(weeks=-2),
        now().replace(weeks=-3),
        now().replace(weeks=-4),
        now().replace(weeks=-5),
        now().replace(weeks=-6),

    ], 'expected_count': 7},
])
def test_points_interpolatedattimes_return_expected_value_count(
        webapi, query, count, key, params,
):
    payload = dict(q=query, count=count)
    points = webapi.points(params=payload)
    assert all(isinstance(x, osisoftpy.Point) for x in points)
    for point in points:
        valuekey = getattr(point, key)
        expected_count = params.pop('expected_count')
        values = valuekey(**params)
        assert values.__len__() == expected_count

#TODO : figure out how to calculate the expected number of recorded values
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
    payload = dict(q=query, count=count)
    points = webapi.points(params=payload)
    assert all(isinstance(x, osisoftpy.Point) for x in points)
    for point in points:
        valuekey = getattr(point, key)
        values = valuekey(**params)
        assert values.__len__() > 0


@pytest.mark.parametrize('query', ['name:sinusoid'])
@pytest.mark.parametrize('count', [10])
@pytest.mark.parametrize('key', ['recordedattime'])
@pytest.mark.parametrize('retrievalmode',
    ['Auto','AtOrBefore','Before','AtOrAfter','After','Exact'])
def test_points_recorded_returns_one_value(
        webapi, query, count, key, now, retrievalmode,
):
    payload = dict(q=query, count=count)
    points = webapi.points(params=payload)
    assert all(isinstance(x, osisoftpy.Point) for x in points)
    for point in points:
        valuekey = getattr(point, key)
        payload = {'time': now, 'retrievalmode': retrievalmode}
        values = valuekey(**payload)
        assert all(isinstance(x, osisoftpy.Value) for x in values)
        assert values.__len__() == 1
        for value in values:
            print('Point {}, recorded value {} {}: {}'.format(
                point.name, retrievalmode, now, value.value))










