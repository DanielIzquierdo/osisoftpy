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

webapi = osisoftpy.webapi('https://gold.dstcontrols.local/piwebapi')
points = webapi.points(query='name:SIN*')
print(len(points))
def callback(sender):
    print('Callback {} {}'.format(sender.name, sender.current_value.value))
webapi.subscribe(points, 'current', callback=callback)

points.current()
# print('Point: {} has inital value {} at {}'.format(point.name, value.value, value.timestamp))

time.sleep(30)

points.current()
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

