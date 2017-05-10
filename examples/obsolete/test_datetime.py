# -*- coding: utf-8 -*-

from __future__ import print_function

import datetime
import json
import logging

import arrow
import colorlog

# Configure logging
loglevel = logging.DEBUG
logformat = '%(log_color)s%(asctime)s [%(filename)s:%(lineno)s - %(' \
            'funcName)5s() ] ' \
            '%(' \
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

log = colorlog.getLogger(__name__)
log.setLevel(loglevel)
log.addHandler(handler)

log.debug('Debug level test message')
log.info('Info level test message')
log.warning('Warning level test message')
log.error('Error level test message')
log.critical('Critical level test message')

response = '{ "Timestamp": "2017-05-02T19:58:23Z", "Value": 74.3863754, "UnitsAbbreviation": "", "Good": true, "Questionable": false, "Substituted": false }'

data = json.loads(response)

human_datetime_format = 'YYYY-MM-DD HH:mm:ss ZZ'
iso8601_datetime_format = 'YYYY-MM-DDTHH:mm:ss.SSSSSSSZ'

log.debug('PI:                        {}'.format(data['Timestamp']))
log.debug('Arrow:                     {}'.format(arrow.get(data['Timestamp']).datetime))
log.debug('Arrow => format(iso):      {}'.format(arrow.get(arrow.get(data['Timestamp']).datetime).format(iso8601_datetime_format)))
log.debug('Arrow => isoformat():      {}'.format(arrow.get(arrow.get(data['Timestamp']).datetime).isoformat()))
log.debug('Arrow => format(friendly): {}'.format(arrow.get(data['Timestamp']).format(human_datetime_format)))
log.debug('Arrow => str2time:         {}'.format(arrow.get(data['Timestamp']).datetime.strftime('%Y-%m-%dT%H:%M:%SZ'),))
log.debug('Arrow friendly: {}'.format(arrow.get(data['Timestamp']).format(human_datetime_format)))
log.debug('From PI: {}'.format(data['Timestamp']))
log.debug('From PI: {}'.format(data['Timestamp']))
log.debug(response)


now = datetime.datetime.utcnow()
now2 = now + datetime.timedelta(seconds=900)
log.debug(now.strftime('%Y-%m-%dT%H:%M:%SZ'))
log.debug(now2.strftime('%Y-%m-%dT%H:%M:%SZ')
          )
