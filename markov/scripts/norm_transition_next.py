#!/usr/bin/env python3

"""Entry-wise comparison of link and next Markov models.

This script was used to generated the figure in the Link-Predictor
Markov as a Next State Predictor section on the Markov Models
page. The parameters were to pass in all session linkographs.

"""

import numpy as np
import matplotlib.pyplot as plt
import argparse
import linkograph.linkoCreate as lc
import markov.Matrix as marktrix

#---------------------------------------------------------------------

def load(linkoNames):
    """Load the linkographs."""
    # Load the data
    linkos = [lc.readLinkoJson(lName) for lName in linkoNames]

    return linkos

def getMarkovs(linkos):
    """Generate the link and next Markov models."""
    # Create markovs
    tmarkovs = []
    nmarkovs = []
    for i in range(len(linkos)):
        tmarkovs.append(marktrix.createMarkov(linkos[i],
                                              linkNum=1,
                                              precision=2,
                                              method='link_predictor'))

        nmarkovs.append(marktrix.createMarkov(linkos[i],
                                              linkNum=1,
                                              precision=2,
                                              method='behavioral'))

    return tmarkovs, nmarkovs

def maxesAndMins(tmarkovs, nmarkovs):
    """Find the max and min entry-wise differences."""
    
    # Calculate the min  and max of entry-wise difference
    maximums = np.zeros(len(tmarkovs))
    minimums = np.zeros(len(tmarkovs))
    for i in range(len(linkos)):
        maximums[i] = marktrix.maxEntryAbs(tmarkovs[i], nmarkovs[i],
                                           zeros=False)

        minimums[i] = marktrix.minEntryAbs(tmarkovs[i], nmarkovs[i],
                                           zeros=False)

    return maximums, minimums

def graphMaxMin(maximums, minimums, linkos):
    """Graph the max and min entry-wise differences."""
    linkoNum = np.arange(len(linkos))

    # Make a figure
    plt.figure(1)

    # Plot maxes
    plt.subplot(311)
    plt.plot(linkoNum, maximums)
    plt.title('Maximum Difference Between Link-Predictor and Behavioral Markov')
    plt.xlabel('Session number')
    plt.ylabel('Maximum value.')
    plt.axis([0, max(linkoNum), -0.1, 1.1])
    plt.xticks(linkoNum)
    plt.grid()

    # Plot mins
    plt.subplot(312)
    plt.plot(linkoNum, minimums)
    plt.title('Minimum Difference Between Link-Predictor and Behavioral Markov')
    plt.xlabel('Session number')
    plt.ylabel('Minimum value.')
    plt.axis([0, max(linkoNum), -0.1, 1.1])
    plt.xticks(linkoNum)
    plt.grid()
    
    # Plot size of ontology
    ontologySize=[len(l.appearanceList()) for l in linkos]
    plt.subplot(313)
    plt.plot(linkoNum, ontologySize)
    plt.title('Number of Labels that Appear in the Linkograph.')
    plt.xlabel('Session number')
    plt.ylabel('Number of Labels')
    plt.axis([0, max(linkoNum), -0.1, 7.1])
    plt.xticks(linkoNum)
    plt.grid()
    
    plt.tight_layout()
    plt.show()



def distance(tmarkovs, nmarkovs, ord='fro'):
    """Calculate the distance based off the ord norm.

    inputs:

    tmarkovs: a list of markov models.

    nmakrovs: a list of markov models.

    ord: order of norm as used by numpy.linalg.norm.

    returns: a list of the corresponding distances of the absolute
    value of the difference, that is, the i-th distance is the norm of
    abs(tmarkovs[i] - nmarkovs[i]).

    """

    dist = np.zeros(len(tmarkovs))
    for i in range(len(linkos)):
        dist[i] = np.linalg.norm(tmarkovs[i] - nmarkovs[i],
                                     ord=ord)

    return dist

def graphNorms(normPair, linkos, includeSize=True):
    """Graph the max and min entry-wise differences."""
    linkoNum = np.arange(len(linkos))

    subFigure = includeSize or (len(normPair)>1)

    numFigures = len(normPair)
    if includeSize:
        numFigures += 1
        
    numColumns = 1
    initialFigure = 1

    spNum = [numFigures, numColumns, initialFigure]

    # Make a figure
    plt.figure(1)

    for normName, values in normPair:
        if subFigure:
            plt.subplot(*spNum)
        plt.plot(linkoNum, values)
        plt.title(normName + ' Difference Between Link-Predictor and'
                  + ' Behavioral Markov')
        plt.xlabel('Session number')
        plt.ylabel(normName + ' value.')
        plt.axis([0, max(linkoNum), -0.1, (1.1)*np.max(values)])
        plt.xticks(linkoNum)
        plt.grid()
        spNum[2] += 1

    if includeSize:
        # Plot size of ontology
        ontologySize=[len(l.appearanceList()) for l in linkos]
        plt.subplot(*spNum)
        plt.plot(linkoNum, ontologySize)
        plt.title('Number of Labels that Appear in the Linkograph.')
        plt.xlabel('Session number')
        plt.ylabel('Number of Labels')
        plt.axis([0, max(linkoNum), -0.1, 7.1])
        plt.xticks(linkoNum)
        plt.grid()

    plt.tight_layout()
    plt.show()


if __name__ == '__main__':
    info = ("Entry-wise comparison of link-predictor and behavioral"
            " Markov models.")

    parser = argparse.ArgumentParser(description=info)
    parser.add_argument('linkographs', metavar='LINKO.json',
                        nargs='+',
                        help='the linkograph file.')

    args = parser.parse_args()

    linkos = load(args.linkographs)
    tmarkovs, nmarkovs = getMarkovs(linkos)
    maximums, minimums = maxesAndMins(tmarkovs, nmarkovs)
    graphMaxMin(maximums, minimums, linkos)

    frobenius = distance(tmarkovs, nmarkovs, ord='fro')
    infinity = distance(tmarkovs, nmarkovs, ord=np.inf)
    l1 = distance(tmarkovs, nmarkovs, ord=1)
    l2 = distance(tmarkovs, nmarkovs, ord=2)

    normPairs = [('Frobenius', frobenius),
                 ('Infinity Norm', infinity),
                 ('L1 Norm', l1),
                 ('L2 Norm', l2)]

    for i in range(2):
        graphNorms(normPairs[2*i:2*(i+1)], linkos, includeSize=False)
