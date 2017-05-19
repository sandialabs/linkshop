#!/usr/bin/env python3

"""Calcualte the graph Shannon entropy."""

import argparse # For command line arguments
import matplotlib.pyplot as plt # For graphing
import time # For making file names unique
import pickle


if __name__ == "__main__":

    description="""Caculate the Shannon entropy for the whole graph
    and subgraphs."""
    
    parser = argparse.ArgumentParser(description=description)

    parser.add_argument('linko', metavar='LINKOGRAPH.json',
                        help='The linkograph to use.')

    parser.add_argument('-g', '--graphSize', type=int, default=5,
                        help='The size of sublinkgraphs.')

    parser.add_argument('-s', '--step', type=int, default=1,
                       help='Steps between the lower bounds considered.')

    parser.add_argument('-l', '--lowerBound', type=int,
                        help='The lowest index to consider.')

    parser.add_argument('-u', '--upperBound', type=int,
                        help='The highest index to consider.')

    parser.add_argument('-f', '--save-to-file', action='store_true',
                        help='Save the figure.')

    parser.add_argument('-m', '--matplot', action='store_true',
                        help='Save the matplot figure.')

    parser.add_argument('-p', '--path', metavar='LINKOGRAPH_PATH',
                        help='Path to linkograph module.')

    args = parser.parse_args()

    if args.path is not None:
        # If a path is provided, add it to the path
        import sys
        import os
        sys.path.append(args.path)

    # Import the linkograph packages. They are loaded here, to
    # provided the ability of adding the their path on the command
    # line.
    import linkograph.linkoCreate as llc # For manipulating linkographs
    import linkograph.stats as ls # For linkograph statistics

    # Set the max and min subgraph size to the specified size.
    minSize = maxSize = args.graphSize

    # Get the linkograph
    linko = llc.readLinkoJson(args.linko)

    # Calcualte the graph Shannon Entropy for the whole linkograph
    totalEntropy = ls.graphEntropy(linko)

    # Calcualte the graph Shannon Entropy for subgraphs.
    subEntropies =  ls.subgraphMetric(linkograph=linko,
                                       metric=ls.graphEntropy,
                                       lowerThreshold=None,
                                       upperThreshold=None,
                                       minSize=minSize,
                                       maxSize=maxSize,
                                       step=args.step,
                                       lowerBound=args.lowerBound,
                                       upperBound=args.upperBound)

    # ls.subgraphMetric returns tuples that give the lower and upper
    # index for each of the subgraph. We just want to graph the
    # entropy portion, which is the third entry of the tuple.
    subEntropies = [entry[2] for entry in subEntropies]


    fig_handle = plt.figure(1, figsize=(20, 10))

    title='Graph Shannon Entropy'
    ylabel='Shannon Entropy'
    xlabel=('Sublinkographs of size {0}'
            ' and step {1}').format(args.graphSize, args.step)

    plt.plot(subEntropies, color='b')
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.axhline(y=totalEntropy, color='r')
    plt.legend(['Entropy for Subgraphs ',
                'Entropy for Whole Linkograph'])

    # Save the figure as an svg
    figureFilename = title.replace(' ', '_')
    figureFilename +=  str(int(time.time()))

    if args.save_to_file:
        plt.savefig(figureFilename + '.svg')

    if args.matplot:
        with open(figureFilename + '.pickle', 'wb') as matplotFile:
            pickle.dump(fig_handle, matplotFile)

    plt.show()

