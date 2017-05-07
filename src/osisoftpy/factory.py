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
Some blah blah about what this file is for...
"""
import logging
from six import iteritems
from osisoftpy.internal import _stringify

log = logging.getLogger(__name__)


def create(factory, thing, session, webapi=None):
    """
    Return an object created with factory
    :param webapi: 
    :param factory: 
    :param params: 
    :param session: 
    :return: 
    """
    kwargs = dict(map(lambda k_v: (k_v[0].lower(), k_v[1]), iteritems(thing)))
    kwargs.update({'session': session, 'webapi': webapi})
    thing = factory.create(**kwargs)
    log.debug('Created %s, kwargs: %s', type(thing), _stringify(**kwargs))
    return thing


class Factory(object):
    def __init__(self, type_):
        self.type = type_

    def create(self, **kwargs):
        return self.type(**kwargs)
