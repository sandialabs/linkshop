#!/usr/bin/env python3

"""Functions useful for processing means and stds."""

import math
import numpy as np

def _mean_standard_single(dist):
    """Find the mean and standard deviation of single record."""

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

def mean_standard(distributions):
    """Find the mean and standard of all records."""

    means_stds = [ _mean_standard_single(dist) for dist in distributions]

    means, stds = zip(*means_stds)

    return np.array(means), np.array(stds)

def dist_int(distributions):
    """Change the key of the distbrutions to an int."""
    ndistributions = [{float(key): value for key, value in dist.items()}
                      for dist in distributions]

    return ndistributions
