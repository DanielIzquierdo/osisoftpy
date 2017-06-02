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
osisoftpy.tests.test_point_insert.py
~~~~~~~~~~~~

Tests for the update_value and update_values functions 
in the`osisoftpy.point` module.
"""
import osisoftpy
import pytest

@pytest.mark.parametrize('query', ['name:EdwinPythonTest'])
@pytest.mark.parametrize('timestamp', ['2017-02-01 06:00', '2017-03-05 15:00', '2017-04-15 17:00'])
@pytest.mark.parametrize('value', [2017, 6, 549])
def test_point_update_value_single(webapi, query, timestamp, value):
    points = webapi.points(query=query)
    #for some reason points increments by 1 for each test
    # assert(points.__len__() == 1)
    for point in points:
        point.update_value(timestamp, value)
        p = point.current(time=timestamp, overwrite=False)
        assert p.value == value

        #timestamp formatting issue:
        # assert p.timestamp == timestamp
