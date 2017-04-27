# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from __future__ import print_function


class DataArchive(object):
    """The DataServer class provides methods for the available dataservers"""

    def __init__(self, name=None, serverversion=None, webid=None,
                 isconnected=False, id=None):
        # type: (string, string, string, bool, string) -> object
        """
        
        :param name: PI server name
        :type name: string
        :type serverversion: PI server version
        :type webid: PI server webid for use with the PI Web API
        :type isconnected: PI server connection status
        :type id: PI server ID

        :rtype: DataArchive object
        """
        self.name = name
        self.serverversion = serverversion
        self.webid = webid
        self.isconnected = isconnected
        self.id = id

    def __getattr__(self, key):
        try:
            return self.__dict__[key]
        except KeyError:
            msg = '"{}" object has no attribute "{}"'
            raise AttributeError(msg.format(type(self).__name__, key))

    def __setattr__(self, key, value):
        try:
            self.__dict__[key] = value
        except KeyError:
            msg = '"{}" object has no attribute "{}"'
            raise AttributeError(msg.format(type(self).__name__, key))
        except ValueError:
            msg = 'Invalid value "{}" for "{}" object attribute "{}"'
            raise AttributeError(msg.format(value, type(self).__name__, key))

