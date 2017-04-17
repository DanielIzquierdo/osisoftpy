
from osisoft_pi_webapi_python_client.client import client

# disable InsecureRequestWarnings
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


# arguments
piWebApi = 'https://applepie.dstcontrols.local'
verifySSL = False

servers = client(piWebApi, authenticationType='kerberos', verifySSL=verifySSL).PIServers()

# workingQuery = servers[0].FindPIPoints('name:sinusoid or name:CDT158')
workingQuery = servers[0].FindPIPoints('SINUSOID*')
brokenQuery = servers[0].FindPIPoints(["SINUSOID"])

tags = workingQuery

current = servers[0].CurrentValues(tags)
recorded = servers[0].RecordedValues(tags, start = "*-7d",end = "*", boundary = "Inside", maxCount = 100)
interpolated = servers[0].InterpolatedValues(tags, start = "*-1d",end = "*", interval = "15m")

print '\n\n======================WORKING QUERY======================\n'
print workingQuery
print '\n\n======================TAGS======================\n'
print tags
print '\n\n======================CURRENT VALUE======================\n'
print current
print '\n\n======================RECORDED VALUES======================\n'
print recorded
print '\n\n======================INTERPOLATED VALUES======================\n'
print interpolated
