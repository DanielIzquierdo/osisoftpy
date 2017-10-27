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
osisoftpy.tests.test_assetdatabase.py
~~~~~~~~~~~~
Tests for the `osisoftpy.assertdatabase` module.
"""
import osisoftpy
import pytest

#questionable implementation

#change below statement from False to True when assetserver and assetdatabase is implemented
assertserver_implemented = False
assetdatabase_implemented = False
ready_for_testing = pytest.mark.skipif(not assertserver_implemented and not assetdatabase_implemented, reason="Assert Server and Asset Database Not Implemented")

@ready_for_testing
class TestAssetDatabase(object):
   
    def test_assetdatabase_has_webid(webapi):
        if webapi.assetservers.__len__() == 0:
            pytest.skip("No Asset Server(s) found")
        if webapi.assetservers[0].assetdatabases.__len__() == 0:
            pytest.skip("No Asset Databases(s) found")
        assetdb = webapi.assetservers[0].assetdatabases[0] 
        assert type(assetdb.webid) == str

    def test_assetdatabase_has_id(webapi):
        if webapi.assetservers.__len__() == 0:
            pytest.skip("No Asset Server(s) found")
        if webapi.assetservers[0].assetdatabases.__len__() == 0:
            pytest.skip("No Asset Databases(s) found")
        assetdb = webapi.assetservers[0].assetdatabases[0] 
        assert type(assetdb.id) == str

    def test_assetdatabase_has_name(webapi):
        if webapi.assetservers.__len__() == 0:
            pytest.skip("No Asset Server(s) found")
        if webapi.assetservers[0].assetdatabases.__len__() == 0:
            pytest.skip("No Asset Databases(s) found")
        assetdb = webapi.assetservers[0].assetdatabases[0] 
        assert type(assetdb.name) == str

    def test_assetdatabase_has_description(webapi):
        if webapi.assetservers.__len__() == 0:
            pytest.skip("No Asset Server(s) found")
        if webapi.assetservers[0].assetdatabases.__len__() == 0:
            pytest.skip("No Asset Databases(s) found")
        assetdb = webapi.assetservers[0].assetdatabases[0] 
        assert type(assetdb.description) == str
    
    def test_assetdatabase_has_path(webapi):
        if webapi.assetservers.__len__() == 0:
            pytest.skip("No Asset Server(s) found")
        if webapi.assetservers[0].assetdatabases.__len__() == 0:
            pytest.skip("No Asset Databases(s) found")
        assetdb = webapi.assetservers[0].assetdatabases[0] 
        assert type(assetdb.path) == str

    def test_assetdatabase_has_extendedproperties(webapi):
        if webapi.assetservers.__len__() == 0:
            pytest.skip("No Asset Server(s) found")
        if webapi.assetservers[0].assetdatabases.__len__() == 0:
            pytest.skip("No Asset Databases(s) found")
        assetdb = webapi.assetservers[0].assetdatabases[0] 
        assert type(assetdb.extendedproperties) == dict

    def test_assetdatabase_has_links(webapi):
        if webapi.assetservers.__len__() == 0:
            pytest.skip("No Asset Server(s) found")
        if webapi.assetservers[0].assetdatabases.__len__() == 0:
            pytest.skip("No Asset Databases(s) found")
        assetdb = webapi.assetservers[0].assetdatabases[0] 
        assert type(assetdb.links) == dict