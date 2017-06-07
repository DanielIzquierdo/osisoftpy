# Subscribing to the 'current' and 'end' method of SINU* points

import osisoftpy
import time     # for time delay

webapi = osisoftpy.webapi('https://localhost/piwebapi', authtype='kerberos')

# <OSIsoft PI Web API [https://localhost/piwebapi]>

points = webapi.points(query='name:SINU*', count=100)

# <osisoftpy.points.Points object at 0x00000000039C1F60>

def callback_current(sender):
	print('CALLBACK: Current Value of {} changed to {} at {}'.format(sender.name, sender.current_value.value, sender.current_value.timestamp))

def callback_end(sender):
	print('CALLBACK: End Value of {} changed to {} at {}'.format(sender.name, sender.end_value.value, sender.end_value.timestamp))

webapi.subscribe(points, 'current', callback=callback_current)
webapi.subscribe(points, 'end', callback=callback_end)

# {u'P0xvVoXJ7fokikNJDlYulSjgAgAAAAR09MRFxTSU5VU09JRFU/current/': <blinker.base.NamedSignal object at 0x00000000043D8EB8; u'P0xvVoXJ7fokikNJDlYulSjgAgAAAAR09MRFxTSU5VU09JRFU/current/'>
# , u'P0xvVoXJ7fokikNJDlYulSjgL4gAAAR09MRFxTSU5VU09JRC5GT1JFQ0FTVA/current/': <blinker.base.NamedSignal object at 0x00000000043D8E48; u'P0xvVoXJ7fokikNJDlYulSjgL4gAAAR09MRFxTSU5VU09JRC5GT1JFQ0FTVA/current/'>
# , u'P0xvVoXJ7fokikNJDlYulSjgAQAAAAR09MRFxTSU5VU09JRA/current/': <blinker.base.NamedSignal object at 0x0000000002D650B8; u'P0xvVoXJ7fokikNJDlYulSjgAQAAAAR09MRFxTSU5VU09JRA/current/'>
# , u'P0xvVoXJ7fokikNJDlYulSjgAgAAAAR09MRFxTSU5VU09JRFU/end/': <blinker.base.NamedSignal object at 0x00000000043D8F98; u'P0xvVoXJ7fokikNJDlYulSjgAgAAAAR09MRFxTSU5VU09JRFU/end/'>
# , u'P0xvVoXJ7fokikNJDlYulSjgL4gAAAR09MRFxTSU5VU09JRC5GT1JFQ0FTVA/end/': <blinker.base.NamedSignal object at 0x00000000043D8EF0; u'P0xvVoXJ7fokikNJDlYulSjgL4gAAAR09MRFxTSU5VU09JRC5GT1JFQ0FTVA/end/'>
# , u'P0xvVoXJ7fokikNJDlYulSjgAQAAAAR09MRFxTSU5VU09JRA/end/': <blinker.base.NamedSignal object at 0x00000000043D8E10; u'P0xvVoXJ7fokikNJDlYulSjgAQAAAAR09MRFxTSU5VU09JRA/end/'>}

for point in points:
	value = point.current()
	print('Initial Current Value of {} is {} at {}'.format(point.name, value.value, value.timestamp))
	value = point.end()
	print('Initial End Value of {} is {} at {}'.format(point.name, value.value, value.timestamp))
	
# Initial Current Value of SINUSOID is 33.85205 at 2017-06-07T18:22:35.149826Z
# Initial End Value of SINUSOID is 33.85205 at 2017-06-07T18:22:19Z
# Initial Current Value of SINUSOID.FORECAST is {u'IsSystem': True, u'Name': u'No Data', u'Value': 248} at 2017-06-07T18:22:35.2279663Z
# Initial End Value of SINUSOID.FORECAST is 98.54495 at 2016-11-01T21:44:00Z
# Initial Current Value of SINUSOIDU is 40.3243675 at 2017-06-07T18:22:35.3060913Z
# Initial End Value of SINUSOIDU is 40.3243675 at 2017-06-07T18:22:19Z

time.sleep(15) # delay for 15 seconds while PI Tag Values Update

for point in points:
	point.current()
	point.end()

# CALLBACK: Current Value of SINUSOID changed to 34.05868 at 2017-06-07T18:22:50.3686981Z
# CALLBACK: End Value of SINUSOID changed to 34.05868 at 2017-06-07T18:22:49Z
# CALLBACK: Current Value of SINUSOIDU changed to 40.1104164 at 2017-06-07T18:22:50.5249481Z
# CALLBACK: End Value of SINUSOIDU changed to 40.1104164 at 2017-06-07T18:22:49Z

webapi.unsubscribe(points, 'current')
webapi.unsubscribe(points, 'end')