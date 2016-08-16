from abc import ABCMeta, abstractmethod
import requests
import re
import HTTPKerberosAuth

class __piBase(metaclass=ABCMeta):
    def __init__(self, piWebApiDomain, userName, password, authenticationType):
        self.__userName = userName
        self.__password = password
        self.__authType = authenticationType
        self.__piWebApiDomain = __domainNameCleanup(piWebApiDomain)

        __testConnection()

    def Host():
        return(self.__piWebApiDomain)

    def __testConnection():
        return true

    def __domainNameCleanup(domainName):
        return re.sub(r"\/?piwebapi.*","",domainName)
