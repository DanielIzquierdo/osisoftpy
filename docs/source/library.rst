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