# -*- coding: utf-8 -*-

import logging

# Set default logging handler to avoid "No handler found" warnings.
try:  # Python 2.7+
    from logging import NullHandler
except ImportError:
    class NullHandler(logging.Handler):
        def emit(self, record):
            pass

loglevel = logging.DEBUG
logformat = '[%(filename)s:%(lineno)s - %(funcName)20s() ] %(levelname).1s %(message)s'

# Configure logging
log = logging.getLogger(__name__)


handler = logging.StreamHandler()
handler.setLevel(loglevel)
handler.setFormatter(logging.Formatter(logformat))

log.setLevel(loglevel)
log.addHandler(handler)
log.addHandler(NullHandler())

# log.debug('debug message')
# log.info('info message')
# log.warn('warn message')

