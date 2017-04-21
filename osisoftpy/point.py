"""
osisoft_pi_webapi_python_client._point
~~~~~~~~~~~~~~~~~~~
This module contains the PI Point class
"""
from osisoftpy.base import Base

class Point(Base):
    """PI Point class"""
    def __init__(self, piWebApiDomain, session, webId):
        super(Point, self)._session(session)
        self._webId = webId
        self._piWebApiDomain = piWebApiDomain
        self._fetchTagInfo()

    def _fetchTagInfo(self):
        """gathers the PI tag information"""
        r = super(Point, self).Request('points/' + self._webId)
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
        """queries the current value for the pi point"""
        return self._dataPointUnpacker(super(Point, self).Request('streams/' + self._webId + '/value'))

    def RecordedValues(self, start = "*-1d",end = "*", boundary = "Inside", maxCount = 1000):
        """queries the recorded values for the pi point"""
        queryParamaterString = super(Point, self)._buildQueryParamaterString([
            ('startTime',start),
            ('endTime',end),
            ('boundaryType',boundary),
            ('maxCount',maxCount)
        ])

        r = super(Point, self).Request('streams/' + self._webId + '/recorded' + queryParamaterString)
        result = {}
        for item in r['Items']:
            result.update(self._dataPointUnpacker(item))
        return result

    def InterpolatedValues(self, start = "*-1d",end = "*", interval = "1h"):
        """queries the interpolated values for the pi point"""
        queryParamaterString = super(Point, self)._buildQueryParamaterString([
            ('startTime',start),
            ('endTime',end),
            ('interval',interval)
        ])

        r = super(Point, self).Request('streams/' + self._webId + '/interpolated' + queryParamaterString)
        result = {}
        for item in r['Items']:
            result.update(self._dataPointUnpacker(item))
        return result

    def UpdateValue(self, data, updateOption="Insert", bufferOption="BufferIfPossible"):
        """update the point with the provided value"""
        queryParamaterString = super(Point, self)._buildQueryParamaterString([
            ('updateOption',updateOption),
            ('bufferOption',bufferOption)
        ])

        return super(Point, self).Post('streams/' + self._webId + '/value' + queryParamaterString, data)

    def UpdateValues(self, data, updateOption="Insert", bufferOption="BufferIfPossible"):
        """update the point with the provided value"""
        queryParamaterString = super(Point, self)._buildQueryParamaterString([
            ('updateOption',updateOption),
            ('bufferOption',bufferOption)
        ])

        return super(Point, self).Post('streams/' + self._webId + '/recorded' + queryParamaterString, data)

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
