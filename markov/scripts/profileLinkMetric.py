#!/usr/bin/env python3

"""Investigate the link functions acrossed a linkograph."""

import argparse # For command line
import matplotlib.pyplot as plt # For plotting
import linkograph.linkoCreate as llc # For manipulating linkos
import linkograph.stats as ls # For linkograph statistics

if __name__ == "__main__":

    description = """Script for displaying the results of the link
    funcitons on linkgraphs."""

    parser = argparse.ArgumentParser(description=description)

    parser.add_argument('linko', metavar="LINKOGRAPH.json",
                       help='The linkograph to consider.')

    parser.add_argument('-f', '--forelinks', action='store_true',
                        help='Use forelinks')

    parser.add_argument('-b', '--backlinks', action='store_true',
                       help='Use backlinks')

    parser.add_argument('-d', '--delta', type=int,
                        help=('Maximum number of links to consider'
                              ' forward or backward.'))

    parser.add_argument('-r', '--restrict', action='store_true',
                        help='Restrict to subgraph.')

    parser.add_argument('-l', '--lowerBound', type=int,
                        help='The lowest index to consider.')

    parser.add_argument('-u', '--upperBound', type=int,
                        help='The highest index to consider.')

    args = parser.parse_args()

    linko = llc.readLinkoJson(args.linko)

    linkNumber=[]

    if(args.forelinks):
        linkNumber.append(2)

    if(args.backlinks):
        linkNumber.append(1)

    if len(linkNumber) == 0:
        linkNumber = [1,2]

    funcArgs = {'linkograph': linko,
                'listNumber': linkNumber,
                'delta': args.delta,
                'restrict': args.restrict,
                'lowerBound': args.lowerBound,
                'upperBound': args.upperBound,
                'lineNumbers': False}

    entropy = ls.linkEntropy(**funcArgs)

    
    
    tcode =ls.linkTComplexity(difference=False,
                              normalize=False,
                              **funcArgs)

    plt.figure(1)
    
    plt.subplot(211)
    plt.title("Link Shannon Entropy")
    plt.ylabel("Shannon Entropy")
    plt.xlabel("Position in Linkograph")
    plt.plot(entropy)

    plt.subplot(212)
    plt.title("T-Code Complexity")
    plt.ylabel("T-Code Complexity")
    plt.xlabel("Position in Linkograph")
    plt.plot(tcode)

    plt.tight_layout()

    plt.show()
