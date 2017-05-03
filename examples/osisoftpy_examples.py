

# -*- coding: utf-8 -*-

from osisoftpy.piwebapi import PIWebAPI

dev = 'https://api.osisoft.dstcontrols.local/piwebapi/'
prod = 'https://dev.dstcontrols.com/piwebapi/'
eecs = 'https://sbb03.eecs.berkeley.edu/piwebapi/'

sample_query = type('Query', (object,), {})()

sample_query.single_tag = 'name:sinusoid'
sample_query.multi_tag = 'name:sinusoid or name:cdt158 or name:cd*'
sample_query.partial_tag = 'name:sinusoid*'
sample_query.wildcard = '*SPF_environment_sensor*'

# Basic authentication example:
api = PIWebAPI(url=eecs, verifyssl=True, authtype='basic', username='albertxu',
               password='Welcome2pi')

pi_server = api.get_data_archive_server('sbb03.eecs.berkeley.edu')

points = api.get_points(query=sample_query.single_tag, count=10,
                        scope='pi:{}'.format(pi_server.name))

points = api.get_values(points=points, calculationtype='current',
                        overwrite=True, )

points = api.get_values(points=points, calculationtype='recorded',
                        overwrite=True, )

for point in points:
    print('1 current value was returned for {}'.format(point.name))
    print('{} value at {}: {}'.format(point.name,
                                       point.current_value.timestamp,
                                      point.current_value.value))



    print('{} {} value(s) were returned for {}'.format(
        point.recorded_values.__len__().__str__(),
                                                       point.recorded_values[0].calculationtype, point.name))
    for value in point.recorded_values:
        print('{} value at {}: {}'.format(point.name, value.timestamp,
                                          value.value))
    # print(point.current_value.value)

    # kerberos authentication example:
    # api = PIWebAPI(url=prod, verifyssl=True, authtype='kerberos')
    # api = PIWebAPI(url=prod, verifyssl=False)
    #
    # points_with_current_value = api.get_values(points=points,
    #                                            calculationtype='current')
    # api = PIWebAPI(url=eecs, verifyssl=True, authtype='basic',
    # username='albertxu', password='Welcome2pi')
    #
    # points = api.get_points(query=query.wildcard, count=100,
    #                         scope='pi:{}'.format(da_server.name))
    #
    # points_with_current_value = api.get_values(points=points,
    #                                            calculationtype='current')
    #
    # for point in points_with_current_value:
    #     msg = 'The current value for {} is {} as of {}'
    #     print(msg.format(point.name, point.current_value.value,
    #                          point.current_value.timestamp))
    #
