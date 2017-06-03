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
osisoftpy.factory
~~~~~~~~~~~~
"""
from __future__ import (absolute_import, division, unicode_literals)
from future.builtins import *
from future.utils import iteritems


def create(factory, thing, session, webapi=None):
    """
    Return an object created with factory
    :param webapi: 
    :param factory: 
    :param params: 
    :param session: 
    :return: 
    """


    payload = dict(map(lambda k_v: (k_v[0].lower(), k_v[1]), iteritems(thing)))

    # added to avoid creating Value objects if the value was considered bad values
    # but we don't need this since we don't want the library to cull bad values that
    # the pi web api gave us.
    #
    # if 'good' in payload:
    #     if not payload['good']:
    #         return None

    payload.update({'session': session, 'webapi': webapi})
    thing = factory.create(**payload)
    return thing


class Factory(object):
    def __init__(self, type_):
        self.type = type_

    def create(self, **kwargs):
        return self.type(**kwargs)
