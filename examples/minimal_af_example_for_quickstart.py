# Import library
import osisoftpy

# Authenticate
webapi = osisoftpy.webapi('https://dev.dstcontrols.com/piwebapi/')

# Get AF elements
afelements = webapi.elements(query='name:Attributes')
for element in afelements:
    print('Element Name: {0}'.format(element.name))
    afattributesdict = element.attributes
    for attribute_key in afattributesdict:
        valueobj = element[attribute_key].current()
        print('Attribute Name: {0} | Attribute Value: {1}'.format(attribute_key, valueobj.value))

# Get AF servers
servers = webapi.assetservers
for server in servers:
    print('AF Server Name: {0}'.format(server.name))
    if (server.name == 'GOLD'):
        server_to_use = server

# Get AF databases
databases = server_to_use.get_databases()
for database in databases:
    print('Database Name: {0}'.format(database.name))