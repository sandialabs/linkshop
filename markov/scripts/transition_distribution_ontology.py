#!/usr/bin/env python3

"""Investigates the distribution for link Markov models.

The link Markov model is based on the linking behavior of a given
linkograph. Since the links in a linkograph are determined by
ontology, the transition model is depending on the ontology. This
script investigages this relationship using next Markov models created
from the ontology.

This script was used to generate the Fixed Marov Model Randomly
Generated Using Ontology using the parameters -m 1 -M 100 -r 1000 -s 1
ontology.json (which is the v2 ontology).

"""

import argparse # For command line parsing.
import numpy as np # For matrices.
import time # For getting the time to use as a random seed.
import math # For modf.
import json # For manipulating json files.
import matplotlib.pyplot as plt # For graphing.
import markov.Model as markel
import linkograph.enumeration as lenumeration # For enumOnt. 

def generateLinkMarkovState(ontologySize, minLinkoSize, maxLinkoSize,
                            stepLinkoSize, runNum, precision=2,
                            timeSize=7):
    """Generate the stats on link models for all ontologies.

    inputs:

    ontologySize = The size of the ontologies to consider.

    minLinkoSize: the minimun number of nodes in the linkographs to
    consider.

    maxLinkoSize: the maximum number of nodes in the linkographs to
    consider. Note that the max is not included to match pythons
    convertions on lists and ranges.

    stepLinkoSize: the step size between minLinkoSize to maxLinkoSize
    for the number of linkographs to Consider.

    runNum:  the number of linkographs to consider for each linkograph
    size.

    precision = the number of decimals places to use for the Markov
    models.

    timeSize = the size of integers to use for seeding the random
    number generator used to generate linkographs.

    outputs

    a numOntology x numLinkos x ontologySize x ontologySize x 2 array
    where numLinkos is to the floor of ((maxLinkoSize - 1) -
    minLinkoSize) // stepLinkoSize, ontologySize is the size of the
    ontology used by the given model, and numOntologies is
    (ontologySize)**(2*(ontologySize)). The first dimension is for the
    linkograph size. For example, an i in this dimension selects the
    linkograph of size minLinkoSize + i*stepLinkoSize. The second and
    third dimensions give the link in the link Markov model. Thus, a
    (j, k) in these two dimensions represent the link (j, k) in the
    tMatrix of the link Markov model. The fourth dimension selects the
    mean or standard deviation. A 0 is the mean and 1 is the standard
    devation. Thus, the (i, j, k, 0) entry is the mean over all the
    links from the ith abstraction class to the jth abstraction class
    for linkNum linkograph of size minLinkoSize + i*stepLinkoSize. A
    similar statement holds for the (i, j, k, 1) and the standard
    deviation.

    """

    numOntologies = ontologySize**(2*ontologySize)

    linkoSizes = range(minLinkoSize, maxLinkoSize, stepLinkoSize)
    
    results = np.zeros((numOntologies, len(linkoSizes), ontologySize,
                        ontologySize, 2))

    # Use a modularCounter to loop through all the ontologies
    enumCounter = lenumeration.modularCounter(ontologySize,
                                              ontologySize**2)
    
    # Loop through all the ontogies with ontologySize.
    for i in range(numOntologies):
        # Generate the ontology.
        ont = enumeration.enumOnt(enum)

        # Generate the Markov model to use for generating linkographs.
        seed = int(math.modf(time.time())[0]*(10**timeSize))
        
        model = genModelFromOntology(ontology, precision=precision,
                                     seed=seed)
        
        results[i, :, :, :, :] = genSingleOntologyState(minLinkoSize,
                                                        maxLinkoSize,
                                                        stepLinkoSize,
                                                        model, runNum,
                                                        precision=precision)

        # Increment the enumCounter
        enumCounter.inc()

def genSingleOntologyStats(minLinkoSize, maxLinkoSize, stepLinkoSize,
                           model, runNum, precision=2):
    """Generate the stats on link models for a given ontology.

    inputs:

    minLinkoSize: the minimun number of nodes in the linkographs to
    consider.

    maxLinkoSize: the maximum number of nodes in the linkographs to
    consider. Note that the max is not included to match pythons
    convertions on lists and ranges.

    stepLinkoSize: the step size between minLinkoSize to maxLinkoSize
    for the number of linkographs to Consider.

    model: the Markov model used to generate the linkographs. Note
    that the Markov model must have an ontology to generate the needed
    linkographs.

    runNum: the number of linkographs to consider for each linkograph
    size.

    precision:  the number of decimals places to use for the Markov
    models.

    output:

    a numLinkos x ontologySize x ontologySize x 2 array where
    numLinkos is to the floor of (maxLinkoSize -
    minLinkoSize)/stepLinkoSize and ontologySize is the size of the
    ontology used by the given model. The first dimension is for the
    linkograph size. For example, an i in this dimension selects the
    linkograph of size minLinkoSize + i*stepLinkoSize. The second and
    third dimensions give the link in the link Markov model. Thus, a
    (j, k) in these two dimensions represent the link (j, k) in the
    tMatrix of the link Markov model. The fourth dimension selects the
    mean or standard deviation. A 0 is the mean and 1 is the standard
    devation. Thus, the (i, j, k, 0) entry is the mean over all the
    links from the ith abstraction class to the jth abstraction class
    for linkNum linkograph of size minLinkoSize + i*stepLinkoSize. A
    similar statement holds for the (i, j, k, 1) and the standard
    deviation.

    """

    linkoSizes = range(minLinkoSize, maxLinkoSize, stepLinkoSize) 

    ontSize = len(model.ontology)

    results = np.zeros((len(linkoSizes), ontSize, ontSize, 2))

    # For each size linkograph, generate the runNum links and caculate
    # the needs statistics.
    for size in linkoSizes:
        # currentModels packs the transition matrix for each run into
        # a single matrix.
        currentModels = np.zeros((ontSize, ontSize, runNum))
        print('Processing linkographs of size {0}'.format(size))
        for i in range(runNum):
            # Change the state.
            model.state = model.random.randint(1,
                                               len(model.absClasses))
            model.state -= 1

            linko = model.genLinkograph(size)
            newModel = markel.genModelFromLinko(linko,
                                                precision=precision,
                                                ontology=model.ontology,
                                                seed=None,
                                                method='link_predictor',
                                                linkNum=1)

            currentModels[:, :, i] = newModel.tMatrix

        # Find the mean of each transition across the different runs.
        index = (size - minLinkoSize) // stepLinkoSize
        results[index, :, :, 0] = np.mean(currentModels, axis=-1)

        # Find the standard deviation across the difference runs.
        results[index, :, :, 1] = np.std(currentModels, axis=-1)

    return results


def genLinkMarkov(linkoSize, model, precision=2, timeSize=7):
    """Generates a link Markov from model generated linkograph.

    inputs:

    linkoSize: the size of linkograph to base the link Markov model
    off of.

    model: the Markov model to use. Note that the model must have an
    ontology in order to generate the linkgraphs.

    precicision: the number of decimal places to use for the
    link Markov model.

    timeSize = the size of integers to use for seeding the random
    number generator of the returned Markov model.

    output:

    A link Markov model based off a linkoSize linkograph generated by
    the provided Markov model.

    """

    seed = int(math.modf(time.time())[0]*(10**timeSize))

    # generate the linkograph
    linko = model.genLinkograph(linkoSize)

    # create the link model
    model = genModelFromLinko(linko, precision=precision,
                              ontology=model.ontology, seed=seed,
                              method='link_predictor', linkNum=1)
    
    return model

if __name__ == '__main__':

    info = "Investigates the distribution of link markov models."

    parser = argparse.ArgumentParser(description=info)
    parser.add_argument('ontology', metavar='ONTOLOGY.json',
                        nargs=1,
                        help='the ontology file.')

    parser.add_argument('-m', '--minimum', type=int, default = 2,
                       help='minimum size of linkographs.')

    parser.add_argument('-M', '--maximum', type=int, default = 100,
                       help='maximum size of linkographs.')

    parser.add_argument('-s', '--step', type=int, default = 1,
                       help='step size of linkographs.')

    parser.add_argument('-r', '--runs', type=int, default = 100,
                        help='the number of runs.')

    parser.add_argument('-p', '--precision', type=int, default = 2,
                        help='the number of runs.')

    parser.add_argument('--graphLimit', type=int, default = 10,
                        help=('The minimum number of graphs'
                              ' before graphs are grouped.'))

    parser.add_argument('--graphGroupSize', type=int, default = 10,
                        help='The number of graphs to group.')


    args = parser.parse_args()

    # Extract the ontology
    ont = None
    with open(args.ontology[0], 'r') as ontFile:
        ont = json.load(ontFile)

    seed = int(math.modf(time.time())[0]*(10**7))

    model = markel.genModelFromOntology(ont,
                                        precision=args.precision,
                                        seed=seed)

    results = genSingleOntologyStats(minLinkoSize=args.minimum,
                                     maxLinkoSize=args.maximum,
                                     stepLinkoSize=args.step,
                                     model=model,
                                     runNum=args.runs,
                                     precision=args.precision)

    # Create graphs for each of the transitions
    # legend = []
    # for initAbs in model.absClasses:
    #     for termAbs in model.absClasses:
    #         legend.append(initAbs + ' -> ' + termAbs)


    exceedLimit = len(model.tMatrix)**2 > args.graphLimit

    linkoSizes = range(args.minimum, args.maximum, args.step)

    for row in range(len(model.tMatrix)):
        for col in range(len(model.tMatrix)):
            plt.figure(row*len(model.tMatrix) + col)
            initClass = model.absClasses[row]
            termClass = model.absClasses[col]
            plt.subplot(211)
            plt.plot(linkoSizes, results[:, row, col, 0])
            plt.xlabel('Size of Linkograph')
            plt.ylabel('Mean')
            plt.title('Mean Versus Size of Linkograph for Link: '
                      '{0} -> {1}'.format(initClass, termClass))

            plt.subplot(212)
            plt.plot(linkoSizes, results[:, row, col, 1])
            plt.xlabel('Size of Linkograph')
            plt.ylabel('Standard Deviation')
            plt.title('Standard Deviation Versus Size of Linkograph'
                      ' for link: {0} -> {1}'.format(initClass, termClass))

            plt.tight_layout()

            groupSize = args.graphGroupSize
            exceedGroupSize = (row*len(model.tMatrix) + col) % groupSize == (groupSize-1)

            if exceedLimit and exceedGroupSize:
                plt.show()


    plt.show()
