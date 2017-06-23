QuickStart
===========

Minimal Example
----------------
This example imports the osisoftpy library, instantiates the piwebapi, queries all PI points that start with “SINU”, reads the current value for each of those points, and prints that value for each point to the console.

    >>> import osisoftpy
    >>> webapi = osisoftpy.webapi('https://dev.dstcontrols.com/piwebapi/')
    >>> point_list = webapi.points(query='name:SINU*')
    >>> for individual_point in point_list:
    ...     valueobj = individual_point.current()
    ...     print('Latest value of {} is {} at time {}'.format(individual_point.name, valueobj.value, valueobj.timestamp))
    Latest value of SINUSOID is 35.11712 at time 2017-06-23T18:25:42.276947Z
    Latest value of SINUSOIDU is 39.02229 at time 2017-06-23T18:25:42.323822Z
