"""
OSIsoftPy._base
~~~~~~~~~~~~~~~~~~~
This module contains the base class for PI objects
"""

import re
import requests
from requests.auth import HTTPBasicAuth
from requests_kerberos import HTTPKerberosAuth, REQUIRED, OPTIONAL

class _base(object):
    """The Base Pi Object"""
    def __init__(self, piWebApiDomain, userName='', password='', authenticationType='kerberos',verifySSL=True):
        self._piWebApiDomain = self.__domainNameCleanup(piWebApiDomain)
        self.__session = requests.Session()
        self.__session.auth = self.__auth(userName, password, authenticationType)
        self.__session.verify = verifySSL;
        self.__testConnection()

    def Session(self):
        """Retrieves the Requests.Session client"""
        return self.__session;

    def _session(self,session):
        """allows derived classes to set the Requests.Session client"""
        self.__session = session;

    def Host(self):
        """Returns the host name"""
        return(self._piWebApiDomain)

    def __testConnection(self):
        """tests connectivity to the piwebapi"""
        r = self.__session.get(self._piWebApiDomain + '/piwebapi')

        if r.status_code != 200:
            raise ValueError('Unable to connect to the PI Web API')

    def __domainNameCleanup(self, domainName):
        """cleans up the provided string"""
        return re.sub(r"\/?piwebapi.*","",domainName)

    def __auth(self, username, password, authenticationType):
        """creates the desired authentication object"""
        if authenticationType == 'basic':
            return HTTPBasicAuth(username, password)
        elif authenticationType == 'kerberos':
            return HTTPKerberosAuth(mutual_authentication=OPTIONAL)
        else:
            raise ValueError('Invalid authentication type')

    def Request(self, url):
        """makes a GET request to the pi web api"""
        return self.__session.get(self._piWebApiDomain + '/piwebapi/' + url).json()

    def Post(self, url, payload):
        """makes a POST request to the pi web api"""
        r = self.__session.post(self._piWebApiDomain + '/piwebapi/' + url, json=payload)

        if r.status_code >= 300:
            return r.status_code
        try:
            return r.json()
        except Exception as e:
            return None

    def RequestUrl(self, url):
        """builds the full url for a request"""
        return self._piWebApiDomain + '/piwebapi/' + url

    def _buildQueryParamaterString(self, params):
        """helper for derived classes building query strings"""
        if not params or len(params) == 0:
            return ''

        queryString = '?'

        for item in params:
            queryString = queryString + str(item[0]) + '=' + str(item[1]) + '&'

        return queryString[0:-1]
