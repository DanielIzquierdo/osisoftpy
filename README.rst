osisoftpy
=========

A python library for OSIsoft's PI Web API
-----------------------------------------

.. image:: https://circleci.com/gh/dstcontrols/osisoftpy/tree/master.svg?style=shield&circle-token=07ae288c282e68695dce08f01f4ffeea36ee9405
   :target: https://circleci.com/gh/dstcontrols/osisoftpy/tree/master
   :alt: Circle CI code test status

.. image:: https://travis-ci.org/dstcontrols/osisoftpy.svg?branch=master
   :target: https://travis-ci.org/dstcontrols/osisoftpy
   :alt: Travis CI code test status

.. image:: https://ci.appveyor.com/api/projects/status/ugkm40a5ry81tjgt/branch/master?svg=true
   :target: https://ci.appveyor.com/project/awp/osisoftpy
   :alt: AppVeyor CI code test status

.. image:: https://codeclimate.com/github/dstcontrols/osisoftpy.svg
   :target: https://codeclimate.com/github/dstcontrols/osisoftpy
   :alt: Code Climate rating

.. image:: https://codecov.io/gh/dstcontrols/osisoftpy/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/dstcontrols/osisoftpy
   :alt: Codecov Coverage Report

.. image:: https://readthedocs.org/projects/osisoftpy/badge/?version=master
   :target: http://osisoftpy.readthedocs.io/en/master/?badge=master
   :alt: Documentation status


This library provides pythonic access to OSIsoft's PI System.

Usage
-----

.. code-block:: python

   import arrow       # Arrow is optional - it's included here make timestamps easier to understand.
   import osisoftpy


   webapi = osisoftpy.webapi('https://localhost/piwebapi', authtype='kerberos')

   # <OSIsoft PI Web API [https://localhost/piwebapi]>

   points = webapi.points(query='name:CD* or name:SINU*', count=100)

   # <osisoftpy.points.Points at 0x108a26850>

   points.current()

   for point in points:

       print('The current value for {} is {}, recorded {}'.format(
           point.name,
           point.current_value.value,
           arrow.get(point.current_value.timestamp).humanize()))

   # The current value for CDEP158 is 267, recorded 2017-05-12T01:46:23Z
   # The current value for CDM158 is {u'IsSystem': False, u'Name': u'Cascade', u'Value': 2}, recorded 2017-05-12T01:51:53Z
   # The current value for CDT158 is 65.66323, recorded 2017-05-12T01:50:53Z
   # The current value for SINUSOID is 28.9156246, recorded 2017-05-12T01:49:53Z
   # The current value for SINUSOIDU is 91.05328, recorded 2017-05-12T01:50:23Z

   for point in points:

       values = point.interpolated(starttime='*-14d', endtime='*', interval='1m')

       print('{} interpolated values for {} were retrieved; '
           'the data ranges from {} to {}.'.format(
           values.__len__(),
           point.name,
           arrow.get(values[0].timestamp).humanize(),
           arrow.get(values[-1].timestamp).humanize()))


   # 20161 interpolated values for CDEP158 were retrieved. The data spans from 2017-04-28T02:00:30.8133676Z to 2017-05-12T02:00:30.8133676Z
   # 20161 interpolated values for CDM158 were retrieved. The data spans from 2017-04-28T02:00:31.6571736Z to 2017-05-12T02:00:31.6571736Z
   # 20161 interpolated values for CDT158 were retrieved. The data spans from 2017-04-28T02:00:32.8447522Z to 2017-05-12T02:00:32.8447522Z
   # 20161 interpolated values for SINUSOID were retrieved. The data spans from 2017-04-28T02:00:33.7666888Z to 2017-05-12T02:00:33.7666888Z
   # 20161 interpolated values for SINUSOIDU were retrieved. The data spans from 2017-04-28T02:00:34.6417451Z to 2017-05-12T02:00:34.6417451Z

Installation
------------

To install osisoftpy, simply:

.. code-block:: bash

    $ pip install osisoftpy

Documentation
-------------

Documentation is available at http://osisoftpy.readthedocs.io/.

Author
------

-  Andrew Pong (`@hakaslak <http://twitter.com/hakaslak>`_)