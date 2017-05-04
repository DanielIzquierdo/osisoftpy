#! /usr/local/bin/python
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
osisoftpy_examples.py
~~~~~~~~~~~~
Examples of how to use the osisoftpy package.
"""

import arrow

from osisoftpy.webapi import WebAPI
from osisoftpy.utils import get_attribute, get_count

# Friendly US datetime format:
human_datetime_format = 'YYYY-MM-DD HH:mm:ss ZZ'
iso8601_datetime_format = 'YYYY-MM-DDTHH:mm:ss.SSSSSSSZ'
#                          2017-05-01T20:59:44.6226961Z


dev = 'https://api.osisoft.dstcontrols.local/piwebapi/'
prod = 'https://dev.dstcontrols.com/piwebapi/'
eecs = 'https://sbb03.eecs.berkeley.edu/piwebapi/'

sample_query = type('Query', (object,), {})()

sample_query.single_tag = 'name:sinusoid'
sample_query.multi_tag = 'name:sinusoid or name:cdt158 or name:cd*'
sample_query.partial_tag = 'name:sinusoid*'
sample_query.wildcard = '*SPF_environment_sensor*'
sample_query.calctypes = ['current', 'interpolated', 'interpolatedattimes',
                          'recorded', 'recordedattime', 'plot', 'summary']

# Basic authentication example:
api = WebAPI(url=eecs, verifyssl=True, authtype='basic', username='albertxu',
             password='Welcome2pi')

# returns a PI Data Archive server object
pi_server = api.get_data_archive_server('sbb03.eecs.berkeley.edu')

# returns PI point objects (without data).
points = api.get_points(query=sample_query.single_tag, count=100,
                        scope='pi:{}'.format(pi_server.name))

lastmonth = arrow.utcnow().replace(months=-1).datetime
# gets data for the provided PI point objects
for calctype in sample_query.calctypes:
    points = api.get_values(points=points, calculationtype=calctype,
                            time=lastmonth, overwrite=False, append=True)

# This is just a simple object to track how many total values are returned
# across all points and calculation types which are requested.
totalizer = type('Totalizer', (object,), {})()

# Create an attribute of type int for each totalizer type
for calctype in sample_query.calctypes:
    setattr(totalizer, calctype, 0)

# Create totalizer.total to track total values returned across all calctypes
setattr(totalizer, 'total', 0)
setattr(totalizer, 'tags', 0)

for point in points:
    totalizer.tags += 1

    for calctype in [x for x in sample_query.calctypes if
                     not x.endswith(('attimes', 'attime'))]:

        values = getattr(point, get_attribute(calctype))

        # Counts the number of values returned for this calculation type and
        #  adds it to the corresponding totalizer attribute
        total = sum((getattr(totalizer, calctype), get_count(values)))
        setattr(totalizer, calctype, total)

        # this once is named and not dynamic, so we can just set the value
        # directly and add the new values to the existing attribute value
        totalizer.total += get_count(values)

        msg_header = '{} {} value(s) were returned for {}'
        print(msg_header.format(get_count(values), calctype, point.name))
        msg_body = '{} {} value at {}: {}'
        if calctype == 'current' or calctype == 'end':
            value = values
            print(msg_body.format(point.name, value.calculationtype,
                                  value.timestamp, value.value))
        else:
            for value in values:
                print(msg_body.format(point.name, value.calculationtype,
                                      value.timestamp, value.value))
msg_summary = '{} values returned - {} current, {} interpolated, {} plot, ' \
              '{} recorded, and {} summary'
print(msg_summary.format(totalizer.total, totalizer.current,
                         totalizer.interpolated, totalizer.plot,
                         totalizer.recorded, totalizer.summary))
