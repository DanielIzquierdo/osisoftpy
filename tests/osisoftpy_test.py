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
osisoftpy.tests.osisoftpy_test.py
~~~~~~~~~~~~
Some blah blah about what this file is for...
"""
import pytest


def add_one(x):
    return x + 1


def test_four_add_one():
    assert add_one(4) == 5


def raise_system_exit():
    raise SystemExit(1)


def test_raise_system_exit():
    with pytest.raises(SystemExit):
        raise_system_exit()
