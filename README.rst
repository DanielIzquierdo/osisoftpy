# -*- coding: utf-8 -*-

osisoftpy
=========

A python library for OSIsoft's PI Web API
-----------------------------------------

.. image:: https://travis-ci.org/dstcontrols/osisoftpy.svg?branch=master
:target: https://travis-ci.org/dstcontrols/osisoftpy

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