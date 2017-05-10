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
osisoftpy.osisoftpy_ex2
~~~~~~~~~~~~
Some blah blah about what this file is for...
"""

import logging      # To disable logging spam
import osisoftpy    # main package
import numpy        # stats
import arrow        # date formatting
from osisoftpy.Points import current

# Disable log spam - from DEBUG => INFO\
loglevel = logging.DEBUG
log = logging.getLogger(osisoftpy.__name__)
log.setLevel(loglevel)
for h in log.handlers[:]:
    h.setLevel(loglevel)

# Connect and instantiate the webapi object
webapi = osisoftpy.webapi('https://sbb03.eecs.berkeley.edu/piwebapi', authtype='basic', username='albertxu', password='Welcome2pi')
print('Connected to {}'.format(webapi.links.get('Self')))

# send the Web API an Indexed Search query for tags named SINU*
points = webapi.points(query='name:sinu*', count=1000)

current(points, 'values', webapi=webapi)

# for each point returned...
for point in points:

    # let's print out it's current value and timestamp...
    print('Name: {}, current: {}, timestamp: {}'.format(
        point.name, point.current.value, point.current.timestamp))

    # let's also get the last 2 weeks of data at 1 minute intervals...
    interpolated = (point.interpolated(
        starttime='*-14d', endtime='*', interval='1m'))
    print('{} interpolated values for {} were retrieved.').format(
        interpolated.__len__(), point.name)

    # and then do some simple numpy calls against the 2 weeks of data:
    min = numpy.amin([v.value for v in interpolated])
    max = numpy.amax([v.value for v in interpolated])
    mean = numpy.mean([v.value for v in interpolated])
    average = numpy.average([v.value for v in interpolated])
    median = numpy.median([v.value for v in interpolated])
    mode = numpy.median([v.value for v in interpolated])
    stdev = numpy.std([v.value for v in interpolated])
    variance = numpy.var([v.value for v in interpolated], ddof=False)
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
    print('-----------------------------------------')
    print('The interpolated data spans from {} to {}').format(
        arrow.get(interpolated[0].timestamp).humanize(),
        arrow.get(interpolated[-1].timestamp).humanize()
    )




    print(point.current.value)
    print(point.uniqueid)
    print(point.webid)
    print(point.datatype)
    print(point.interpolated())
    for value in point.interpolated():
        print(value.timestamp, value.value)
    for value in point.recorded():
        print(value.timestamp, value.value)




for point in points:
    print(point)

print('{} PI points were retrieved.'.format(points.__len__()))

print()




for point in points:
    print('The current value for {} is {}, recorded {}'.format(
        point.name,
        point.current.value,
        arrow.get(point.current.timestamp).humanize(), ))

# for point in points:
#     print('{} interpolated values for {} were recorded:'.format(
#         point.interpolated.__len__(), point.name))
#     for value in point.interpolated:
#         print('... {} {}'.format(
#             value.value,
#             arrow.get(value.timestamp).humanize(), ))

for point in (p for p in points):
    values = point.interpolated(starttime='*-14d', endtime='*', interval='1m')
    points_msg = '{} PI points were retrieved.'.format(points.__len__())
    summary_msg = ('{} interpolated values for {} were retrieved. '
           'The data spans from {} to {}').format(
        values.__len__(),
        point.name,
        arrow.get(values[0].timestamp).humanize(),
        arrow.get(values[-1].timestamp).humanize()
    )
    min = numpy.amin([v.value for v in values])
    max = numpy.amax([v.value for v in values])
    mean = numpy.mean([v.value for v in values])
    average = numpy.average([v.value for v in values])
    median = numpy.median([v.value for v in values])
    mode = numpy.median([v.value for v in values])
    stdev = numpy.std([v.value for v in values])
    variance = numpy.var([v.value for v in values], ddof=False)
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
print(points_msg)




