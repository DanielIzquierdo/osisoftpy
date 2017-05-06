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
import requests
from .conftest import query

skip = True

@pytest.mark.skipif(skip, reason="Takes an extra 8s...")
@pytest.mark.parametrize('query', query())
def test_point_current(webapi, query):
    payload = {"q": query, "count": 10}
    points = webapi.points(params=payload)
    assert all(isinstance(x, osisoftpy.Point) for x in points)
    for point in points:
        current = point.current()
        if re.match('int\d{0,2}', point.datatype, re.IGNORECASE):
            assert type(current.value) is int
        elif re.match('float\d{0,2}', point.datatype, re.IGNORECASE):
            assert type(current.value) is float

def test_point_sinusoid_current_is_immutable(webapi):
    tag = 'sinusoid'
    payload = {"q": "name:{}".format(tag), "count": 10}
    points = webapi.points(params=payload)
    assert all(isinstance(x, osisoftpy.Point) for x in points)
    for point in points:
        with pytest.raises(AttributeError) as e:
            point.current = 'foo'
        e.match('can\'t set attribute')
        assert isinstance(point.current, osisoftpy.Value)

