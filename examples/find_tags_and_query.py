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
osisoftpy.find_tags_and_query
~~~~~~~~~~~~
Some blah blah about what this file is for...
"""

# Fix print functions
from __future__ import print_function

import osisoftpy    # main package
import numpy        # stats
import arrow        # date formatting
from requests.packages.urllib3.exceptions import InsecureRequestWarning


# disable InsecureRequestWarnings
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# Connect and instantiate the webapi object for basic
webapi = osisoftpy.webapi('https://sbb03.eecs.berkeley.edu/piwebapi', authtype='basic', username='albertxu', password='Welcome2pi')

# Connect and instantiate the webapi object for kerberos
# webapi = osisoftpy.webapi('https://piudnpiwebapi/piwebapi', authtype='kerberos', verifyssl=False)

print('Connected to {}'.format(webapi.links.get('Self')))


# Send the Web API an Indexed Search query for tags named SINU*
search_paramaters = {'q': "name:SINU*"}
points = webapi.points(params=search_paramaters)


# for each point returned...
for point in (p for p in points):


    # let's print out it's current value and timestamp...
    print('Name: {}, current: {}, timestamp: {}'.format(
        point.name, point.current.value, point.current.timestamp))


    # let's also get the last 2 weeks of data at 1 minute intervals...
    interpolated_values = point.interpolated(starttime='*-14d', endtime='*', interval='1m')


    # create some messages to be printed out...
    points_msg = '{} PI points were retrieved.'.format(points.__len__())
    summary_msg = ('{} interpolated values for {} were retrieved. '
                   'The data spans from {} to {}').format(
        interpolated_values.__len__(),
        point.name,
        arrow.get(interpolated_values[0].timestamp).humanize(),
        arrow.get(interpolated_values[-1].timestamp).humanize()
    )


    # and then do some simple numpy calls against the 2 weeks of data:
    min = numpy.amin([v.value for v in interpolated_values])
    max = numpy.amax([v.value for v in interpolated_values])
    mean = numpy.mean([v.value for v in interpolated_values])
    average = numpy.average([v.value for v in interpolated_values])
    median = numpy.median([v.value for v in interpolated_values])
    mode = numpy.median([v.value for v in interpolated_values])
    stdev = numpy.std([v.value for v in interpolated_values])
    variance = numpy.var([v.value for v in interpolated_values], ddof=False)


    # now let's print out our results for each point
    print('Summary: for {}'.format(point.name))
    print('--------')
    print('Current:  {}'.format(point.current.value))
    print('Min:      {}'.format(min))
    print('Max:      {}'.format(max))
    print('Mean:     {}'.format(mean))
    print('Average:  {}'.format(average))
    print('Median:   {}'.format(median))
    print('Mode:     {}'.format(mode))
    print('Stdev:    {}'.format(stdev))
    print('Variance: {}'.format(variance))
    print(summary_msg)


# and print out a single summary for all points
print(points_msg)