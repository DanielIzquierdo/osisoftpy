from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
from future.utils import iteritems
from datetime import datetime
import osisoftpy  # main package
from dateutil import parser

# x = parser.parse(None)
# print(x)
# print(None if x == None else x.strftime('%Y%m%d%H%M%S'))
# print(datetime.strptime('05-24-2017', '%Y-%m-%dT%H:%M:%SZ'))

webapi = osisoftpy.webapi('https://dev.dstcontrols.com/piwebapi/')
print('Connected to {}'.format(webapi.links.get('Self')))
points = webapi.points(query='name:EdwinPythonTest')
# shittyPoints = webapi.points(query='name:EdwinPythonTest2')
print('good points: {}'.format(points))
# print('shitty points: {}'.format(shittyPoints))

def callback(sender):
    print('{} changed! {}'.format(sender.name, sender))

webapi.subscribe(points, 'interpolatedattimes', startdatetime='2015-01-01T00:00:00Z', callback=callback)
subscriptions = webapi.subscribe(points, 'interpolatedattimes', startdatetime='2015-01-01T00:00:00Z', callback=callback)
print(len(subscriptions))

for point in points:
    # point.update_value('2015-01-01T00:00:00Z', 123)
    x = point.interpolatedattimes(['2015-01-01T00:00:00Z','2015-01-02T00:00:00Z'])
    # x = point.interpolatedattimes('2015-01-01T00:00:00Z')
    for value in x:
        print('{} : {}'.format(value.timestamp, value.value))

# subscriptions = webapi.unsubscribe(points, 'interpolatedattimes', '05-20-2017')
# print(len(subscriptions))
# subscriptions = webapi.unsubscribe(points, 'interpolatedattimes', '05-21-2017')
# print(len(subscriptions))
# subscriptions = webapi.unsubscribe(points, 'getvalue')
# print(subscriptions)
# #     if v1 == v2:    
#         print('objects match')
#         print(v1)
#         print(v2)
#     else:
#         print('objects don''t match')
#         print(v1)
#         print(v2)


#subscriber example
# def callback(sender):
#     print('{} changed! {}'.format(sender.name, sender))

# subscriptions = webapi.subscribe(points, 'current', callback)

# print(subscriptions)

# print(points)
# print(len(points))

# for point in points:
#     #current
#     point.current(time='2017-05-15')
#     point.current(time='2017-05-16')
#     point.current(time='2017-05-16')



# subscriptions = webapi.unsubscribe(shittyPoints, 'current')

# print(subscriptions)
    
    
    #recorded
    # recordedpoints = point.recorded()
    # print(len(recordedpoints))

    # recordedpoints = point.recordedattime('2016-06-01')
    # print(len(recordedpoints))

    #interpolated
    # interpolatedpoints = point.interpolatedattimes(time = ['2016-06-01','2016-05-31','2016-05-30'])
    # interpolatedpoints = point.interpolated()
    # print(interpolatedpoints.__len__())
    # for interpolatedpoint in interpolatedpoints:
    #     print(interpolatedpoint.timestamp)
    #     print(interpolatedpoint.value)
        
    #end
    # p = point.plot(starttime='*-2d')
    # print(p[0].value)

    # p = point.recorded(starttime='*-2d')
    # q = point.summary(summarytype='Average')
    # print(q)

    #update insert
    # point.update_value('2017-06-01 06:00', 900, updateoption='Insert')
    # p = point.current(time='2017-06-01 06:00')
    # print(len(p))
    # print(len(p.timestamp))
    # print(len(p.value))
    
    #updating     
    #  point.update_values(["2017-06-01 04:20","2017-06-01 04:25","2017-06-01 04:30"], [5,2,4])
    #  point.update_value("2017-06-01 05:00", 100)
    #  p = point.current(time="2017-06-01 05:00")
    #  print(point.name)


