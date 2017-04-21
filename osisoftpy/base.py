"""
osisoftpy._base
~~~~~~~~~~~~~~~~~~~
This module contains the base class for PI objects
"""

import re
import requests
import requests.auth
import requests.exceptions
import sys
from requests_kerberos import HTTPKerberosAuth, REQUIRED, OPTIONAL
from osisoftpy.exceptions import ConnectTimeout
import osisoftpy.exceptions


class Base(object):
    """The Base Pi Object"""

    def __init__(self, piWebApiDomain, userName='', password='',
                 authenticationType='kerberos', verifySSL=True):
        self._piWebApiDomain = self.__domainNameCleanup(piWebApiDomain)
        self.__session = requests.Session()
        self.__session.auth = self.__auth(userName, password,
                                          authenticationType)
        self.__session.verify = verifySSL
        self.__testConnection()

    def Session(self):
        """Retrieves the Requests.Session Client"""
        return self.__session

    def _session(self, session):
        """allows derived classes to set the Requests.Session Client"""
        self.__session = session

    def Host(self):
        """Returns the host name"""
        return (self._piWebApiDomain)

    def __testConnection(self):
        """tests connectivity to the piwebapi"""
        try:
            r = self.__session.get(self._piWebApiDomain + '/piwebapi',
                                   timeout=3)
        except requests.exceptions.RequestException as e:
            # if r.status_code != 200:
            print e
            sys.exit(1)
            # raise ValueError('Unable to connect to the PI Web API')

    def __domainNameCleanup(self, domainName):
        """cleans up the provided string"""
        return re.sub(r"\/?piwebapi.*", "", domainName)

    def __auth(self, username, password, authenticationType):
        """creates the desired authentication object"""
        if authenticationType == 'basic':
            return requests.auth.HTTPBasicAuth(username, password)
        elif authenticationType == 'kerberos':
            return HTTPKerberosAuth(mutual_authentication=OPTIONAL)
        else:
            raise ValueError('Invalid authentication type')

    def Request(self, url):
        """makes a GET request to the pi web api"""
        try:
            response = self.__session.get(
                self._piWebApiDomain + '/piwebapi/' + url)
            if not response.status_code // 100 == 2:
                return "Error: Unexpected response {}".format(response)
        except requests.exceptions.RequestException as e:
            return "Error: {}".format(e)

    def Post(self, url, payload):
        """makes a POST request to the pi web api"""
        r = self.__session.post(self._piWebApiDomain + '/piwebapi/' + url,
                                json=payload)

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
