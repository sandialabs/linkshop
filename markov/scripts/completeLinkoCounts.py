#!/usr/bin/env python3

"""Find the frequencies of the sublinkographs."""

import argparse # For command line parsing
import numpy as np
import json
import matplotlib.pyplot as plt # For graphing
import linkograph.enumeration as le # for enumerating linkographs


def count_sublinkos(ont, min_linko_size=2, max_linko_size=None,
                    function=le.linkoToEnum):
    """Count the sublinkograph frequency according to function value.

    inputs:

    ont: the ontology to consider.

    min_linko_size: the minimum sublinkograph size to consider.

    max_linko_size: the maximum sublinkograph size to consider.

    function(linko): the function to apply to each linkograph to group
    them by. The function should take a linkograph as its only
    required parameter. The default is linkoToEnum, which produces a
    tuple representation of a linkograph. The result of using
    linkoToEnum is to count the number of times a each particular
    linkograph is seen.

    output:

    [{function_value: count}, ...] -- a list of dictionaries. The ith
    dictionary is for the ith size considered. Each dictionary
    consists of keys corresponding the different possible function
    values for the sublinkograph and the values give the number of
    linkographs, linko, for which function(linko) == key.

    """

    # The strategy for this function is to pass off most of the work
    # to the function linkograph.enumeration.frequency.

    # group the linkograph dictionaries according to their sizes. Note
    # that 1 is added to the max size so that the max size is
    # included in the range.
    sublinko_counts = []
    for size in range(min_linko_size, max_linko_size + 1):
        size_counts = le.frequency(length=size,
                                   ontology=ont,
                                   function=function)
        sublinko_counts.append(size_counts)

    return sublinko_counts

def graph_sublinko_counts(sublinko_counts, width=1):
    """Graph the sublinkograph counts."""

    offset = [0]
    tick_locations = []
    tick_labels = []
    for size_counts in sublinko_counts:

        # format data
        keys, values = zip(*size_counts.items())


        p_values = np.array(values)/sum(values)

        ind = np.arange(len(keys)) + offset[-1] - width/2

        tick_locations.append((ind[-1] + ind[0])/2 + width/2)
        tick_labels.append(str(keys[0][0]))

        plt.bar(ind, p_values, width)

        offset.append(offset[-1] + 3 + len(keys))

    _, _, _, ymax = plt.axis()
    plt.vlines(np.array(offset) - 1.5, 0, ymax, linestyles='dashed')
    plt.xticks(tick_locations, tick_labels)

    plt.title("Linkograph Frequencies by Size")
    plt.xlabel("Size of Linkograph")
    plt.ylabel("Fraction of Total Linkographs")

    plt.show()


if __name__ == "__main__":

    description="""Find the number of disinct sublinkgraphs."""

    parser = argparse.ArgumentParser(description=description)

    parser.add_argument("ont", metavar="ONTOLOGY.json",
                        help="The ontology to process.")

    parser.add_argument("-m", "--min_linko_size", type=int, default=2,
                        help="Minimum linkograph size to consider.")

    parser.add_argument("-M", "--max_linko_size", type=int, default=2,
                        help="Maximum linkograph size to consider.")

    args = parser.parse_args()

    # construct a dictionary, whose keys are the linkographs and
    # values are the corresponding dictionary-list provided by
    # count_linkographs.

    ont = None
    with open(args.ont, 'r') as ont_file:
        ont = json.load(ont_file)

    sublinko_counts = count_sublinkos(ont=ont,
                                      min_linko_size = args.min_linko_size,
                                      max_linko_size = args.max_linko_size,
                                      function=le.linkoToEnum)

    # Graph the results.
    graph_sublinko_counts(sublinko_counts, width=1)
