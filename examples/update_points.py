from OSIsoftPy.client import client
import datetime
import random
from time import sleep

# arguments
piWebApi = 'https://applepie.dstcontrols.local'
verifySSL = False

server = client(piWebApi, authenticationType='kerberos', verifySSL=verifySSL).PIServers()[0]

testTag = "AlansPythonTestTag"
testTag2 = "AlansPythonTestTag2"

now = datetime.datetime.utcnow()
now2 = now + datetime.timedelta(seconds=1)
value1 = random.random()
value2 = random.random()
value3 = random.random()
value4 = random.random()
data = {
    now.strftime('%Y-%m-%dT%H:%M:%SZ'):{
        testTag: value1,
        testTag2: value2
    },
    now2.strftime('%Y-%m-%dT%H:%M:%SZ'):{
        testTag: value3,
        testTag2: value4
    }
}

server.UpdateValues(data)
sleep(10) #sleep for a bit to allow PI to buffer
results = server.RecordedValues([testTag, testTag2],now.strftime('%Y-%m-%dT%H:%M:%SZ'), now2.strftime('%Y-%m-%dT%H:%M:%SZ'))

print '\n\n======================ATTEMPED UPDATED VALUES======================\n'
print data
print '\n\n======================UPDATED VALUES======================\n'
print results
print '\nIf Attempted and Updated match all was successful. If they do not match there was either an error updating or more time needs to be allowed for PI to buffer. Allow for floating point truncation'
