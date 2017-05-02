# -*- coding: utf-8 -*-

import logging

import colorlog

# Set default logging handler to avoid "No handler found" warnings.
try:  # Python 2.7+
    from logging import NullHandler
except ImportError:
    class NullHandler(logging.Handler):
        def emit(self, record):
            pass

# Configure logging
loglevel = logging.DEBUG
logformat = '%(log_color)s[%(filename)s:%(lineno)s - %(funcName)5s() ] %(' \
            'levelname).1s %(message_log_color)s%(message)s'
logcolors = {'DEBUG': 'cyan', 'INFO': 'green', 'WARNING': 'yellow',
             'ERROR': 'red', 'CRITICAL': 'red,bg_white'}
logmessagecolors = {
    'message': {'DEBUG': 'white', 'INFO': 'white', 'WARNING': 'yellow',
                'ERROR': 'red', 'CRITICAL': 'red'}}

formatter = colorlog.ColoredFormatter(logformat, datefmt=None, reset=True,
                                      log_colors=logcolors,
                                      secondary_log_colors=logmessagecolors,
                                      style='%')

handler = colorlog.StreamHandler()
handler.setLevel(loglevel)
handler.setFormatter(formatter)

logger = colorlog.getLogger(__name__)
logger.setLevel(loglevel)
logger.addHandler(handler)
logger.addHandler(NullHandler())

# logger.debug('debug message')
# logger.info('info message')
# logger.warn('warn message')
