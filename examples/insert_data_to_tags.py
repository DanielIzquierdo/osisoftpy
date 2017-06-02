import osisoftpy  # main package

webapi = osisoftpy.webapi('https://dev.dstcontrols.com/piwebapi/')
print('Connected to {}'.format(webapi.links.get('Self')))
points = webapi.points(query='name:Edwin*')
for point in points:
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
    q = point.summary(summarytype='Average')

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


