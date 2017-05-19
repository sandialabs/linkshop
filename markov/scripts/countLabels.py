#!/usr/bin/env python3

"""Determine if all the labels appear roughly the same number of
times.


"""


import time
from collections import Counter
import linkograph.stats as stats
import markov.Model as markel


# Not going to use an ontology, but one needs to be defined for the
# markov models to produce linkographs.
ont = {}

# Make some simple labels. Does not really matter what they are.
absClasses = [str(i) for i in range(6)]

# Create 1000 models
models = []
for i in range(1000):
    seed = time.time()
    m=markel.genModel(6, absClasses=absClasses,
                      ontology=ont, seed=seed)

# Define the total count.for m in models:
freq = Counter()

# Make a linkograph with a 1000 nodes for each model and find the
# label count.
for m in models:
    linko = m.genLinkograph(1000)
    
    c = stats.totalLabels(linko)

    freq.update(c)

print(freq)
