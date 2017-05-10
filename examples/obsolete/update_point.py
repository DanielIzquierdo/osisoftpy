from OSIsoftPy.client import client
import datetime
import random
from time import sleep

# arguments
piWebApi = 'https://applepie.dstcontrols.local'
verifySSL = False

servers = client(piWebApi, authenticationType='kerberos', verifySSL=verifySSL).PIServers()

testTag = servers[0].FindPIPoint("AlansPythonTestTag")

now = datetime.datetime.utcnow()
now2 = now + datetime.timedelta(seconds=1)
value1 = random.random()
value2 = random.random()
data = [{
    'Timestamp': now.strftime('%Y-%m-%dT%H:%M:%SZ'),
    'Value': value1
    },{
    'Timestamp': now2.strftime('%Y-%m-%dT%H:%M:%SZ'),
    'Value': value2
    }]

testTag.UpdateValues(data)
sleep(10) #sleep for a bit to allow PI to buffer
results = testTag.RecordedValues(now.strftime('%Y-%m-%dT%H:%M:%SZ'), now2.strftime('%Y-%m-%dT%H:%M:%SZ'))

print '\n\n======================ATTEMPED UPDATED VALUES======================\n'
print data
print '\n\n======================UPDATED VALUES======================\n'
print results
print '\nIf Attempted and Updated match all was successful. If they do not match there was either an error updating or more time needs to be allowed for PI to buffer.'
