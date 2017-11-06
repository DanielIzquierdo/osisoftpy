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
assertserver_implemented = True
assetdatabase_implemented = True
ready_for_testing = pytest.mark.skipif(not assertserver_implemented or not assetdatabase_implemented, reason="Assert Server and Asset Database Not Implemented")

@ready_for_testing
class TestAssetDatabase(object):
   
    def test_assetdatabase_has_webid(self, webapi):
        if webapi.assetservers.__len__() == 0:
            pytest.skip("No Asset Server(s) found")
        else:
            webapi.assetservers[0].get_databases()
        if webapi.assetservers[0].assetdatabases.__len__() == 0:
            pytest.skip("No Asset Databases(s) found")
        assetdb = webapi.assetservers[0].assetdatabases[0]
        assert type(assetdb.webid) == unicode

    def test_assetdatabase_has_id(self, webapi):
        if webapi.assetservers.__len__() == 0:
            pytest.skip("No Asset Server(s) found")
        else:
            webapi.assetservers[0].get_databases()
        if webapi.assetservers[0].assetdatabases.__len__() == 0:
            pytest.skip("No Asset Databases(s) found")
        assetdb = webapi.assetservers[0].assetdatabases[0] 
        assert type(assetdb.id) == unicode

    def test_assetdatabase_has_name(self, webapi):
        if webapi.assetservers.__len__() == 0:
            pytest.skip("No Asset Server(s) found")
        else:
            webapi.assetservers[0].get_databases()
        if webapi.assetservers[0].assetdatabases.__len__() == 0:
            pytest.skip("No Asset Databases(s) found")
        assetdb = webapi.assetservers[0].assetdatabases[0] 
        assert type(assetdb.name) == unicode

    def test_assetdatabase_has_description(self, webapi):
        if webapi.assetservers.__len__() == 0:
            pytest.skip("No Asset Server(s) found")
        else:
            webapi.assetservers[0].get_databases()
        if webapi.assetservers[0].assetdatabases.__len__() == 0:
            pytest.skip("No Asset Databases(s) found")
        assetdb = webapi.assetservers[0].assetdatabases[0] 
        assert type(assetdb.description) == unicode
    
    def test_assetdatabase_has_path(self, webapi):
        if webapi.assetservers.__len__() == 0:
            pytest.skip("No Asset Server(s) found")
        else:
            webapi.assetservers[0].get_databases()
        if webapi.assetservers[0].assetdatabases.__len__() == 0:
            pytest.skip("No Asset Databases(s) found")
        assetdb = webapi.assetservers[0].assetdatabases[0] 
        assert type(assetdb.path) == unicode

    def test_assetdatabase_has_extendedproperties(self, webapi):
        if webapi.assetservers.__len__() == 0:
            pytest.skip("No Asset Server(s) found")
        else:
            webapi.assetservers[0].get_databases()
        if webapi.assetservers[0].assetdatabases.__len__() == 0:
            pytest.skip("No Asset Databases(s) found")
        assetdb = webapi.assetservers[0].assetdatabases[0] 
        assert type(assetdb.extendedproperties) == dict

    def test_assetdatabase_has_links(self, webapi):
        if webapi.assetservers.__len__() == 0:
            pytest.skip("No Asset Server(s) found")
        else:
            webapi.assetservers[0].get_databases()
        if webapi.assetservers[0].assetdatabases.__len__() == 0:
            pytest.skip("No Asset Databases(s) found")
        assetdb = webapi.assetservers[0].assetdatabases[0] 
        assert type(assetdb.links) == dict