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
osisoftpy.point
~~~~~~~~~~~~
This module contains the class definition for the Point class, 
which represents a PI System Point it's described by the PI Web API."""

import logging

from osisoftpy.base import Base
from osisoftpy.factory import Factory
from osisoftpy.factory import create
from osisoftpy.internal import get
from osisoftpy.value import Value

log = logging.getLogger(__name__)

class Point(Base):
    """An :class:`OSIsoftPy <osisoftpy.dataarchive.Point>` object.
    
    Representation of a PI System Point as described by the PI Web API. 
    
    :param name: Point name
    :param description: Description for the PI Point
    :param webid: Unique GUID for the Point created by the PI Web API
    :param uniqueid: Unique GUID for the Point created by the PI System
    :param datatype: PI Point datatype
    
    :return: :class:`OSIsoftPy <osisoftpy.dataarchive.Point>` object
    :rtype: osisoftpy.dataarchive.Point
    """

    valid_attr = {'name', 'description', 'uniqueid', 'webid', 'datatype',
                  'links', 'session', 'webapi'}

    def __init__(self, **kwargs):
        super(self.__class__, self).__init__(**kwargs)

    def __str__(self):
        return '<OSIsoft PI Point [{} - {}]>'.format(self.name, self.description)

        self.current_value = None
        self.interpolated_values = None
        self.recorded_values = None
        self.plot_values = None
        self.summary_values = None
        self.end_value = None

    # TODO: add checks to prevent erroneous returns from creating values
    # TODO: i.e.: some of the *spf* tags return invalid webid errors...
    @property
    def current(self, time=None):
        try:
            return self._get_current(time=time)
        except Exception as e:
            raise e

    def interpolated(self, **kwargs):
        try:
            return self._get_interpolated(**kwargs)
        except Exception as e:
            raise e

    @property
    def interpolatedattimes(self, **kwargs):
        try:
            return self._get_interpolatedattimes(**kwargs)
        except Exception as e:
            raise e

    @property
    def recorded(self, **kwargs):
        try:
            return self._get_recorded(**kwargs)
        except Exception as e:
            raise e

    @property
    def recordedattime(self, **kwargs):
        try:
            return self._get_recordedattime(**kwargs)
        except Exception as e:
            raise e

    @property
    def plot(self, **kwargs):
        try:
            return self._get_plot(**kwargs)
        except Exception as e:
            raise e

    @property
    def summary(self, **kwargs):
        try:
            return self._get_summary(**kwargs)
        except Exception as e:
            raise e

    @property
    def end(self, **kwargs):
        try:
            return self._get_end(**kwargs)
        except Exception as e:
            raise e

    def _get_value(self, payload, endpoint, **kwargs):
        log.debug('payload: %s', payload)
        url = '{}/streams/{}/{}'.format(self.webapi.links.get('Self'),
                                        self.webid, endpoint)
        r = get(url, self.session, params=payload, **kwargs)
        value = create(Factory(Value), r.response.json(), self.session,
                       self.webapi)
        return value

    def _get_values(self, payload, endpoint, **kwargs):
        url = '{}/streams/{}/{}'.format(self.webapi.links.get('Self'),
                                        self.webid, endpoint)
        r = get(url, self.session, params=payload, **kwargs)
        values = list(map(
            lambda x: create(Factory(Value), x, self.session, self.webapi),
            r.response.json().get('Items', None)
        ))
        return values

    def _get_current(self, **kwargs):
        payload = {'time': kwargs.get('time', None)}
        endpoint = 'value'
        return self._get_value(payload=payload, endpoint=endpoint, **kwargs)

    def _get_interpolated(self, **kwargs):
        payload = {
            'starttime': kwargs.get('starttime', None),
            'endtime': kwargs.get('endtime', None),
            'interval': kwargs.get('interval', None),
            'filterexpression': kwargs.get('filterexpression', None),
            'includefilteredvalues': kwargs.get('includefilteredvalues', None),
        }
        endpoint = 'interpolated'
        return self._get_values(payload=payload, endpoint=endpoint, **kwargs)

    def _get_interpolatedattimes(self, **kwargs):
        payload = {
            'time': kwargs.get('starttime', None),
            'time': kwargs.get('endtime', None),
            'time': kwargs.get('interval', None),
            'time': kwargs.get('filterexpression', None),
            'time': kwargs.get('includefilteredvalues', None),
        }
        endpoint = 'interpolated'
        return self._get_values(payload=payload, endpoint=endpoint, **kwargs)

    def _get_recorded(self, **kwargs):
        payload = {
            'time': kwargs.get('starttime', None),
            'time': kwargs.get('endtime', None),
            'time': kwargs.get('interval', None),
            'time': kwargs.get('filterexpression', None),
            'time': kwargs.get('includefilteredvalues', None),
        }
        endpoint = 'interpolated'
        return self._get_values(payload=payload, endpoint=endpoint, **kwargs)

    def _get_recordedattime(self, **kwargs):
        payload = {
            'time': kwargs.get('starttime', None),
            'time': kwargs.get('endtime', None),
            'time': kwargs.get('interval', None),
            'time': kwargs.get('filterexpression', None),
            'time': kwargs.get('includefilteredvalues', None),
        }
        endpoint = 'interpolated'
        return self._get_values(payload=payload, endpoint=endpoint, **kwargs)

    def _get_plot(self, **kwargs):
        payload = {
            'time': kwargs.get('starttime', None),
            'time': kwargs.get('endtime', None),
            'time': kwargs.get('interval', None),
            'time': kwargs.get('filterexpression', None),
            'time': kwargs.get('includefilteredvalues', None),
        }
        endpoint = 'interpolated'
        return self._get_values(payload=payload, endpoint=endpoint, **kwargs)

    def _get_summary(self, **kwargs):
        payload = {
            'time': kwargs.get('starttime', None),
            'time': kwargs.get('endtime', None),
            'time': kwargs.get('interval', None),
            'time': kwargs.get('filterexpression', None),
            'time': kwargs.get('includefilteredvalues', None),
        }
        endpoint = 'interpolated'
        return self._get_values(payload=payload, endpoint=endpoint, **kwargs)

    def _get_end(self, **kwargs):
        payload = {
            'time': kwargs.get('starttime', None),
            'time': kwargs.get('endtime', None),
            'time': kwargs.get('interval', None),
            'time': kwargs.get('filterexpression', None),
            'time': kwargs.get('includefilteredvalues', None),
        }
        endpoint = 'interpolated'
        return self._get_values(payload=payload, endpoint=endpoint, **kwargs)
