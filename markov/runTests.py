#!/usr/bin/env python3

"""Set up file for running tests."""

import unittest

def test(package='markov'):
    if package is None:
        testString = 'tests'
    else:
        testString = package + '.tests'
    
    loader = unittest.TestLoader()
    testSuite = loader.discover(testString)
    runner = unittest.TextTestRunner()
    runner.run(testSuite)

#---------------------------------------------------------------------

if __name__ == '__main__':
    test(package=None)
