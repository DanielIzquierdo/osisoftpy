from __future__ import print_function

import datetime
import random
from time import sleep

# silence the certificate warnings
import requests
from nose.tools import *
from osisoft_pi_webapi_python_client.client import client
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from rx.core import Scheduler

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# test parameters
useBasic = False
testBasicAuth = False
testKerberosAuth = True
testDataPipe = False

# piWebApi = 'https://dev.dstcontrols.com'
piWebApi = 'https://applepie.dstcontrols.local/'
user = 'ak-piwebapi-svc'
password = 'DP$28GhMyp*!E&gc'
verifySSL = False
serverCount = 1
serverName = 'banoffee.dstcontrols.local'
floatingPointPrecision = 0.00001

testPoint = 'SINUSOID'
testPointType = 'Float32'
testPointClass = 'classic'

testPoint2 = 'SINUSOIDU'
testPoint2Type = 'Float32'
testPoint2Class = 'classic'

testPoint3 = 'AlansPythonTestTag'
testPoint3Type = 'Float32'
testPoint3Class = 'classic'

testPoint4 = 'AlansPythonTestTag2'
testPoint4Type = 'Float32'
testPoint4Class = 'classic'

# # ENABLE THIS CODE FOR HTTP LOGGING
# import logging
#
# # These two lines enable debugging at httplib level (requests->urllib3->http.client)
# # You will see the REQUEST, including HEADERS and DATA, and RESPONSE with HEADERS but without DATA.
# # The only thing missing will be the response.body which is not logged.
# try:
#     import http.client as http_client
# except ImportError:
#     # Python 2
#     import httplib as http_client
# http_client.HTTPConnection.debuglevel = 1
#
# # You must initialize logging, otherwise you'll not see debug output.
# logging.basicConfig()
# logging.getLogger().setLevel(logging.DEBUG)
# requests_log = logging.getLogger("requests.packages.urllib3")
# requests_log.setLevel(logging.DEBUG)
# requests_log.propagate = True

# PICLIENT TESTS


def test_piclient_unknown_auth():
    # bad authenticationType throws error
    try:
        piclient = client(piWebApi, authenticationType='BAD',
                          verifySSL=verifySSL)
    except ValueError as e:
        pass


def test_piclient_basic_auth():
    # test basic authenticationType
    if not testBasicAuth:
        return
    piclient = client(piWebApi, 'ak-piwebapi-svc',
                      'DP$28GhMyp*!E&gc', 'basic', verifySSL=verifySSL)
    pass


def test_piclient_kerberos_auth():
    # test kerberos authentication
    if not testKerberosAuth:
        return
    piclient = client(piWebApi, authenticationType='kerberos',
                      verifySSL=verifySSL)
    pass


def test_piclient_host_name():
    # verify the pi client cleans up the host name
    piclient = client(piWebApi + '/piwebapi/',
                      authenticationType='kerberos', verifySSL=verifySSL)
    assert piclient.Host() == piWebApi


# BASIC PI SERVER TESTS

def test_piclient_piservers():
    # fetch servers
    client = helper_fetch_client()
    servers = client.PIServers()
    assert len(servers) == serverCount


def test_find_test_piserver():
    # examine the main server
    server = helper_fetch_server()
    assert server
    assert server.Name() == serverName


def test_find_pipoints():
    # find SINUSOID pi points
    server = helper_fetch_server()
    points = server.FindPIPoints('SINUSOID*', 0, 100)
    assert len(points) == 2

    for point in points:
        if point.Name() == testPoint:
            point1 = point
        elif point.Name() == testPoint2:
            point2 = point

    assert point1
    assert point2


def test_find_pipoint():
    # find a single pi point
    server = helper_fetch_server()
    point = server.FindPIPoint(testPoint)

    assert point.Name() == testPoint
    assert point.PointType() == testPointType
    assert point.PointClass() == testPointClass


def test_find_pipoint2():
    # find the other pi point
    server = helper_fetch_server()
    point = server.FindPIPoint(testPoint2)

    assert point.Name() == testPoint2
    assert point.PointType() == testPoint2Type
    assert point.PointClass() == testPoint2Class


# PI POINT TESTS
def test_pipoint_current():
    # get the pi point current values
    value = helper_fetch_point1().CurrentValue()
    assert value
    time = value.keys()[0]
    valueKeys = value[time].keys()
    assert 'Value' in valueKeys
    assert 'Good' in valueKeys
    assert 'Questionable' in valueKeys
    assert 'UnitsAbbreviation' in valueKeys
    assert 'Substituted' in valueKeys


def test_pipoint_recorded():
    # test the pi point recorded values
    values = helper_fetch_point1().RecordedValues(maxCount=10)
    assert values
    assert len(values) == 10
    for key in values.keys():
        assert len(values[key]) == 5


def test_pipoint_recorded2():
    # test the pi point recorded values
    values = helper_fetch_point1().RecordedValues(maxCount=100)
    assert values
    assert len(values) == 100
    for key in values.keys():
        assert len(values[key]) == 5


def test_pipoint_interpolated():
    # test the pi point interpolated values
    values = helper_fetch_point1().InterpolatedValues()
    assert values
    assert len(values) == 25
    for key in values.keys():
        assert len(values[key]) == 5


def test_pipoint_interpolated2():
    # test the pi point interpolated values
    values = helper_fetch_point1().InterpolatedValues(interval='30m')
    assert values
    assert len(values) == 49
    for key in values.keys():
        assert len(values[key]) == 5


# PI SERVER BULK QUERY

def test_piserver_bulk_current():
    # batch query with multiple tags
    server = helper_fetch_server()
    tags = [helper_fetch_point1(), helper_fetch_point2()]

    values = server.CurrentValues(tags)

    assert len(values) <= 2
    for key in values.keys():
        assert len(values[key]) <= 2


def test_piserver_bulk_recorded():
    # batch query with multiple tags
    server = helper_fetch_server()
    tags = [helper_fetch_point1(), helper_fetch_point2()]

    values = server.RecordedValues(tags, maxCount=10)
    print(values)
    assert len(values) <= 20
    for key in values.keys():
        assert len(values[key]) <= 2


def test_piserver_bulk_recorded2():
    # batch query with multiple tags
    server = helper_fetch_server()
    tags = [helper_fetch_point1(), helper_fetch_point2()]

    values = server.RecordedValues(tags, maxCount=100)

    assert len(values) <= 200
    for key in values.keys():
        assert len(values[key]) <= 2


def test_piserver_bulk_interpolated():
    # batch query with multiple tags
    server = helper_fetch_server()
    tags = [helper_fetch_point1(), helper_fetch_point2()]

    values = server.InterpolatedValues(tags)

    assert len(values) == 25
    for key in values.keys():
        assert len(values[key]) == 2


def test_piserver_bulk_interpolated2():
    # batch query with multiple tags
    server = helper_fetch_server()
    tags = [helper_fetch_point1(), helper_fetch_point2()]

    values = server.InterpolatedValues(tags, interval='30m')

    assert len(values) == 49
    for key in values.keys():
        assert len(values[key]) == 2


def test_datapipe_single_subscription():
    # test data pipe
    if not testDataPipe:
        return

    results = {}

    server = helper_fetch_server()
    tag = helper_fetch_point1()
    tag2 = helper_fetch_point2()

    obs = server.Observable([tag, tag2])
    connection = obs.connect()
    d = obs.subscribe(lambda x: helper_addToResults(results, x))

    sleep(30)
    d.dispose()
    connection.dispose()

    print(results)

    assert len(results) == 2

    for key in results.keys():
        assert len(results[key]) == 2


def test_datapipe_multiple_subscriptions():
    # test data pipe with multiple subscriptions
    if not testDataPipe:
        return

    results = {}
    results2 = {}

    server = helper_fetch_server()
    tag = helper_fetch_point1()
    tag2 = helper_fetch_point2()

    obs = server.Observable([tag, tag2])
    d = obs.subscribe(lambda x: helper_addToResults(results, x))
    d2 = obs.subscribe(lambda x: helper_addToResults(results2, x))

    connection = obs.connect()
    sleep(30)
    d.dispose()
    sleep(30)
    d2.dispose()
    connection.dispose()

    assert len(results) == 2 or 3
    for key in results.keys():
        assert len(results[key].keys()) == 2

    assert len(results2) == 3 or 4
    for key in results2.keys():
        assert len(results2[key].keys()) == 2


def test_datapipe_multiple_subscriptions2():
    # test data pipe with multiple subscriptions, test that scheduler stops
    # after disconnect
    if not testDataPipe:
        return

    results = {}
    results2 = {}

    server = helper_fetch_server()
    tag = helper_fetch_point1()
    tag2 = helper_fetch_point2()

    obs = server.Observable([tag, tag2])
    d = obs.subscribe(lambda x: helper_addToResults(results, x))
    d2 = obs.subscribe(lambda x: helper_addToResults(results2, x))

    connection = obs.connect()
    sleep(30)
    connection.dispose()
    assert len(results) == 1 or 2
    for key in results.keys():
        assert len(results[key].keys()) == 2

        assert len(results2) == 1 or 2
        for key in results2.keys():
            assert len(results2[key].keys()) == 2

    results = {}
    results2 = {}

    sleep(30)
    d.dispose()
    d2.dispose()

    assert len(results) == 1 or 2
    for key in results.keys():
        assert len(results[key].keys()) == 2

    assert len(results2) == 1 or 2
    for key in results2.keys():
        assert len(results2[key].keys()) == 2


def test_point_update():
    point = helper_fetch_point3()

    now = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
    value = random.random()
    data = {
        'Timestamp': now,
        'Questionable': 'false',
        'Good': 'true',
        'Value': value
    }

    point.UpdateValue(data)
    sleep(10)
    current = point.CurrentValue()
    assert len(current[now]) > 0
    for key in current.keys():
        assert key == now

    assert abs(current[now]['Value'] - value) < floatingPointPrecision


def test_point_updates():
    point = helper_fetch_point3()

    now = datetime.datetime.utcnow()
    now2 = now + datetime.timedelta(seconds=1)
    value1 = random.random()
    value2 = random.random()
    data = [{
        'Timestamp': now.strftime('%Y-%m-%dT%H:%M:%SZ'),
        'Questionable': 'false',
        'Good': 'true',
        'Value': value1
    }, {
        'Timestamp': now2.strftime('%Y-%m-%dT%H:%M:%SZ'),
        'Questionable': 'false',
        'Good': 'true',
        'Value': value2
    }]

    point.UpdateValues(data)
    sleep(10)
    result = point.RecordedValues(now.strftime(
        '%Y-%m-%dT%H:%M:%SZ'), now2.strftime('%Y-%m-%dT%H:%M:%SZ'))

    assert len(result) == 2

    for key in result:
        assert key in [now.strftime(
            '%Y-%m-%dT%H:%M:%SZ'), now2.strftime('%Y-%m-%dT%H:%M:%SZ')]

        if key == now.strftime('%Y-%m-%dT%H:%M:%SZ'):
            assert abs(result[key]['Value'] - value1) < floatingPointPrecision
        if key == now2.strftime('%Y-%m-%dT%H:%M:%SZ'):
            assert abs(result[key]['Value'] - value2) < floatingPointPrecision


def test_server_updates():
    server = helper_fetch_server()

    now = datetime.datetime.utcnow()
    now2 = now + datetime.timedelta(seconds=1)
    value1 = random.random()
    value2 = random.random()
    data = {
        now.strftime('%Y-%m-%dT%H:%M:%SZ'): {
            testPoint3: value1
        },
        now2.strftime('%Y-%m-%dT%H:%M:%SZ'): {
            testPoint3: value2
        }
    }

    server.UpdateValues(data)
    sleep(10)
    results = server.RecordedValues([testPoint3], now.strftime(
        '%Y-%m-%dT%H:%M:%SZ'), now2.strftime('%Y-%m-%dT%H:%M:%SZ'))

    assert results
    assert len(results) == 2
    for timeKey in results.keys():
        assert timeKey in [now.strftime(
            '%Y-%m-%dT%H:%M:%SZ'), now2.strftime('%Y-%m-%dT%H:%M:%SZ')]

        if timeKey == now.strftime('%Y-%m-%dT%H:%M:%SZ'):
            assert abs(results[timeKey][testPoint3] -
                       value1) < floatingPointPrecision
        if timeKey == now2.strftime('%Y-%m-%dT%H:%M:%SZ'):
            assert abs(results[timeKey][testPoint3] -
                       value2) < floatingPointPrecision


def test_server_updates2():
    server = helper_fetch_server()

    now = datetime.datetime.utcnow()
    now2 = now + datetime.timedelta(seconds=1)
    value1 = random.random()
    value2 = random.random()
    value3 = random.random()
    value4 = random.random()
    data = {
        now.strftime('%Y-%m-%dT%H:%M:%SZ'): {
            testPoint3: value1,
            testPoint4: value3
        },
        now2.strftime('%Y-%m-%dT%H:%M:%SZ'): {
            testPoint3: value2,
            testPoint4: value4
        }
    }

    server.UpdateValues(data)
    sleep(10)
    results = server.RecordedValues([testPoint3, testPoint4], now.strftime(
        '%Y-%m-%dT%H:%M:%SZ'), now2.strftime('%Y-%m-%dT%H:%M:%SZ'))

    assert results
    assert len(results) == 2
    for timeKey in results.keys():
        assert timeKey in [now.strftime(
            '%Y-%m-%dT%H:%M:%SZ'), now2.strftime('%Y-%m-%dT%H:%M:%SZ')]
        assert len(results[timeKey])

        if timeKey == now.strftime('%Y-%m-%dT%H:%M:%SZ'):
            assert abs(results[timeKey][testPoint3] -
                       value1) < floatingPointPrecision
            assert abs(results[timeKey][testPoint4] -
                       value3) < floatingPointPrecision
        if timeKey == now2.strftime('%Y-%m-%dT%H:%M:%SZ'):
            assert abs(results[timeKey][testPoint3] -
                       value2) < floatingPointPrecision
            assert abs(results[timeKey][testPoint4] -
                       value4) < floatingPointPrecision

# HELPERS


def helper_addToResults(result, addition):
    for dateKey in addition.keys():
        if dateKey not in result.keys():
            result[dateKey] = {}

        for tagKey in addition[dateKey].keys():
            result[dateKey][tagKey] = addition[dateKey][tagKey]


def helper_fetch_point1():
    return helper_fetch_server().FindPIPoint(testPoint)


def helper_fetch_point2():
    return helper_fetch_server().FindPIPoint(testPoint2)


def helper_fetch_point3():
    return helper_fetch_server().FindPIPoint(testPoint3)


def helper_fetch_point4():
    return helper_fetch_server().FindPIPoint(testPoint4)


def helper_fetch_server():
    client = helper_fetch_client()
    servers = client.PIServers()
    assert len(servers) == serverCount

    for serverObject in servers:
        if serverObject.Name() == serverName:
            server = serverObject
    return server


def helper_fetch_client():
    if useBasic:
        return client(piWebApi, 'ak-piwebapi-svc', 'DP$28GhMyp*!E&gc', 'basic', verifySSL=verifySSL)
    else:
        return client(piWebApi, authenticationType='kerberos', verifySSL=verifySSL)
