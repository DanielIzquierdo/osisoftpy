from PI._piBase import _piBase
from PI._piServer import _piServer

class PIClient(_piBase):
    def __init__(self, piWebApiDomain, userName='', password='', authenticationType='kerberos',verifySSL=True):
        super(PIClient,self).__init__(piWebApiDomain, userName, password, authenticationType,verifySSL)

    def PIServers(self):
        r = super(PIClient,self).Request('dataservers')

        results = []
        for item in r['Items']:
            results.insert(-1,_piServer(super(PIClient,self).Host(), super(PIClient,self).Session(),item['WebId']))

        return results
