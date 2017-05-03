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

import requests
from requests.auth import HTTPBasicAuth
from requests_kerberos import HTTPKerberosAuth, OPTIONAL

from .point import Point
from .structures import TypedList
from .value import Value

log = logging.getLogger(__name__)


def get_credentials(authtype, username, password):
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
    # type: (str, requests.Session) -> bool

    """

    :param url: PI Web API URL to test connectivity with
    :param session: Requests session object
    :return: Boolean to indicate connectivity state
    """
    log.debug('Testing connection to PI Web PIWebAPI...')
    r = session.get(url)
    if r.status_code == requests.codes.ok:
        log.debug('PI Web PIWebAPI connection OK, returning True')
        return True
    log.debug('PI Web PIWebAPI connection error, Returning False')
    r.raise_for_status()
    return False

def get_endpoint(url, point, calculationtype):
    # type: (str, Point, str) -> TypedList[Point]
    """

    :type url: str
    :param url: 
    :param point: 
    :param calculationtype: 
    :return: 
    """
    endpoints = {'current': 'value', 'interpolated': 'interpolated',
                 'recorded': 'recorded', 'plot': 'plot', 'summary': 'summary',
                 'end': 'end', }

    return '{}/streams/{}/{}'.format(url, point.webid,
                                     endpoints.get(calculationtype))


def get_attribute(calculationtype):
    attributes = dict(current='current_value',
                      interpolated='interpolated_values',
                      recorded='recorded_values', plot='plot_values',
                      summary='summary_values', end='end_value')

    return attributes.get(calculationtype)


def get_count(obj):
    # type: (any) -> int
    """

    :param obj: 
    :return: int
    """
    try:
        return obj.__len__().__str__()
    except TypeError:
        return 1 if obj is not None else 0


def get_point_values(point, calculationtype, data):
    # type: (Point, str, str) -> TypedList[Point]
    """

    :param point: 
    :param calculationtype: 
    :param data: 
    :return: 
    """
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
            value.timestamp = item['Timestamp']
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
        value.timestamp = data['Timestamp']
        value.value = data['Value']
        value.unitsabbreviation = data['UnitsAbbreviation']
        value.good = data['Good']
        value.questionable = data['Questionable']
        value.substituted = data['Substituted']
        values.append(value)

    log.debug('Value instantiation success - %s %s value(s) were '
              'instantiated for %s!', values.__len__().__str__(),
              calculationtype, point.name)
    return values
