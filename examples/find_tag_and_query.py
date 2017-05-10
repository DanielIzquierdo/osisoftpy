import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

from src.osisoftpy import client


# disable InsecureRequestWarnings
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# arguments
piWebApi = 'https://applepie.dstcontrols.local'

servers = client(
    piWebApi, authenticationType='kerberos', verifySSL=False).PIServers()

sinusoid = servers[0].FindPIPoint("SINUSOID")

current = sinusoid.CurrentValue()
recorded = sinusoid.RecordedValues(
    start="*-1d", end="*", boundary="Inside", maxCount=25)
interpolated = sinusoid.InterpolatedValues(
    start="*-1d", end="*", interval="15m")

print '\n\n======================CURRENT VALUE======================\n'
print current
print '\n\n======================RECORDED VALUES======================\n'
print recorded
print '\n\n======================INTERPOLATED VALUES======================\n'
print interpolated
