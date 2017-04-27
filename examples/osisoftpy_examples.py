from osisoftpy.api import API

dev = 'https://api.osisoft.dstcontrols.local/piwebapi/'
prod = 'https://dev.dstcontrols.com/piwebapi/'
eecs = 'https://sbb03.eecs.berkeley.edu/piwebapi/'

# kerberos authentication example:
# api = API(url=prod, verifyssl=True, authtype='kerberos')

# basic authentication example:
api = API(url=eecs, verifyssl=True, authtype='basic', username='albertxu',
          password='Welcome2pi')

da_server = api.get_data_archive_server('sbb03.eecs.berkeley.edu')

query = 'name:sinusoid or name:cdt158'
query = '*'
# query = 'name:sinusoid'

points = api.get_points(query=query, count=8,
                        scope='pi:{}'.format(da_server.name))

points_with_current_value = api.get_values(points=points,
                                           calculationtype='current')

for point in points_with_current_value:
    message = 'The current value for {} is {} as of {}'
    print(message.format(point.name, point.current_value.value,
                         point.current_value.timestamp))
