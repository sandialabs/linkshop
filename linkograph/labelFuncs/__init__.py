#!/usr/bin/env python3

import sys
import os
import importlib

packages = []

location = ''
packagePrefix = ''

if (__file__ is not None) and (len(__file__) > 0):

    # import inspect
    # print(inspect.getframeinfo(inspect.currentframe()).filename)

    location = os.path.dirname(os.path.abspath(__file__))
    location = location + os.path.sep


if (__package__ is not None) and (len(__package__) > 0):
    packagePrefix = __package__ + '.'

with open(location + 'load_package_config') as lpc:
    for line in lpc:
        line = line.strip()

        if line[0] == '#':
            # Ignore lines starting with '#'
            continue

        packages.append(line)


#packages = ['SLMET']

absClassLabelers = {}
additionalArgs = {}

for p in packages:
    p = importlib.import_module(packagePrefix + p)
    for (key, value) in p.absClassLabelers:
        absClassLabelers[key] = value

    # Check for the additional args.
    if 'additionalArgs' in dir(p):
        for (key, value) in p.additionalArgs:
            additionalArgs[key] = value

util = importlib.import_module(packagePrefix + 'util')

addArgs = util.addArgs
applyArgs = util.applyArgs
