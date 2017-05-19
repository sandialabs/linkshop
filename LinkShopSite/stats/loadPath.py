#!/usr/bin/env python3

"""Adds the project path"""

import sys
import os

scriptdir = sys.path[0]
sourcedir = os.path.dirname(scriptdir)
projectdir = os.path.dirname(sourcedir)
sys.path.append(projectdir)
