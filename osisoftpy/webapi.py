# -*- coding: utf-8 -*-

from __future__ import print_function
from __future__ import unicode_literals

import logging
from six import iteritems

import requests

from .base import Base
from .dataarchive import DataArchive
from .exceptions import OSIsoftPyException
from .factory import Factory, create_thing
from .point import Point
from .structures import TypedList
from .utils import get_attribute, get_count, get_credentials, get_endpoint, \
    get_point_values, iterfy, test_connectivity, stringify_kwargs, get_result
from .value import Value

log = logging.getLogger(__name__)


class PIWebAPI(Base):
    valid_attr = set(['links', 'session'])

    def __init__(self, **kwargs):
        keys = PIWebAPI.get_valid_attr()
        log.debug(stringify_kwargs(**kwargs))
        self.__dict__.update((k, False) for k in keys)
        self.__dict__.update((k, v) for k, v in kwargs.items() if k in keys)

    @classmethod
    def get_valid_attr(cls):
        return cls.valid_attr

    def search(self, **kwargs):
        r = get_result(self.links.get('Search'), self.session,  **kwargs)
        return r[0]

    def query(self, **kwargs):
        r = get_result(self.links.get('Search') + '/query', self.session,  **kwargs)
        return r[0]



class WebAPI(Base):
    """Provide integration with the OSIsoft PI Web API.

    """

    def __init__(self, url='https://dev.dstcontrols.local/piwebapi',
                 verifyssl=True, authtype='kerberos', username=None,
                 password=None):
        # type: (str, bool, str, str, str) -> None

        """

        :rtype: None
        """
        log.info('Instantiating the OSIsoftPy WebAPI with the following '
                 'arguments: URL: %s, VerifySSL: %s, AuthType: %s, '
                 'Username: %s', url, verifyssl, authtype, username)

        self.url = url
        self.verifyssl = verifyssl
        self.authtype = authtype

        log.debug('Creating Requests Session object. VerifySSL: %s, '
                  'AuthType: %s', self.verifyssl, self.authtype)

        self.session = requests.Session()
        self.session.verify = verifyssl
        self.session.auth = get_credentials(authtype=self.authtype,
                                            username=username,
                                            password=password)

        if test_connectivity(self.url, self.session):
            log.info('OSIsoftPy WebAPI instantiation success using %s '
                     'against %s', authtype, self.url)
            self.dataservers = TypedList(validtypes=DataArchive)
        else:
            log.error(
                'OSIsoftPy WebAPI instantiatian failed using %s against '
                '%s', authtype, self.url, exc_info=True)

    def get_data_archive_servers(self):
        # type: () -> osisoftpy.structures.TypedList[DataArchive]
        """

        :return: 
        """
        log.debug('Retrieving all PI Data Archive servers from %s', self.url)
        r = self.session.get(self.url + '/dataservers')
        if r.status_code == requests.codes.ok:
            data = r.json()
            if len(data['Items']) > 0:
                log.debug('HTTP %s - Instantiating OSIsoftPy.DataArchives()',
                          r.status_code)
                factory = Factory(DataArchive)
                servers = TypedList(validtypes=DataArchive)
                log.debug('Staging %s PI server(s) for instantiation...',
                          get_count(data['Items']))
                for i in data['Items']:
                    try:
                        log.debug('Instantiating "%s" as '
                                  'OSIsoftPy.DataArchive...', i['Name'])
                        server = factory.create(name=i['Name'],
                                                serverversion=i[
                                                    'ServerVersion'],
                                                webid=i['WebId'],
                                                isconnected=i['IsConnected'],
                                                id=i['Id'])
                        servers.append(server)
                    except OSIsoftPyException as e:
                        log.error('Unable to retrieve server info for '
                                  '"%s"', i['Name'], exc_info=True)
                log.debug('PI Data Archive server retrieval success! %s PI '
                          'server(s) were '
                          'found and instantiated.', get_count(servers))
                return servers
        r.raise_for_status()

    def get_data_archive_server(self, name):
        # type: (str) -> OSIsoftPy.DataArchive
        """

        :return: 
        :param name: 
        :return: 
        """
        log.debug('Getting PI Data Archive server named "%s" from %s', name,
                  self.url)
        try:
            pi_servers = self.get_data_archive_servers()
            log.debug('Searching for a PI Data Archive server named "%s"...',
                      name)
            pi_server = next((x for x in pi_servers if x.name == name), None)
            if pi_server:
                log.debug(
                    'Found a PI Data Archive named "%s" with WebID "%s" on '
                    '%s', pi_server.name, pi_server.webid, self.url)
                return pi_server
            else:
                log.error('No PI Data Archive named "%s" was found on %s',
                          name, self.url, exc_info=True)
        except Exception as e:
            log.error(
                'Exception while searching for a PI Data Archive named "%s" '
                'from %s', name, self.url, exc_info=True)

    def get_points(self, query, count=10, scope='*'):
        # type: (str, int, str) -> osisoftpy.structures.TypedList[Point]
        """

        :param query: 
        :param count: 
        :param scope: 
        :return: 
        """
        payload = {'q': query, 'count': count, 'scope': scope}
        log.debug(
            'Executing Query against PI Web WebAPI Indexed Search with '
            'the following parameters: Query: "%s", Count: "%s". Payload: %s',
            query, count, payload)
        r = self.session.get(self.url + '/search/query', params=payload)
        if r.status_code != requests.codes.ok:
            r.raise_for_status()
        else:
            data = r.json()
            log.debug('HTTP %s - Instantiating %s PI points', r.status_code,
                      get_count(data.get('Items', None)))
            factory = Factory(Point)
            items = list(map(lambda x: create_thing(factory, x),
                             data.get('Items', None)))
            points = TypedList(Point)
            for point in items:
                points.append(point)
            log.debug('PI Point retrieval success! %s PI '
                      'point(s) were '
                      'found and instantiated.', get_count(points))

            if len(data['Errors']) != 0:
                for error in data['Errors']:
                    try:
                        log.warning('The PI Web WebAPI returned the '
                                    'following error while instantiating '
                                    'PI points. '
                                    'ErrorCode: {0}, Source: {1}, '
                                    'Message {2}'.format(
                            error['ErrorCode'], error['Source'],
                            error['Message']))
                    except Exception as e:
                        log.error('Exception encounted while '
                                  'instantiating '
                                  'PI points!', exc_info=True)

            return points

    def get_values(self, points, calculationtype=None, starttime='*-1d',
                   endtime='*', boundary=None, boundarytype=None,
                   maxcount='1000', desiredunits=None, interval=None,
                   intervals='24', retrievalmode='Auto', summarytype='Total',
                   calculationbasis='TimeWeighted', timetype='Auto',
                   summaryduration=None, sampletype='ExpressionRecordedValues',
                   sampleinterval=None, time=None, filterexpression=None,
                   includefilteredvalues=False, sortorder='Ascending',
                   append=False, overwrite=False):
        # starttime is Time String
        # endtime is Time String
        # interval is AFTimeSpan
        # desiredUnits is a uom, cannot be specified for PI points
        # fiterexpression is filtering like * or SINU*
        # includefilteredvalues bool: Specify 'true' to indicate that values which fail the filter criteria are present in the returned data at the times where they occurred with a value set to a 'Filtered' enumeration value with bad status. Repeated consecutive failures are omitted.
        # sortorder default is 'Ascending'
        # summaryDuration The duration of each summary interval. If specified in hours, minutes, seconds, or milliseconds, the summary durations will be evenly spaced UTC time intervals. Longer interval types are interpreted using wall clock rules and are time zone dependent.
        # TODO: add starttime parameter
        # TODO: add endtime parameter
        # TODO: add boundary parameter
        # TODO: add interval parameter
        calctype = calculationtype.lower()

        is_single_value = True if calctype == 'current' or calctype == 'end' \
            else False

        log.debug('Calculation type: %s, Single value: %s', calctype,
                  is_single_value)

        for point in iterfy(points):
            log.debug('Retrieving %s data for %s...', calctype, point.name)

            if calctype == 'current':
                payload = {'time': time}
            elif calctype == 'interpolated':
                payload = {'startTime': starttime, 'endTime': endtime,
                           'interval': interval,
                           'filterExpression': filterexpression,
                           'includeFilteredValues': includefilteredvalues}
            elif calctype == 'interpolatedattimes':
                payload = {'time': time, 'filterExpression': filterexpression,
                           'includeFilteredValues': includefilteredvalues,
                           'sortOrder': sortorder}
            elif calctype == 'recorded':
                payload = {'startTime': starttime, 'endTime': endtime,
                           'boundaryType': boundarytype,
                           'filterExpression': filterexpression,
                           'includeFilteredValues': includefilteredvalues,
                           'maxCount': maxcount}
            elif calctype == 'recordedattime':
                payload = {'time': time, 'retrievalMode': retrievalmode}
            elif calctype == 'plot':
                payload = {'startTime': starttime, 'endTime': endtime,
                           'intervals': intervals}
            elif calctype == 'summary':
                payload = {'startTime': starttime, 'endTime': endtime,
                           'summaryType': summarytype,
                           'calculationBasis': calculationbasis,
                           'timeType': timetype,
                           'summaryDuration': summaryduration,
                           'sampleType': sampletype,
                           'sampleInterval': sampleinterval,
                           'filterExpression': filterexpression}
            elif calctype == 'end':
                payload = {}
            else:
                log.debug('This %s request has no URL parameters', calctype)

            endpoint = get_endpoint(self.url, point, calctype)

            # TODO: add queryParamater generator function here?
            try:
                log.debug('Instantiating %s request for PI point %s to '
                          'endpoint %s with the following parameters: %s',
                          calctype, point.name, endpoint, payload)

                r = self.session.get(endpoint, params=payload)
                if r.status_code != requests.codes.ok:
                    r.raise_for_status()
            except OSIsoftPyException as e:
                log.error('Exception while retrieving recorded values'
                          'from %s for %s. Raw JSON: %s', endpoint, point.name,
                          exc_info=True)

            data = r.json()
            log.debug('HTTP %s - Instantiating OSIsoftPy.Values()',
                      r.status_code)
            log.debug('Staging PI point value for '
                      'instantiation...')
            try:
                new_values = get_point_values(point, calctype, data)
                log.debug('%s %s value(s) were instantiated for %s.',
                          get_count(new_values), calctype, point.name)
            except OSIsoftPyException as e:
                log.error('Exception while instantiating PI Point value(s)'
                          'for %s. Raw JSON: %s', point.name, data,
                          exc_info=True)
            current_values = TypedList(validtypes=Value)

            if is_single_value:
                try:
                    value = getattr(point, get_attribute(calctype))
                    log.debug('Storing %s value.', calctype)
                    current_values.append(value)
                except TypeError as e:
                    log.warning('TypeError encountered - the attribute %s is '
                                'empty for %s, which will raise an '
                                'exception when trying to iterate.',
                                get_attribute(calctype), point.name,
                                exc_info=False)
            else:
                try:
                    for value in getattr(point, get_attribute(calctype)):
                        log.debug(
                            'Storing %s value for PI point %s, attribute: %s',
                            calctype, point.name, get_attribute(calctype))
                        current_values.append(value)
                except TypeError as e:
                    log.warning('TypeError encountered - the attribute %s is '
                                'empty for %s, which will raise an '
                                'exception when trying to iterate.',
                                get_attribute(calctype), point.name,
                                exc_info=False)

            log.debug('PI point %s currently has %s %s values.', point.name,
                      get_count(current_values), calctype)

            if is_single_value and overwrite:
                log.debug('Single point value - overwriting existing %s '
                          'value, Single value: %s.', calctype,
                          is_single_value)
                setattr(point, get_attribute(calctype), new_values[0])
            elif is_single_value and append:
                log.debug('Single point value - append is true but cannot '
                          'append...overwriting existing %s '
                          'value, Single value: %s.', calctype,
                          is_single_value)
                setattr(point, get_attribute(calctype), new_values[0])
            elif not is_single_value and overwrite:
                log.debug('Multiple point values - overwriting %s existing '
                          '%s values, Single value: %s.',
                          get_count(current_values), calctype, is_single_value)
                setattr(point, get_attribute(calctype), new_values)
            elif not is_single_value and append:
                for new_value in new_values:
                    current_values.append(new_value)
                setattr(point, get_attribute(calctype), current_values)
            else:
                # TODO: allow both to be false if no data exists.
                log.error('Error saving %s new %s point value(s) for PI '
                          'point %s. Single value: %s, Overwrite: %s, Append: '
                          '%s.', get_count(new_values), calctype, point.name,
                          is_single_value, overwrite, append)
        return points
