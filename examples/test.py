#1
# foo = None
# print (foo)
# print ("test {}.".format(foo))

# foo = 1.0
# print (foo)

# print ("test {}.".format(foo))

# print ("test __str__() {}.".format(foo.__str__()))

#2
import osisoftpy  # main package
import time
from datetime import datetime
import pytz

webapi = osisoftpy.webapi('https://dev.dstcontrols.com/piwebapi')
elements = webapi.elements(query='attributename:PythonAFInserted AND name:Attributes')
element = elements[0]
print element
att = element['PythonAFInserted']
att.update_value('11/22/2017 3PM', 12321)

# webapi = osisoftpy.webapi('https://gold.dstcontrols.local/piwebapi')
# point = webapi.points(query='name:PythonInserted_test')[0]
# point.update_value('2000-01-01T07:00:00Z', 53)

# end_value = point.end()
# timestamp = end_value.timestamp
# value = end_value.value
# print('{}: {}'.format(timestamp, value))

# summary_values = point.summary(summarytype='Total', starttime='*-1w', endtime='*', summaryduration='1d')
# for summary_value in summary_values:
#     calculationtype = summary_value.calculationtype
#     timestamp = summary_value.timestamp
#     value = summary_value.value
#     print('{} is {} starting at {}'.format(calculationtype, value, timestamp))

# def callback_current(sender):
#     print('CALLBACK: Current Value of {} changed to {} at {}'.format(sender.name, sender.current_value.value, sender.current_value.timestamp))
# def callback_end(sender):
#     print('CALLBACK: End Value of {} changed to {} at {}'.format(sender.name, sender.end_value.value, sender.end_value.timestamp)) 
# webapi.subscribe(points, 'current', callback=callback_current)
# webapi.subscribe(points, 'end', callback=callback_end)
# for point in points:
#     point.current()
#     point.end()
# time.sleep(30)
# for point in points:
#     point.current()
#     point.end()

# interpolated_values_at_times = point.interpolatedattimes(['2017-01-01T00:00:00Z','2017-05-03T00:00:00Z'])
# print('Number of Values for {}: {}'.format(point.name, interpolated_values_at_times.__len__()))
# for interpolated_value in interpolated_values_at_times:
#    timestamp = interpolated_value.timestamp
#    value = interpolated_value.value
#    print('{}: {}'.format(timestamp, value))

# print(len(points))
# def callback(sender):
#     print('Callback {} {}'.format(sender.name, sender.current_value.value))
# webapi.subscribe(points, 'current', callback=callback)

# points.current()
# # print('Point: {} has inital value {} at {}'.format(point.name, value.value, value.timestamp))

# time.sleep(30)

# points.current()
# points = 0
# points = webapi.points(query='name:EdwinPythonTest')
# for point in points:
#     print(point)

# point = points[0]
# ts = point.current().timestamp
# y = time.strptime(ts, '%Y-%m-%dT%H:%M:%SZ')

# localFormat = "%Y-%m-%d %H:%M"
# localmoment_naive = datetime.strptime('2013-09-06 14:05', localFormat)
# localtimezone = pytz.timezone('America/Los_Angeles')
# localmoment = localtimezone.localize(localmoment_naive, is_dst=None)
# utcmoment = localmoment.astimezone(pytz.utc)
# print(utcmoment)


# print(len(points))
# points = webapi.points(query='name:EdwinPythonTest')
# print(len(points))

#3
# string = '2017-02-01 06:00'
# print(string)
# x = time.strptime(string, '%Y-%m-%d %H:%M')
# print(x)

#
# times = ['2017-02-01 06:00', '2017-03-05 15:00', '2017-04-15 17:00']
# for t in times: 
#     s = time.strptime(t, '%Y-%m-%d %H:%M')
#     print(s)
#     print(time.strftime('%Y-%m-%dT%H:%M:%SZ', s))

# ##