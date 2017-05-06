# -*- coding: utf-8 -*-

import arrow
from osisoftpy.utils import get_count

from webapi import WebAPI

# Friendly US datetime format:
human_datetime_format = 'YYYY-MM-DD HH:mm:ss ZZ'
iso8601_datetime_format = 'YYYY-MM-DDTHH:mm:ss.SSSSSSSZ'
#                          2017-05-01T20:59:44.6226961Z

utcnow = arrow.utcnow()

webid = 'E06p4VDYuL1Ua-zPLKSAbL4ADGzt6vtB5RGAvwBQVpk9KwLkNSMTEuQklNRy5EQ19CUkFOQ0hfMDAwXzAxMg'

eecs = 'https://sbb03.eecs.berkeley.edu/piwebapi/'

# Basic authentication example:
api = WebAPI(url=eecs, verifyssl=True, authtype='basic', username='albertxu',
             password='Welcome2pi')

# returns a PI Data Archive server object
pi_server = api.get_data_archive_server('sbb03.eecs.berkeley.edu')

# returns PI point objects (without data).
points = api.get_points(query='name:sinusoid', count=1,
                        scope='pi:{}'.format(pi_server.name))
sinusoid = next(point for point in points if point.name.lower() == 'sinusoid')

sinusoid = api.get_values(points=sinusoid, calculationtype='interpolatedattimes', overwrite=True)

print(sinusoid)

point = sinusoid
values = sinusoid.interpolated_values
calctype = 'interpolatedattimes'

msg_header = '{} {} value(s) were returned for {}'
msg_body = '{} {} value at {}: {}'

print(msg_header.format(get_count(values), calctype, point.name))
for value in values:
    print(msg_body.format(point.name, value.calculationtype,
                          value.timestamp, value.value))


#
# sinusoid =
#
# # gets data for the provided PI point objects
# for calctype in sample_query.calctypes:
#     points = api.get_values(points=points, calculationtype=calctype,
#                             overwrite=True)
#
# # This is just a simple object to track how many total values are returned
# # across all points and calculation types which are requested.
# totalizer = type('Totalizer', (object,), {})()
#
# # Create an attribute of type int for each totalizer type
# for calctype in sample_query.calctypes:
#     setattr(totalizer, calctype, 0)
#
# # Create totalizer.total to track total values returned across all calctypes
# setattr(totalizer, 'total', 0)
# setattr(totalizer, 'tags', 0)
#
# for point in points:
#     totalizer.tags += 1
#     for calctype in sample_query.calctypes:
#
#         values = getattr(point, get_attribute(calctype))
#
#         # Counts the number of values returned for this calculation type and
#         #  adds it to the corresponding totalizer attribute
#         total = sum((getattr(totalizer, calctype), get_count(values)))
#         setattr(totalizer, calctype, total)
#
#         # this once is named and not dynamic, so we can just set the value
#         # directly and add the new values to the existing attribute value
#         totalizer.total += get_count(values)
#
#         msg_header = '{} {} value(s) were returned for {}'
#         print(msg_header.format(get_count(values), calctype, point.name))
#         msg_body = '{} {} value at {}: {}'
#         if calctype == 'current' or calctype == 'end':
#             value = values
#             print(msg_body.format(point.name, value.calculationtype,
#                                   value.timestamp, value.value))
#         else:
#             for value in values:
#                 print(msg_body.format(point.name, value.calculationtype,
#                                       value.timestamp, value.value))
# msg_summary = '{} values returned - {} current, {} interpolated, {} plot, ' \
#               '{} recorded, and {} summary'
# print(msg_summary.format(totalizer.total, totalizer.current,
#                          totalizer.interpolated, totalizer.plot,
#                          totalizer.recorded, totalizer.summary))
