# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from __future__ import print_function

import collections


class Collection(collections.MutableSequence):
    def __init__(self, validtypes, *args):
        # type: (object, object) -> None
        """

        :param validtypes: Provide a type for this collection object
        :param args: 
        """
        self.validtypes = validtypes
        self.list = list()
        self.extend(list(args))

    def check(self, v):
        if not isinstance(v, self.validtypes):
            raise TypeError(v)

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
