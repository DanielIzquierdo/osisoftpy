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
from osisoftpy.assetserver import AssetServer
from osisoftpy.assetdatabase import AssetDatabase
from six import string_types

class TestAssetServer(object):

    def test_webapi_has_assertservers(self, webapi):
        if webapi.assetservers.__len__() > 0:
            assert all(isinstance(assetserver, osisoftpy.AssetServer) for assetserver in webapi.assetservers)
        else:
            #empty list evaluate to False
            assert webapi.assetservers

    def test_assertserver_has_webid(self, webapi):
        
        if webapi.assetservers.__len__() == 0:
            pytest.skip("No Asset Server(s) found")
        assetserver = webapi.assetservers[0]
        assert isinstance(assetserver.webid, string_types)
    
    def test_assertserver_has_id(self, webapi):
        if webapi.assetservers.__len__() == 0:
            pytest.skip("No Asset Server(s) found")
        assetserver = webapi.assetservers[0] 
        assert isinstance(assetserver.id, string_types)

    def test_assertserver_has_name(self, webapi):
        if webapi.assetservers.__len__() == 0:
            pytest.skip("No Asset Server(s) found")
        assetserver = webapi.assetservers[0] 
        assert isinstance(assetserver.name, string_types)

    def test_assertserver_has_description(self, webapi):
        if webapi.assetservers.__len__() == 0:
            pytest.skip("No Asset Server(s) found")
        assetserver = webapi.assetservers[0] 
        assert isinstance(assetserver.description, string_types)

    def test_assertserver_has_path(self, webapi):
        if webapi.assetservers.__len__() == 0:
            pytest.skip("No Asset Server(s) found")
        assetserver = webapi.assetservers[0] 
        assert isinstance(assetserver.path, string_types)

    def test_assertserver_has_isconnected(self, webapi):
        if webapi.assetservers.__len__() == 0:
            pytest.skip("No Asset Server(s) found")
        assetserver = webapi.assetservers[0] 
        assert isinstance(assetserver.isconnected, bool)

    def test_assertserver_has_serverversion(self, webapi):
        if webapi.assetservers.__len__() == 0:
            pytest.skip("No Asset Server(s) found")
        assetserver = webapi.assetservers[0] 
        assert isinstance(assetserver.serverversion, string_types)

    def test_assertserver_has_extendedproperties(self, webapi):
        if webapi.assetservers.__len__() == 0:
            pytest.skip("No Asset Server(s) found")
        assetserver = webapi.assetservers[0] 
        assert isinstance(assetserver.extendedproperties, dict)

    def test_assertserver_has_links(self, webapi):
        if webapi.assetservers.__len__() == 0:
            pytest.skip("No Asset Server(s) found")
        assetserver = webapi.assetservers[0] 
        assert isinstance(assetserver.links, dict)

    def test_assertserver_has_assetdatabases(self, webapi):
        if webapi.assetservers.__len__() == 0:
            pytest.skip("No Asset Server(s) found")
        assetserver = webapi.assetservers[0]
        assetserver.get_databases()
        assetdatabases = assetserver.assetdatabases
        assert all(isinstance(database, AssetDatabase) for database in assetdatabases)