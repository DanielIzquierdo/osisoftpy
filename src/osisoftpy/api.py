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
osisoftpy.api
~~~~~~~~~~~~
This module implements the OSIsoftPy API.
"""

import logging

from osisoftpy.factory import Factory, create
from osisoftpy.internal import get
from osisoftpy.internal import wrapt_handle_exceptions
from osisoftpy.webapi import WebAPI
from osisoftpy.points import Points
import rx

log = logging.getLogger(__name__)


@wrapt_handle_exceptions
def webapi(url, **kwargs):
    r = get(url, **kwargs)
    return create(Factory(WebAPI), r.response.json(), r.session)


@wrapt_handle_exceptions
def response(url, **kwargs):
    r = get(url, **kwargs)
    return r.response

@wrapt_handle_exceptions
def setloglevel(loglevel):
    numeric_level = getattr(logging, loglevel.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError('Invalid log level: %s' % loglevel.upper())
    log.setLevel(loglevel.upper())
    print('Log level: %s' % log.level)

def observable(points):
    if not isinstance(points, Points):
        raise TypeError('The object "{}" is not of type "{}"'.format(
            points, Points))
    return rx.Observable.from_(points).publish().auto_connect()

