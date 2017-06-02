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

# webapi = osisoftpy.webapi('https://dev.dstcontrols.com/piwebapi/')
# points = webapi.points(query='name:EdwinPythonTest')
# print(len(points))
# points = 0
# points = webapi.points(query='name:EdwinPythonTest')
# for point in points:
#     print(point)

# point = points[0]
# ts = point.current().timestamp
# y = time.strptime(ts, '%Y-%m-%dT%H:%M:%SZ')

def _compare_pi_and_local_datetime(pidatetime, localdatetime):
    pi = datetime.strptime(pidatetime, '%Y-%m-%dT%H:%M:%SZ')

    local = datetime.strptime(localdatetime, '%Y-%m-%d %H:%M')
    localtimezone = pytz.timezone('America/Los_Angeles')
    localmoment = localtimezone.localize(local, is_dst=None)
    utcmoment = localmoment.astimezone(pytz.utc)
    print(utcmoment.strftime('%Y-%m-%d %H:%M'))
    print(pi.strftime('%Y-%m-%d %H:%M'))

_compare_pi_and_local_datetime('2017-03-05T15:00:00Z', '2017-03-05 07:00')

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

