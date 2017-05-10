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
from osisoftpy.internal import _stringify
from osisoftpy.points import Points
import inspect

# Disable log spam - from DEBUG => INFO\
loglevel = logging.DEBUG
log = logging.getLogger(osisoftpy.__name__)
log.setLevel(loglevel)
for h in log.handlers[:]:
    h.setLevel(loglevel)

# Connect and instantiate the webapi object
webapi = osisoftpy.webapi('https://sbb03.eecs.berkeley.edu/piwebapi', authtype='basic', username='albertxu', password='Welcome2pi')
print('Connected to {}'.format(webapi.url))

# send the Web API an Indexed Search query for tags named SINU*
points = webapi.points(query='name:sinu*', count=1000)

for p in points:
    print(p.name)

# bulk = points.current()

# bulk = current('GET', webapi.url, points, 'value', webapi=webapi)
# bulk_points = bulk.response.json()
# print(points)
# print(_stringify(**points))
# for point in bulk_points:
#     print(point, bulk_points[point])
