# -*- coding: utf-8 -*-

# content of test_sample.py
def test_ci(ci):
    if ci in ['travis', 'circle', 'appveyor']:
        print ("CI is valid, set to: {}".format(ci))
    elif ci:
        print ("Invalid CI specified: {}".format(ci))
    else:
        print ("No CI was specified")
    assert 0 # to see what was printed