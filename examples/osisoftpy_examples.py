# -*- coding: utf-8 -*-



dev = 'https://api.osisoft.dstcontrols.local/piwebapi/'
prod = 'https://dev.dstcontrols.com/piwebapi/'
eecs = 'https://sbb03.eecs.berkeley.edu/piwebapi/'

prod_pi = 'sbb03.eecs.berkeley.edu'

# kerberos authentication example:
# api = PIWebAPI(url=prod, verifyssl=True, authtype='kerberos')
# api = PIWebAPI(url=prod, verifyssl=False)
# da_server = api.get_data_archive_server('megatron.dstcontrols.local')

# # basic authentication example:
# api = PIWebAPI(url=eecs, verifyssl=True, authtype='basic', username='albertxu',
#                password='Welcome2pi')
#
#
#
# query = type('Query', (object,), {})()
#
# query.single_tag = 'name:sinusoid'
#
# query.multi_tag = 'name:sinusoid or name:cdt158 or name:cd*'
# query.partial_tag = 'name:sinusoid*'
# query.wildcard = '*'
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

from osisoftpy.piwebapi import PIWebAPI

api = PIWebAPI(url=eecs, verifyssl=True, authtype='basic', username='albertxu',
               password='Welcome2pi')

points = api.get_points(query='*SPF_environment_sensor*', count=1000,
                        scope='pi:{}'.format(prod_pi))

for point in points:
    print(point.name)
#
# points_with_current_value = api.get_values(points=points,
#                                            calculationtype='current')