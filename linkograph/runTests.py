#!/usr/bin/env python3

"""Set up file for running tests."""

import unittest

def test():
    loader = unittest.TestLoader()
    testSuite = loader.discover('linkograph.tests')
    runner = unittest.TextTestRunner()
    runner.run(testSuite)
