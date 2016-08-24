from nose.tools import *
from PI.piClient import PIClient

piWebApi = 'https://applepie.dstcontrols.local'
user = 'ak-piwebapi-svc'
password = 'DP$28GhMyp*!E&gc'
verifySSL = False;

def test_piclient_unknown_auth():
    try:
        client = PIClient(piWebApi, authenticationType='BAD',verifySSL=verifySSL)
    except ValueError as e:
        x = 'success'

def test_piclient_basic_auth():
    client = PIClient(piWebApi,'ak-piwebapi-svc','DP$28GhMyp*!E&gc','basic',verifySSL=verifySSL)

def test_piclient_basic_kerberos():
    client = PIClient(piWebApi, authenticationType='kerberos',verifySSL=verifySSL)

def test_piclient_host_name():
    client = PIClient(piWebApi + '/piwebapi/','ak-piwebapi-svc','DP$28GhMyp*!E&gc','basic',verifySSL=verifySSL)

    if client.Host() != piWebApi:
        raise ValueError('Bad host name')

def test_piclient_piservers():
    client = PIClient(piWebApi,'ak-piwebapi-svc','DP$28GhMyp*!E&gc','basic',verifySSL=verifySSL)
    servers = client.PIServers()
