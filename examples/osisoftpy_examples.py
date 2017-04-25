
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

from osisoftpy.piwebapi import PIWebAPI

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

api = PIWebAPI(url='https://applepie.dstcontrols.local/piwebapi/')

print api.url

api.test_connection()


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
