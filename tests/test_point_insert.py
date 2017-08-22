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
import time
from osisoftpy.exceptions import MismatchEntriesError
from datetime import datetime

# https://techsupport.osisoft.com/Troubleshooting/Known-Issues/176830
piserverissue = True

# Testing values
# @pytest.mark.skipif(piserverissue, reason='PI Server times out when retrieving archived values')
@pytest.mark.parametrize('query', ['name:PythonInserted'])
# @pytest.mark.parametrize('timestamp', ['2017-02-01 11:00','2017-03-05 15:00','2017-04-15 17:00'])
@pytest.mark.parametrize('value', [618])
def test_point_update_value_single(webapi, query, now, value, ci, pythonversion):
    timestamp = now.shift(hours=-1).format('YYYY-MM-DD HH:mm:ss ZZ')
    points = webapi.points(query='{}_{}{}'.format(query, ci, pythonversion))
    assert(len(points) == 1)
    for point in points:
        point.update_value(timestamp, value)
        time.sleep(0.5)
        v = point.recordedattime(time=timestamp)
        assert v.value == value
        
# Testing "good"
# @pytest.mark.skipif(piserverissue, reason='PI Server times out when retrieving archived values')
@pytest.mark.parametrize('query', ['name:PythonInserted'])
# @pytest.mark.parametrize('timestamp', ['2017-02-01 07:00'])
@pytest.mark.parametrize('value', [2017])
@pytest.mark.parametrize('good', [True, False])
def test_point_update_good_flag(webapi, query, now, value, good, ci, pythonversion):
    timestamp = now.shift(hours=-2).format('YYYY-MM-DD HH:mm:ss ZZ')
    points = webapi.points(query='{}_{}{}'.format(query, ci, pythonversion))
    assert(len(points) == 1)
    for point in points:
        point.update_value(timestamp, value, good=good)
        time.sleep(0.5)
        p = point.recordedattime(time=timestamp)
        assert p.good == good

# Testing "questionable"
# @pytest.mark.skipif(piserverissue, reason='PI Server times out when retrieving archived values')
@pytest.mark.parametrize('query', ['name:PythonInserted'])
# @pytest.mark.parametrize('timestamp', ['2017-02-01 08:00'])
@pytest.mark.parametrize('value', [2018])
@pytest.mark.parametrize('questionable', [True, False])
def test_point_update_questionable_flag(webapi, query, now, value, questionable, ci, pythonversion):
    timestamp = now.shift(hours=-3).format('YYYY-MM-DD HH:mm:ss ZZ')
    points = webapi.points(query='{}_{}{}'.format(query, ci, pythonversion))
    assert(len(points) == 1)
    for point in points:
        point.update_value(timestamp, value, questionable=questionable)
        time.sleep(0.5)
        p = point.recordedattime(time=timestamp)
        assert p.questionable == questionable


# Testing "unitsabbreviation"
# @pytest.mark.skipif(piserverissue, reason='PI Server times out when retrieving archived values')
@pytest.mark.skipif(True, reason="units of measure aren't being written")
@pytest.mark.parametrize('query', ['name:PythonInserted'])
# @pytest.mark.parametrize('timestamp', ['2017-02-01 06:00'])
@pytest.mark.parametrize('value', [2017])
@pytest.mark.parametrize('unitsabbreviation', ['m', 's', 'm/s', 'A', 'K'])
def test_point_update_unitsabbreviation(webapi, query, now, value, unitsabbreviation, ci, pythonversion):
    timestamp = now.shift(hours=-4).format('YYYY-MM-DD HH:mm:ss ZZ')
    points = webapi.points(query='{}_{}{}'.format(query, ci, pythonversion))
    assert(len(points) == 1)
    for point in points:
        point.update_value(timestamp, value, unitsabbreviation=unitsabbreviation)
        time.sleep(0.5)
        p = point.recordedattime(time=timestamp)
        assert p.unitsabbreviation == unitsabbreviation

# Testing "updateoption" Replace
# @pytest.mark.skipif(piserverissue, reason='PI Server times out when retrieving archived values')
@pytest.mark.parametrize('query', ['name:PythonInserted'])
# @pytest.mark.parametrize('timestamp', ['2017-03-01 06:00'])
@pytest.mark.parametrize('value', [289])
@pytest.mark.parametrize('updateoption', ['Replace'])
def test_point_update_updatereplace(webapi, query, now, value, updateoption, ci, pythonversion):
    timestamp = now.shift(hours=-5).format('YYYY-MM-DD HH:mm:ss ZZ')
    points = webapi.points(query='{}_{}{}'.format(query, ci, pythonversion))
    assert(len(points) == 1)
    for point in points:
        point.update_value(timestamp, 0, updateoption='Replace')
        time.sleep(0.5)
        point.update_value(timestamp, value, updateoption=updateoption)
        time.sleep(0.5)
        p = point.recordedattime(time=timestamp)
        assert p.value == value

# Testing "updateoption" Insert
# @pytest.mark.skipif(piserverissue, reason='PI Server times out when retrieving archived values')
@pytest.mark.parametrize('query', ['name:PythonInserted'])
# @pytest.mark.parametrize('timestamp', ['2017-03-02 07:00'])
@pytest.mark.parametrize('value', [345])
@pytest.mark.parametrize('updateoption', ['Insert'])
def test_point_update_updateinsert(webapi, query, now, value, updateoption, ci, pythonversion):
    timestamp = now.shift(hours=-6).format('YYYY-MM-DD HH:mm:ss ZZ')
    points = webapi.points(query='{}_{}{}'.format(query, ci, pythonversion))
    assert(len(points) == 1)
    for point in points:
        point.update_value(timestamp, 0, updateoption='Replace')
        time.sleep(0.5)
        point.update_value(timestamp, value, updateoption=updateoption)
        time.sleep(0.5)
        p = point.recordedattime(time=timestamp)
        assert p.value == value

# Testing "updateoption" NoReplace
# @pytest.mark.skipif(piserverissue, reason='PI Server times out when retrieving archived values')
@pytest.mark.parametrize('query', ['name:PythonInserted'])
# @pytest.mark.parametrize('timestamp', ['2017-03-03 09:00'])
@pytest.mark.parametrize('value', [2000])
@pytest.mark.parametrize('updateoption', ['NoReplace'])
def test_point_update_updatenoreplace(webapi, query, now, value, updateoption, ci, pythonversion):
    timestamp = now.shift(hours=-7).format('YYYY-MM-DD HH:mm:ss ZZ')
    points = webapi.points(query='{}_{}{}'.format(query, ci, pythonversion))
    assert(len(points) == 1)
    for point in points:
        point.update_value(timestamp, 0, updateoption='Replace')
        time.sleep(0.5)
        point.update_value(timestamp, value, updateoption=updateoption)
        time.sleep(0.5)
        p = point.recordedattime(time=timestamp)
        assert p.value == 0

# Testing "updateoption" ReplaceOnly
# @pytest.mark.skipif(piserverissue, reason='PI Server times out when retrieving archived values')
@pytest.mark.parametrize('query', ['name:PythonInserted'])
# @pytest.mark.parametrize('timestamp', ['2017-03-04 10:00'])
@pytest.mark.parametrize('value', [65])
@pytest.mark.parametrize('updateoption', ['ReplaceOnly'])
def test_point_update_updatereplaceonly(webapi, query, now, value, updateoption, ci, pythonversion):
    timestamp = now.shift(hours=-8).format('YYYY-MM-DD HH:mm:ss ZZ')
    points = webapi.points(query='{}_{}{}'.format(query, ci, pythonversion))
    assert(len(points) == 1)
    for point in points:
        point.update_value(timestamp, 0, updateoption='Replace')
        time.sleep(0.5)
        point.update_value(timestamp, value, updateoption=updateoption)
        time.sleep(0.5)
        p = point.recordedattime(time=timestamp)
        assert p.value == value

# Testing "updateoption" InsertNoCompression
# @pytest.mark.skipif(piserverissue, reason='PI Server times out when retrieving archived values')
@pytest.mark.parametrize('query', ['name:PythonInserted'])
# @pytest.mark.parametrize('timestamp', ['2017-03-05 11:00'])
@pytest.mark.parametrize('value', [1])
@pytest.mark.parametrize('updateoption', ['InsertNoCompression'])
def test_point_update_updateinsertnocomp(webapi, query, now, value, updateoption, ci, pythonversion):
    timestamp = now.shift(hours=-13).format('YYYY-MM-DD HH:mm:ss ZZ')
    points = webapi.points(query='{}_{}{}'.format(query, ci, pythonversion))
    assert(len(points) == 1)
    for point in points:
        point.update_value(timestamp, 0, updateoption='Replace')
        time.sleep(0.5)
        point.update_value(timestamp, value, updateoption=updateoption)
        time.sleep(0.5)
        p = point.recordedattime(time=timestamp)
        assert p.value == value

# Testing "updateoption" Remove
# @pytest.mark.skipif(piserverissue, reason='PI Server times out when retrieving archived values')
@pytest.mark.parametrize('query', ['name:PythonInserted'])
# @pytest.mark.parametrize('timestamp', ['2017-03-06 12:00'])
@pytest.mark.parametrize('value', [908])
@pytest.mark.parametrize('updateoption', ['Remove'])
def test_point_update_updateremove(webapi, query, now, value, updateoption, ci, pythonversion):
    timestamp = now.shift(hours=-9).format('YYYY-MM-DD HH:mm:ss ZZ')
    points = webapi.points(query='{}_{}{}'.format(query, ci, pythonversion))
    assert(len(points) == 1)
    for point in points:
        point.update_value(timestamp, 0, updateoption='Replace')
        time.sleep(0.5)
        point.update_value(timestamp, value, updateoption=updateoption)
        time.sleep(0.5)
        p = point.recordedattime(time=timestamp)
        assert p.value == 0

#update_values
# Test Multiple Inputs
# @pytest.mark.skipif(piserverissue, reason='PI Server times out when retrieving archived values')
@pytest.mark.parametrize('query', ['name:PythonInserted'])
# @pytest.mark.parametrize('timestamps', [['2017-03-07 06:00','2017-03-07 07:00','2017-03-07 08:00','2017-03-07 09:00','2017-03-07 10:00']])
@pytest.mark.parametrize('values', [[217,218,216]])
def test_point_multiple_update(webapi, query, now, values, ci, pythonversion):
    timestamps = [now.shift(hours=-10).format('YYYY-MM-DD HH:mm:ss ZZ'), now.shift(hours=-11).format('YYYY-MM-DD HH:mm:ss ZZ'), now.shift(hours=-12).format('YYYY-MM-DD HH:mm:ss ZZ')]
    points = webapi.points(query='{}_{}{}'.format(query, ci, pythonversion))
    assert(len(points) == 1)
    for point in points:
        point.update_values(timestamps, values)
        time.sleep(0.5)
        for timestamp, value in zip(timestamps, values):
            p = point.recordedattime(time=timestamp)
            assert p.value == value

# Test Mismatched arrays (Timestamps and Values)
@pytest.mark.parametrize('query', ['name:PythonInserted'])
@pytest.mark.parametrize('timestamps', [['2017-02-01 06:00','2017-02-01 07:00','2017-02-01 08:00','2017-02-01 09:00','2017-02-01 10:00']])
@pytest.mark.parametrize('values', [[2017,2018,2019,2020]])
def test_point_multiple_mismatch(webapi, query, timestamps, values, ci, pythonversion):
    points = webapi.points(query='{}_{}{}'.format(query, ci, pythonversion))
    assert(len(points) == 1)
    with pytest.raises(MismatchEntriesError) as err:
        for point in points:
            point.update_values(timestamps, values)