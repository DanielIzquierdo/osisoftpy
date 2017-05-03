# -*- coding: utf-8 -*-

from osisoftpy.piwebapi import PIWebAPI
from osisoftpy.utils import get_attribute, get_count

dev = 'https://api.osisoft.dstcontrols.local/piwebapi/'
prod = 'https://dev.dstcontrols.com/piwebapi/'
eecs = 'https://sbb03.eecs.berkeley.edu/piwebapi/'

sample_query = type('Query', (object,), {})()

sample_query.single_tag = 'name:sinusoid'
sample_query.multi_tag = 'name:sinusoid or name:cdt158 or name:cd*'
sample_query.partial_tag = 'name:sinusoid*'
sample_query.wildcard = '*SPF_environment_sensor*'
sample_query.calctypes = ['current', 'interpolated', 'recorded', 'plot', 'summary']

# Basic authentication example:
api = PIWebAPI(url=eecs, verifyssl=True, authtype='basic', username='albertxu',
               password='Welcome2pi')

pi_server = api.get_data_archive_server('sbb03.eecs.berkeley.edu')

points = api.get_points(query=sample_query.single_tag, count=10,
                        scope='pi:{}'.format(pi_server.name))

for calctype in sample_query.calctypes:
    points = api.get_values(points=points, calculationtype=calctype,
                            overwrite=True)

for point in points:
    for calctype in sample_query.calctypes:
        msg = '{} {} value(s) were returned for {}'
        print(msg.format(get_count(getattr(point, get_attribute(calctype))),
                         calctype, point.name))
        msg = '{} {} value at {}: {}'
        if calctype == 'current' or calctype == 'end':
            print(msg.format(point.name,
                             getattr(point, get_attribute(
                                 calctype)).calculationtype,
                             getattr(point, get_attribute(calctype)).timestamp,
                             getattr(point, get_attribute(calctype)).value))
        else:
            for value in getattr(point, get_attribute(calctype)):
                print(msg.format(point.name, value.calculationtype,
                                 value.timestamp, value.value))