# -*- coding: utf-8 -*-

#    Copyright 2017 DST Controls
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.
"""
osisoftpy.base
~~~~~~~~~~~~
This module contains the Base class from which the interesting osisoftpy 
classes are derived, such as the WebAPI, DataArchive, AssetFramework, Point, 
and Value classes.
"""

from __future__ import print_function
from __future__ import unicode_literals

import logging

log = logging.getLogger(__name__)


class Base(object):
    """
        This is the Base osisoftpy object which other objects inherit from.
    """

    valid_attr = set()

    def __init__(self, **kwargs):
        keys = self.keys()
        self.__dict__.update((k, False) for k in keys)
        self.__dict__.update((k, v) for k, v in kwargs.items() if k in keys)

    def __len__(self):
        # type: () -> int
        """

        :return: Number of items in this object. Returns 1 for objects.
        """
        return 1

    @classmethod
    def keys(cls):
        return cls.valid_attr
