# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from __future__ import print_function

import requests
from requests_kerberos import HTTPKerberosAuth, REQUIRED, OPTIONAL

class DataServer(object):
    """The DataServer class provides methods for the available dataservers"""

    def __init__(self):


class PIWebAPI(object):
    """Provide integration with the OSIsoft PI Web API.
    
    TODO: document class methods.
    
    TODO: document class parameters.
    """

    def __init__(self, url='https://dev.dstcontrols.local/piwebapi/'):
        self._url = url
        self._session = requests.Session()
        self._session.auth = HTTPKerberosAuth(mutual_authentication=OPTIONAL)
        self._session.verify = False

        # self.test_connection()

    def test_connection(self):
        r = self._session.get(self._url)
        if r.status_code == requests.codes.ok:
            print('Connection OK')
            print(r.headers)
            print(r.json())
        elif r.status_code != requests.codes.ok:
            r.raise_for_status()

    @property
    def url(self):
        print('Getting PIWebAPI._url')
        return self._url

    @url.setter
    def url(self, url):
        print('Setting PIWebAPI._url')
        self._url = url
