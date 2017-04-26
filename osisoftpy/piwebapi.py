# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from __future__ import print_function

import requests
from requests_kerberos import HTTPKerberosAuth, OPTIONAL

from .piserver import PIServer, PIServers


class PIWebAPI(object):
    """Provide integration with the OSIsoft PI Web API.
    
    TODO: document class methods.
    
    TODO: document class parameters.
    """

    def __init__(self, url='https://dev.dstcontrols.local/piwebapi/'):
        self._dataservers = None
        self._url = url
        self._session = requests.Session()
        self._session.auth = HTTPKerberosAuth(mutual_authentication=OPTIONAL)
        self._session.verify = False

    def test_connection(self):
        r = self._session.get(self._url)
        if r.status_code == requests.codes.ok:
            print('Connection OK')
            print(r.headers)
            print(r.json())
        elif r.status_code != requests.codes.ok:
            r.raise_for_status()

    def get_pi_servers(self):
        r = self._session.get(self._url + 'dataservers')
        if r.status_code == requests.codes.ok:
            pi_servers = PIServers(PIServer)
            data = r.json()
            for item in data['Items']:
                try:
                    pi_servers.append(PIServer(
                        name=item['Name'],
                        serverversion=item['ServerVersion'],
                        webid=item['WebId'],
                        isconnected=item['IsConnected'],
                        id=item['Id']))
                except Exception as e:
                    print('Unable to retrieve server information for "' +
                          item['Name'] + '".')

            return pi_servers
        elif r.status_code != requests.codes.ok:
            r.raise_for_status()

    def get_pi_server(self, name):
        try:
            pi_server = next((x for x in self.get_pi_servers() if x.name ==
                              name), None)
            return pi_server
        except Exception as e:
            print('Unable to retrieve server information for ' + name)

    def get_pi_points(self, query, count=10):
        payload = {'q': query, 'count': count}
        r = self._session.get(self.url + 'search/query', params=payload)
        if r.status_code == requests.codes.ok:
            data = r.json()
            if len(data['Errors']) > 0:
                for error in data['Errors']:
                    try:
                        raise ValueError('Error Getting PI points. '
                                         'ErrorCode: {0}, Source: {1}, '
                                         'Message {2}'.format(error['ErrorCode'], error['Source'], error['Message']))
                    except Exception as e:
                        print(e)
            else:
                return data
        elif r.status_code != requests.codes.ok:
            r.raise_for_status()

    # @property
    # def dataservers(self):
    #     print('Getting PIWebAPI._dataservers')
    #     return self._dataservers
    #
    # @dataservers.setter
    # def dataservers(self, dataserver):
    #     print('Setting PIWebAPI._url')
    #     self._url = url

    @property
    def url(self):
        print('Getting PIWebAPI._url')
        return self._url

    @url.setter
    def url(self, url):
        print('Setting PIWebAPI._url')
        self._url = url
