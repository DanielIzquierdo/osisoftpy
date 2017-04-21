# -*- coding: utf-8 -*-
"""
osisoft_pi_webapi_python_client.Client
~~~~~~~~~~~~~~~~~~~
This module contains the Client used to access OSIsoft PI infrastructure and data
"""
from osisoftpy.base import Base
from osisoftpy.server import _server


class Client(Base):
    """A Client to interact with the PI Web API"""

    def __init__(self,
                 piWebApiDomain,
                 userName='',
                 password='',
                 authenticationType='kerberos',
                 verifySSL=False):
        super(Client, self).__init__(piWebApiDomain, userName, password,
                                     authenticationType, verifySSL)

    def PIServers(self):
        """Retrieves the servers"""
        r = super(Client, self).Request('dataservers')

        results = []
        for item in r['Items']:
            try:
                results.insert(-1,
                               _server(
                                   super(Client, self).Host(),
                                   super(Client, self).Session(),
                                   item['WebId']))
            except Exception as e:
                print
                print('Unable to retrieve server information for "' +
                      item['Name'] + '".')

        return results
