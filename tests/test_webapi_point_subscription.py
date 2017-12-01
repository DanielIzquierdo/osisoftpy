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
osisoftpy.tests.test_webapi_point_subscription.py
~~~~~~~~~~~~

Tests for subscriptions in the `osisoftpy.webapi` module.
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

def test_webapi_subscribe_typeerror(webapi):
    points = 1
    try:
        webapi.subscribe(points, 'current')
    except Exception as err:
        assert isinstance(err, TypeError)

# a list to store modified points in:
updated_points = []
def callback(sender):
    updated_points.append(sender)

# test getvalue
@pytest.mark.skipif(True, reason='Method only used for internal testing')
@pytest.mark.parametrize('query', ['name:PythonInserted_appveyor*'])
@pytest.mark.parametrize('stream', ['getvalue'])
def test_subscription_getvalue(webapi, query, stream, callback=callback):
    updated_points[:] = []
    points = webapi.points(query=query)
    subscriptions = webapi.subscribe(points, stream, callback=callback)
    for point in points:
        v1 = point.getvalue("5-16-2017 07:00")
        v2 = point.getvalue("5-17-2017 07:00")
    assert len(updated_points) > 0
    subscriptions = webapi.unsubscribe(points, stream)

updated_points_current = []
def callback_current(sender):
    updated_points_current.append(sender)

# test current_value
@pytest.mark.parametrize('query', ['name:PythonInserted_appveyor'])
@pytest.mark.parametrize('stream', ['current'])
def test_subscription_current(webapi, query, stream, callback=callback_current):
    #clear array from previous tests
    updated_points_current[:] = []

    points = webapi.points(query=query)
    subscriptions = webapi.subscribe(points, stream, callback=callback_current)
    for point in points:
        v1 = point.current()
        point.update_values(["*"], [random.uniform(0,100)])
        time.sleep(0.5)
        v2 = point.current()
    assert len(updated_points_current) == 1 # one point updated
    subscriptions = webapi.unsubscribe(points, stream)

updated_points_end = []
def callback_end(sender):
    updated_points_end.append(sender)

# test end_value
@pytest.mark.parametrize('query', ['name:PythonInserted_travis'])
@pytest.mark.parametrize('stream', ['end'])
def test_subscription_end(webapi, query, stream, callback=callback_end):
    #clear array from previous tests
    updated_points_end[:] = []

    points = webapi.points(query=query)
    subscriptions = webapi.subscribe(points, stream, callback=callback_end)
    for point in points:
        point.update_values(["*"], [random.uniform(0,100)])
        time.sleep(0.5)
        v1 = point.end()
        point.update_values(["*+1m"], [random.uniform(0,100)])
        time.sleep(0.5)
        v2 = point.end()
    assert len(updated_points_end) == 1
    subscriptions = webapi.unsubscribe(points, stream)

updated_points_interp_1 = []
def callback_interp_1(sender):
    updated_points_interp_1.append(sender)

# test interpolatedattimes - assumes no one has used this tag
# @pytest.mark.skipif(piserverissue, reason='PI Server times out when retrieving archived values')
@pytest.mark.parametrize('query', ['name:PythonInterpolatedAtTime'])
# @pytest.mark.parametrize('times', [['2017-01-01T00:00:00Z']])
def test_subscription_interpolatedattimes_single_timestamp_notify_one(webapi, query, now, ci, pythonversion, callback=callback_interp_1):
    #clear array from previous tests
    updated_points_interp_1[:] = []
    times = [now.shift(hours=-168).format('YYYY-MM-DD HH:mm:ss ZZ')]
    #query points (should be 1)
    points = webapi.points(query='{}_{}{}'.format(query, ci, pythonversion))
    for point in points:
        for t in times:
            #subscriber each timestamp for this point
            webapi.subscribe(points, 'interpolatedattimes', startdatetime=t, callback=callback_interp_1)

            #setup with values here: insert a value 1 day before and after timestamp: 0 to 1000
            #datetime is parsed so days can added/subtracted
            parseddatetime = parser.parse(t)
            date1 = (parseddatetime + timedelta(minutes=-1)).strftime('%Y-%m-%dT%H:%M:%SZ')
            point.update_value(date1, 0)
            time.sleep(0.5)

            date2 = (parseddatetime + timedelta(minutes=1)).strftime('%Y-%m-%dT%H:%M:%SZ')
            point.update_value(date2, 1000)
            time.sleep(0.5)

            #gets initial value for subscriber
            point.interpolatedattimes([t])

            #updates after value to 500, so there should be a new interpolated value
            point.update_value(date1, 500)
            time.sleep(0.5)

            #queries new point and should trigger callback function
            point.interpolatedattimes([t])
    assert len(updated_points_interp_1) == 1
    webapi.unsubscribe(points, 'interpolatedattimes')
    
updated_points_interp_2 = []
def callback_interp_2(sender):
    updated_points_interp_2.append(sender)

# test interpolatedattimes - assumes no one has used this tag
# @pytest.mark.skipif(piserverissue, reason='PI Server times out when retrieving archived values')
@pytest.mark.parametrize('query', ['name:PythonInterpolatedAtTime'])
# @pytest.mark.parametrize('times', [['2016-05-01T00:00:00Z','2016-06-01T00:00:00Z']])
def test_subscription_interpolatedattimes_single_timestamp_notify_two(webapi, query, now, ci, pythonversion, callback=callback_interp_2):
    #clear array from previous tests
    updated_points_interp_2[:] = []
    times = [now.shift(hours=-48).format('YYYY-MM-DD HH:mm:ss ZZ'), now.shift(hours=-96).format('YYYY-MM-DD HH:mm:ss ZZ')]
    #query points (should be 1)
    points = webapi.points(query='{}_{}{}'.format(query, ci, pythonversion))
    for point in points:
        for t in times:
            #subscriber each timestamp for this point
            webapi.subscribe(points, 'interpolatedattimes', startdatetime=t, callback=callback_interp_2)

            #setup with values here: insert a value 1 day before and after timestamp: 0 to 1000
            #datetime is parsed so days can added/subtracted
            parseddatetime = parser.parse(t)
            date1 = (parseddatetime + timedelta(minutes=-1)).strftime('%Y-%m-%dT%H:%M:%SZ')
            point.update_value(date1, 0)
            time.sleep(0.5)

            date2 = (parseddatetime + timedelta(minutes=1)).strftime('%Y-%m-%dT%H:%M:%SZ')
            point.update_value(date2, 1000)
            time.sleep(0.5)

    #gets initial values for subscriber
    point.interpolatedattimes(times)

    #queries new value and should trigger callback function
    for point in points:
        for t in times:
            #updates after value to 500, so there should be a new interpolated value
            parseddatetime = parser.parse(t)
            date2 = (parseddatetime + timedelta(minutes=1)).strftime('%Y-%m-%dT%H:%M:%SZ')
            point.update_value(date2, 500)
            time.sleep(0.5)

    point.interpolatedattimes(times)
    assert updated_points_interp_2.__len__() == 2
    webapi.unsubscribe(points, 'interpolatedattimes')

updated_points_recorded = []
def callback_recorded(sender):
    updated_points_recorded.append(sender)

# @pytest.mark.skipif(piserverissue, reason='PI Server times out when retrieving archived values')
@pytest.mark.parametrize('query', ['name:PythonRecordedAtTime'])
# @pytest.mark.parametrize('time', ['2017-01-01T00:00:00Z','2017-01-02T00:00:00Z'])
def test_subscription_recordedattimes(webapi, query, now, ci, pythonversion, callback=callback_recorded):
    #clear array from previous test
    updated_points_recorded[:] = []

    t = now.shift(hours=-26).format('YYYY-MM-DD HH:mm:ss ZZ')

    #query points (should be 1)
    points = webapi.points(query='{}_{}{}'.format(query, ci, pythonversion))
    for point in points:
        webapi.subscribe(points, 'recordedattime', startdatetime=t, callback=callback_recorded)
        # parseddatetime = parser.parse(time)
        # date = (parseddatetime + timedelta(days=-1)).strftime('%Y-%m-%dT%H:%M:%SZ')
        point.update_value(t, 134)
        time.sleep(0.5)

        point.recordedattime(t)
        point.update_value(t, 160)
        time.sleep(0.5)
        #should trigger callback function
        point.recordedattime(t)
    assert len(updated_points_recorded) == 1
    webapi.unsubscribe(points, 'recordedattime')