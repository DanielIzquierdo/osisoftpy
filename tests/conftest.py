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
osisoftpy.tests.conftest.py
~~~~~~~~~~~~
Contains pytest fixtures which are globally available throughout the suite.
"""

from collections import namedtuple
from itertools import product
import arrow
import pytest
import osisoftpy
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

def pytest_addoption(parser):
    parser.addoption("--ci", action="store", default="test",
                     help="my option: travis, circle, or appveyor")
    parser.addoption("--pythonversion", action="store", default="",
                     help="my option: 2.7 to nightly build")

@pytest.fixture
def ci(request):
    return request.config.getoption("--ci")

@pytest.fixture
def pythonversion(request):
    return request.config.getoption("--pythonversion")

usekerberos = False

@pytest.fixture(scope='module')
def url():
    return 'https://dev.dstcontrols.com/piwebapi'

@pytest.fixture(scope='module')
def hostname_override():
    return 'api.osisoft.dstcontrols.local'

@pytest.fixture(scope='module')
def verifyssl():
    return False

@pytest.fixture(scope='module')
def authtype():
    if usekerberos:
        return 'kerberos'
    else:
        return 'basic'

@pytest.fixture(scope='module')
def username():
    return 'ak-piwebapi-svc@dstcontrols.local'

@pytest.fixture(scope='module')
def password():
    return 'DP$28GhMyp*!E&gc'

@pytest.fixture(scope='module')
def now():
    return arrow.utcnow()

def query():
    Query = namedtuple('Query', ['single', 'partial', 'wildcard', 'multi'])
    query = Query(single='name:sinusoid',
                  partial='name:sinusoid*',
                  wildcard='name:*SPF_environment_sensor*',
                  multi='name:sinusoid OR name:cdt158 OR name:cd*')
    return query


def credentials():
    authtypes = frozenset()
    usernames = frozenset()
    passwords = frozenset()

    valid = list(product(['kerberos'], ['albertxu'], ['Welcome2pi']))
    unknown = list(product(authtypes, usernames, passwords))

    Credentials = namedtuple('Credentials', ['valid', 'unknown'])
    return Credentials(valid=valid, unknown=unknown)


def pointvalues():
    single = ['current']
    multi = ['interpolated', 'interpolatedattimes', 'recorded', 'plot']
    PointValues = namedtuple('PointValues', ['single', 'multi'])
    return PointValues(single=single, multi=multi)


@pytest.fixture(scope='module')
def webapi(url, authtype, username, password, verifyssl, hostname_override):
    if usekerberos:
        return osisoftpy.webapi(
            url, authtype=authtype, verifyssl=False,
            hostname_override=hostname_override)
    else:
        return osisoftpy.webapi(
            url, authtype=authtype, username='ak-piwebapi-svc@dstcontrols.local', password='DP$28GhMyp*!E&gc',
            verifyssl=False, hostname_override=hostname_override)
