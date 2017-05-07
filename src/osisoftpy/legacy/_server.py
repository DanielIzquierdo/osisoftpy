"""
osisoft_pi_webapi_python_client._server
~~~~~~~~~~~~~~~~~~~
This module contains the PI Point class
"""

from rx import Observable
from rx.core import Scheduler

from src.osisoftpy import _base, _point


class _server(_base):
    """PI Server used to query tags and execute batch queries"""

    def __init__(self, piWebApiDomain, session, webId):
        super(_server, self)._session(session)
        self._webId = webId
        self._piWebApiDomain = piWebApiDomain
        self._fetchServerInfo()
        self.__observableTags = set([])
        self.__observable = {}
        self.__previousValues = {}

    def _fetchServerInfo(self):
        """fetches server information"""
        r = super(_server, self).Request('dataservers/' + self._webId)
        self._name = r['Name']
        self._serverVersion = r['ServerVersion']
        self._id = r['Id']
        self._isConnected = r['IsConnected']

    def FindPIPoints(self, nameQuery='*', startIndex=0, maxCount=100):
        """Queries for pi points, returns list of results"""
        queryParamaterString = super(_server, self)._buildQueryParamaterString(
            [('nameFilter', nameQuery), ('startIndex', startIndex),
             ('maxCount', maxCount)])
        r = super(_server, self).Request('dataservers/' +
                                         self._webId + '/points' + queryParamaterString)

        if not r['Items'] or len(r['Items']) == 0:
            return []

        results = []

        for tag in r['Items']:
            try:
                results.insert(-1, _point(super(_server, self).Host(),
                                          super(_server, self).Session(),
                                          tag['WebId']))
            except Exception as e:
                print('Unable to retrieve PI Point information for "' +
                      item['Name'] + '".')

        return results

    def FindPIPoint(self, nameQuery='*'):
        """queries for a singel PI point"""
        points = self.FindPIPoints(nameQuery, 0, 1)
        if not points or len(points) == 0:
            return None

        return self.FindPIPoints(nameQuery, 0, 1)[0]

    def CurrentValues(self, tags):
        """Batch query for multiple tags"""
        # sanitize tags
        sanitizedTags = self._sanitizeTags(tags)
        # execute
        r = super(_server, self).Post(
            'batch', self._buildBulkPayload(sanitizedTags, None, 'value'))
        # unpack
        results = {}
        for i in range(0, len(sanitizedTags)):
            value = r[str(i)]['Content']

            if str(value['Timestamp']) in results:
                results[str(value['Timestamp'])
                ][sanitizedTags[i].Name()] = value['Value']
            else:
                results[str(value['Timestamp'])] = {
                    sanitizedTags[i].Name(): value['Value']}

        return results

    def RecordedValues(self, tags, start="*-1d", end="*", boundary="Inside",
                       maxCount=1000):
        """Batch query for multiple tags"""
        # sanitize tags
        sanitizedTags = self._sanitizeTags(tags)
        # execute
        return self._unpackArray(sanitizedTags,
                                 super(_server, self).Post('batch',
                                                           self._buildBulkPayload(
                                                               sanitizedTags, [
                                                                   (
                                                                   'startTime',
                                                                   start),
                                                                   ('endTime',
                                                                    end),
                                                                   (
                                                                   'boundaryType',
                                                                   boundary),
                                                                   ('maxCount',
                                                                    maxCount)
                                                               ], 'recorded')))

    def InterpolatedValues(self, tags, start="*-1d", end="*", interval="1h"):
        """Batch query for multiple tags"""
        # sanitize tags
        sanitizedTags = self._sanitizeTags(tags)
        # execute
        return self._unpackArray(sanitizedTags,
                                 super(_server, self).Post('batch',
                                                           self._buildBulkPayload(
                                                               sanitizedTags, [
                                                                   (
                                                                   'startTime',
                                                                   start),
                                                                   ('endTime',
                                                                    end),
                                                                   ('interval',
                                                                    interval)
                                                               ],
                                                               'interpolated')))

    def UpdateValues(self, data, updateOption="Insert",
                     bufferOption="BufferIfPossible"):
        """Update multiple tags"""
        sanitizedData = self._processData(data)

        for rawTag in sanitizedData.keys():
            sanitizedTag = self._sanitizeTags([rawTag])[0]
            if sanitizedTag:
                sanitizedData[rawTag].sort(
                    key=lambda tag: tag.get('Timestamp'))
                sanitizedTag.UpdateValues(
                    sanitizedData[rawTag], updateOption, bufferOption)

    def _sanitizeTags(self, rawTags):
        tags = []

        for tag in rawTags:
            if type(tag) is _point:
                tags.insert(-1, tag)
            elif type(tag) is str:
                tags.insert(-1, self.FindPIPoint(tag))
            else:
                raise ValueError('Unable to webapi to the PI Web WebAPI')

        return tags

    def _buildBulkPayload(self, tags, queryParams, extension):
        payload = {}
        queryParams = super(
            _server, self)._buildQueryParamaterString(queryParams)

        for item in range(0, len(tags)):
            payload[item] = {
                "Method": "GET",
                "Resource": super(_server, self).RequestUrl('streams/' + tags[
                    item].WebId() + '/' + extension + queryParams)
            }

        return payload

    def _unpackArray(self, tags, content):

        results = {}
        for i in range(0, len(tags)):
            for j in content[str(i)]['Content']['Items']:
                if str(j['Timestamp']) in results:
                    results[str(j['Timestamp'])][tags[i].Name()] = j['Value']
                else:
                    results[str(j['Timestamp'])] = {tags[i].Name(): j['Value']}

        return results

    def _processData(self, data):
        processed = {}

        for timeKey in data.keys():
            for tagKey in data[timeKey].keys():
                if tagKey not in processed:
                    processed[tagKey] = []

                processed[tagKey].append(
                    {'Timestamp': timeKey, 'Value': data[timeKey][tagKey],
                     'Questionable': 'false', 'Good': 'true'})

        return processed

    def Name(self):
        return self._name

    def ServerVersion(self):
        return self._serverVersion

    def WebId(self):
        return self._webId

    def Id(self):
        return self._id

    def IsConnected(self):
        return self._isConnected

    # DATA PIPE MADNESS

    def Observable(self, tags):
        sanitizedTags = self._sanitizeTags(tags)
        """returns an observable object"""
        return Observable.timer(1000, 1000, Scheduler.timeout).map(
            lambda second: sanitizedTags) \
            .map(lambda tagList: self.CurrentValues(list(tagList))) \
            .map(lambda qResult: self._checkAgainstPrevious(qResult)).filter(
            lambda y: y is not None).publish()

    def _checkAgainstPrevious(self, dictionary):
        result = {}

        for timeKey in dictionary.keys():
            for tagKey in dictionary[timeKey].keys():
                if tagKey in self.__previousValues.keys():
                    if self.__previousValues[tagKey] < timeKey:
                        if timeKey not in result.keys():
                            result[timeKey] = {}
                        result[timeKey][tagKey] = dictionary[timeKey][tagKey]
                        self.__previousValues[tagKey] = timeKey
                else:
                    if timeKey not in result.keys():
                        result[timeKey] = {}
                    result[timeKey][tagKey] = dictionary[timeKey][tagKey]
                    self.__previousValues[tagKey] = timeKey

        if len(result) == 0:
            return None
        else:
            return result
