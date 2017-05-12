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
osisoftpy.__init__
~~~~~~~~~~~~

"""
from __future__ import (absolute_import, division, unicode_literals)
from future.builtins import *
import logging

__author__ = 'Andrew Pong'
__email__ = 'apong@dstcontrols.com'
__version__ = '2.0.8'

# Configure logging
fmt = '[%(filename)s:%(lineno)s %(funcName)5s() ] %(levelname).1s %(message)s'

handler = logging.StreamHandler()
handler.setLevel(logging.DEBUG)
handler.setFormatter(logging.Formatter(fmt))

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)
log.addHandler(handler)
log.addHandler(logging.NullHandler())

from osisoftpy.exceptions import (PIWebAPIError)
from osisoftpy.webapi import (WebAPI)
from osisoftpy.point import (Point)
from osisoftpy.value import (Value)
from osisoftpy.api import webapi
