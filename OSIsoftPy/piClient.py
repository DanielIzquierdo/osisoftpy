# -*- coding: utf-8 -*-

"""
PI.piClient
~~~~~~~~~~~~~~~~~~~
This module contains the piClient object used to access pi infrastructure and data
"""
from OSIsoftPy._piBase import _piBase
from OSIsoftPy._piServer import _piServer

class pi_client(_piBase):
    def __init__(self, piWebApiDomain, userName='', password='', authenticationType='kerberos',verifySSL=True):
        super(pi_client,self).__init__(piWebApiDomain, userName, password, authenticationType,verifySSL)

    def PIServers(self):
        r = super(pi_client,self).Request('dataservers')

        results = []
        for item in r['Items']:
            results.insert(-1,_piServer(super(pi_client,self).Host(), super(pi_client,self).Session(),item['WebId']))

        return results
