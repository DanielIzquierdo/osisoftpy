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
osisoftpy.elements
~~~~~~~~~~~~
Some blah blah about what this file is for...
max values = 2147483647
"""
#Update comment block above

from __future__ import (absolute_import, division, unicode_literals)
from future.builtins import *

import collections
import logging

from osisoftpy.factory import Factory
from osisoftpy.factory import create
from osisoftpy.internal import get_batch
from osisoftpy.value import Value

log = logging.getLogger(__name__)


class Elements(collections.MutableSequence):
    def __init__(self, iterable, webapi):
        self.list = list()
        self.webapi = webapi
        self.extend(list(iterable))

    def __getitem__(self, key):
        return self.list[key]

    def __setitem__(self, key, value):
        self.list[key] = value

    def __delitem__(self, key):
        del self.list[key]

    def __len__(self):
        return len(self.list)

    def insert(self, key, value):
        self.list.insert(key, value)

    def __str__(self):
        return str(self.list)

    @property
    def session(self):
        return self.webapi.session
