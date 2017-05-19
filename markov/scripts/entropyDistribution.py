#!/usr/bin/env python3

"""Finds the distribution for (graph) Shannon entropy values for
linkograph sizes using a given ontology.

This script was used to create the first figure in the V2 Ontology
(Shannon Entropy Graphical View) on the Shannon Entropy (Graph
Version) page. The parameters were -m 1 -M 10 -s 1 onotlogy.json.

"""

import argparse # For parsing command lines
import numpy as np # For numerics
import math # For ceil
import json # For pasing json files
import matplotlib.pyplot as plt
import time
from functools import wraps
import linkograph.enumeration as le # For frequency function
import linkograph.stats as ls # For linkograph statistics

currentMetric = ls.graphEntropy

def distribution(ontology, metric, minLinkoSize=2, maxLinkoSize=100,
                 stepLinkoSize=1, precision=2, samples=None,
                 random=False, seed=None):
    """Calculate the distribution of value for metric on provided
    linkograph sizes.

    inputs:

    ontology: ontology used for constructing linkographs.

    metric: the function to collect data on for each of the
    linkographs. The function take a linkograph as its argument.

    minLinkoSize: the minimun number of nodes in the linkographs to
    consider.

    maxLinkoSize: the maximum number of nodes in the linkographs to
    consider. Note that the max is not included to match pythons
    convertions on lists and ranges.

    stepLinkoSize: the step size between minLinkoSize to maxLinkoSize
    for the number of linkographs to Consider.

    precision: the number of digits to consider for the metric.

    samples: determines the number of labelings to consider. If none
    is provided, then the number is set to the total number of
    possible labelings. If random is False, then every labeling will
    be considered. If random is True, then there is no guarantee the
    labelings chosen will be distinct.

    random: If False, then labelings are considered in a sequential
    order. If True, then labelings are randomly selected.

    seed: provides a seed for the internal random number generator
    used to produce random labelings.

    output:

    an array of size number_of_linkograph_sizes where the ith entry
    provides a dictionay that has the counter for how many times each
    distinct value of the metric was seen.

    """
    
    # wrap the metric with precision
    metric = precision_decorator(metric)

    frequencies = []

    for size in range(minLinkoSize, maxLinkoSize, stepLinkoSize):
        
        print('Working on size: {0}'.format(size))

        frequencies.append(le.frequency(length=size,
                                        ontology=ontology,
                                        function=metric,
                                        absClasses=None,
                                        samples=samples,
                                        random=random,
                                        seed=seed))

    return frequencies

#############
#           #
# Decorator #
#           #
#############

# Wraps a function's output with decimal precision control.
def precision_decorator(f):
    @wraps(f)
    def wrapper(*args, precision= 2, **kwds):
        return round(f(*args, **kwds), precision)
    return wrapper

def _mean_standard(dist):
    """Find the mean and standard deviation."""

    # In the dist dictionary, the key is the value of the metric and
    # the value is the number of times it appears. So, the sample
    # value is the key and the number of samples for the value is the
    # value in dist for that key.

    total_samples = sum(dist.values())

    total_values = sum(key*value
                       for key, value in dist.items())

    mean = total_values/total_samples

    std_squared = sum((value/total_samples) * (key - mean)**2
                   for key, value in dist.items())

    std = math.sqrt(std_squared)

    return mean, std

if __name__ == "__main__":

    desctiption="""Calculate the distribution for (graph) Shannon
    entropy for a given range of linkographs using a specified
    ontology."""

    parser = argparse.ArgumentParser(description=desctiption)

    parser.add_argument("ontology", metavar="ONTOLOGY.json",
                        help="Ontology to use for linking.")

    parser.add_argument('-m', '--minimum', type=int, default = 2,
                       help='minimum size of linkographs.')

    parser.add_argument('-M', '--maximum', type=int, default = 100,
                       help='maximum size of linkographs.')

    parser.add_argument('-s', '--step', type=int, default = 1,
                       help='step size of linkographs.')

    parser.add_argument('-p', '--precision', type=int, default = 2,
                        help='the number of runs.')

    parser.add_argument('-l', '--limit', type=int,
                        help='specify the number of samples.')

    parser.add_argument('-r', '--random', action='store_true',
                        help='use random labelings.')

    parser.add_argument('-d', '--seed', type=int,
                        help='seed for generating random labelings')

    parser.add_argument('-n', '--noGraph', action='store_true',
                        help='turn the graph output off.')
    args = parser.parse_args()

    ont = None
    with open(args.ontology, 'r') as ontFile:
        ont = json.load(ontFile)

    distributions = distribution(ontology=ont,
                                 metric=currentMetric,
                                 minLinkoSize=args.minimum,
                                 maxLinkoSize=args.maximum,
                                 stepLinkoSize=args.step,
                                 precision=args.precision,
                                 samples=args.limit,
                                 random=args.random,
                                 seed=args.seed)

    if args.random:
        fileName = 'randomShannonEntropyDistribution'
    else:
        fileName = 'completeShannonEntropyDistribution'
    fileName += str(int(time.time()))
    fileName += "_m{0}_M{1}_s{2}".format(args.minimum,
                                         args.maximum,
                                         args.step)
    fileName += '.json'
    with open(fileName, 'w') as distFile:
        json.dump(distributions, distFile, indent=4)

    means_stds = [ _mean_standard(dist) for dist in distributions]

    means, stds = zip(*means_stds)

    # ind = np.arange(args.minimum, args.maximum, args.step) - 0.4

    # width = 0.8

    # plt.bar(ind, means, width, color='r', yerr=stds)

    # plt.show()

    linkoSizes = range(args.minimum, args.maximum, args.step)

    if not args.noGraph:
        plt.figure(1)

        plt.subplot(211)
        plt.plot(linkoSizes, means)
        plt.xlabel("Size of Linkograph")
        plt.ylabel("Mean Shannon Entropy")
        plt.title("Mean Shannon Entropy vs. Linkograph Sizes")

        plt.subplot(212)
        plt.plot(linkoSizes, stds)
        plt.xlabel("Size of Linkograph")
        plt.ylabel("Standard Deviation Shannon Entropy")
        plt.title("Standard Deviation Shannon Entropy vs. Linkograph Sizes")

        plt.tight_layout()

        plt.show()

