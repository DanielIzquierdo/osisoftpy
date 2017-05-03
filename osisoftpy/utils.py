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

from .structures import TypedList
from .point import Point
from .value import Value

log = logging.getLogger(__name__)


def get_endpoint(url, point, calculationtype):
    # type: (str, Point, str) -> TypedList[Point]
    """

    :param url: 
    :param point: 
    :param calculationtype: 
    :return: 
    """
    endpoints = {'current': 'value', 'interpolated': 'interpolated',
                 'recorded': 'recorded', 'plot': None, 'summary': None,
                 'end': None, }

    return '{}/streams/{}/{}'.format(url, point.webid,
                                     endpoints.get(calculationtype))


def get_attribute(calculationtype):
    attributes = dict(current='current_value',
                         interpolated='interpolated_values',
                         recorded='recorded_values', plot='plot_values',
                         summary='summary_values', end='end_value')

    return attributes.get(calculationtype)


def get_point_values(point, calculationtype, data):
    # type: (Point, str, str) -> TypedList[Point]
    """

    :param point: 
    :param calculationtype: 
    :param data: 
    :return: 
    """
    # log.debug('Arguments: %s, %s, %s', point, calculationtype, data)
    values = TypedList(Value)
    if 'Items' in data:
        log.debug('Instantiating multiple values for PI point %s...',
                  point.name)
        for item in data['Items']:
            value = Value()
            value.calculationtype = calculationtype
            value.datatype = point.datatype
            value.timestamp = item['Timestamp']
            value.value = item['Value']
            value.unitsabbreviation = item['UnitsAbbreviation']
            value.good = item['Good']
            value.questionable = item['Questionable']
            value.substituted = item['Substituted']
            values.append(value)
    else:
        log.debug('Instantiating single value from %s for %s...', data['Timestamp'], point.name)
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
              'instantiated for %s!',
              values.__len__().__str__(), calculationtype, point.name)
    return values
