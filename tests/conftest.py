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
    # return 'basic'
    return 'kerberos'

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
                  wildcard='*SPF_environment_sensor*',
                  multi='name:sinusoid or name:cdt158 or name:cd*')
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
    return osisoftpy.webapi(
        url, authtype=authtype, verifyssl=False,
        hostname_override=hostname_override)

