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

import logging

__author__ = 'Andrew Pong'
__email__ = 'apong@dstcontrols.com'
__version__ = '1.2.0'


# Set default logging handler to avoid "No handler found" warnings.
try:  # Python 2.7+
    from logging import NullHandler
except ImportError:
    class NullHandler(logging.Handler):
        def emit(self, record):
            pass

# Configure logging
loglevel = logging.DEBUG
fmt = '[%(filename)s:%(lineno)s %(funcName)5s() ] %(levelname).1s %(message)s'

handler = logging.StreamHandler()
handler.setLevel(loglevel)
handler.setFormatter(logging.Formatter(fmt))

log = logging.getLogger(__name__)
log.setLevel(loglevel)
log.addHandler(handler)
log.addHandler(logging.NullHandler())

# log.debug('debug message')
# log.info('info message')
# log.warn('warn message')

from osisoftpy.api import (webapi, response)
from osisoftpy.webapi import (WebAPI)
from osisoftpy.point import (Point)
from osisoftpy.value import (Value)
