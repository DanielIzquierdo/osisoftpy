from nose.tools import *
from PI.piClient import PIClient

useBasic = False
testBasicAuth = False
testKerberosAuth = False

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
    try:
        client = PIClient(piWebApi, authenticationType='BAD', verifySSL=verifySSL)
    except ValueError as e:
        pass

def test_piclient_basic_auth():
    if not testBasicAuth:
        return
    client = PIClient(piWebApi,'ak-piwebapi-svc','DP$28GhMyp*!E&gc','basic',verifySSL=verifySSL)
    pass

def test_piclient_kerberos_auth():
    if not testKerberosAuth:
        return
    client = PIClient(piWebApi, authenticationType='kerberos', verifySSL=verifySSL)
    pass

def test_piclient_host_name():
    client = PIClient(piWebApi + '/piwebapi/', authenticationType='kerberos', verifySSL=verifySSL)
    assert client.Host() == piWebApi

# BASIC PI SERVER TESTS

def test_piclient_piservers():
    client = fetch_test_client()
    servers = client.PIServers()
    assert len(servers) == serverCount

def test_find_test_piserver():
    server = fetch_test_server()
    assert server
    assert server.Name() == serverName

def test_find_pipoints():
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
    server = fetch_test_server()
    point = server.FindPIPoint(testPoint)

    assert point.Name() == testPoint
    assert point.PointType() == testPointType
    assert point.PointClass() == testPointClass

def test_find_pipoint2():
    server = fetch_test_server()
    point = server.FindPIPoint(testPoint2)

    assert point.Name() == testPoint2
    assert point.PointType() == testPoint2Type
    assert point.PointClass() == testPoint2Class

# PI POINT TESTS
def test_pipoint_current():
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
    values = fetch_test_point1().RecordedValues(maxCount=10)
    assert values
    assert len(values) == 10
    for key in values.keys():
        assert len(values[key]) == 5

def test_pipoint_recorded2():
    values = fetch_test_point1().RecordedValues(maxCount=100)
    assert values
    assert len(values) == 100
    for key in values.keys():
        assert len(values[key]) == 5

def test_pipoint_interpolated():
    values = fetch_test_point1().InterpolatedValues()
    assert values
    assert len(values) == 25
    for key in values.keys():
        assert len(values[key]) == 5

def test_pipoint_interpolated2():
    values = fetch_test_point1().InterpolatedValues(interval='30m')
    assert values
    assert len(values) == 49
    for key in values.keys():
        assert len(values[key]) == 5

# PI SERVER BULK QUERY

def test_piserver_bulk_current():
    server = fetch_test_server()
    tags = [fetch_test_point1(), fetch_test_point2()]

    values = server.CurrentValues(tags)

    assert len(values) <= 2
    for key in values.keys():
        assert len(values[key]) <= 2

def test_piserver_bulk_recorded():
    server = fetch_test_server()
    tags = [fetch_test_point1(), fetch_test_point2()]

    values = server.RecordedValues(tags,maxCount=10)

    assert len(values) <= 20
    for key in values.keys():
        assert len(values[key]) <= 2

def test_piserver_bulk_recorded2():
    server = fetch_test_server()
    tags = [fetch_test_point1(), fetch_test_point2()]

    values = server.RecordedValues(tags,maxCount=100)

    assert len(values) <= 200
    for key in values.keys():
        assert len(values[key]) <= 2

def test_piserver_bulk_interpolated():
    server = fetch_test_server()
    tags = [fetch_test_point1(), fetch_test_point2()]

    values = server.InterpolatedValues(tags)

    assert len(values) == 25
    for key in values.keys():
        assert len(values[key]) == 2

def test_piserver_bulk_interpolated2():
    server = fetch_test_server()
    tags = [fetch_test_point1(), fetch_test_point2()]

    values = server.InterpolatedValues(tags, interval='30m')

    assert len(values) == 49
    for key in values.keys():
        assert len(values[key]) == 2

# HELPERS

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
        return PIClient(piWebApi,'ak-piwebapi-svc','DP$28GhMyp*!E&gc','basic',verifySSL=verifySSL)
    else:
        return PIClient(piWebApi, authenticationType='kerberos', verifySSL=verifySSL)
