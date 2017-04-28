# -*- coding: utf-8 -*-
"""
osisoft_pi_webapi_python_client.client
~~~~~~~~~~~~~~~~~~~
This module contains the client used to access OSIsoft PI infrastructure and data
"""
from osisoftpy._base import _base
from osisoftpy._server import _server


class client(_base):
    """A client to interact with the PI Web PIWebAPI"""

    def __init__(self,
                 piWebApiDomain,
                 userName='',
                 password='',
                 authenticationType='kerberos',
                 verifySSL=False):
        super(client, self).__init__(piWebApiDomain, userName, password,
                                     authenticationType, verifySSL)

    def PIServers(self):
        """Retrieves the servers"""
        r = super(client, self).Request('dataservers')

        results = []
        for item in r['Items']:
            try:
                results.insert(-1,
                               _server(
                                   super(client, self).≈(),
                                   super(client, self).Session(),
                                   item['WebId']))
            except Exception as e:
                print
                print('Unable to retrieve server information for "' +
                      item['Name'] + '".')

        return results
