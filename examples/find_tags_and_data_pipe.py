from __future__ import print_function
from OSIsoftPy.client import client
from time import sleep

# arguments
piWebApi = 'https://applepie.dstcontrols.local'
verifySSL = False

server = client(piWebApi, authenticationType='kerberos', verifySSL=verifySSL).PIServers()[0]

tags = server.FindPIPoints("SINUSOID*")

obs = server.Observable(tags)
d = obs.subscribe(lambda x: print(x))

connection = obs.connect()
sleep(60)
connection.dispose()
