
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

from osisoftpy.piwebapi import PIWebAPI
from osisoftpy.piserver import PIServer, PIServers



requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

dev = 'https://api.osisoft.dstcontrols.local/piwebapi/'
prod = 'https://dev.dstcontrols.com/piwebapi/'

# kerberos authentication example:
api = PIWebAPI(url=dev, verifyssl=False, authtype='kerberos')

# basic authentication example:
#api = PIWebAPI(url=dev, verifyssl=False, authtype='basic', username=None,
# password=None)

# print(api)
#
# print (api.url)
#
# print(api.get_piservers())


# api.test_connection()

# bannoffee = DataArchiveServer('Bannoffee')
# print(bannoffee)
# print(bannoffee.name)


# help(pi_servers)


pi_server = api.get_pi_server('megatron.dstcontrols.local')

pi_servers = api.get_pi_servers()

if pi_servers.__len__() > 0:

    print('There are ' + pi_servers.__len__().__str__() + ' PI servers:')

    for pi_server in pi_servers:
        print('Server: {0}, WebID: {1}'.format(pi_server.name, pi_server.webid))

pi_points = api.get_pi_points('name:sinusoid or name:cdt158', count=5)

print(pi_points)

# # print api.getDataArchiveServer('dev.dstcontrols.com')
# print "{0} {1}".format('hello', 'world!')
#
# dir('a string')
#
#
# class Animal(object):
#     """Animal class has a docstring, here!"""
#
#     def __init__(self, name):
#         self.name = name
#
#     def talk(self):
#         """Have the animal emit a sound."""
#         print '{0} makes a generic animal sound!'.format(self.name)
#
# bear = Animal('Bear')
# bear.talk()
# help(bear.talk)
