#!/usr/bin/env python3

import argparse  # For command line parsing.
import subprocess # For converting dot to svg
import os # For file manipulation

def dot2svg(dotFile, svgFile):
    """Python wrapper for using dot to create an SVG file."""

    basename = os.path.splitext(dotFile)[0]
    unflatname = "{0}-unflat".format(basename)

    subprocess.call(["unflatten", "-l6",
                     "-o",
                     unflatname,
                     dotFile])

    subprocess.call(["dot", "-Tsvg", "-O", unflatname])

    # Clean up
    os.remove(unflatname)
    os.rename(unflatname + '.svg', svgFile)

if __name__ == '__main__':

    """Command line interface for converting dot to svg."""

    info = 'Converts dot to svg.'

    parser = argparse.ArgumentParser(description=info)

    parser.add_argument('dotFile', metavar='DOT_FILE.dot',
                        nargs=1,
                        help='The dot file')

    parser.add_argument('svgFile', metavar='SVG_FILE.svg',
                        nargs=1,
                        help='The svg file')

    args = parser.parse_args()

    dot2svg(args.dotFile[0], args.svgFile[0])
