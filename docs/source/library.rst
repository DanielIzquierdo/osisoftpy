Library
========

Importing the Library 
----------------------
To import the library, import the osisoftpy library in your python script.

Example:
    >>> import osisoftpy

Authentication and Instantiation
---------------------------------
Create an instance of the web api by calling osisoftpy.webapi using the following parameters:

.. autofunction:: osisoftpy.webapi

Minimal example:
    >>> webapi = osisoftpy.webapi('https://dev.dstcontrols.com/piwebapi/')

Example with authtype:
    >>> webapi = osisoftpy.webapi('https://dev.dstcontrols.com/piwebapi/', authtype='kerberos')

Querying and Identifying PI Points
-----------------------------------
Before performing any read/write operations, the webapi must be queried for PI points to read from/write to using the webapi.points:

.. automethod:: osisoftpy.WebAPI.points()

Example:
    >>> points = webapi.points(query='name:CD* or name:SINU*', count=100)

Reading Values from PI Points 
------------------------------
Several functions exist to read data from PI points at different timestamps. The following sections describe these methods in further detail.

.. method:: current
    :annotation: = Returns the current value of the stream.
.. method:: interpolated
    :annotation: = Retrieves values over the specified time range at the specified sampling interval
.. method:: interpolatedattimes
    :annotation: = Retrieves interpolated values for a list of time stamps
.. method:: plot
    :annotation: = Retrieves values over the specified time range suitable for plotting over the number of intervals (typically represents pixels)
.. method:: recorded
    :annotation: = Returns a list of compressed values for the requested time range from the source provider
.. method:: recordedattime
    :annotation: = Returns a list of compressed values for a single time stamp
.. method:: summary
    :annotation: = Returns a summary over the specified time range for the stream
.. method:: end
    :annotation: = Returns the end-of-stream value of the stream
    

Many of these methods return an object of class Value. The actual numeric value is stored in the object’s “value” attribute. 

.. autoclass:: osisoftpy.Value
.. autoattribute:: osisoftpy.Value.valid_attr

Retrieving the Current Value
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Use the point.current method to retrieve the current value of the stream.

.. automethod:: osisoftpy.Point.current

Example of using the current method on a Point object and getting its value from the resulting Value object:
    >>> for individual_point in points:
    ...     current_value_object = individual_point.current()
    ...     name = individual_point.name
    ...     value = current_value_object.value
    ...     timestamp = current_value_object.timestamp
    ...     print('Latest value of {} is {} at time {}'.format(individual_point.name, valueobj.value, valueobj.timestamp))
    SINUSOID currently has 86.309 at 2017-06-23T23:27:09.068283Z
    SINUSOIDU currently has 35.7429466 at 2017-06-23T23:27:09.099533Z

Retrieving Interpolated Values at Fixed Intervals
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Use the point.interpolated method to retrieve interpolated data at a fixed time interval given start and end times.

.. automethod:: osisoftpy.Point.interpolated

Example to retrieve last 2 weeks of data at 1 minutes intervals:
    >>> interpolated_values = individual_point.interpolated(starttime='*-14d', endtime='*', interval='1m')
    >>> print('Number of Values for {}: {}'.format(individual_point.name, interpolated_values.__len__()))
    Number of Values for SINUSOID: 20161
    >>> for interpolated_value in interpolated_values:
    ...    timestamp = interpolated_value.timestamp
    ...    value = interpolated_value.value
    ...    print('{}: {}'.format(timestamp, value))
    2017-06-10T00:16:30.7815651Z: 68.52295
    2017-06-10T00:17:30.7815651Z: 68.11697
    2017-06-10T00:18:30.7815651Z: 67.7096
        ...
    2017-06-24T00:16:30.7815651Z: 68.62864
    2017-06-24T00:17:30.7815651Z: 68.22302
    2017-06-24T00:18:30.7815651Z: 67.97307

Retrieving Interpolated Values at Given Timestamps
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Use the point.interpolatedattimes method to retrieve interpolated data at given timestamps. 

.. automethod:: osisoftpy.Point.interpolatedattimes

Retrieving Values for Plotting
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. automethod:: osisoftpy.Point.plot

Retrieving Compressed Values from within a Time Range
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. automethod:: osisoftpy.Point.recorded

Retrieving a Compressed Value for a Specific Time Stamp
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. automethod:: osisoftpy.Point.recordedattime

Retrieving Summary Values
~~~~~~~~~~~~~~~~~~~~~~~~~~
.. automethod:: osisoftpy.Point.summary

Retrieving End of Stream Values
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. automethod:: osisoftpy.Point.end

Writing Values to PI Points
----------------------------

Writing a Single Value for a Stream
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Monitoring PI Points for Updates
---------------------------------

Subscribing to Updates for a PI Point
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~