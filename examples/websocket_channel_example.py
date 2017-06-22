import websocket
try:
    import thread
except ImportError:  # TODO use Threading instead of _thread in python3
    import _thread as thread
import time
import sys
import ssl
import osisoftpy
import requests_kerberos
import requests
from requests.compat import urlparse

def on_message(ws, message):
    print('on_message: {}'.format(message))

def on_error(ws, error):
    print('on_error: {}'.format(error))

def on_close(ws):
    print("### closed ###")

if __name__ == "__main__":
    websocket.enableTrace(True)
    if len(sys.argv) < 2:
        host = "wss://dev.dstcontrols.com/piwebapi/streams/P0xvVoXJ7fokikNJDlYulSjgAQAAAAR09MRFxTSU5VU09JRA/channel"
    else:
        host = sys.argv[1]
    link = 'https://gold.dstcontrols.local/piwebapi'
    webapi = osisoftpy.webapi(link)
    # webapi2 = osisoftpy.webapi('wss://dev.dstcontrols.com/piwebapi/streams/P0xvVoXJ7fokikNJDlYulSjgAQAAAAR09MRFxTSU5VU09JRA/channel')
    # webapi.session.auth
    response = requests.Response()
    response.url = link
    response.headers = {'www-authenticate': 'negotiate token'}
    host2 = urlparse(response.url).hostname
    auth = requests_kerberos.HTTPKerberosAuth()
    x = auth.generate_request_header(response, host2)

    ws = websocket.create_connection(host, sslopt={"cert_reqs": ssl.CERT_NONE}, header = {'Authorization': x})
    result =  ws.recv()
    print(result)
    # ws = websocket.WebSocketApp(host,
    #                             on_message=on_message,
    #                             on_error=on_error,
    #                             on_close=on_close,
    #                             header = {'Authorization': x})
                                # header = {'www-authenticate': 'negotiate token'})
                                # header={'Authorization':'Basic YWstcGl3ZWJhcGktc3ZjOkRQJDI4R2hNeXAqIUUmZ2M='})
                                
    # ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})

    print('does this get hit?') #answer: no


# print('y')

# YIIGWwYJKoZIhvcSAQICAQBuggZKMIIGRqADAgEFoQMCAQ6iBwMFACAAAACjggTOYYIEyjCCBMagAwIBBaETGxFEU1RDT05UUk9MUy5MT0NBTKIpMCegAwIBAqEgMB4bBEhUVFAbFmdvbGQuZHN0Y29udHJvbHMubG9jYWyjggR9MIIEeaADAgEXoQMCAQKiggRrBIIEZ10liBmR1DUpzUhvDfHTANVz1h6qD97rTSFeIH51G/qX7WHRX9mdop/rViWJ0dHLQSEisxMGhxROkmJvW0B9mQJhRpLWF8JpfPrDZjAbA+nmKK7u9TEW4pfed3hiLjE4ecpMZxQZTHISI47M4ov/6rTLpGcTRe3UtM1ZC9iFgURKuBDiTi5Zr16t7QymbrmRMrmSu27ES39qs8cky0EZif5id1Y/lkOv+XTopgXkXWXcCUQ0cgTwo9a0tqWAzzkgwHyHmqUE/pZY0ay2Sut9UU/Khz6id71u4sypNwOzbdM84PQHuGamyZz5dFbu7uiNrMiBFX9M8hGj5SLXXtgKAxPYJqsNhQnlquNk0IdVtEetkQiJIAaqu8gXkgfqgXhpefN0zYOc3UN3VOUBC74P3uj9ajX/k8+RtUmatjW4f0zDHA+eRQfDhpM5FAnuC8Xy2tOmxm4itC+Cql1UfXIjvlwtskylf9o3pq/aMVGRT+fnfHKEjhpjSJzQFTGNVzANnmhPYT5dndhkZ+mOymZmF2Xc+LriS5UKxeRm6sNlhg2qFKLOfYBBDFPwrRLxtvO6pYadMa/YVe0sZXmF0ePnTyLGNLMYvmgrB6xr/aTOenDDftK1gQIToAN9Uej+VGgMXQm7nRevMeutePqZh+lrkeghjkIemhoa7/tH0N9H33CGgB+XSlO6uTtxZJzDkWztQWqDDL5S5D8OWvvTVKwkIZwJo8+44a5B5FHnHEjgRtxlBi2y7vJX77cw6IKxrGYpH9b0oAX92OIUiR4dvf3LlHqy6wuEIGT1xFSLEJ4fpl5AXnL5WatZPnSpf1gaVXs9yt2nOYIGFWSblbYjwVnBbw0rPqUvNiXDh3W9Br23IFlONO72p/UThlM5ZpkV9twyXUzaFWMWrJ1ww7IysO0knfeUcAE6ti13e97OdGHnRkyIfG1iKVdGw87ZTFG6jTLg6qSKzl1bS7DTYWiZaSUdwtwvfvCk+//SsbEHKV/uT00w2sAMBTGX6PAWxC9oOMIzHh+HzHaCF5yf3H9bpzvMr16g+2TT0MH+82ELNAKA1mDd9XVjR/z80RvvVh8xF66cKzWSYKACBP1KKUNy3KHsrsRqB0/FvsqRGH+qGLslaDcxNJ8EPxj8NQOU1nabkYdG3y/vmuNkcOsNSHefFnk6VFfZ9uYewmszi5TC98ownWPRMsWMCHHRnPkK71+F9jRZkTrmDI8mWJ50+ianD5xX7tP49Nt9Z+BHMBfytaUGnJOiRM5d2OX0rjvdMkRBcd+noICiOS9/x4xPGwlZsE0ToadesX7mVCkf5i20ch5EfE8qqawL120OWIu2usHFJe6afsK/EEQ8w14zvCWsy/04wzyLlGe3TyW3hzUcYh8+7GAj35qujOHBjZXVZmkSJwo7df8s9/gfGhy3kewCmMyfDBNOEOQLVFIhNm8s9sWna/fG9h98LJHL+FoZ8ksvd0zedOMqMqHjSunilKu0QRx/pWd4Vh2pj224pIIBXTCCAVmgAwIBF6KCAVAEggFMBKGNsntUXm8IJWmLvY/dIxaZE80Kp2iFNJCsxLkry+lrRjnhGEmMxRMtKEMOoelg6164SSQXzy2aE7C8/GyDKH7IIDOKE/OWh0uKe2FwwYLrjtBCuHBYJut/4O4cE7Y0X16SH6dX/U/sRRJeC/hORn5oBxP4iiRRs5zDgeeAeEc5asCPHrbt26J0yKillAoEqYJbcklDB5GTAcz/+yx82qLilPcH1XI8ssa0ED8tUV5XVZeScFQInzSNalmM9JLPjp3FguzToOnUb3s1ZjLBfgCsKkI0xmxh9a0nx1rRobd8uR7WHFV3di3H8Xzpu7r7tsKmswNxfWNwU74X3EOXEkYwkkyCNNpyXESa0gvCm31wp+9UN0RvUB2lXgWF/hKHRAoL2Ib8c22QDKQwJQ36mI32c4KU/TWd6CfHOf0BoG80WC4Cb70Q0w22AFI=
    # self.assertEqual(
    #     auth.generate_request_header(response, host),
    #     "Negotiate GSSRESPONSE"
    # )