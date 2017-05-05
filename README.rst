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

   import osisoftpy

   webapi = osisoftpy.webapi('https://localhost/piwebapi', authtype='kerberos')
   webapi.search('indexed search query')

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