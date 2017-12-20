# Import library
import osisoftpy

# Authenticate
webapi = osisoftpy.webapi('https://dev.dstcontrols.com/piwebapi/')#, authtype='basic', username='ABCDEF', password='1234567890')

# Get points
point_list = webapi.points(query='name:SINU*')
point_list2 = webapi.points(query='name:CDT*')
for individual_point in point_list2:
    point_list.append(individual_point)

# Read latest value
for i in range(1000):
    for individual_point in point_list:
        if individual_point.name.lower() == 'sinusoid':
            individual_point.webid = individual_point.webid[:-1]
        valueobj = individual_point.current(error_action='Continue')
        if hasattr(valueobj, 'value'):
            print('Latest value of {} is {} at time {}'.format(individual_point.name, valueobj.value, valueobj.timestamp))