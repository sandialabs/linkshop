#!/usr/bin/env python3

import argparse # For command line options processing.
import json # For handling json format.

def ontlogyDrawDot(ontology):
    """Creates a dot file representation of an ontoloyg."""

    dotString = ''

    # Header.
    header = ('digraph markov {\n'
              '  node [shape=oval,fontname="Helvetica",fontcolor=blue'
              ',fontsize=10];\n'
              '  edge [style=solid,color=black];')

    dotString += dotString + header + '\n'
    edge = ''

    for (iClass, terminalClassList) in ontology.items():
        # Add current abstraction class to ensure all classes are
        # printed.
        dotString += iClass + '\n'
        edge = '  "' + iClass + '" ->'
        for tClass in terminalClassList:
            dotString += edge + ' {"' + tClass + '"}\n'
    dotString += '}\n'

    return dotString

######################################################################
#----------------------- Command Line Programs -----------------------

def cli_ontologyDrawDot():
    """Command liine interface for drawing an ontology in dot."""

    info = "Draw an ontology as in dot format."

    parser = argparse.ArgumentParser(description=info)

    parser.add_argument('ontology', metavar='ONTOLOGY.json',
                        nargs=1,
                        help='The ontology.')

    parser.add_argument('-o', '--output', metavar='OUTPUT_FILE.dot',
                        help='The file to output dot format to.')

    args = parser.parse_args()

    ont = None
    with open(args.ontology[0], 'r') as ontFile:
        ont = json.load(ontFile)

    ontDotString = ontlogyDrawDot(ont)

    if args.output:
        with open(args.output, 'w') as dotFile:
            dotFile.write(ontDotString)
    else:
        print(ontDotString)
