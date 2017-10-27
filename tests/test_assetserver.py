# -*- coding: utf-8 -*-

#    Copyright 2017 DST Controls
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.
"""
osisoftpy.tests.test_assetserver.py
~~~~~~~~~~~~
Tests for the `osisoftpy.assertserver` module.
"""
import osisoftpy
import pytest

#change below statement from False to True when assetserver and/or assetdatabase is implemented
assertserver_implemented = pytest.mark.skipif(not False, reason="Assert Server Not Implemented")
assetdatabase_implemented = pytest.mark.skipif(not False, reason="Assert Database Not Implemented")

@assertserver_implemented
class TestAssetServer(object):

    def test_webapi_has_assertservers(webapi):
        if webapi.assetservers.__len__() > 0:
            assert all(isinstance(assetserver, osisoftpy.assetserver) for assetserver in webapi.assetservers)
        else:
            #empty list evaluate to False
            assert webapi.assetservers

    def test_assertserver_has_webid(webapi):
        
        if webapi.assetservers.__len__() == 0:
            pytest.skip("No Asset Server(s) found")
        assetserver = webapi.assetservers[0]
        assert type(assetserver.webid) == str
    
    def test_assertserver_has_id(webapi):
        if webapi.assetservers.__len__() == 0:
            pytest.skip("No Asset Server(s) found")
        assetserver = webapi.assetservers[0] 
        assert type(assetserver.id) == str

    def test_assertserver_has_name(webapi):
        if webapi.assetservers.__len__() == 0:
            pytest.skip("No Asset Server(s) found")
        assetserver = webapi.assetservers[0] 
        assert type(assetserver.name) == str

    def test_assertserver_has_description(webapi):
        if webapi.assetservers.__len__() == 0:
            pytest.skip("No Asset Server(s) found")
        assetserver = webapi.assetservers[0] 
        assert type(assetserver.description) == str

    def test_assertserver_has_path(webapi):
        if webapi.assetservers.__len__() == 0:
            pytest.skip("No Asset Server(s) found")
        assetserver = webapi.assetservers[0] 
        assert type(assetserver.path) == str

    def test_assertserver_has_isconnected(webapi):
        if webapi.assetservers.__len__() == 0:
            pytest.skip("No Asset Server(s) found")
        assetserver = webapi.assetservers[0] 
        assert type(assetserver.isconnected) == bool

    def test_assertserver_has_serverversion(webapi):
        if webapi.assetservers.__len__() == 0:
            pytest.skip("No Asset Server(s) found")
        assetserver = webapi.assetservers[0] 
        assert type(assetserver.serverversion) == bool

    def test_assertserver_has_extendedproperties(webapi):
        if webapi.assetservers.__len__() == 0:
            pytest.skip("No Asset Server(s) found")
        assetserver = webapi.assetservers[0] 
        assert type(assetserver.extendedproperties) == dict

    def test_assertserver_has_links(webapi):
        if webapi.assetservers.__len__() == 0:
            pytest.skip("No Asset Server(s) found")
        assetserver = webapi.assetservers[0] 
        assert type(assetserver.links) == dict

    @assetdatabase_implemented
    def test_assertserver_has_assetdatabases(webapi):
        if webapi.assetservers.__len__() == 0:
            pytest.skip("No Asset Server(s) found")
        assetserver = webapi.assetservers[0] 
        assetdatabases = assetserver.assetdatabases
        assert all(isinstance(assetdatabase, osisoftpy.assetdatabase) for assetdatabase in assetdatabases)