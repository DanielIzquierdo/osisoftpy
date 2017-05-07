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
import arrow
import osisoftpy
import numpy

webapi = osisoftpy.webapi(
    'https://sbb03.eecs.berkeley.edu/piwebapi',
    authtype='basic',
    username='albertxu',
    password='Welcome2pi', )

print(webapi)

print('Connected to {}'.format(webapi.links.get('Self')))

params= dict(q="name:CDT158", count=10)
points = webapi.points(params=params)

for point in points:
    print(point)

print(points)

print('{} PI points were retrieved.'.format(points.__len__()))

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

    # for value in values:
    #     print('... {} {}'.format(
    #         value.value,
    #         arrow.get(value.timestamp).humanize(), ))
    msg = ('{} interpolated values for {} were retrieved. '
           'The data spans from {} to {}').format(
        values.__len__(),
        point.name,
        arrow.get(values[0].timestamp).humanize(),
        arrow.get(values[-1].timestamp).humanize()
    )

    print(msg)

    min = numpy.amin([v.value for v in values])
    max = numpy.amax([v.value for v in values])
    mean = numpy.mean([v.value for v in values])
    average = numpy.average([v.value for v in values])
    median = numpy.median([v.value for v in values])
    mode = numpy.median([v.value for v in values])
    stdev = numpy.std([v.value for v in values])
    variance = numpy.var([v.value for v in values], ddof=False)

    print('Current:  {}'.format(point.current.value))
    print('Min:      {}'.format(min))
    print('Max:      {}'.format(max))
    print('Mean:     {}'.format(mean))
    print('Average:  {}'.format(average))
    print('Median:   {}'.format(median))
    print('Mode:     {}'.format(mode))
    print('Stdev:    {}'.format(stdev))
    print('Variance: {}'.format(variance))


