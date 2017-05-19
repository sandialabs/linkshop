#!/usr/bin/env python3

"""Investigation of behavioral Markov model convergence.

This script was used to produce the figure in the Markov Model
Convergence section of the Markov Model Profiling page. The
parameteres were: -m 1 ontology.json 10001. Note that only the
Distance of Generated Behavioral Model from Generating Markov Model
was used. The other figure was commented out.

"""

import numpy as np
import matplotlib.pyplot as plt
import argparse
import json
import linkograph.linkoCreate as lc
import markov.Model as markel
import numpy as np

if __name__ == "__main__":

    info = ("Investigation of behavioral Markov model convergence.")

    parser = argparse.ArgumentParser(description=info)
    parser.add_argument('ontology', metavar='ONTOLOGY.json',
                        nargs=1,
                        help='the ontology file.')

    parser.add_argument('max', metavar='MAX', type=int,
                        help=('the maximum size of the linkograph'
                             ' to consider'))

    parser.add_argument('-m', '--min', metavar='MIN', type=int,
                        default=1,
                        help=('the minimum size of the linkograph'
                             ' to consider'))
    parser.add_argument('-s', '--seed', type=int, default=42,
                        help='seed for the random number generator')

    parser.add_argument('-p', '--precision', type=int, default=2,
                        help='precision of the probabilities')
    
    args = parser.parse_args()

    # Read in ontology
    ont = None
    with open(args.ontology[0], 'r') as ontFile:
        ont = json.load(ontFile)

    # Get list of absClasses
    absClasses = list(ont.keys()).sort()

    # Generate model
    model = markel.genModel(len(ont), absClasses=absClasses,
                            ontology=ont, precision=args.precision,
                            seed=args.seed)

    # Get the random variable's state for resetting it.
    ranstate = model.random.getstate()

    nnorms = np.zeros(args.max - args.min + 1)
    tnorms = np.zeros(args.max - args.min + 1)

    for i in range(args.min, args.max + 1):

        # Reset the random variable's state
        model.random.setstate(ranstate)

        # Generate a linkograph
        linko = model.genLinkograph(i)

        # Generate Markov model
        genNModel = markel.genModelFromLinko(linko,
                                             precision=args.precision,
                                             method='behavioral')

        genTModel = markel.genModelFromLinko(linko,
                                             precision=args.precision,
                                             method='link_predictor')

        # Compare generated Markov model to Markov model's tMatrix
        nnorms[i-args.min] = model.dist(genNModel)
        tnorms[i-args.min] = model.dist(genTModel)

    # graph it
    # step = (args.max - args.min) // 5

    # labels = np.arange(args.min, args.max+1, step)
    # loc = labels - args.min

    linkoSizes = range(args.min, args.max + 1)

    plt.figure(1)
    # plt.subplot(211)
    # plt.plot(tnorms)
    # plt.title(('Distance of Generated Link-Predictor Model from'
    #            'Generating Model.'))
    # plt.xlabel('Size of Linkograph')
    # plt.ylabel('Distance')
    # plt.xticks(loc, labels)

    #plt.subplot(212)
    plt.plot(linkoSizes, nnorms)
    plt.title('Distance of Generated Behavioral Model from Generating Markov Model.')
    plt.xlabel('Size of Linkograph')
    plt.ylabel('Distance')
    #plt.xticks(loc, labels)

    plt.tight_layout()
    plt.show()
