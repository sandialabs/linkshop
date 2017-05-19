#!/usr/bin/env python3

"""An ASCII printer for linkographs."""

import argparse  # For command line parsing.
import linkograph.stats as stats
from linkograph import linkoCreate

class OffsetError(Exception):
    """Error for a missing ontology."""
    def __init__(self, message):
        super().__init__(message)

def linkoPrint(linko, x_offset=None, labels=True):
    """Create a string representation of a linkograph."""

    # Find the longest link
    linkWidth = max(stats.linkDifference(linko))

    if x_offset is None:
        x_offset = linkWidth + 1
    elif x_offset < linkWidth + 1:
        msg = 'Offset must be at least {}'.format(linkWidth+1)
        raise OffsetError(msg)


    linkWidth = 2*linkWidth

    for r in range(4*(len(linko)-1)+1):
        # r walks through the lines. A node is placed every fourth
        # line.
        line = ''

        #import pdb; pdb.set_trace()
        
        for p in range(linkWidth + 1):
            c = linkWidth - p

            if c == 0 and r%4 == 0:
                # Adds the node's star
                line += '*'
                if labels:
                    labels = [str(l) for l in linko[r//4][0]]
                    labelString = ' '.join(labels)
                    line += ' ' + labelString
            elif r%4 == 1 and c%4 == 1 and _checkFore(r, c, linko):
                line += '/'
            elif r%4 == 1 and c%4 == 3 and _checkBack(r, c, linko):
                line += '\\'
            elif r%4 == 3 and c%4 == 1 and _checkBack(r, c, linko):
                line += '\\'
            elif r%4 == 3 and c%4 == 3 and _checkFore(r, c, linko):
                line += '/'
            elif (r%4 == 2 and c%4 == 2) or (r%4 == 0 and c%4 == 0):
                if _checkLink(r, c, linko):
                    line += '*'
                elif _checkFore(r, c, linko) and _checkBack(r, c, linko):
                    line += 'x'
                elif _checkFore(r, c, linko):
                    line += '/'
                elif _checkBack(r, c, linko):
                    line += '\\'
                else:
                    line += ' '
            else:
                line += ' '

        print(line)

def _checkBack(r, c, linko):
    """Checks if (r,c) lies on a backlink for a node."""
    finalNode = (r+c)//4

    if finalNode >= len(linko):
        return False
    
    backlinks = linko[finalNode][1]
    if len(backlinks) == 0:
        return False
    
    minBacklink = min(backlinks)

    return 2*minBacklink < 2*finalNode - c

def _checkFore(r, c, linko):
    """Checks if (r,c) lies on a forelink for a node."""
    initialNode = (r-c)//4

    if initialNode < 0:
        return False
    
    forelinks = linko[initialNode][2]
    if len(forelinks) == 0:
        return False

    maxForelink = max(forelinks)

    return 2*maxForelink > 2*initialNode + c

def _checkLink(r, c, linko):
    """Checks if (r,c) is a link for a pair of nodes."""
    x, y = (r-c)//4, (r+c)//4

    if x < 0 or x >= len(linko):
        return False

    return y in linko[x][2]

######################################################################
#----------------------- Command Line Programs -----------------------

def cli_linkoPrint():
    """Draws the linkograph in text format."""

    info = 'Draws the linkograph in SVG format.'

    parser = argparse.ArgumentParser(description=info)
    parser.add_argument('linkograph', metavar='LINKOGRAPH.json',
                        nargs=1,
                        help='The linkograph to draw.')

    parser.add_argument('--offset', type=int, default=None,
                        help='Controls x offset.')

    args = parser.parse_args()

    # Read in the linkograph
    linko = linkoCreate.readLinkoJson(args.linkograph[0])

    offset = args.offset
    
    linkoPrint(linko, offset)
