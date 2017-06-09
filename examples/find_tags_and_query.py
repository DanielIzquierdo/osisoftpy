# -*- coding: utf-8 -*-

#    Copyright 2017 DST Controls
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE,-2.0
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
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
from future.utils import iteritems
import arrow
import time
import osisoftpy  # main package
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# Connect and instantiate the webapi object for basic
# webapi = osisoftpy.webapi('https://sbb03.eecs.berkeley.edu/piwebapi',
#                           authtype='basic', username='albertxu',
#                           password='Welcome2pi')

# Connect and instantiate the webapi object for kerberos
# webapi = osisoftpy.webapi('https://piudnpiwebapi.sli.pge.com/piwebapi', authtype='kerberos', verifyssl=False)
# webapi = osisoftpy.webapi('https://dev.dstcontrols.com/piwebapi/', authtype='kerberos', verifyssl=False, hostname_override='api.osisoft.dstcontrols.local')
webapi = osisoftpy.webapi('https://dev.dstcontrols.com/piwebapi/')

# webapi = osisoftpy.webapi('https://gold.dstcontrols.local/piwebapi/')

print('Connected to {}'.format(webapi.links.get('Self')))

# Get a list of Points from the Web API:
points = webapi.points(query='name:CD* or name:SINU*', count=100)

# Get a list of point signals for the points we'd like to monitor for changes.
# We're passing in a list of points, and the Point's method we're monitoring.
signals = webapi.subscribe(points, 'current')

# a list to store modified points in:
updated_points = []

# When the monitored point's value changes, it emits a signal.
# This will call a function, known as as the receiver. Here, We're creating
# receiver named notify which will simply print out the changed Point's
# attributes, and saving the updated point to a list for us to use later.


def notify(sender):
    msg = 'Current value for {} has changed to {}'
    if sender not in updated_points: 
        updated_points.append(sender)  
    print(msg.format(sender.name, sender.current_value))


# Here is where we're connecting to the signals that will be emitted. We're
# going through the signals we retrieved earlier, and connecting to each
# one, passing in the reciver function we just defined
for (k, signal) in iteritems(signals):
    signal.connect(notify)

# Here, we're creating a simple 500ms timer which will grab the latest value
#  for each PI point. The point.current() method will emit the change signal
#  when the value changes.
# we'll just run this until we receive 10 point changes:
starttime = time.time()

# for point in points:
#     point.recorded(starttime='*-14d', endtime='*', maxcount=1000)

# points.current()

for point in points:
    point.current()
    print('The current value for {} is {}, recorded {}'.format(
        point.name,
        point.current_value.value,
        arrow.get(point.current_value.timestamp).humanize()))

# for point in points:
#     point.end()
#     print('The end value for {} is {}, recorded {}'.format(
#         point.name,
#         point.end_value.value,
#         arrow.get(point.end_value.timestamp).humanize()))

# for point in points:
#     values = point.interpolated(starttime='*-14d', endtime='*', interval='1m')

#     print('{} interpolated values for {} were retrieved; '
#           'the data ranges from {} to {}.'.format(
#               values.__len__(),
#               point.name,
#               arrow.get(values[0].timestamp).humanize(),
#               arrow.get(values[-1].timestamp).humanize()))

while updated_points.__len__() < 10:
    for point in points:
        point.current()
        # run every 500 milliseconds
        sleep = 1 / 2
        time.sleep(sleep - ((time.time() - starttime) % sleep))


# print out the modified points
for point in updated_points:
    print(point)


# obs = osisoftpy.observable(points)
# obs2 = points.current_observable()
#
# # obs.subscribe(on_next=lambda value: print("obs Received {0}".format(value)),
# #               on_completed=lambda: print("obs Done!"),
# #               on_error=lambda error: print("obs Error Occurred: {0}".format(error))
# #               )
#
#
# obs2.subscribe(on_next=lambda value: print("obs2 Received {0}".format(value)),
#               on_completed=lambda: print("obs2 Done!"),
#               on_error=lambda error: print("obs2 Error Occurred: {0}".format(error))
#               )
#
# print('foo')


# Send the Web API an Indexed Search query for tags named SINU*
# search_paramaters = {'q': "name:SINU*"}
# points = webapi.points(params=search_paramaters)


# points = webapi.foopoints(query='name:*SPF*', count=100)


quit()

# .map(lambda point: getInterpolatedValues(point)) \
#  \
#  \
for point in points:
    print('getting data for %s...' % point.name)
    # let's also get the last 2 weeks of data at 1 minute intervals...
    interpolated_values = point.interpolated(starttime='*-14d', endtime='*',
                                             interval='1m')
    values[point.name] = interpolated_values

points.current()

for point in points:
    print(point.name)
    print('1: current value: %s' % point.current_value)
    print('2: Return from current(): %s' % point.current())
    print('3: current value: %s' % point.current_value)
    print('4: Overwrite=False, current(): %s' % point.current(overwrite=False))

    # for value in point:
    #     print(value.timestamp)

# for each point returned...
for point in (p for p in points):
    # let's print out it's current value and timestamp...
    print('Name: {}, current: {}, timestamp: {}'.format(
        point.name, point.current.value, point.current.timestamp))

    # let's also get the last 2 weeks of data at 1 minute intervals...
    interpolated_values = point.interpolated(starttime='*-14d', endtime='*',
                                             interval='1m')

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
