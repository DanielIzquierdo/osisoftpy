# -*- coding: utf-8 -*-

"""
osisoftpy.utils
~~~~~~~~~~~~~~
This module provides utility functions that are used within OSIsoftPy
that are also useful for external consumption.
"""

from __future__ import print_function
from __future__ import unicode_literals

import logging
import re

import arrow
import requests
import requests_kerberos
from six import string_types

from osisoftpy.point import Point
from osisoftpy.structures import TypedList
from osisoftpy.value import Value

log = logging.getLogger(__name__)


def _get_auth(authtype, username=None, password=None):
    if authtype == 'kerberos':
        return requests_kerberos.HTTPKerberosAuth(
            mutual_authentication=requests_kerberos.OPTIONAL)
    else:
        return requests.auth.HTTPBasicAuth(username, password)


def stringify(**kwargs):
    """
    Return a concatenated string of the keys and values of the kwargs
    Source: http://stackoverflow.com/a/39623935
    :param kwargs: kwargs to be combined into a single string
    :return: String representation of the kwargs
    """
    return (','.join('{0}={1!r}'.format(k, v) for k, v in kwargs.items()))


def get_credentials(authtype, username, password):
    # type: (str, str, str) -> requests.auth.HTTPBasicAuth
    """

    :param authtype: 
    :param username: 
    :param password: 
    :return: 
    """
    log.debug('Creating %s authentication object for Requests...', authtype)
    if authtype.lower() == 'basic':
        return HTTPBasicAuth(username, password)
    elif authtype.lower() == 'kerberos':
        return HTTPKerberosAuth(mutual_authentication=OPTIONAL)
    else:
        raise TypeError('Error: {0} is an invalid authentication type. '
                        'Valid options are Basic and Kerberos.')


def test_connectivity(url, session):
    # type: (string_types, requests.Session) -> bool

    """

    :param url: PI Web API URL to test connectivity with
    :param session: Requests session object
    :return: Boolean to indicate connectivity state
    """
    log.debug('Testing connection to PI Web WebAPI...')
    r = session.get(url)
    if r.status_code == requests.codes.ok:
        log.debug('PI Web WebAPI connection OK, returning True')
        return True
    log.debug('PI Web WebAPI connection error, Returning False')
    r.raise_for_status()
    return False


def get_endpoint(url, point, calculationtype):
    # type: (string_types, Point, string_types) -> string_types
    """

    :type url: str
    :param url: 
    :param point: 
    :param calculationtype: 
    :return: URL
    """
    endpoints = {'current': 'value', 'interpolated': 'interpolated',
                 'interpolatedattimes': 'interpolatedattimes',
                 'recorded': 'recorded', 'recordedattime': 'recordedattime',
                 'plot': 'plot', 'summary': 'summary', 'end': 'end', }
    return '{}/streams/{}/{}'.format(url, point.webid,
                                     endpoints.get(calculationtype))


def get_attribute(calculationtype):
    # type: (str) -> str
    """

    :param calculationtype: 
    :return: 
    """
    attributes = dict(current='current_value',
                      interpolated='interpolated_values',
                      interpolatedattimes='interpolated_values',
                      recorded='recorded_values',
                      recordedattime='recorded_values', plot='plot_values',
                      summary='summary_values', end='end_value')

    return attributes.get(calculationtype)


def get_count(obj):
    # type: (any) -> int
    """

    :param obj: 
    :return: int
    """
    try:
        return obj.__len__()
    except TypeError:
        return 1 if obj is not None else 0


def iterfy(iterable):
    # type: (any) -> list
    """

    :param iterable: 
    :return: 
    """
    if isinstance(iterable, string_types):
        iterable = [iterable]
    try:
        iter(iterable)
    except TypeError:
        iterable = [iterable]
    return iterable


def get_point_values(point, calculationtype, data):
    # type: (Point, str, str) -> TypedList[Point]
    """

    :param point: 
    :param calculationtype: 
    :param data: 
    :return: 
    """
    calculationtype = re.sub('attimes?$', '', calculationtype)

    values = TypedList(Value)
    if 'Items' in data:
        log.debug('Instantiating multiple values for PI point %s...',
                  point.name)
        for item in data['Items']:
            value = Value()
            value.calculationtype = calculationtype
            value.datatype = point.datatype
            if 'Type' in item and 'Value' in item:
                item = item['Value']
            value.timestamp = arrow.get(item['Timestamp']).datetime
            value.value = item['Value']
            value.unitsabbreviation = item['UnitsAbbreviation']
            value.good = item['Good']
            value.questionable = item['Questionable']
            value.substituted = item['Substituted']
            values.append(value)

    else:
        log.debug('Instantiating single value from %s for %s...',
                  data['Timestamp'], point.name)
        value = Value()
        value.calculationtype = calculationtype
        value.datatype = point.datatype
        value.timestamp = arrow.get(data['Timestamp']).datetime
        value.value = data['Value']
        value.unitsabbreviation = data['UnitsAbbreviation']
        value.good = data['Good']
        value.questionable = data['Questionable']
        value.substituted = data['Substituted']
        values.append(value)

    log.debug('Value instantiation success - %s %s value(s) were '
              'instantiated for %s!', get_count(values), calculationtype,
              point.name)
    return values
