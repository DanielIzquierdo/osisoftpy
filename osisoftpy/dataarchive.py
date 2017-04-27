# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from __future__ import print_function

import collections


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
        self._name = name
        self._serverversion = serverversion
        self._webid = webid
        self._isconnected = isconnected
        self._id = id

    @property
    def name(self): return self._name

    @property
    def serverversion(self): return self._serverversion

    @property
    def webid(self): return self._webid

    @property
    def isconnected(self): return self._isconnected

    @property
    def id(self): return self._id

class DataArchives(collections.MutableSequence):
    def __init__(self, types, *args):
        self.types = types
        self.list = list()
        self.extend(list(args))

    def check(self, v):
        if not isinstance(v, self.types):
            raise TypeError, v

    def __len__(self): return len(self.list)

    def __getitem__(self, i): return self.list[i]

    def __delitem__(self, i): del self.list[i]

    def __setitem__(self, i, v):
        self.check(v)
        self.list[i] = v

    def insert(self, i, v):
        self.check(v)
        self.list.insert(i, v)

    def __str__(self):
        return str(self.list)

