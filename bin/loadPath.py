#!/usr/bin/env python3

"""Adds the project path"""

import sys
import os

scriptdir = sys.path[0]
projectdir = os.path.dirname(scriptdir)

sys.path.append(projectdir)
