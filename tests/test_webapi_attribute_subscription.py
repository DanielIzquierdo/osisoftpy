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
osisoftpy.tests.test_webapi_attribute_subscription.py
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

# a list to store modified points in:
updated_attributes_current = []
def callback_current(sender):
    updated_attributes_current.append(sender)

@pytest.mark.parametrize('query', ['attributename:PythonAFInserted'])
@pytest.mark.parametrize('stream', ['current'])
def test_subscription_current(webapi, query, stream, ci, pythonversion, callback=callback_current):
    #clear array from previous tests
    updated_attributes_current[:] = []

    if ci == 'test':
        elementname = 'Attributes'
    else:
        elementname = pythonversion or ci
        parent = ci
    elements = webapi.elements(query='{} AND name:{}'.format(query, elementname))
    if len(elements) > 1:
        elementlist = [ele for ele in elements if parent in ele.paths[0]]
    else:
        elementlist = elements
    
    subscriptions = webapi.subscribe(elementlist, stream, callback=callback_current)
    for element in elementlist:
        afattribute = element['PythonAFInserted']
        v1 = afattribute.current()
        afattribute.update_values(["*"], [random.uniform(0,100)])
        time.sleep(0.5)
        v2 = afattribute.current()
    assert len(updated_attributes_current) == 1 # one point updated
    subscriptions = webapi.unsubscribe(elements, stream)
    

# test end_value
updated_attributes_end = []
def callback_end(sender):
    updated_attributes_end.append(sender)

@pytest.mark.parametrize('query', ['attributename:PythonAFInserted'])
@pytest.mark.parametrize('stream', ['end'])
def test_subscription_end(webapi, query, stream, ci, pythonversion, callback=callback_end):
    #clear array from previous tests
    updated_attributes_end[:] = []

    if ci == 'test':
        elementname = 'Attributes'
    else:
        elementname = pythonversion or ci
        parent = ci
    elements = webapi.elements(query='{} AND name:{}'.format(query, elementname))
    if len(elements) > 1:
        elementlist = [ele for ele in elements if parent in ele.paths[0]]
    else:
        elementlist = elements

    subscriptions = webapi.subscribe(elementlist, stream, callback=callback_end)
    for element in elementlist:
        afattribute = element['PythonAFInserted']

        afattribute.update_values(["*"], [random.uniform(0,100)])
        time.sleep(0.5)
        v1 = afattribute.end()
        afattribute.update_values(["*+1m"], [random.uniform(0,100)])
        time.sleep(0.5)
        v2 = afattribute.end()
    assert len(updated_attributes_end) == 1
    subscriptions = webapi.unsubscribe(elementlist, stream)

# test interpolatedattimes - assumes no one has used this tag
updated_attributes_interp_1 = []
def callback_interp_1(sender):
    updated_attributes_interp_1.append(sender)

# @pytest.mark.skipif(piserverissue, reason='PI Server times out when retrieving archived values')
@pytest.mark.parametrize('query', ['attributename:PythonAFInterpolatedAtTime'])
# @pytest.mark.parametrize('times', [['2017-01-01T00:00:00Z']])
def test_subscription_interpolatedattimes_single_timestamp_notify_one(webapi, query, now, ci, pythonversion, callback=callback_interp_1):
    #clear array from previous tests
    updated_attributes_interp_1[:] = []
    times = [now.shift(hours=-168).format('YYYY-MM-DD HH:mm:ss ZZ')]

    if ci == 'test':
        elementname = 'Attributes'
    else:
        elementname = pythonversion or ci
        parent = ci
    elements = webapi.elements(query='{} AND name:{}'.format(query, elementname))
    if len(elements) > 1:
        elementlist = [ele for ele in elements if parent in ele.paths[0]]
    else:
        elementlist = elements

    #query points (should be 1)
    for element in elementlist:
        for t in times:
            #subscribe each timestamp for this point
            webapi.subscribe(elementlist, 'interpolatedattimes', startdatetime=t, callback=callback_interp_1)
            afattribute = element['PythonAFInterpolatedAtTime']
            #setup with values here: insert a value 1 minute before and after timestamp: 0 to 1000
            #datetime is parsed so days can added/subtracted
            parseddatetime = parser.parse(t)
            date1 = (parseddatetime + timedelta(minutes=-1)).strftime('%Y-%m-%dT%H:%M:%SZ')
            afattribute.update_value(date1, 0)
            time.sleep(0.5)

            date2 = (parseddatetime + timedelta(minutes=1)).strftime('%Y-%m-%dT%H:%M:%SZ')
            afattribute.update_value(date2, 1000)
            time.sleep(0.5)

            #gets initial value for subscriber
            afattribute.interpolatedattimes([t])

            #updates after value to 500, so there should be a new interpolated value
            afattribute.update_value(date1, 500)
            time.sleep(0.5)

            #queries new point and should trigger callback function
            afattribute.interpolatedattimes([t])
    assert len(updated_attributes_interp_1) == 1
    webapi.unsubscribe(elementlist, 'interpolatedattimes')
    
# test interpolatedattimes - assumes no one has used this tag
updated_attributes_interp_2 = []
def callback_interp_2(sender):
    updated_attributes_interp_2.append(sender)

# @pytest.mark.skipif(piserverissue, reason='PI Server times out when retrieving archived values')
@pytest.mark.parametrize('query', ['attributename:PythonAFInterpolatedAtTime'])
# @pytest.mark.parametrize('times', [['2016-05-01T00:00:00Z','2016-06-01T00:00:00Z']])
def test_subscription_interpolatedattimes_single_timestamp_notify_two(webapi, query, now, ci, pythonversion, callback=callback_interp_2):
    #clear array from previous tests
    updated_attributes_interp_2[:] = []
    times = [now.shift(hours=-48).format('YYYY-MM-DD HH:mm:ss ZZ'), now.shift(hours=-96).format('YYYY-MM-DD HH:mm:ss ZZ')]

    if ci == 'test':
        elementname = 'Attributes'
    else:
        elementname = pythonversion or ci
        parent = ci
    elements = webapi.elements(query='{} AND name:{}'.format(query, elementname))
    if len(elements) > 1:
        elementlist = [ele for ele in elements if parent in ele.paths[0]]
    else:
        elementlist = elements

    #query elements (should be 1)
    for element in elementlist:
        for t in times:
            #subscriber each timestamp for this point
            webapi.subscribe(elementlist, 'interpolatedattimes', startdatetime=t, callback=callback_interp_2)
            afattribute = element['PythonAFInterpolatedAtTime']
            #setup with values here: insert a value 1 minute before and after timestamp: 0 to 1000
            #datetime is parsed so minute can added/subtracted
            parseddatetime = parser.parse(t)
            date1 = (parseddatetime + timedelta(minutes=-1)).strftime('%Y-%m-%dT%H:%M:%SZ')
            afattribute.update_value(date1, 0)
            time.sleep(0.5)

            date2 = (parseddatetime + timedelta(minutes=1)).strftime('%Y-%m-%dT%H:%M:%SZ')
            afattribute.update_value(date2, 1000)
            time.sleep(0.5)

    #gets initial values for subscriber
    afattribute.interpolatedattimes(times)

    #queries new value and should trigger callback function
    for element in elementlist:
        for t in times:
            #updates after value to 500, so there should be a new interpolated value
            parseddatetime = parser.parse(t)
            date2 = (parseddatetime + timedelta(minutes=1)).strftime('%Y-%m-%dT%H:%M:%SZ')
            afattribute.update_value(date2, 500)
            time.sleep(0.5)

    afattribute.interpolatedattimes(times)
    assert updated_attributes_interp_2.__len__() == 2
    webapi.unsubscribe(elementlist, 'interpolatedattimes')


updated_attributes_recorded = []
def callback_recorded(sender):
    updated_attributes_recorded.append(sender)

# @pytest.mark.skipif(piserverissue, reason='PI Server times out when retrieving archived values')
@pytest.mark.parametrize('query', ['attributename:PythonAFRecordedAtTime'])
# @pytest.mark.parametrize('time', ['2017-01-01T00:00:00Z','2017-01-02T00:00:00Z'])
def test_subscription_recordedattimes(webapi, query, now, ci, pythonversion, callback=callback_recorded):
    #clear array from previous test
    updated_attributes_recorded[:] = []

    t = now.shift(hours=-26).format('YYYY-MM-DD HH:mm:ss ZZ')

    if ci == 'test':
        elementname = 'Attributes'
    else:
        elementname = pythonversion or ci
        parent = ci
    elements = webapi.elements(query='{} AND name:{}'.format(query, elementname))
    if len(elements) > 1:
        elementlist = [ele for ele in elements if parent in ele.paths[0]]
    else:
        elementlist = elements

    #query elements (should be 1)
    for element in elementlist:
        webapi.subscribe(elementlist, 'recordedattime', startdatetime=t, callback=callback_recorded)
        afattribute = element['PythonAFRecordedAtTime']
        afattribute.update_value(t, 134)
        time.sleep(0.5)

        afattribute.recordedattime(t)
        afattribute.update_value(t, 160)
        time.sleep(0.5)
        #should trigger callback function
        afattribute.recordedattime(t)
    assert len(updated_attributes_recorded) == 1
    webapi.unsubscribe(elementlist, 'recordedattime')
