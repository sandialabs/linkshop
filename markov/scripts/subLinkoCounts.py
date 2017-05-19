#!/usr/bin/env python3

"""Find the frequencies of the sublinkographs."""

import argparse # For command line parsing
import numpy as np
import matplotlib.pyplot as plt # For graphing
import linkograph.linkoCreate as lc # for reading linkographs.
import linkograph.enumeration as le # for enumerating linkographs


def count_sublinkos(linko, min_linko_size=2, max_linko_size=None,
                    overlap=True, function=le.linkoToEnum):
    """Count the sublinkograph frequency according to function value.

    inputs:

    linko: the linkograph to consider.

    min_linko_size: the minimum sublinkograph size to consider.

    max_linko_size: the maximum sublinkograph size to consider.

    overlap: if True, every sublinkograph of the provided sizes. If
    false, only considers non-overlapping linkographs of each size.

    function(linko): the function to apply to each sublinkograph to
    group them by. The function should take a linkograph as its only
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
    # to the function linkograph.enumeration.subLinkographFrequency.

    # If max_linko_size was not passed, set to the largest linkograph
    # size. If max_linko_size is passed, restirct it to the size of
    # the linkograph.
    if max_linko_size is None:
        max_linko_size = len(linko)
    else:
        max_linko_size = min(max_linko_size, len(linko))

    # group the linkograph dictionaries according to their sizes. Note
    # that 1 is added to the max size so that the max size is
    # included in the range.
    sublinko_counts = []
    for size in range(min_linko_size, max_linko_size + 1):
        size_counts = le.subLinkographFrequency(linkos=[linko],
                                                 size=size,
                                                 overlap=overlap,
                                                 function=function)
        sublinko_counts.append(size_counts)

    return sublinko_counts

def graph_sublinko_counts(sublinko_counts, sort_key=None, width=1):
    """Graph the sublinkograph counts."""

    # If no sorting function is provided, just use the identity
    if sort_key is None:
        sort_key = lambda x: x

    # We use the sort_key function to sort key, value pairs of a
    # dictionary by the affect the sort_key has on the key. Thus, we
    # need to wrap the key_value function so that it can take a key,
    # value pair and operate on the key portion.
    wraped_sort_key = lambda key_value: sort_key(key_value[0])

    offset = [0]
    tick_locations = []
    tick_labels = []
    for size_counts in sublinko_counts:

        # format data
        keys, values = zip(*sorted(size_counts.items(),
                                   key=wraped_sort_key))

        p_values = np.array(values)/sum(values)

        ind = np.arange(len(keys)) + offset[-1] - width/2

        tick_locations.append((ind[-1] + ind[0])/2 + width/2)
        tick_labels.append(str(keys[0][0]))

        plt.bar(ind, p_values, width)

        offset.append(offset[-1] + 3 + len(keys))

    _, _, _, ymax = plt.axis()
    plt.vlines(np.array(offset) - 1.5, 0, ymax, linestyles='dashed')
    plt.xticks(tick_locations, tick_labels)

    plt.title("Sublinkograph Frequency")
    plt.xlabel("Size of Linkographs")
    plt.ylabel("Fraction of Total Linkographs Per Size of"
               " Linkograpgh")

    plt.show()


def entropy_order(linko_enum):
    """Key function to sort by graph shannon entropy.

    Adds another dimention to the linko_enum that is the count of the
    number of links. With this added dimension, this function will
    cause the sort routine to sort first on linograph size, then on
    the number of links, and finally on the backlink encoding using
    that number of links.

    """

    number_of_ones = sum(int(c) for c in bin(linko_enum[1])[2:])

    return linko_enum[0], number_of_ones, linko_enum[1]

if __name__ == "__main__":

    orderings = {
        'backlink': lambda x: x, # default ordering based on enumeration
        'entropy': entropy_order # based partly on number of links
    }


    description="""Find the number of disinct sublinkgraphs."""

    parser = argparse.ArgumentParser(description=description)

    parser.add_argument("linkos", metavar="LINKOGRAPH.json",
                        nargs="+",
                        help="The linkographs to process.")

    parser.add_argument("-m", "--min_linko_size", type=int, default=2,
                        help="Minimum linkograph size to consider.")

    parser.add_argument("-M", "--max_linko_size", type=int,
                        help="Maximum linkograph size to consider.")

    parser.add_argument("-n", "--no-overlap", action="store_false",
                        help=("Do not allow sublinkographs to"
                              "overlap."))

    parser.add_argument("-s", "--sort-by", default='backlink',
                        help=("Function to sort linkographs by"))

    args = parser.parse_args()

    # construct a dictionary, whose keys are the linkographs and
    # values are the corresponding dictionary-list provided by
    # count_linkographs.

    linkos_count_dict = {}

    for linko_name in args.linkos:

        linko=lc.readLinkoJson(linko_name)

        sublinko_counts = count_sublinkos(linko=linko,
                                          min_linko_size = args.min_linko_size,
                                          max_linko_size = args.max_linko_size,
                                          overlap= args.no_overlap,
                                          function=le.linkoToEnum)


        linkos_count_dict[linko_name] = sublinko_counts

        # Graph the results.
        graph_sublinko_counts(sublinko_counts,
                              sort_key=orderings[args.sort_by],
                              width=1)
