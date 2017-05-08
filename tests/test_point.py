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
from .conftest import query
from .conftest import pointvalues

skip = False


@pytest.mark.skipif(skip, reason='Takes an extra 2s...')
@pytest.mark.parametrize('query', [(query())])
@pytest.mark.parametrize('count', [10])
@pytest.mark.parametrize('key', ['current'])
def test_points_singlevaluekeys_are_immutable(webapi, query, count, key):
    """

    :param webapi: 
    :param query: 
    :param count: 
    :param key: 
    """
    points = webapi.points(params=dict(q=query, count=count))
    assert all(isinstance(x, osisoftpy.Point) for x in points)
    for point in points:
        with pytest.raises(AttributeError) as e:
            print(point, key, 'foo')
            setattr(point, key, 'foo')
        e.match('can\'t set attribute')
        assert isinstance(point.current, osisoftpy.Value)


@pytest.mark.skipif(skip, reason='Takes an extra 2s...')
@pytest.mark.parametrize('query', ['name:sinusoid'])
@pytest.mark.parametrize('count', [10])
@pytest.mark.parametrize('keys', [pointvalues().single])
def test_points_singlevaluekeys_are_validtypes(webapi, query, count, keys):
    """

    :param webapi: 
    :param query: 
    :param count: 
    :param keys: 
    """
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

@pytest.mark.skipif(skip, reason='Takes an extra 2s...')
@pytest.mark.parametrize('query', ['name:sinusoid'])
@pytest.mark.parametrize('count', [10])
@pytest.mark.parametrize('keys', [pointvalues().multi])
def test_points_multivaluekeys_are_validtypes(webapi, query, count, keys):
    """

    :param webapi: 
    :param query: 
    :param count: 
    :param keys: 
    """
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

@pytest.mark.skipif(skip, reason='Takes an extra 2s...')
@pytest.mark.parametrize('query', ['name:sinusoid'])
@pytest.mark.parametrize('count', [10])
@pytest.mark.parametrize('keys', [pointvalues().multi])
def test_points_interpolated_default_kwargs(webapi, query, count, keys):
    """

    :param webapi: 
    :param query: 
    :param count: 
    :param keys: 
    """
    payload = dict(q=query, count=count)
    points = webapi.points(params=payload)
    assert all(isinstance(x, osisoftpy.Point) for x in points)
    for point in points:
        for k in keys:
            valuekey = getattr(point, k)
            print(valuekey)
            values = valuekey()
            for v in values:
                print(v)


