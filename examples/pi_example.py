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
osisoftpy.pi_example
~~~~~~~~~~~~
Examples of using osisoftpy library
"""

# Fix print functions
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
from future.utils import iteritems
import osisoftpy  # main package
import arrow
import time

import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

#user-inputed variables
piwebapiurl = 'https://dev.dstcontrols.com/piwebapi/'
query = 'name:SINU*'

# Connect and instantiate the webapi object (using kerberos as default)
webapi = osisoftpy.webapi(piwebapiurl)
print('Connected to {}'.format(webapi.links.get('Self')))

# Get a list of Points from the Web API:
points = webapi.points(query=query, count=100)

# Get count of number of points:
print('Number of Tags founds are {}', len(points))
print()

# a list to store modified points in:
updated_points = []

# When the monitored point's value changes, it emits a signal.
# This will call a function, known as as the receiver. Here, We're creating
# receiver named notify which will simply print out the changed Point's
# attributes, and saving the updated point to a list for us to use later.
def notify_current_value(sender):
    msg = 'Current value for {} has changed to {}'
    test = any(point[0] == sender.webid for point in updated_points)
    if not test:
        updated_points.append([sender.webid, 'current', sender])  # TODO: change ex to remove old point
    print(msg.format(sender.name, sender.current_value.value))

def notify_end_value(sender):
    msg = 'End value for {} has changed to {}'
    updated_points.append([sender, 'end'])  # TODO: change ex to remove old point
    print(msg.format(sender.name, sender.current_value.value))

# Get a list of point signals for the points we'd like to monitor for changes.
# We're passing in a list of points, and the Point's method we're monitoring.
webapi.subscribe(points, 'current', callback=notify_current_value)
# webapi.subscribe(points, 'end', callback=notify_end_value)

# subscribed with no callback
webapi.subscribe(points, 'interpolatedattimes', '2017-06-01T07:00:00Z')
webapi.subscribe(points, 'recordedattime', '2017-06-01T07:00:00Z')

# Here, we're creating a simple 500ms timer which will grab the latest value
#  for each PI point. The point.current() method will emit the change signal
#  when the value changes.
# we'll just run this until we receive 10 point changes:
starttime = time.time()

for point in points:
    point.current()
    print('The current value for {} is {}, recorded {}'.format(
        point.name,
        point.current_value.value,
        arrow.get(point.current_value.timestamp).humanize()))

while updated_points.__len__() < 10:
    for point in points:
        point.current()
        # run every 500 milliseconds
        sleep = 1 / 2
        time.sleep(sleep - ((time.time() - starttime) % sleep))

quit()