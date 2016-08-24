from PI._piBase import _piBase

class _piServer(_piBase):
    def __init__(self, piWebApiDomain, session, webId):
        super(_piServer,self)._session(session)
        self.__webId = webId
        self._piWebApiDomain = piWebApiDomain
        self.__fetchServerInfo()

    def __fetchServerInfo(self):
        r = super(_piServer,self).Request('dataservers/' + self.__webId)
        print r
