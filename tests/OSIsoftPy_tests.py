from __future__ import print_function

from nose.tools import *
from OSIsoftPy.client import client
from time import sleep
from rx.core import Scheduler

#silence the certificate warnings
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# test parameters
useBasic = False
testBasicAuth = False
testKerberosAuth = True
testDataPipe = False

piWebApi = 'https://applepie.dstcontrols.local'
user = 'ak-piwebapi-svc'
password = 'DP$28GhMyp*!E&gc'
verifySSL = False
serverCount = 1
serverName = 'banoffee.dstcontrols.local'

testPoint = 'SINUSOID'
testPointType = 'Float32'
testPointClass = 'classic'

testPoint2 = 'SINUSOIDU'
testPoint2Type = 'Float32'
testPoint2Class = 'classic'

# PICLIENT TESTS


def test_piclient_unknown_auth():
# bad authenticationType throws error
    try:
        piclient = client(piWebApi, authenticationType='BAD', verifySSL=verifySSL)
    except ValueError as e:
        pass

def test_piclient_basic_auth():
# test basic authenticationType
    if not testBasicAuth:
        return
    piclient = client(piWebApi,'ak-piwebapi-svc','DP$28GhMyp*!E&gc','basic',verifySSL=verifySSL)
    pass

def test_piclient_kerberos_auth():
# test kerberos authentication
    if not testKerberosAuth:
        return
    piclient = client(piWebApi, authenticationType='kerberos', verifySSL=verifySSL)
    pass

def test_piclient_host_name():
# verify the pi client cleans up the host name
    piclient = client(piWebApi + '/piwebapi/', authenticationType='kerberos', verifySSL=verifySSL)
    assert piclient.Host() == piWebApi



# BASIC PI SERVER TESTS

def test_piclient_piservers():
# fetch servers
    client = fetch_test_client()
    servers = client.PIServers()
    assert len(servers) == serverCount

def test_find_test_piserver():
# examine the main server
    server = fetch_test_server()
    assert server
    assert server.Name() == serverName

def test_find_pipoints():
# find SINUSOID pi points
    server = fetch_test_server()
    points = server.FindPIPoints('SINUSOID*',0, 100)
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
    server = fetch_test_server()
    point = server.FindPIPoint(testPoint)

    assert point.Name() == testPoint
    assert point.PointType() == testPointType
    assert point.PointClass() == testPointClass

def test_find_pipoint2():
# find the other pi point
    server = fetch_test_server()
    point = server.FindPIPoint(testPoint2)

    assert point.Name() == testPoint2
    assert point.PointType() == testPoint2Type
    assert point.PointClass() == testPoint2Class




# PI POINT TESTS
def test_pipoint_current():
# get the pi point current values
    value = fetch_test_point1().CurrentValue()
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
    values = fetch_test_point1().RecordedValues(maxCount=10)
    assert values
    assert len(values) == 10
    for key in values.keys():
        assert len(values[key]) == 5

def test_pipoint_recorded2():
# test the pi point recorded values
    values = fetch_test_point1().RecordedValues(maxCount=100)
    assert values
    assert len(values) == 100
    for key in values.keys():
        assert len(values[key]) == 5

def test_pipoint_interpolated():
# test the pi point interpolated values
    values = fetch_test_point1().InterpolatedValues()
    assert values
    assert len(values) == 25
    for key in values.keys():
        assert len(values[key]) == 5

def test_pipoint_interpolated2():
# test the pi point interpolated values
    values = fetch_test_point1().InterpolatedValues(interval='30m')
    assert values
    assert len(values) == 49
    for key in values.keys():
        assert len(values[key]) == 5



# PI SERVER BULK QUERY

def test_piserver_bulk_current():
# batch query with multiple tags
    server = fetch_test_server()
    tags = [fetch_test_point1(), fetch_test_point2()]

    values = server.CurrentValues(tags)

    assert len(values) <= 2
    for key in values.keys():
        assert len(values[key]) <= 2

def test_piserver_bulk_recorded():
# batch query with multiple tags
    server = fetch_test_server()
    tags = [fetch_test_point1(), fetch_test_point2()]

    values = server.RecordedValues(tags,maxCount=10)

    assert len(values) <= 20
    for key in values.keys():
        assert len(values[key]) <= 2

def test_piserver_bulk_recorded2():
# batch query with multiple tags
    server = fetch_test_server()
    tags = [fetch_test_point1(), fetch_test_point2()]

    values = server.RecordedValues(tags,maxCount=100)

    assert len(values) <= 200
    for key in values.keys():
        assert len(values[key]) <= 2

def test_piserver_bulk_interpolated():
# batch query with multiple tags
    server = fetch_test_server()
    tags = [fetch_test_point1(), fetch_test_point2()]

    values = server.InterpolatedValues(tags)

    assert len(values) == 25
    for key in values.keys():
        assert len(values[key]) == 2

def test_piserver_bulk_interpolated2():
# batch query with multiple tags
    server = fetch_test_server()
    tags = [fetch_test_point1(), fetch_test_point2()]

    values = server.InterpolatedValues(tags, interval='30m')

    assert len(values) == 49
    for key in values.keys():
        assert len(values[key]) == 2

def test_datapipe_single_subscription():
# test data pipe
    if not testDataPipe:
        pass

    results = {}

    server = fetch_test_server()
    tag = fetch_test_point1()
    tag2 = fetch_test_point2()

    obs = server.Observable([tag, tag2])
    connection = obs.connect()
    d = obs.subscribe(lambda x: addToResults(results,x))

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
        pass

    results = {}
    results2 = {}

    server = fetch_test_server()
    tag = fetch_test_point1()
    tag2 = fetch_test_point2()

    obs = server.Observable([tag, tag2])
    d = obs.subscribe(lambda x: addToResults(results,x))
    d2 = obs.subscribe(lambda x: addToResults(results2,x))

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
# test data pipe with multiple subscriptions, test that scheduler stops after disconnect
    if not testDataPipe:
        pass

    results = {}
    results2 = {}

    server = fetch_test_server()
    tag = fetch_test_point1()
    tag2 = fetch_test_point2()

    obs = server.Observable([tag, tag2])
    d = obs.subscribe(lambda x: addToResults(results,x))
    d2 = obs.subscribe(lambda x: addToResults(results2,x))

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


# HELPERS

def addToResults(result, addition):
    for dateKey in addition.keys():
        if dateKey not in result.keys():
            result[dateKey] = {}

        for tagKey in addition[dateKey].keys():
            result[dateKey][tagKey] = addition[dateKey][tagKey]


def fetch_test_point1():
    return fetch_test_server().FindPIPoint(testPoint)

def fetch_test_point2():
    return fetch_test_server().FindPIPoint(testPoint2)

def fetch_test_server():
    client = fetch_test_client()
    servers = client.PIServers()
    assert len(servers) == serverCount

    for serverObject in servers:
        if serverObject.Name() == serverName:
            server = serverObject
    return server

def fetch_test_client():
    if useBasic:
        return client(piWebApi,'ak-piwebapi-svc','DP$28GhMyp*!E&gc','basic',verifySSL=verifySSL)
    else:
        return client(piWebApi, authenticationType='kerberos', verifySSL=verifySSL)
