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

from osisoftpy.exceptions import (PIWebAPIError)
from osisoftpy.webapi import (WebAPI)
from osisoftpy.point import (Point)
from osisoftpy.value import (Value)
from osisoftpy.api import webapi

__author__ = 'Andrew Pong'
__email__ = 'apong@dstcontrols.com'
__version__ = '2.1.1'


# Configure logging

def init_log():
    format = logging.Formatter(
        '[%(filename)s:%(lineno)s %(funcName)5s() ] %(levelname).1s %(message)s')
    log_level = logging.DEBUG
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(format)
    stream_handler.setLevel(log_level)

    log = logging.getLogger(__name__)
    rklog = logging.getLogger('requests_kerberos')
    klog = logging.getLogger('requests_kerberos.kerberos_')

    log.setLevel(log_level)
    rklog.setLevel(log_level)
    klog.setLevel(log_level)

    log.addHandler(stream_handler)
    # rklog.addHandler(stream_handler)
    # klog.addHandler(stream_handler)

init_log()

