import pytest
import requests
# from .conftest import ci_input
# from .conftest import ci

import osisoftpy

def test_name(ci):
    print(ci)
    assert ci == 'Test'

# def test_name2():
#     assert ci_input(cmdopt) == 'Test'

# def test_name3():
#     assert ci_input == 'Test'