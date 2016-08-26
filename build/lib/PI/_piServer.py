from PI._piBase import _piBase
from PI._piPoint import _piPoint

class _piServer(_piBase):
    def __init__(self, piWebApiDomain, session, webId):
        super(_piServer,self)._session(session)
        self._webId = webId
        self._piWebApiDomain = piWebApiDomain
        self._fetchServerInfo()

    def _fetchServerInfo(self):
        r = super(_piServer,self).Request('dataservers/' + self._webId)
        self._name = r['Name']
        self._serverVersion = r['ServerVersion']
        self._id = r['Id']
        self._isConnected = r['IsConnected']

    def FindPIPoints(self, nameQuery='*', startIndex=0, maxCount=100):
        queryParamaterString = super(_piServer,self)._buildQueryParamaterString([('nameFilter',nameQuery),('startIndex',startIndex),('maxCount',maxCount)])
        r = super(_piServer,self).Request('dataservers/' + self._webId + '/points' + queryParamaterString)

        if not r['Items'] or len(r['Items']) == 0:
            return []

        results = []

        for tag in r['Items']:
            results.insert(-1,_piPoint(super(_piServer,self).Host(), super(_piServer,self).Session(),tag['WebId']))

        return results

    def FindPIPoint(self, nameQuery='*'):
        points = self.FindPIPoints(nameQuery,0,1)
        if not points or len(points) == 0:
            return None

        return self.FindPIPoints(nameQuery,0,1)[0]

    def CurrentValues(self,tags):
        # sanitize tags
        sanitizedTags = tags
        # execute
        r = super(_piServer,self).Post('batch', self._buildBulkPayload(sanitizedTags, None,'value'))
        # unpack
        results = {}
        for i in range(0,len(sanitizedTags)):
            value = r[str(i)]['Content']

            if str(value['Timestamp']) in results:
                results[str(value['Timestamp'])][sanitizedTags[i].Name()] = value['Value']
            else:
                results[str(value['Timestamp'])] = {sanitizedTags[i].Name():value['Value']}

        return results

    def RecordedValues(self, tags, start = "*-1d",end = "*", boundary = "Inside", maxCount = 1000):
        # sanitize tags
        sanitizedTags = tags
        # execute
        return self._unpackArray(sanitizedTags, super(_piServer,self).Post('batch', self._buildBulkPayload(sanitizedTags, [
            ('startTime',start),
            ('endTime',end),
            ('boundaryType',boundary),
            ('maxCount',maxCount)
        ],'recorded')))

    def InterpolatedValues(self, tags, start = "*-1d",end = "*", interval = "1h"):
        # sanitize tags
        sanitizedTags = tags
        # execute
        return self._unpackArray(sanitizedTags, super(_piServer,self).Post('batch', self._buildBulkPayload(sanitizedTags, [
            ('startTime',start),
            ('endTime',end),
            ('interval',interval)
        ],'interpolated')))

    def _buildBulkPayload(self, tags, queryParams, extension):
        payload = {}
        queryParams = super(_piServer,self)._buildQueryParamaterString(queryParams)

        for item in range(0,len(tags)):
            payload[item] = {
                "Method": "GET",
                "Resource": super(_piServer,self).RequestUrl('streams/' + tags[item].WebId() + '/' + extension + queryParams)
            }

        return payload

    def _unpackArray(self,tags,content):

        results = {}
        for i in range(0,len(tags)):
            for j in content[str(i)]['Content']['Items']:
                if str(j['Timestamp']) in results:
                    results[str(j['Timestamp'])][tags[i].Name()] = j['Value']
                else:
                    results[str(j['Timestamp'])] = {tags[i].Name(): j['Value']}

        return results

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
