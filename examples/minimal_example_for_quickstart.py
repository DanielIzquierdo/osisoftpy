# Import library
import osisoftpy

# Authenticate
webapi = osisoftpy.webapi('https://dev.dstcontrols.com/piwebapi/')

# Get points
point_list = webapi.points(query='name:SINU*')
point_list2 = webapi.points(query='name:CDT*')
for individual_point in point_list2:
    point_list.append(individual_point)

# Read latest value
for individual_point in point_list:
    valueobj = individual_point.current()
    print('Latest value of {} is {} at time {}'.format(individual_point.name, valueobj.value, valueobj.timestamp))

servers = webapi.assetservers
for server in servers:
    print('AF Server Name: {0}'.format(server.name))
    if (server.name == 'GOLD'):
        server_to_use = server

databases = server_to_use.get_databases()
for database in databases:
    print('Database Name: {0}'.format(database.name))