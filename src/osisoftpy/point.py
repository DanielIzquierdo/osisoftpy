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
from __future__ import (absolute_import, division, unicode_literals)
from future.builtins import *

import logging
import warnings
import json

from datetime import datetime
from dateutil import parser

from osisoftpy.base import Base
from osisoftpy.factory import Factory
from osisoftpy.factory import create
from osisoftpy.internal import get
from osisoftpy.internal import put
from osisoftpy.internal import post
from osisoftpy.value import Value
from osisoftpy.exceptions import MismatchEntriesError
from osisoftpy.internal import _stringify

log = logging.getLogger(__name__)


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

        self.current_value = None
        self.interpolated_values = None
        self.interpolated_at_time_values = {}
        self.recorded_values = None
        self.recorded_at_time_values = {}
        self.plot_values = None
        self.summary_values = None
        self.end_value = None
        #test
        self.value_value = None

    def __str__(self):
        self_str = '<OSIsoft PI Point [{} - {}]>'
        return self_str.format(self.name, self.description)

    def attributes(self, namefilter=None, selectedfields=None):
        payload = {
            'namefilter': namefilter,
            'selectedfields': selectedfields,
        }
        return self._get_values(
            payload=payload, endpoint='attributes', controller='points')

    def update_value(self, timestamp, value, unitsabbreviation=None, good=None, questionable=None, updateoption='Replace', bufferoption='BufferIfPossible'):
        """
        Updates a value for the specified stream.
        Exception and Compression rules take effort in a batch POST request.

        :param timestamp: Manual entry of a datetime to be inserted
            into the PI tag
        :param value: Manual entry of value to be inserted 
        :param unitsabbreviation: Optional. Unit of measure abbreviation
            of the value. Defaults to "".
        :param good: Optional. The status indicates whether 
            the value is good or bad. Defaults to True
        :param questionable: Optional. The status indicates whether
            the data quality is accurate. Defaults to False
        :param updateoption: Optional. Indicates how to treat multiple values
            with the same timestamp. Default is 'Replace'. 
        :param bufferoption: Optional. Indicates how to buffer values
            updates. Default is 'BufferIfPossible'. 
        """
        payload = {'updateOption': updateoption, 'bufferOption': bufferoption }
        request = {'Timestamp': timestamp, 'Value': value, 'UnitsAbbreviation': unitsabbreviation, 'Good':good, 'Questionable':questionable}
        self._post_values(payload, request, 'value')

    def update_values(self, timestamps, values, unitsabbreviation=None, good=None, questionable=None, updateoption='Replace', bufferoption='BufferIfPossible'):
        """
        Updates multiple values for the specified stream.
        Assumes values property remains the same within the single call.
        Exception and Compression rules take effort in a batch POST request.

        :param timestamps: Manual entry of a list of datetimes to be inserted
            into the PI tag
        :param values: Manual entry of a list of values to be inserted 
        :param unitsabbreviation: Optional. Unit of measure abbreviation
            of the value. Defaults to "".
        :param good: Optional. The status indicates whether 
            the value is good or bad. Defaults to True
        :param questionable: Optional. The status indicates whether
            the data quality is accurate. Defaults to False
        :param updateoption: Optional. Indicates how to treat multiple values
            with the same timestamp. Default is 'Replace'. 
        :param bufferoption: Optional. Indicates how to buffer values
            updates. Default is 'BufferIfPossible'. 
        """
        #throws error if number of timestamps doesn't correspond to number of values
        if len(timestamps) != len(values):
            raise MismatchEntriesError(
                "The length of timestamps and values lists are not equal."
            )   
        payload = {'updateOption': updateoption, 'bufferOption': bufferoption }
        request = []
        for timestamp, value in zip(timestamps, values):
            request.append({'Timestamp': timestamp, 'Value': value, 'UnitsAbbreviation': unitsabbreviation, 'Good':good, 'Questionable':questionable})
        self._post_values(payload, request, 'recorded')

    def current(self, overwrite=True):
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
        :param overwrite: An optional boolean. 
        :return: :class:`OSIsoftPy <osisoftpy.Value>` object
        :rtype: osisoftpy.Value
        """
        payload={'time':'*'}

        # save the "old" current value before grabbing the "latest" current value
        oldvalue = self.current_value
        
        # grab and set the current value
        newvalue = self._get_value(payload=payload, endpoint='value')

        if not overwrite:
            warnings.warn('You have set the overwrite boolean to False - '
                          'the current value has been retrieved, but not '
                          'stored for this point.', UserWarning)
            return newvalue
        
        self.current_value = newvalue

        # emit a signal if the value changes. exclude changes to booleans or timestmap
        # currently, checking the Value objects doesn't work, so we compare the
        # Value.value values.
        # if oldvalue and oldvalue != self.end_value:\
        if oldvalue and self.current_value and self.current_value.value != oldvalue.value:
            signalkey = '{}/current/'.format(self.webid.__str__())
            self._send_signal(signalkey)

        return self.current_value
        

    def interpolated(
            self,
            starttime='*-1d',
            endtime='*',
            interval='1h',
            filterexpression=None,
            includefilteredvalues=False,
            selectedfields=None,
            overwrite=True ):
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
        values = self._get_values(payload=payload, endpoint='interpolated')
        return values
        # if not overwrite:
        #     warnings.warn('You have set the overwrite boolean to False - '
        #                   'the interpolated value(s) has been retrieved, but not '
        #                   'stored for this point.', UserWarning)
        #     return values
        # signalkey = '{}/interpolated'.format(self.webid.__str__())
        # if self.interpolated_values and self.interpolated_values != values:
        #     self.interpolated_values = values
        #     self.webapi.signals[signalkey].send(self)
        # elif not self.interpolated_values:
        #     self.interpolated_values = values

        # return self.interpolated_values

    def interpolatedattimes(
            self,
            timestamps,
            filterexpression=None,
            includefilteredvalues=False,
            sortorder='Ascending',
            selectedfields=None,
            overwrite=True ):
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
            'time': timestamps,
            'filterexpression': filterexpression,
            'includefilteredvalues': includefilteredvalues,
            'sortorder': sortorder,
            'selectedfields': selectedfields,
        }
        new_intp_values = self._get_values(payload=payload, endpoint='interpolatedattimes')
        if not overwrite:
            warnings.warn('You have set the overwrite boolean to False - '
                          'the interpolated value(s) has been retrieved, but not '
                          'stored for this point.', UserWarning)
            return new_intp_values

        oldvalues = {}
        newvalues = {}
        
        if not isinstance(timestamps, list):
            timestamps = [timestamps]

        for timestamp in timestamps:
            formattedtimestamp = self._parse_timestamp(timestamp)
            oldvalues[formattedtimestamp] = self.interpolated_at_time_values.get(formattedtimestamp)

        for value in new_intp_values:
            #assume pi and inputted timestamps are the same UTC timestamp
            pitimestamp = self._parse_timestamp(value.timestamp)
            oldvalue = oldvalues[pitimestamp]
            self.interpolated_at_time_values[pitimestamp] = value

            #compares old and new value to see if new value has changed
            if oldvalue and value and value.value != oldvalue.value:
                signalkey = '{}/interpolatedattimes/{}'.format(self.webid.__str__(), pitimestamp)
                self._send_signal(signalkey)

        return new_intp_values


    def plot(
        self, 
        starttime=None,
        endtime=None,
        timezone=None,
        intervals=None,
        desiredunits=None,
        selectedFields=None,
        overwrite=True,
        **kwargs):

        payload={
            'startTime': starttime,
            'endTime': endtime,
            'timeZone': timezone,
            'intervals': intervals,
            'desiredUnits': desiredunits,
            'selectedFields': selectedFields
        }

        values = self._get_values(payload=payload, endpoint='plot')
        return values
        # if not overwrite:
        #     warnings.warn('You have set the overwrite boolean to False - '
        #                   'the plot value(s) has been retrieved, but not '
        #                   'stored for this point.', UserWarning)
        #     return values
        # signalkey = '{}/plot/'.format(self.webid.__str__())
        # if self.plot_values and self.plot_values != values:
        #     self.plot_values = values
        #     self.webapi.signals[signalkey].send(self)
        # elif not self.plot_values:
        #     self.plot_values = values

        # return self.plot_values

    def recorded(
            self,
            starttime='*-1d',
            endtime='*',
            boundarytype='Inside',
            filterexpression=None,
            maxcount=1000,
            includefilteredvalues=False,
            selectedfields=None,
            overwrite=True):
        """
        Returns a list of compressed values for the requested time range 
        from the source provider. 

        Returned times are affected by the specified boundary type. If no 
        values are found for the time range and conditions specified then 
        the HTTP response will be success, with a body containing an empty 
        array of Items. When specifying true for the includeFilteredValues 
        parameter, consecutive filtered events are not returned. The first 
        value that would be filtered out is returned with its time and the 
        enumeration value "Filtered". The next value in the collection will 
        be the next compressed value in the specified direction that passes 
        the filter criteria - if any. When both boundaryType and a 
        filterExpression are specified, the events returned for the boundary 
        condition specified are passed through the filter. If the 
        includeFilteredValues parameter is true, the boundary values will be 
        reported at the proper timestamps with the enumeration value 
        "Filtered" when the filter conditions are not met at the boundary 
        time. If the includeFilteredValues parameter is false for this case, 
        no event is returned for the boundary time. 
        :param maxcount: 
        :param starttime: An optional start time. The default is '*-1d' for 
            element attributes and points. For event frame attributes, 
            the default is the event frame's start time, or '*-1d' if that is 
            not set. 
        :param endtime: An optional end time. The default is '*' 
            for element attributes and points. For event frame attributes, 
            the default is the event frame's end time, or '*' if that is not 
            set. Note that if endTime is earlier than startTime, the resulting 
            values will be in time-descending order. 
        :param boundarytype: An optional value that determines how the times 
            and values of the returned end points are determined.
            The default is 'Inside'.
        :param filterexpression: An optional string containing a filter 
            expression. Expression variables are relative to the data point. 
            Use '.' to reference the containing attribute. 
            The default is no filtering.
        :param includefilteredvalues: Specify 'true' to indicate that values 
            which  fail the filter criteria are present in the returned data 
            at the times where they occurred with a value set to a 'Filtered' 
            enumeration value with bad status. Repeated consecutive failures 
            are omitted. 
        :param selectedfields: List of fields to be returned in the 
            response, separated by semicolons (;). If this parameter is not 
            specified, all available fields will be returned. This parameter 
            filters PI Web API response so that the response only includes a 
            selected set of fields. It allows PI Web API to return none but the 
            information that you are interested in, and therefore reduce your 
            bandwidth usage. 
        :return: :class:`OSIsoftPy <osisoftpy.structures.TypedList>` 
            object containing a list of :class:`OSIsoftPy 
            <osisoftpy.dataarchive.Point>` objects. :rtype: 
            osisoftpy.TypedList<osisoftpy.Point> 
        """
        payload = {
            'starttime': starttime,
            'endtime': endtime,
            'boundarytype': boundarytype,
            'filterexpression': filterexpression,
            'maxcount': maxcount,
            'includefilteredvalues': includefilteredvalues,
            'selectedfields': selectedfields,
        }

        values = self._get_values(payload=payload, endpoint='recorded')
        return values
        # if not overwrite:
        #     warnings.warn('You have set the overwrite boolean to False - '
        #                   'the recorded value(s) has been retrieved, but not '
        #                   'stored for this point.', UserWarning)
        #     return values
        # signalkey = '{}/recorded/'.format(self.webid.__str__())
        # if self.recorded_values and self.recorded_values != values:
        #     self.recorded_values = values
        #     self.webapi.signals[signalkey].send(self)
        # elif not self.recorded_values:
        #     self.recorded_values = values

        # return self.recorded_values

    def recordedattime(
            self,
            time,
            retrievalmode='Auto',
            selectedfields=None,
            overwrite=True ):
        """
        Returns a single recorded value based on the passed time and 
        retrieval mode from the stream. 

        :param time: The timestamp at which the value is desired.
        :param retrievalmode: An optional value that determines the value to 
            return when a value doesn't exist at the exact time specified.
            The default is 'Auto'. The retrieval mode is an enumeration of the 
            possible values for retrieving recorded values from a stream. 
            The following values are accepted:
            Auto: Automatically determine the best retrieval mode.
            AtOrBefore: Return a recorded value at the passed time or if no 
                value exists at that time, the previous recorded value.
            Before: Return the first recorded value before the passed time.
            AtOrAfter: Return a recorded value at the passed time or if no 
                value exists at that time, the next recorded value.
            After: Return the first recorded value after the passed time.
            Exact: Return a recorded value at the passed time or return an 
                error if none exists.
        :param selectedfields: List of fields to be returned in the 
            response, separated by semicolons (;). If this parameter is not 
            specified, all available fields will be returned. 
        :return: :class:`OSIsoftPy <osisoftpy.dataarchive.Point>` object 
        :rtype: osisoftpy.osisoftpy.Point
        """
        payload = {
            'time': time,
            'retrievalmode': retrievalmode,
            'selectedfields': selectedfields,
        }

        formattedtime = self._parse_timestamp(time)
        old_recorded_at_time_value = self.recorded_at_time_values.get(formattedtime)
        
        new_recorded_at_time_value = self._get_value(payload=payload, endpoint='recordedattime')

        if not overwrite:
            warnings.warn('You have set the overwrite boolean to False - '
                          'the recorded at time value has been retrieved'
                          ', but not stored for this point.', UserWarning)
            return new_recorded_at_time_value

        self.recorded_at_time_values[formattedtime] = new_recorded_at_time_value
        if old_recorded_at_time_value and self.recorded_at_time_values[formattedtime] and self.recorded_at_time_values[formattedtime].value != old_recorded_at_time_value.value:
            signalkey = '{}/recordedattime/{}'.format(self.webid.__str__(),formattedtime or '')
            self._send_signal(signalkey)

        return new_recorded_at_time_value

    def summary(
        self,
        starttime=None,
        endtime=None,
        timezone=None,
        summarytype=None,
        calculationbasis=None,
        timetype=None,
        summaryduration=None,
        sampletype=None,
        sampleinterval=None,
        filterexpression=None,
        selectedfields=None,
        overwrite=True,
        **kwargs):

        payload = {
            'startTime': starttime,
            'endTime': endtime,
            'timeZone': timezone,
            'summaryType': summarytype,
            'calculationBasis': calculationbasis,
            'timeType': timetype,
            'summaryDuration': summaryduration,
            'sampleType': sampletype,
            'sampleInterval': sampleinterval,
            'filterExpression': filterexpression,
            'selectedFields': selectedfields
        }

        values = self._get_summary(payload=payload)
        return values
        # if not overwrite:
        #     warnings.warn('You have set the overwrite boolean to False - '
        #                   'the summary value(s) has been retrieved, but not '
        #                   'stored for this point.', UserWarning)
        #     return value
        # signalkey = '{}/summary/'.format(self.webid.__str__())
        # if self.summary_values and self.summary_values != values:
        #     self.summary_values = values
        #     self.webapi.signals[signalkey].send(self)
        # elif not self.summary_values:
        #     self.summary_values = values

        # return self.summary_values

    def end(
        self,
        overwrite=True):
        """
        Retrieves the end-of-stream (latest) value of the PI Tag.
        
        :return: :class:`OSIsoftPy <osisoftpy.dataarchive.Value>` object 
        :rtype: osisoftpy.osisoftpy.Value
        """
        # save the "old" end value before grabbing the "latest" end value
        oldendvalue = self.end_value

        newendvalue = self._get_value(payload=None, endpoint='end')

        if not overwrite:
            warnings.warn('You have set the overwrite boolean to False - '
                          'the end value has been retrieved, but not '
                          'stored for this point.', UserWarning)
            return newendvalue
            
        self.end_value = newendvalue

        # emit a signal if the value changes. exclude changes to booleans or timestmap
        # currently, checking the Value objects doesn't work, so we compare the
        # Value.value values.
        if oldendvalue and self.end_value and self.end_value.value != oldendvalue.value:
            signalkey = '{}/end/'.format(self.webid.__str__())
            self._send_signal(signalkey)
            
        return self.end_value


    def _get_value(self, payload, endpoint, controller='streams', **kwargs):
        # log.debug('payload: %s', payload)
        url = '{}/{}/{}/{}'.format(
            self.webapi.links.get('Self'), controller, self.webid, endpoint)
        r = get(url, self.session, params=payload, **kwargs)
        value = create(Factory(Value), r.response.json(), self.session,
                       self.webapi)
        return value

    def _get_values(self, payload, endpoint, controller='streams', **kwargs):
        url = '{}/{}/{}/{}'.format(self.webapi.links.get('Self'), controller,
                                        self.webid, endpoint)
        r = get(url, self.session, params=payload, **kwargs)
        values = list(map(
            lambda x: create(Factory(Value), x, self.session, self.webapi),
            r.response.json().get('Items', None)
        ))
        return values

    def _get_summary(self, payload, endpoint='summary', controller='streams', **kwargs):
        url = '{}/{}/{}/{}'.format(
            self.webapi.links.get('Self'), controller, self.webid, endpoint)
        r = get(url, self.session, params=payload, **kwargs)

        items = r.response.json().get('Items')
        for item in items:
            item.get('Value')['calculationtype'] = item.get('Type')

        values = list(map(
            lambda x: create(Factory(Value), x.get('Value'), self.session, self.webapi),
                items
        ))
        
        return values

    def _post_values(self, payload, request, endpoint):
        url = '{}/{}/{}/{}'.format(
            self.webapi.links.get('Self'), 'streams', self.webid, endpoint)
        post(url, self.session, params=payload, json=request)

    def _send_signal(self, signalkey):
        if signalkey in self.webapi.signals:
            self.webapi.signals[signalkey].send(self)

    def _parse_timestamp(self, datetime):
        if datetime:
            parseddatetime = parser.parse(datetime)
            formatteddatetime = None if parseddatetime == None else parseddatetime.strftime('%Y%m%d%H%M%S')
        else:  
            formatteddatetime = None
        return formatteddatetime
    
    def getvalue(self, time=None, overwrite=True):
        """
        Test method
        """
        payload={'time':time}

        # save the "old" current value before grabbing the "latest" current value
        oldvalue = self.value_value
        
        # grab and set the current value
        newvalue = self._get_value(payload=payload, endpoint='value')

        if not overwrite:
            warnings.warn('You have set the overwrite boolean to False - '
                          'the current value has been retrieved, but not '
                          'stored for this point.', UserWarning)
            return newvalue
        
        self.value_value = newvalue

        # emit a signal if the value changes. exclude changes to booleans or timestmap
        # currently, checking the Value objects doesn't work, so we compare the
        # Value.value values.
        # if oldvalue and oldvalue != self.end_value:\
        if not oldvalue:
            pass
        elif self.value_value and self.value_value.value != oldvalue.value:
            signalkey = '{}/getvalue/'.format(self.webid.__str__())
            self.webapi.signals[signalkey].send(self)

        return self.value_value
