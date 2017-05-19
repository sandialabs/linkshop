#!/usr/bin/env python3

"""Find the frequencies of the sublinkographs."""

import argparse # For command line parsing
import math
from functools import wraps
import numpy as np
import matplotlib.pyplot as plt # For graphing
import matplotlib.cm as cm
import matplotlib.colors as colors
import linkograph.linkoCreate as lc # for reading linkographs.
import linkograph.enumeration as le # for enumerating linkographs
import linkograph.stats as ls # For graph entropy.

def count_sublinkos(linko, min_linko_size=2, max_linko_size=None,
                    overlap=True, function=ls.graphEntropy):
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

    function = precision_decorator(function)

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

def graph_sublinko_counts(sublinko_counts, minimum_size, name=None,
                          means=None, stds=None, sigma_num=1,
                          default_width=0.5,
                          require_default_width=False,
                          graph_counts=False):
    """Graph the sublinkograph counts."""

    # This should be restructored to not sort these lists multiple
    # times. Each list is sorted twice here and one later. This logic
    # takes each series of entropy values for each of the sizes, finds
    # the minimum distance between two succesive entropy values, and
    # then finds the minimum of each of these minimums.
    # width = min(min(np.array(sorted(size_counts.keys())[1:]) -
    #                 np.array(sorted(size_counts.keys())[:-1])) for
    #             size_counts in sublinko_counts)
    total_keys = {key
                  for counts in sublinko_counts
                  for key in counts.keys()}

    if require_default_width or len(total_keys) < 2:
        width = default_width
    else:
        total_keys = np.array(sorted(total_keys))
        width = min(total_keys[1:] - total_keys[:-1])

    norm = colors.Normalize(0, 1)
    max_heights = []
    chosen_colors = []
    labels_set = set()
    for series_num, size_counts in enumerate(sublinko_counts):

        def get_first_value(pair):
            return pair[0]

        # format data
        entropy, count = zip(*sorted(size_counts.items(),
                                     key=get_first_value))

        entropy = np.array(entropy)

        if not graph_counts:
            # Percentage of linkographs for this size
            count = np.array(count)/sum(count)

        max_heights.append(max(count))

        # if len(entropy) > 1:
        #     width = min(entropy[1:] - entropy[:-1])
        # else:
        #     width = 1

        labels = entropy
        labels_set = labels_set.union(entropy)

        locations = labels - (width/2)

        color = cm.jet(norm(series_num/len(sublinko_counts)))
        #import pdb; pdb.set_trace()
        chosen_colors.extend([color,color])

        size = minimum_size + series_num

        series_name = "Linkograph size {0}".format(size)

        plt.bar(locations, count, width, color=color,
                label=series_name)

        #plt.xticks(labels)

    ymax = 1.1 * max(max_heights)

    if means is not None:
        plt.vlines(means, 0, ymax,
                   colors=chosen_colors[0:-1:2],
                   linestyles="solid")

    if stds is not None:

        #std_pm = np.array(stds[series_num])
        std_pm = sigma_num * np.repeat(stds, 2)
        std_pm[1::2] = -1*std_pm[1::2]
        std_pm = np.repeat(means, 2) + std_pm



        plt.vlines(std_pm, 0, ymax, colors=chosen_colors,
                   linestyles="dashed")

    plt.legend()

    if graph_counts:
        title = "Shannon Entropy Histogram"
        plt.ylabel("Count")
    else:
        title = "Shannon Entropy Distributions"

        plt.ylabel("Normalized Count (Actual Count"
                   " / Total_Count_For_Size)")

    if name:
        title = name + ": " + title

    plt.title(title)
    plt.xlabel("Shannon Entropy")

    plt.xticks(sorted(list(labels_set)), rotation=45)

    plt.show()

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

def _unpack(sublinko_counts):

    means_stds = [ _mean_standard(dist) for dist in sublinko_counts]

    means, stds = zip(*means_stds)

    return means, stds

#############
#           #
# Decorator #
#           #
#############

# Wraps a function's output with decimal precision control.
def precision_decorator(f):
    @wraps(f)
    def wrapper(*args, precision=2, **kwds):
        return round(f(*args, **kwds), precision)
    return wrapper

if __name__ == "__main__":

    description="""Find the number of disinct sublinkgraphs."""

    parser = argparse.ArgumentParser(description=description)

    parser.add_argument("linkos", metavar="LINKOGRAPH.json",
                        nargs="+",
                        help="The linkographs to process.")

    parser.add_argument("-m", "--min_linko_size", type=int, default=2,
                        help="Minimum linkograph size to consider.")

    parser.add_argument("-M", "--max_linko_size", type=int,
                        help="Maximum linkograph size to consider.")

    parser.add_argument("-s", "-show-means-stds", action="store_true",
                        help=("Show lines marking the mean and standard"
                              " deviation."))

    parser.add_argument("-o", "--no-overlap", action="store_false",
                        help=("Do not allow sublinkographs to"
                              "overlap."))

    parser.add_argument("-n", "--sigma-num", type=int, default=1,
                        help=("Number of sigmas to for drawing the"
                              " dashed boundaries."))

    parser.add_argument("-c", "--counts", action="store_true",
                        help="Display counts.")

    args = parser.parse_args()

    # construct a dictionary, whose keys are the linkographs and
    # values are the corresponding dictionary-list provided by
    # count_linkographs.

    linkos_count_dict = {}

    for linko_name in args.linkos:

        linko=lc.readLinkoJson(linko_name)

        if len(linko) < args.min_linko_size:
            print(("linko in file {0} has length less then given minimum size"
                   " ({1}) and will not be processed.").format(linko_name,
                                                               args.min_linko_size))
            continue

        sublinko_counts = count_sublinkos(linko=linko,
                                          min_linko_size = args.min_linko_size,
                                          max_linko_size = args.max_linko_size,
                                          overlap= args.no_overlap,
                                          function=ls.graphEntropy)

        linkos_count_dict[linko_name] = sublinko_counts

        # # Graph the results.
        # graph_sublinko_counts(sublinko_counts, args.min_linko_size,
        #                       width=1)

    if args.s:
        means_stds_dict = {linko_name: _unpack(dist)
                           for linko_name, dist in
                           linkos_count_dict.items()}
    else:
        means_stds_dict = None


    for linko_name in args.linkos:

        if linko_name not in linkos_count_dict:
            continue

        sublinko_counts = linkos_count_dict[linko_name]

        if means_stds_dict is not None:
            means, stds = means_stds_dict[linko_name]
        else:
            means = stds = None

        # Graph the results.
        graph_sublinko_counts(sublinko_counts=sublinko_counts,
                              minimum_size = args.min_linko_size,
                              name=linko_name,
                              means=means,
                              stds=stds,
                              sigma_num=args.sigma_num,
                              graph_counts=args.counts)
