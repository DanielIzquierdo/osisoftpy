from OSIsoftPy.client import client

# arguments
piWebApi = 'https://applepie.dstcontrols.local'
verifySSL = False

servers = client(piWebApi, authenticationType='kerberos', verifySSL=verifySSL).PIServers()

tags = servers[0].FindPIPoints("SINUSOID*")

current = servers[0].CurrentValues(tags)
recorded = servers[0].RecordedValues(tags, start = "*-1d",end = "*", boundary = "Inside", maxCount = 25)
interpolated = servers[0].InterpolatedValues(tags, start = "*-1d",end = "*", interval = "15m")

print '\n\n======================CURRENT VALUE======================\n'
print current
print '\n\n======================RECORDED VALUES======================\n'
print recorded
print '\n\n======================INTERPOLATED VALUES======================\n'
print interpolated
