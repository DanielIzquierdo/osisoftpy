osisoftpy
=========

A python library for OSIsoft's PI Web API
-----------------------------------------

.. image:: https://travis-ci.org/dstcontrols/osisoftpy.svg?branch=master
   :target: https://travis-ci.org/dstcontrols/osisoftpy
   :alt: Code Testing Status

.. image:: https://readthedocs.org/projects/osisoftpy/badge/?version=master
   :target: http://osisoftpy.readthedocs.io/en/master/?badge=master
   :alt: Documentation Status


This library provides pythonic access to OSIsoft's PI System.

Usage
-----

.. code-block:: python

   >>> import arrow
   >>> import osisoftpy
   >>> webapi = osisoftpy.webapi('https://localhost/piwebapi', authtype='kerberos')
   <OSIsoft PI Web API [https://localhost/piwebapi]>
   >>> points = webapi.points(params=dict(q="name:CDT158", count=10))
   <OSIsoft PI Point [CDT158 - Atmospheric Tower OH Vapor]>
   >>> for point in points:
   >>>     print('The current value for {} is {}, recorded {}'.format(
   >>>         point.name,
   >>>         point.current.value,
   >>>         arrow.get(point.current.timestamp).humanize(), ))
   The current value for CDT158 is 150.1271, recorded a minute ago

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