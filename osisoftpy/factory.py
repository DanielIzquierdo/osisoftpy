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
from .utils import stringify_kwargs

log = logging.getLogger(__name__)


def create_thing(factory, dict_, session):
    """
    Return an object created with factory
    :param factory: 
    :param dict_: 
    :param session: 
    :return: 
    """
    kwargs = dict(map(lambda k_v: (k_v[0].lower().replace('self', 'url'), k_v[1]), iteritems(dict_)))
    kwargs.update({'session': session})
    thing = factory.create(**kwargs)
    log.debug('Created %s', thing)
    return thing


class Factory(object):
    """ Construct :class:`DataArchive <osisoftpy.dataarchive.DataArchive>`
    objects.
    
    :param type: (optional) the :class:`DataArchive <osisoftpy.dataarchive.DataArchive>`-based class to construct from.
        Defaults to :class:`DataArchive <osisoftpy.dataarchive.DataArchive>`.
    """

    def __init__(self, type_):
        log.debug('Factory initialized.')
        self.type = type_

    def create(self, **kwargs):
        """ Return a :class:`DataArchive <osisoftpy.dataarchive.DataArchive>` object.
        serverversion
        :param name: PI Data Archive server name
        :param webid: PI Data Archive Web ID
        :param serverversion: PI Data Archive software version
        :param isconnected: Connection status between the PI Web API and the PI Data Archive
        :param id: PI Data Archive ID
        
        """
        log.debug('Constructing %s, args are %s.', self.type,
                  stringify_kwargs(**kwargs))

        return self.type(**kwargs)
