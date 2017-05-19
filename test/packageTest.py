#!/usr/bin/env python3

import argparse
import loadPath

packages = ['linkograph', 'markov']

info = ('Run tests on the packages.')

parser = argparse.ArgumentParser(description=info)
parser.add_argument('--packages', metavar='PACKAGES',
                    nargs='+',
                    help='the linkograph file.')
args = parser.parse_args()

if args.packages is None:
    args.packages = packages

if 'linkograph' in args.packages:

    print("Running tests for package: linkograph")

    import linkograph.runTests

    linkograph.runTests.test()

if 'markov' in args.packages:
    
    print("Running tests for markov package: markov")
    
    import markov.runTests

    markov.runTests.test()

