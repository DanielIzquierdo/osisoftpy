from __future__ import print_function

from requests.sessions import Session


class PIClientSession(Session):
    def __init__(self):
        super(PIClientSession, self).__init__()
        for adapter in self.adapters.values():
            adapter.max_retries = 3

    # @property
    def prefix(self, host):
        """Return the appropriate URL prefix to prepend to requests,
        based on the host provided in settings.
        """
        if '://' not in host:
            host = 'https://%s' % host.strip('/')
        # elif host.startswith('http://'):
        #     raise SSLError(
        #         'Can not verify ssl with non-https protocol. Change the '
        #         'verify_ssl configuration setting to continue.')
        return '%s/piwebapi/' % host.rstrip('/')

    def getDataArchiveServer(self, host):
        url = self.prefix(host)
        self.verify = False
        # url = '%s' % (self.prefix(host))
        # return self.get(url).json()
        print(url)
        r = self.get(url)
        print(r.status_code)
        print(r)
        return r.json()


client = Client()
