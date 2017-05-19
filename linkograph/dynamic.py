#!/usr/bin/env python3

"""Functions supporting dynamically changing linkographs.

The functions in this package are aimed at linkographs that
change. Specifically, they are meant to support linokgraphs changing
as more commands are added to them. The idea is for the linkograph to
update online. As new commands get added, the linkograph changes to
account for them and also drops the older commands to keep a fixed
size. The same mechanism can be used to study the different
sublinkographs that are present in a static list of commands.

"""

import json  # For handling files in the json format.
import argparse  # For command line parsing.
from linkograph import linkoCreate

def addNode(linko, newLabels, ontology, size=None):
    """Adds a node to the linkograph and optionally maintains a size.

    Adds a node to the linkograph. If the size is not none, then the
    first node is dropped if the linkograph is already at the size
    provided by the size argument. Thus, when the linkograph is at the
    provided size, adding the node kicks the first node out.

    Arguments:
    linko -- the linkograph.
    newLabels -- A set of abstraction classes for the new node.
    size -- the size to maintain.

    Return:
    The resulting linkograph.

    """

    newLinko = linkoCreate.Linkograph()

    # Copy over the labels.
    newLinko.labels = [l for l in linko.labels]

    # Add any necessary new labels.
    for l in newLabels:
        if l not in newLinko.labels:
            newLinko.labels.append(l)

    updateFunction = lambda x : x

    newNodeNumber = len(linko)

    # The lowerBound value is used to drop the first node off if
    # necessary.
    lowerBound = 0

    # If the linkograph is at the size, then the first node needs to
    # be dropped off before adding a new node.
    if (size is not None) and (len(linko) >= size):
        # The updateFunction is used to decrement the indecies.
        updateFunction = lambda x : x-1

        # Setting the lowerBound to 1 effectively drops the first
        # node off when slicing later.
        lowerBound = 1

        # The last index number does not change if the limiting size
        # has been reached.
        newNodeNumber += -1

    # Create a record for the new node. It will be built as part of
    # the next for loop.
    newNode = (newLabels, set(), set())

    # Loop through all the entries starting at 1 and not 0, which
    # effectively removes the first node.
    for (presentLineNumber, entry) in enumerate(linko[lowerBound:]):

        lineLabel = entry[0]

        # Make a copy of the backlinks, remove node 0, and possible
        # decrement entry by 1.
        lineBackLinks = {updateFunction(x) for x in entry[1]}

        # Any reference to the 0 node becomes -1. So remove
        # it. Does nothing if -1 is not present.
        lineBackLinks = lineBackLinks - {-1}

        # Make a copy of the forelinks and possibly decrement each
        # entry by 1.
        lineForeLinks = {updateFunction(x) for x in entry[2]}

        # Add in forelink to new node and backlink to present node.
        for lTerminal in newLabels:
            for lInitial in lineLabel:
                # Check if the edge lInitial -> lTerminal is in the
                # ontolgoy.
                if lTerminal in ontology[lInitial]:
                    # The edge is present, so add the last nodes
                    # number to the forelinks and the present node's
                    # line number to the backlinks.
                    lineForeLinks.add(newNodeNumber)
                    newNode[1].add(presentLineNumber)

        newLinko.append((lineLabel, lineBackLinks,
                         lineForeLinks))

    # Add in the new node.
    newLinko.append(newNode)

    return newLinko

######################################################################
#----------------------- Command Line Programs -----------------------
