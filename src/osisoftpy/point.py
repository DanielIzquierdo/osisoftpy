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
This module contains the class definition for the Point class, which
represents a PI System Point it's described by the PI Web API.
"""

import logging
import wrapt
from osisoftpy.base import Base
from osisoftpy.factory import Factory
from osisoftpy.factory import create
from osisoftpy.internal import get
from osisoftpy.value import Value

log = logging.getLogger(__name__)

@wrapt.decorator
def wrapt_handle_exceptions(wrapped, instance, args, kw):
    log.debug('Calling decorated function %s', wrapped)
    try:
        return wrapped(*args, **kw)
    except Exception as e:
        raise e


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
        self_str = '<OSIsoft PI Point [{} - {}]>'
        return self_str.format(self.name, self.description)

        self.current_value = None
        self.interpolated_values = None
        self.recorded_values = None
        self.plot_values = None
        self.summary_values = None
        self.end_value = None

    @property
    @wrapt_handle_exceptions
    def current(self, time=None):
        payload = {'time': time}
        return self._get_value(payload=payload, endpoint='value')

    @wrapt_handle_exceptions
    def interpolated(
            self,
            starttime='*-3h',
            endtime='*',
            interval='1h',
            filterexpression=None,
            includefilteredvalues=False,
            selectedfields=None,):
        payload = {
            'starttime': starttime,
            'endtime': endtime,
            'interval': interval,
            'filterexpression': filterexpression,
            'includefilteredvalues': includefilteredvalues,
            'selectedfields': selectedfields,
        }
        return self._get_values(payload=payload, endpoint='interpolated')

    @wrapt_handle_exceptions
    def interpolatedattimes(self, **kwargs):
        return self._get_interpolatedattimes(**kwargs)

    @wrapt_handle_exceptions
    def recorded(self, **kwargs):
        return self._get_recorded(**kwargs)

    @wrapt_handle_exceptions
    def recordedattime(self, **kwargs):
        return self._get_recordedattime(**kwargs)

    @wrapt_handle_exceptions
    def plot(self, **kwargs):
        return self._get_plot(**kwargs)

    @wrapt_handle_exceptions
    def summary(self, **kwargs):
        return self._get_summary(**kwargs)

    @wrapt_handle_exceptions
    def end(self, **kwargs):
        return self._get_end(**kwargs)

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
