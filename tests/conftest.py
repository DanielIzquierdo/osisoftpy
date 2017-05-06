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
import itertools
import pytest
import osisoftpy


@pytest.fixture(scope='module')
def url():
    return 'https://sbb03.eecs.berkeley.edu/piwebapi'


@pytest.fixture(scope='module')
def username():
    return 'albertxu'


@pytest.fixture(scope='module')
def password():
    return 'Welcome2pi'


@pytest.fixture(scope='module')
def authtype():
    return 'basic'


@pytest.fixture(scope='module')
def dataarchive():
    return 'sbb03.eecs.berkeley.edu'


def query():
    Query = namedtuple('Query', ['single', 'partial', 'wildcard', 'multi'])
    query = Query(single='name:sinusoid',
                  partial='name:sinusoid*',
                  wildcard='*SPF_environment_sensor*',
                  multi='name:sinusoid or name:cdt158 or name:cd*')
    return query


def credentials():
    a = frozenset(['kerberos', 'basic', ''])
    u = frozenset(['albertxu', 'andrew', ' ', 'apong'])
    p = frozenset(['Welcome2pi', 'p@ssw0rd', ''])
    Credentials = namedtuple('Credentials', ['valid', 'unknown'])
    credtuple = Credentials(valid=[('basic', 'albertxu', 'Welcome2pi'),],
                            unknown=list(itertools.product(a, u, p)))
    return credtuple


@pytest.fixture(scope='module')
def webapi(url, authtype, username, password):
    return osisoftpy.webapi(url,
                            authtype=authtype,
                            username=username,
                            password=password)
