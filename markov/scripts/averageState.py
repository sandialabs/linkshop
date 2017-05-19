#!/usr/bin/env python3


import argparse # For command line arguments
import numpy as np # For arrays
import time # For getting a random seed.
import math # For modf.
import json # For parsing json files
import matplotlib.pyplot as plt # For graphing values
from scipy import stats # To calculate the mode and frequency
import markov.Model as markel # To create Markov Models.

if __name__ == '__main__':

    info = "Numerically investigates the most likely states."

    parser = argparse.ArgumentParser(description=info)
    parser.add_argument('ontology', metavar='ONTOLOGY.json',
                        nargs=1,
                        help='the ontology file.')

    parser.add_argument('-m', '--minimum', type=int, default = 0,
                       help='minimum number of events.')

    parser.add_argument('-M', '--maximum', type=int, default = 100,
                       help='maximum number of events.')

    parser.add_argument('-s', '--step', type=int, default = 1,
                       help='step number of events.')

    parser.add_argument('-r', '--runs', type=int, default = 100,
                        help='the number of runs.')

    parser.add_argument('-p', '--precision', type=int, default = 2,
                        help='the number of runs.')

    targetModelHelp = ('Markov model to compare the tMatrices of the'
                       'markov models to. If specified then the'
                       'distance of the powers of the transitions'
                       'matrices is calculated and the average'
                       'distance for each power is graphed.')

    parser.add_argument('-t', '--targetModel',
                        metavar='TARGET_MODEL.json',
                        help=targetModelHelp)

    args = parser.parse_args()

    # Extract the ontology
    ont = None
    with open(args.ontology[0], 'r') as ontFile:
        ont = json.load(ontFile)

    tModel = None
    if args.targetModel:
        tModel = markel.readJson(args.targetModel)

    totalEvents = (args.maximum - args.minimum)//args.step

    # Record the events over the required number times for the
    # required number of runs. So the array is number_of_runs x
    # total_events size array.
    results = np.zeros((args.runs, totalEvents))

    # Difference from supplied transition matrix.
    if tModel:
        # The distance are a number_of_runs x total_events size
        # array. The (i, j) entry corresponds to the ditance from the
        # tModel of the j-th power of the i-th Markov model's
        # tMatrix.
        distances = np.zeros((args.runs, totalEvents))

    models = []

    for runNum in range(args.runs):

        # A new model is created for every run.
        seed = int(math.modf(time.time())[0]*(10**7))

        model = markel. genModelFromOntology(ont,
                                             precision=args.precision,
                                             seed=seed)

        if tModel:
            power = np.eye(len(model.absClasses))

        # Generate the first set of events that are not recorded
        for eventNum in range(args.minimum):
            model.next()

            if tranMatrix:
                # Calculate the next power.
                power = model.tMatrix.dot(power)

        # eventIndex = 0
        # results[runNum, eventIndex] = model.state # The state is an
        #                                           # integer.

        # Generate the rest of the events. Every event needs to be
        # generated, so the range does not use the step. The step will
        # just determine which events are eventually recorded.
        eventIndex = 0
        for eventNum in range(args.minimum, args.maximum):

            if (eventNum - args.minimum) % args.step == 0:
                # Record events every args.step
                results[runNum, eventIndex] = model.state

                if tModel:
                    # Store the distance.
                    difference = tModel.tMatrix - power
                    tmpDist = np.linalg.norm(difference, ord = 'fro')

                    distances[runNum, eventIndex] = tmpDist

                    # Calculate the next power.
                    power = model.tMatrix.dot(power)

                eventIndex += 1



            # Generating the next state at the allows us to consider
            # args.minimum like the zeroth event.
            model.next()


    # Find the mode for each number of steps
    modes, frequencies = stats.mode(results, axis=0)

    percentages = frequencies/runNum

    # The x-axis values to plot against
    x = np.arange(args.minimum, args.maximum, args.step)

    plt.figure(1)

    plt.subplot(211)
    plt.plot(x, modes.squeeze())
    plt.xlabel('Size of Linkograph')
    plt.ylabel('Most Frequent Event')
    plt.title('Most Frequent Events')
    plt.axis([args.minimum, args.maximum, 0, 1.1*(len(model.absClasses)-1)])

    plt.subplot(212)
    plt.plot(x, percentages.squeeze())
    plt.xlabel('Size of Linkograph')
    plt.ylabel('Fraction of Total Events')
    plt.title('The Fraction of Total Events')
    plt.axis([args.minimum, args.maximum, 0, 1.1])

    plt.tight_layout()
    plt.show()

    if tModel:

        # Calculate the average distance.
        aveDistances = np.mean(distances, axis=0)

        # Graph
        plt.plot(x, aveDistances)
        plt.xlabel('Powers of the Transition Matrix')
        plt.ylabel('Distance from Fixed Transitiion Matrix')
        plt.title('Limit of Powers of the Transition Matrix')

        plt.show()
