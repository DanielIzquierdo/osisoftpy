import osisoftpy  # main package

webapi = osisoftpy.webapi('https://dev.dstcontrols.com/piwebapi/')
print('Connected to {}'.format(webapi.links.get('Self')))
points = webapi.points(query='name:Edwin*', count=100)
for point in points:
     point.update_values(["2017-06-01 04:20","2017-06-01 04:25","2017-06-01 04:30"], [5,2,4])
     #point.update_value("2017-06-01 05:00", 100)


