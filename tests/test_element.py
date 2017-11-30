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
osisoftpy.tests.element.py
~~~~~~~~~~~~
Tests for the `osisoftpy.element` module.
"""
import osisoftpy
import pytest
from six import string_types

class TestElements(object):

    #Attributes - Element with Attributes
    #Python - Element with no Attributes
    #Points - Element with Attributes; also has PI Point in query

    @pytest.mark.parametrize('query', ['name:Attributes', 'name:Python', 'name:Points'])
    def test_element_is_object(self, webapi, query):
        elements = webapi.elements(query)
        assert all(isinstance(element, osisoftpy.Element) for element in elements)

    @pytest.mark.parametrize('query', ['name:Attributes', 'name:Python', 'name:Points'])
    @pytest.mark.parametrize('count', [1])
    def test_element_has_name(self, webapi, query, count):
        elements = webapi.elements(query=query, count=count)
        assert all(isinstance(element, osisoftpy.Element) for element in elements)
        assert all(isinstance(element.name, string_types) for element in elements)

    @pytest.mark.parametrize('query', ['name:Attributes', 'name:Python', 'name:Points'])
    @pytest.mark.parametrize('count', [1])
    def test_element_has_haschildren(self, webapi, query, count):
        elements = webapi.elements(query=query, count=count)
        assert all(isinstance(element, osisoftpy.Element) for element in elements)
        assert all(isinstance(element.haschildren, bool) for element in elements)
    
    @pytest.mark.parametrize('query', ['name:Attributes', 'name:Points'])
    @pytest.mark.parametrize('count', [1])
    def test_element_has_attributes(self, webapi, query, count):
        elements = webapi.elements(query=query, count=count)
        assert all(isinstance(element, osisoftpy.Element) for element in elements)
        for element in elements:
            attributes = element.attributes
            assert all(isinstance(attributes[attribute], osisoftpy.Attribute) for attribute in attributes)

    @pytest.mark.skipif(True, reason="Varying category states")
    @pytest.mark.parametrize('query', ['name:Attributes', 'name:Python', 'name:Points'])
    @pytest.mark.parametrize('count', [1])
    def test_element_has_afcategories(self, webapi, query, count):
        elements = webapi.elements(query=query, count=count)
        assert all(isinstance(element.afcategories, dict) for element in elements)

    @pytest.mark.parametrize('query', ['name:Attributes', 'name:Python', 'name:Points'])
    @pytest.mark.parametrize('count', [1])
    def test_element_has_uniqueid(self, webapi, query, count):
        elements = webapi.elements(query=query, count=count)
        assert all(isinstance(element.uniqueid, string_types) for element in elements)

    @pytest.mark.parametrize('query', ['name:Attributes', 'name:Python', 'name:Points'])
    @pytest.mark.parametrize('count', [1])
    def test_element_has_webid(self, webapi, query, count):
        elements = webapi.elements(query=query, count=count)
        assert all(isinstance(element.webid, string_types) for element in elements)

    @pytest.mark.skipif(True, reason="Varying template states")
    @pytest.mark.parametrize('query', ['name:Attributes', 'name:Python', 'name:Points'])
    @pytest.mark.parametrize('count', [1])
    def test_element_has_template(self, webapi, query, count):
        elements = webapi.elements(query=query, count=count)
        assert all(isinstance(element.template, dict) for element in elements)

    @pytest.mark.parametrize('query', ['name:Attributes', 'name:Python', 'name:Points'])
    @pytest.mark.parametrize('count', [1])
    def test_element_has_links(self, webapi, query, count):
        elements = webapi.elements(query=query, count=count)
        assert all(isinstance(element.links, dict) for element in elements)