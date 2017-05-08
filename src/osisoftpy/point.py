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
    
    :return: :class:`OSIsoftPy <osisoftpy.Point>` object
    :rtype: osisoftpy.Point
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
        """
        Returns the value of the stream at the specified time. By default, 
        this is usually the current value. 

        :param time: An optional time. The default time context is 
            determined from the owning object - for example, the time range of 
            the event frame or transfer which holds this attribute. Otherwise, 
            the implementation of the Data Reference determines the meaning of 
            no context. For Points or simply configured PI Point Data 
            References, this means the snapshot value of the PI Point on the 
            Data Server.
        :return: :class:`OSIsoftPy <osisoftpy.Point>` object
        :rtype: osisoftpy.Point
        """
        payload = {'time': time}
        return self._get_value(payload=payload, endpoint='value')

    @wrapt_handle_exceptions
    def interpolated(
            self,
            starttime='*-1d',
            endtime='*',
            interval='1h',
            filterexpression=None,
            includefilteredvalues=False,
            selectedfields=None,):
        """
        Retrieves interpolated values over the specified time range at 
        the specified sampling interval. 

        :param starttime: An optional start time. The default is '*-1d' for 
            element attributes and points. For event frame attributes, 
            the default is the event frame's start time, or '*-1d' if that is 
            not set. 
        :param endtime: An optional end time. The default is '*' 
            for element attributes and points. For event frame attributes, 
            the default is the event frame's end time, or '*' if that is not 
            set. Note that if endTime is earlier than startTime, the resulting 
            values will be in time-descending order. 
        :param interval: The sampling interval, in AFTimeSpan format. 
        :param filterexpression: An 
            optional string containing a filter expression. Expression 
            variables are relative to the data point. Use '.' to reference the 
            containing attribute. If the attribute does not support filtering, 
            the filter will be ignored. The default is no filtering. 
        :param 
            includefilteredvalues: Specify 'true' to indicate that values which 
            fail the filter criteria are present in the returned data at the 
            times where they occurred with a value set to a 'Filtered' 
            enumeration value with bad status. Repeated consecutive failures 
            are omitted. 
        :param selectedfields: List of fields to be returned in the 
            response, separated by semicolons (;). If this parameter is not 
            specified, all available fields will be returned. 
        :return: :class:`OSIsoftPy <osisoftpy.structures.TypedList>` object 
            containing a list of 
            :class:`OSIsoftPy <osisoftpy.dataarchive.Point>` objects. 
        :rtype: osisoftpy.TypedList<osisoftpy.Point>
        """
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
    def interpolatedattimes(
            self,
            time,
            filterexpression=None,
            includefilteredvalues=False,
            sortorder='Ascending',
            selectedfields=None,):
        """
        Retrieves interpolated values over the specified time range at the 
        specified sampling interval. 
 
        :param time: A list of timestamps at which to retrieve interpolated 
                values. 
        :param filterexpression: An 
            optional string containing a filter expression. Expression 
            variables are relative to the data point. Use '.' to reference the 
            containing attribute. If the attribute does not support filtering, 
            the filter will be ignored. The default is no filtering. 
        :param 
            includefilteredvalues: Specify 'true' to indicate that values which 
            fail the filter criteria are present in the returned data at the 
            times where they occurred with a value set to a 'Filtered' 
            enumeration value with bad status. Repeated consecutive failures 
            are omitted. 
        :param selectedfields: List of fields to be returned in the 
            response, separated by semicolons (;). If this parameter is not 
            specified, all available fields will be returned. 
        :param sortorder The order that the returned collection is sorted. The 
            default is 'Ascending'. 
        :return: :class:`OSIsoftPy <osisoftpy.structures.TypedList>` object 
            containing a list of 
            :class:`OSIsoftPy <osisoftpy.dataarchive.Point>` objects. 
        :rtype: osisoftpy.TypedList<osisoftpy.Point>
        """
        payload = {
            'time': time,
            'filterexpression': filterexpression,
            'includefilteredvalues': includefilteredvalues,
            'sortorder': sortorder,
            'selectedfields': selectedfields,
        }
        endpoint = 'interpolatedattimes'
        return self._get_values(payload=payload, endpoint=endpoint)

    @wrapt_handle_exceptions
    def recorded(self, **kwargs):
        return self._get_recorded(**kwargs)

    @property
    @wrapt_handle_exceptions
    def recordedattime(self, **kwargs):
        return self._get_recordedattime(**kwargs)

    @wrapt_handle_exceptions
    def plot(self, **kwargs):
        return self._get_plot(**kwargs)

    @property
    @wrapt_handle_exceptions
    def summary(self, **kwargs):
        return self._get_summary(**kwargs)

    @property
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
