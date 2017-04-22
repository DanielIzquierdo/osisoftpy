import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

from osisoftpy.client import Client

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

api = Client()

print api.getDataArchiveServer('dev.dstcontrols.com')
