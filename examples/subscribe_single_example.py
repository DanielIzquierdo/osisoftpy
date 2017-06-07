# Subscribing to the 'current' method of SINU* points

import osisoftpy
import time     # for time delay

webapi = osisoftpy.webapi('https://localhost/piwebapi', authtype='kerberos')

# <OSIsoft PI Web API [https://localhost/piwebapi]>

points = webapi.points(query='name:SINU*', count=100)

#<osisoftpy.points.Points object at 0x00000000039C9FD0>

def callback_current(sender):
	print('Current Value of {} changed to {} at {}'.format(sender.name, sender.current_value.value, sender.current_value.timestamp))

subscription = webapi.subscribe(points, 'current', callback=callback_current)

# {u'P0xvVoXJ7fokikNJDlYulSjgAgAAAAR09MRFxTSU5VU09JRFU/current/': <blinker.base.NamedSignal object at 0x00000000043BAEB8; u'P0xvVoXJ7fokikNJDlYulSjgAgAAAAR09MRFxTSU5VU09JRFU/current/'>
# , u'P0xvVoXJ7fokikNJDlYulSjgL4gAAAR09MRFxTSU5VU09JRC5GT1JFQ0FTVA/current/': <blinker.base.NamedSignal object at 0x00000000043BAE48; u'P0xvVoXJ7fokikNJDlYulSjgL4gAAAR09MRFxTSU5VU09JRC5GT1JFQ0FTVA/current/'>
# , u'P0xvVoXJ7fokikNJDlYulSjgAQAAAAR09MRFxTSU5VU09JRA/current/': <blinker.base.NamedSignal object at 0x0000000002D550B8; u'P0xvVoXJ7fokikNJDlYulSjgAQAAAAR09MRFxTSU5VU09JRA/current/'>}

for point in points:
	point.current()
	
time.sleep(15) # delay for 15 seconds while PI Tag Values Update

for point in points:
	point.current()

# Current Value of SINUSOID changed to 19.1537361 at 2017-06-07T17:43:50.3364562Z
# Current Value of SINUSOIDU changed to 57.0382652 at 2017-06-07T17:43:52.6645965Z

webapi.unsubscribe(points, 'current')