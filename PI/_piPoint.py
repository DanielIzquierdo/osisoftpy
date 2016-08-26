from PI._piBase import _piBase

class _piPoint(_piBase):
    def __init__(self, piWebApiDomain, session, webId):
        super(_piPoint,self)._session(session)
        self._webId = webId
        self._piWebApiDomain = piWebApiDomain
        self._fetchTagInfo()

    def _fetchTagInfo(self):
        r = super(_piPoint,self).Request('points/' + self._webId)
        self._name = r['Name']
        self._id = r['Id']
        self._future = r['Future']
        self._pointClass = r['PointClass']
        self._pointType = r['PointType']

    def Name(self):
        return self._name

    def WebId(self):
        return self._webId

    def Id(self):
        return self._id

    def PointClass(self):
        return self._pointClass

    def Future(self):
        return self._future

    def PointType(self):
        return self._pointType

    def CurrentValue(self):
        return self._dataPointUnpacker(super(_piPoint,self).Request('streams/' + self._webId + '/value'))

    def RecordedValues(self, start = "*-1d",end = "*", boundary = "Inside", maxCount = 1000):
        queryParamaterString = super(_piPoint,self)._buildQueryParamaterString([
            ('startTime',start),
            ('endTime',end),
            ('boundaryType',boundary),
            ('maxCount',maxCount)
        ])

        r = super(_piPoint,self).Request('streams/' + self._webId + '/recorded' + queryParamaterString)
        result = {}
        for item in r['Items']:
            result.update(self._dataPointUnpacker(item))
        return result

    def InterpolatedValues(self, start = "*-1d",end = "*", interval = "1h"):
        queryParamaterString = super(_piPoint,self)._buildQueryParamaterString([
            ('startTime',start),
            ('endTime',end),
            ('interval',interval)
        ])

        r = super(_piPoint,self).Request('streams/' + self._webId + '/interpolated' + queryParamaterString)
        result = {}
        for item in r['Items']:
            result.update(self._dataPointUnpacker(item))
        return result

    def _dataPointUnpacker(self, item):
        return {
            item['Timestamp']:{
                'Value': item['Value'],
                'Good': item['Good'],
                'Questionable': item['Questionable'],
                'UnitsAbbreviation': item['UnitsAbbreviation'],
                'Substituted': item['Substituted']
            }
        }
