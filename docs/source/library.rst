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

Example to retrieve 2 values at 2 specified timestamps:
    >>> interpolated_values_at_times = individual_point.interpolatedattimes(['2015-01-01T00:00:00Z','2015-01-02T00:00:00Z'])
    >>> print('Number of Values for {}: {}'.format(individual_point.name, interpolated_values.__len__()))
    Number of Values for SINUSOID: 2
    >>> for interpolated_value in interpolated_values_at_times:
    ...    timestamp = interpolated_value.timestamp
    ...    value = interpolated_value.value
    ...    print('{}: {}'.format(timestamp, value))
    2017-01-01T00:00:00Z: 93.30135
    2017-05-03T00:00:00Z: 75.00031

Retrieving Values for Plotting
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Use the point.plot method to retrieve values at intervals designed for plotting on a graph.

.. automethod:: osisoftpy.Point.plot

Example to retrieve values to populate a graph:
    >>> plot_values = individual_point.plot(starttime='*-2d') 
    >>> print('Number of Values for {}: {}'.format(individual_point.name, plot_values.__len__()))
    Number of Values for SINUSOID: 57
    >>> for plot_value in plot_values:
    ...     timestamp = plot_value.timestamp
    ...     value = plot_value.value
    ...     print('{}: {}'.format(timestamp, value))
    2017-06-24T18:44:14.9283142Z: 43.148613
    2017-06-24T20:43:52Z: 89.3645
    2017-06-24T20:44:22Z: 89.49864
        ...
    2017-06-26T16:43:52Z: 3.61896157
    2017-06-26T16:44:22Z: 3.700893
    2017-06-26T18:43:52Z: 42.98347

Retrieving Compressed Values from within a Time Range
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Use the point.recorded method to retrieve compressed values for a time range given start and end times.

.. automethod:: osisoftpy.Point.recorded

Example to retrieve the values as-is in PI for the past week:
    >>> recorded_values = point.recorded(starttime='*-7d', endtime='*', maxcount=1000)
    >>> print('Number of Values for {}: {}'.format(point.name, recorded_values.__len__()))
    Number of Values for SINUSOID: 1000
    >>> for recorded_value in recorded_values:
    ...     timestamp = recorded_value.timestamp
    ...     value = recorded_value.value
    ...     print('{}: {}'.format(timestamp, value))
    2017-06-19T22:44:22Z: 96.29916
    2017-06-19T22:44:52Z: 96.21635
        ...
    2017-06-20T07:03:22Z: 51.4615021
    2017-06-20T07:03:52Z: 51.68683

Retrieving a Compressed Value for a Specific Time Stamp
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Use the point.recordedattime method to retrieve compressed values for a specific time stamp.

.. automethod:: osisoftpy.Point.recordedattime

Example to retrieve the values as-is in PI for a specific timestamp:
    >>> recorded_value = point.recordedattime('2017-03-15T07:00:00Z')
    >>> timestamp = recorded_value.timestamp
    >>> value = recorded_value.value
    >>> print('{}: {}'.format(timestamp, value))
    2017-03-15T07:00:00Z: 49.9999237

Retrieving Summary Values
~~~~~~~~~~~~~~~~~~~~~~~~~~
Use the point.summary method to retrieve a summary value over a time range given start and end times. 

.. automethod:: osisoftpy.Point.summary

Example to retrieve an average summary of PI Point values between two timestamps:
    >>> summary_values = point.summary(summarytype='Average', starttime='*-1w', endtime='*')
    >>> for summary_value in summary_values:
    ...    calculationtype = summary_value.calculationtype
    ...    timestamp = summary_value.timestamp
    ...    value = summary_value.value
    ...    print('{} is {} starting at {}'.format(calculationtype, value, timestamp))
    Average is 49.9999917322 starting at 2017-06-19T23:08:22.3572743Z

Example to retrieve a daily total summary of PI Point values between two timestamps:
    >>> summary_values = point.summary(summarytype='Total', starttime='*-1w', endtime='*', summaryduration='1d')
    >>> for summary_value in summary_values:
    ...    calculationtype = summary_value.calculationtype
    ...    timestamp = summary_value.timestamp
    ...    value = summary_value.value
    ...    print('{} is {} starting at {}'.format(calculationtype, value, timestamp))
    Total is 50.0000411563 starting at 2017-06-19T23:08:45.6071225Z
    Total is 49.9999553215 starting at 2017-06-20T23:08:45.6071225Z
    Total is 49.9999884571 starting at 2017-06-21T23:08:45.6071225Z
    Total is 49.9999169777 starting at 2017-06-22T23:08:45.6071225Z
    Total is 49.9999673219 starting at 2017-06-23T23:08:45.6071225Z
    Total is 50.0001375652 starting at 2017-06-24T23:08:45.6071225Z
    Total is 49.9999474406 starting at 2017-06-25T23:08:45.6071225Z

Retrieving End of Stream Values
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Use the point.end method to retrieve the value at the end of the stream (equivalent to current value if no future data).

.. automethod:: osisoftpy.Point.end

Example to retrieve the end-of-stream value for 2 points:
    >>> end_value = point.end()
    >>> timestamp = end_value.timestamp
    >>> value = end_value.value
    >>> print('{}: {}'.format(timestamp, value))
    2017-06-26T23:17:22Z: 89.0308456

Writing Values to PI Points
----------------------------

Writing a Single Value for a Stream
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Use the point.update_value method to update a single value at a single timestamp in a stream.

.. automethod:: osisoftpy.Point.update_value

Example to write the value 53 to the tag 'PythonInserted_test' at the current timestamp: 
    >>> point = webapi.points(query='name:PythonInserted_test')[0]
    >>> point.update_value('*', 53)

Writing Multiple Values for a Stream
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Use the point.update_values method to update multiple values at multiple corresponding timestamps in a stream. The length of the timestamps and values lists must match.

.. automethod:: osisoftpy.Point.update_values

Example to write multiple values to the tag 'PythonInserted_test':
    >>> point = webapi.points(query='name:PythonInserted_test')[0]
    >>> timestamps_to_be_inserted = ['2017-04-01T07:00:00Z', '2017-04-02T07:00:00Z', '2017-04-03T07:00:00Z']
    >>> values_to_be_inserted = [50, 95, 120]
    >>> point.update_values(timestamps_to_be_inserted, values_to_be_inserted)

    ====================   ============
    Timestamp               Value
    ====================   ============
    2017-04-01T07:00:00Z    50
    2017-04-02T07:00:00Z    95
    2017-04-03T07:00:00Z    120
    ====================   ============

Monitoring PI Points for Updates
---------------------------------

Subscribing to Updates for a PI Point
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Use the webapi.subscribe method to trigger a given function for a given list of PI points whenever the PI point is read and an update has occurred.

.. automethod:: osisoftpy.WebAPI.subscribe

Example of setting up subscriptions and their corresponding callback functions:

    >>> def callback_current(sender):
    ...     print('CALLBACK: Current Value of {} changed to {} at {}'.format(sender.name, sender.current_value.value, sender.current_value.timestamp))
    >>> def callback_end(sender):
    ...     print('CALLBACK: End Value of {} changed to {} at {}'.format(sender.name, sender.end_value.value, sender.end_value.timestamp)) 
    >>> webapi.subscribe(points, 'current', callback=callback_current)
    >>> webapi.subscribe(points, 'end', callback=callback_end)

Calling the corresponding read methods to trigger the callback functions:

    >>> for point in points:
    ...    point.current()
    ...    point.end()
    CALLBACK: Current Value of SINUSOID changed to 62.6735535 at 2017-06-26T19:29:37.584793Z
    CALLBACK: End Value of SINUSOID changed to 62.6735535 at 2017-06-26T19:29:22Z

Unsubscribing to Updates for a PI Point
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Use the webapi.unsubscribe method to stop monitoring a given list of PI points for updates. 

.. automethod:: osisoftpy.WebAPI.unsubscribe

Example to stop monitoring points:

    >>> webapi.unsubscribe(points, 'current')
    >>> webapi.unsubscribe(points, 'end')
    >>> for point in points:
    ...    point.current()
    ...    point.end()
    # No Response
