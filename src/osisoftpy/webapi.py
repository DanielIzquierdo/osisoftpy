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
osisoftpy.webapi
~~~~~~~~~~~~
Some blah blah about what this file is for...
"""
import logging

from osisoftpy.base import Base
from osisoftpy.internal import get
from osisoftpy.internal import wrapt_handle_exceptions
from osisoftpy.factory import Factory, create
from osisoftpy.point import Point

log = logging.getLogger(__name__)


class WebAPI(Base):
    """

    """
    valid_attr = {'links', 'session'}

    def __init__(self, **kwargs):
        super(self.__class__, self).__init__(**kwargs)

    def __str__(self):
        self_str = '<OSIsoft PI Web API [{}]>'
        return self_str.format(self.links.get('Self'))

    def search(self, **kwargs):
        try:
            return self._get_search(**kwargs)
        except Exception as e:
            raise e

    def response(self, **kwargs):
        try:
            return self._get_response(**kwargs)
        except Exception as e:
            raise e

    def points(self, **kwargs):
        try:
            return self._get_points(**kwargs)
        except Exception as e:
            raise e

    @wrapt_handle_exceptions
    def streamset(self, **kwargs):
        # log.debug('payload: %s', kwargs.get('payload', None))
        # for point in kwargs.get('points'):
        #
        #
        # url = '{}/streamsets/{}/{}'.format(
        #     self.links.get('Self'),
        #     'pointsplaceholder',
        #     kwargs.get('action'),
        #     self.webid, action)
        # r = get(url, self.session, params=payload, **kwargs)
        # value = create(Factory(Value), r.response.json(), self.session,
        #                self.webapi)
        # return value
        pass



    def _get_search(self, **kwargs):
        r = get(self.links.get('Search'), self.session, **kwargs)
        return r.response

    def _get_response(self, **kwargs):
        r = get(self.links.get('Search') + '/query', self.session, **kwargs)
        return r.response

    def _get_points(self, **kwargs):
        r = get(self.links.get('Search') + '/query', self.session, **kwargs)

        points = list(
            map(lambda x: create(Factory(Point), x, self.session, self),
                r.response.json().get('Items', None)))
        return points
