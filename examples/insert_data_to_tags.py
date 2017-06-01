import osisoftpy  # main package

webapi = osisoftpy.webapi('https://dev.dstcontrols.com/piwebapi/')
print('Connected to {}'.format(webapi.links.get('Self')))
points = webapi.points(query='name:Edwin*', count=100)
for point in points:
    point.update_value("2017-06-01T00:32:00Z", 32, questionable=True)
    print(point.name)
