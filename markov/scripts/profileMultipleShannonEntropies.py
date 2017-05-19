#!/usr/bin/env python3

"""Investigates link entropy, graph entropy, and T-code complexity.

The main purpose of this script is to look at the three entropy
metrics using different parameters.

"""

import argparse # For command line
import matplotlib.pyplot as plt # For plotting
import numpy as np # For matrices

def calculateMetrics(linko, linkNumber, delta, restrict, lowerBound,
                     upperBound):
    # Set up graph function parameters
    graphFuncArgs = {'linkograph': linko,
                     'metric': ls.graphEntropy,
                     'lowerThreshold': None,
                     'upperThreshold': None,
                     'minSize': delta + 1,
                     'maxSize': delta + 1,
                     'step': 1,
                     'lowerBound': lowerBound,
                     'upperBound': upperBound}

    g_entropy = ls.subgraphMetric(**graphFuncArgs)

    # ls.subgraphMetric returns tuples that give the lower and upper
    # index for each of the subgraph. We just want to graph the
    # entropy portion, which is the third entry of the tuple.
    g_entropy = [entry[2] for entry in g_entropy]

    # Set up link function parameters
    linkFuncArgs = {'linkograph': linko,
                    'listNumber': linkNumber,
                    'delta': delta,
                    'restrict': restrict,
                    'lowerBound': lowerBound,
                    'upperBound': upperBound,
                    'lineNumbers': False}

    l_entropy = ls.linkEntropy(**linkFuncArgs)

    t_code = ls.linkTComplexity(difference=False,
                                        normalize=False,
                                        **linkFuncArgs)

    return g_entropy, l_entropy, t_code


def _subplot(nrows, ncols, plot_number, title, ylabel, xlabel,
             legend, metric_values):
    """Perform subplotting."""

    plt.subplot(nrows, ncols, plot_number)
    plt.title(title)
    plt.ylabel(ylabel)
    plt.xlabel(xlabel)
    for values in metric_values:
        plt.plot(values)
    plt.legend(legend)


def _plot_metrics(linko, linkNumber, sizes, restrict, lowerBound,
                  upperBound, series_name, nrows, ncols,
                  series_number):
    """Plot the metrics for a single linkograph."""
    g_entropy = []
    l_entropy = []
    t_code = []

    for s in sizes:
        (g, l, t) = calculateMetrics(linko=linko,
                                     linkNumber=linkNumber,
                                     delta=s,
                                     restrict=restrict,
                                     lowerBound=lowerBound,
                                     upperBound=upperBound)
        g_entropy.append(g)
        l_entropy.append(l)
        t_code.append(t)

    legend = ["Delta {0}".format(s) for s in sizes]

    _subplot(nrows=nrows,
             ncols=ncols,
             plot_number=series_number,
             title=" Graph Shannon Entropy: {0}".format(series_name),
             ylabel="Graph Shannon Entropy",
             xlabel="Position in Linkograph",
             legend=legend,
             metric_values=g_entropy)

    _subplot(nrows=nrows,
             ncols=ncols,
             plot_number=series_number + ncols,
             title="Link Shannon Entropy: {0}".format(series_name),
             ylabel="Shannon Entropy",
             xlabel="Position in Linkograph",
             legend=legend,
             metric_values=l_entropy)

    _subplot(nrows=nrows,
             ncols=ncols,
             plot_number=series_number + 2 * ncols,
             title="T-Code Complexity: {0}".format(series_name),
             ylabel="T-Code Complexity",
             xlabel="Position in Linkograph",
             legend=legend,
             metric_values=t_code)



if __name__ == "__main__":

    description = """Script for displaying the results of the link
    funcitons on linkgraphs."""

    parser = argparse.ArgumentParser(description=description)

    parser.add_argument('linkos', metavar="LINKOGRAPH.json",
                        nargs='+',
                        help='The linkograph to consider.')

    parser.add_argument('-f', '--forelinks', action='store_true',
                        help='Use forelinks')

    parser.add_argument('-b', '--backlinks', action='store_true',
                       help='Use backlinks')

    parser.add_argument('-m', '--delta-min', type=int,
                        help=('Minimum delta for the link'
                              ' functions.'))

    parser.add_argument('-M', '--delta-max', type=int,
                        help=('Maximum delta for the link'
                              ' functions.'))

    parser.add_argument('-s', '--delta-step', type=int, default=1,
                        help=('Maximum delta for the link'
                              ' functions.'))

    parser.add_argument('-r', '--restrict', action='store_true',
                        help=('Restrict to subgraph for link.'
                              ' functions'))

    parser.add_argument('-l', '--lowerBound', type=int,
                        help='The lowest index to consider.')

    parser.add_argument('-u', '--upperBound', type=int,
                        help='The highest index to consider.')

    parser.add_argument('--graph-limit', type=int, default=4,
                        help=('The number of figures to allow'
                              'at one time.'))

    parser.add_argument('--graph-group-size', type=int, default=3,
                        help='The number of graphs to group.')

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

    linkNumber=[]

    if(args.forelinks):
        linkNumber.append(2)

    if(args.backlinks):
        linkNumber.append(1)

    if len(linkNumber) == 0:
        linkNumber = [1,2]

    sizes = range(args.delta_min,
                  args.delta_max + 1,
                  args.delta_step)

    ncols = min(len(args.linkos), args.graph_group_size)

    for first_link_index in range(0, len(args.linkos),
                                  args.graph_group_size):

        series = args.linkos[first_link_index: (first_link_index +
                                                args.graph_group_size)]

        step_mult = first_link_index / args.graph_group_size

        plt.figure(step_mult + 1, figsize=(20, 10))
        for series_number, linko_name in enumerate(series):
            # Get the linkograph.
            linko = llc.readLinkoJson(linko_name)

            # Plot the values for the linkograph.
            _plot_metrics(linko=linko,
                          linkNumber=linkNumber,
                          sizes=sizes,
                          restrict=args.restrict,
                          lowerBound=args.lowerBound,
                          upperBound=args.upperBound,
                          series_name=linko_name,
                          nrows=3,
                          ncols=len(series),
                          series_number=series_number + 1)

        plt.tight_layout()

        if step_mult % args.graph_limit == args.graph_limit - 1:

            plt.show()

    plt.show()
