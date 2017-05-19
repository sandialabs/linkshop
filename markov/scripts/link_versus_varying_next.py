#!/usr/bin/env python3

"""Investigates the distribution for link Markov models.

The link Markov model is based on the linking behavior of a given
linkograph. Since the links in a linkograph are determined by
ontology, the transition model is depending on the ontology. This
script investigages this relationship using random next state models
generated from an ontology and linking with a different ontology.

This script was used to generate the results for the Modified V2
Ontology For Generating section. The parameters were -m 1 -M 100 -s 1
-r 1000 v2_ontology_non_absorbing.json ontology.json. Note that
ontology.json is the v2 ontology.

"""

import argparse # For command line parsing.
import numpy as np # For matrices.
import time # For getting the time to use as a random seed.
import math # For modf.
import json # For manipulating json files.
import matplotlib.pyplot as plt # For graphing.
import markov.Model as markel
import linkograph.enumeration as lenumeration # For enumOnt. 

def genSingleOntologyStats(ontNext, ontLink, minLinkoSize,
                           maxLinkoSize, stepLinkoSize, runNum,
                           precision=2, seeds=None):
    """Generate the stats on link models for a given ontology.

    inputs:

    ontNext: ontology used to generate Markov model that create the
    next state.

    ontLink: ontology used for constructing linkographs.

    minLinkoSize: the minimun number of nodes in the linkographs to
    consider.

    maxLinkoSize: the maximum number of nodes in the linkographs to
    consider. Note that the max is not included to match pythons
    convertions on lists and ranges.

    stepLinkoSize: the step size between minLinkoSize to maxLinkoSize
    for the number of linkographs to Consider.

    runNum: the number of linkographs to consider for each linkograph
    size.

    precision:  the number of decimals places to use for the Markov
    models.

    seeds: a list of seeds to use for the generated next Markov
    models. The size of the list should be the same as the number of
    runs.

    output:

    a numLinkos x ontologySize x ontologySize x 2 array where
    numLinkos is to the floor of ((maxLinkoSize - 1) - minLinkoSize)
    // stepLinkoSize and ontologySize is the size of the ontology used
    by the given model. The first dimension is for the linkograph
    size. For example, an i in this dimension selects the linkograph
    of size minLinkoSize + i*stepLinkoSize. The second and third
    dimensions give the link in the link Markov model. Thus, a (j, k)
    in these two dimensions represent the link (j, k) in the tMatrix
    of the link Markov model. The fourth dimension selects the mean or
    standard deviation. A 0 is the mean and 1 is the standard
    devation. Thus, the (i, j, k, 0) entry is the mean over all the
    links from the ith abstraction class to the jth abstraction class
    for linkNum linkograph of size minLinkoSize + i*stepLinkoSize. A
    similar statement holds for the (i, j, k, 1) and the standard
    deviation.

    """

    linkoSizes = range(minLinkoSize, maxLinkoSize, stepLinkoSize)

    ontSize = len(ontNext)
    absClasses = list(ontNext.keys())
    absClasses.sort()

    results = np.zeros((len(linkoSizes), ontSize, ontSize, 2))

    if seeds is None:
        seeds = [time.time() for i in range(runNum)]

    models = []
    # Create the generating models
    for i in range(runNum):
        m = markel.genModelFromOntology(ontology=ontNext,
                                        precision=2,
                                        seed=seeds[i])

        # Storing the model and the current state
        models.append(m)

    # For each size linkograph, generate the runNum links and
    # caculate the needed statistics.
    for size in linkoSizes:

        # currentModels packs the transition matrix for each run into
        # a single matrix.
        linkModels = np.zeros((ontSize, ontSize, runNum))
        print('size: {0}'.format(size))

        for i in range(runNum):

            m = models[i]
            
            # Randomize the initial state
            m.state = m.random.randint(1, len(m.absClasses)) - 1

            linko = m.genLinkograph(size, ontology=ontLink)

            newModel = markel.genModelFromLinko(linko,
                                                precision=precision,
                                                ontology=None,
                                                seed=None,
                                                method='link_predictor',
                                                linkNum=1)

            linkModels[:, :, i] = newModel.tMatrix

        # Find the mean of each transition across the different runs.
        index = (size - minLinkoSize)//stepLinkoSize
        results[index, :, :, 0] = np.mean(linkModels, axis=-1)

        # Find the standard deviation across the difference runs.
        results[index, :, :, 1] = np.std(linkModels, axis=-1)

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
    parser.add_argument('ontNext', metavar='ONTOLOGY_NEXT.json',
                        nargs=1,
                        help='the ontology file for producing.')

    parser.add_argument('ontLink', metavar='ONTOLOGY_LINK.json',
                        nargs=1,
                        help='the ontology file for learning.')

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
    ontNext = None
    with open(args.ontNext[0], 'r') as ontNextFile:
        ontNext = json.load(ontNextFile)

    ontLink = None
    with open(args.ontLink[0], 'r') as ontLinkFile:
        ontLink = json.load(ontLinkFile)

    seed = int(math.modf(time.time())[0]*(10**7))

    results = genSingleOntologyStats(ontNext=ontNext,
                                     ontLink=ontLink,
                                     minLinkoSize=args.minimum,
                                     maxLinkoSize=args.maximum,
                                     stepLinkoSize=args.step,
                                     runNum=args.runs,
                                     precision=args.precision)

    # Create graphs for each of the transitions
    # legend = []
    # for initAbs in model.absClasses:
    #     for termAbs in model.absClasses:
    #         legend.append(initAbs + ' -> ' + termAbs)


    absClasses = list(ontNext.keys())
    absClasses.sort()

    exceedLimit = len(ontNext)**2 > args.graphLimit

    linkoSizes = range(args.minimum, args.maximum, args.step)

    for row in range(len(ontNext)):
        for col in range(len(ontNext)):
            plt.figure(row*len(ontNext) + col)
            initClass = absClasses[row]
            termClass = absClasses[col]
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
            exceedGroupSize = (row*len(ontNext) + col) % groupSize == (groupSize-1)

            if exceedLimit and exceedGroupSize:
                plt.show()


    plt.show()
