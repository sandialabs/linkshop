#!/usr/bin/env python3
"""Functions that operate on Markov matrices."""

import numpy as np # For matrices
import argparse  # For command line parsing.
import json  # For reading and writing to json files.
import sys # For stdout

from linkograph import linkoCreate

def createMarkov(linkograph, linkNum=1, method='link_predictor',
                 precision=2):
    """Creates a Markov model for the linkograph.

    """

    if method.lower() == 'link_predictor':
        return createLinkPredictorMarkov(linkograph, linkNum=linkNum,
                                precision=precision)
    elif method.lower() == 'behavioral':
        return createBehavioralMarkov(linkograph, linkNum=linkNum,
                                precision=precision)
    else:
        raise ValueError('Unrecognized method.')

def createLinkPredictorMarkov(linkograph, linkNum=1, precision=2):
    """Creates a Markov model for the linkograph.

    Creates a Markov model off the forelinks or the backlinks. To use
    forelinks, set linkNum = 1 (or leave off the option). To use
    backlinks use linkNum = 0.

    The entries in the Markov model give the likelilhood that an event
    with one abstraction class is linked to an event with another
    abstraction class. For example, if the Markov model gives a
    probability of 0.5 for a row labeled 'A' and column labeled 'B',
    then given an event labeled 'A' there is a 50% chance that this
    event has a link to an event labeled 'B'.

    """

    # create an index dictionary for the labels,
    # so that the index of label l can be found by
    # index['l'].
    # Note: if a linkograph is changed so that
    # the label index is used to label the entries
    # instead of the label itself, then this is
    # not really needed. Such a modification is
    # helpful if the number of labels is large.
    index = {entry[1]:entry[0] for entry in
                enumerate(linkograph.labels)}

    # create the markov chain
    markovSize = len(linkograph.labels)
    markov = np.zeros((markovSize, markovSize))

    # loop through the entries of the linograph.
    for entry in linkograph:
        # for each of the forelinks or backlinks, loop through the set
        # of labels for that link and increment the cooresponding
        # entry of the markov chain.
        for link in entry[linkNum+1]:
            for labellink in linkograph[link][0]:
                for labelentry in entry[0]:
                    markov[index[labelentry]][index[labellink]] += 1


    # normalize the markov chain
    row_sums = markov.sum(axis=1)

    # Account for possible zero rows:
    for (i,v) in enumerate(row_sums):
        if v == 0:
            row_sums[i] = 1

    markov  = np.round(markov / row_sums[:, np.newaxis], precision)

    return markov

def createBehavioralMarkov(linkograph, linkNum=1, precision=2):
    """Creates a Markov model for a linkograph based on next label.

    The entries in the Markov model give the likelilhood that an event
    with one abstraction class is followed or preceded by an event
    with another abstraction class. For example, if the Markov model
    gives a probability of 0.5 for a row labeled 'A' and column
    labeled 'B', then given an event labeled 'A' there is a 50% chance
    that this event is followed preceded by an event labeled 'B'.

    """

    # create an index dictionary for the labels,
    # so that the index of label l can be found by
    # index['l'].
    # Note: if a linkograph is changed so that
    # the label index is used to label the entries
    # instead of the label itself, then this is
    # not really needed. Such a modification is
    # helpful if the number of labels is large.
    labelIndex = {entry[1]:entry[0] for entry in
                enumerate(linkograph.labels)}

    # create the markov chain
    markovSize = len(linkograph.labels)
    markov = np.zeros((markovSize, markovSize))

    # Get those entries that have a previous or a next as appropriate
    if linkNum == 0:
        nextEntries = linkograph[1:]
        nextIndex = lambda x: x-1
    else:
        nextEntries = linkograph[:-1]
        nextIndex = lambda x: x+1

    # loop through the entries of the linograph.
    for (nodeIndex, entry) in enumerate(nextEntries):
        # Get the current labels
        cLabels = entry[0]

        # Get the next labels
        nextEntry = linkograph[nextIndex(nodeIndex)]
        nLabels = nextEntry[0]

        # For each current label and each next label increment the
        # markov model
        for cl in cLabels:
            for nL in nLabels:
                row = labelIndex[cl]
                column = labelIndex[nL]
                markov[row][column] += 1

    # normalize the markov chain
    row_sums = markov.sum(axis=1)

    # Account for possible zero rows:
    for (i,v) in enumerate(row_sums):
        if v == 0:
            row_sums[i] = 1

    markov  = np.round(markov / row_sums[:, np.newaxis], precision)

    return markov

def markovToDot(markov, labels, precision=2):
    '''Takes a markov chain and outputs a dot file representation.

    markov -- The markov chain (matrix)
    labels -- The labels.
    fh -- a file handle 

    '''
    dotString = ''

    # Header.
    header = ('digraph markov {\n'
              '  node [shape=oval,fontname="Helvetica",fontcolor=blue'
              ',fontsize=10];\n'
              '  edge [style=solid,color=black];')

    dotString += dotString + header + '\n'
    edge = ''
    for i in range(len(markov)):
        # Add the current label to ensure all labels are printed.
        dotString += labels[i] + '\n'
        edge = '  "' + labels[i] + '" ->'
        for j in range(len(markov)):
            value = round(markov[i][j], precision)
            # Only print link that have a non-zero probability.
            if (value > 0):
                dotString += edge + ' {"' + labels[j] + '"}\n'
                dotString += ' [label="' + str(value) +'"]\n'
    dotString += '}\n'

    return dotString

def markovToLatex(markov, labels, precision=2):
    """Prints the transition matrix in a latex format."""

    lstring = ''

    # print the labels
    lstring += '\\text{' + str(labels[0]) + '}'

    for i in range(1, len(labels)):
        lstring += ' \\text{ ' + str(labels[i]) + '}'

    lstring += '\\\\\n'

    # header
    lstring += '\\begin{bmatrix}\n'

    # print the transition matrix
    for i in range(len(markov)):

        rowstring = str(round(markov[i][0], precision))

        for j in range(1, len(markov)):
            value = round(markov[i][j], precision)
            rowstring += ' & {0}'.format(value)

        # add line termination \\ and \n
        lstring += rowstring + '\\\\\n'
    # footer
    lstring += '\\end{bmatrix}\n'

    return lstring

def minEntryAbs(m1, m2, zeros=True):
    """The entry-wise minimum is absolute value.

    Given two martrices m1 and m2, return the minimum of the their
    entry-wise difference in absolute value. The zeros keywords
    filters out entries where both entries are zero. However, if all
    entries are zero, the 0.0 is returned.

    """

    if zeros:
        return np.min(np.abs(m1-m2))
    else:
        result = [np.abs(x-y) for x, y in
                  zip(m1.flatten(), m2.flatten())
                  if x > 0 or y >0]

        if len(result) > 0:
            return np.min(result)
        else:
            return 0.0

def maxEntryAbs(m1, m2, zeros=True):
    """The entry-wise maximum is absolute value.

    Given two martrices m1 and m2, return the maximum of the their
    entry-wise difference in absolute value. The zeros keywords
    filters out entries where both entries are zero. However, if all
    entries are zero, the 0.0 is returned.

    """

    if zeros:
        return np.max(np.abs(m1-m2))
    else:
        result = [np.abs(x-y) for x, y in
                  zip(m1.flatten(), m2.flatten())
                  if x > 0 or y > 0]

        if len(result) > 0:
            return np.max(result)
        else:
            return 0.0

#----------------------- Command Line Programs -----------------------

def cli_markov():
    """Command line interface for creating markov chains."""

    info = 'Creates a transition matrix from a linkograph.'

    parser = argparse.ArgumentParser(description=info)

    parser.add_argument('linkograph', metavar='LINKOGRAPH.json',
                        nargs=1,
                        help='The linkograph')

    parser.add_argument('-o', '--out', metavar='OUTPUT_FILE',
                        help='Prints the result to a file.')

    parser.add_argument('-m', '--method',
                        help='The method used to create the model.')

    parser.add_argument('-f', '--forelinks', action='store_true',
                        help='Use forelinks')

    parser.add_argument('-b', '--backlinks', action='store_true',
                        help='Use backlinks')

    parser.add_argument('-d', '--dot', action='store_true',
                        help='Create dot file.')

    parser.add_argument('-l', '--latex', action='store_true',
                        help='Create latex file.')

    parser.add_argument('-t', '--transition', action='store_true',
                        help='Use transition matrix')

    parser.add_argument('-p', '--precision', type=int,
                        help='Number of digits retained.')

    args = parser.parse_args()

    linkNum = 1  # For forelinks.

    if args.backlinks:
        linkNum = 0 # For backlinks.

    if args.precision is None:
        args.precision = 2

    if args.method is None:
        args.method = 'link_predictor'

    linko = linkoCreate.readLinkoJson(args.linkograph[0])

    markovChain = createMarkov(linko, linkNum=linkNum,
                               method = args.method,
                               precision=args.precision)

    if args.out is not None:
        fh = open(args.out, 'w')
    else:
        fh = sys.stdout

    if args.transition:
        fh.write(str(linko.labels))
        fh.write('\n')
        fh.write(str(markovChain))
        fh.write('\n')
    elif args.latex:
        latexString = markovToLatex(markovChain, linko.labels,
                                args.precision)
        fh.write(latexString)
    else:
        # markovToDot(markovChain, linko.labels, fh,
        #             args.precision)

        dotString = markovToDot(markovChain, linko.labels,
                                args.precision)
        fh.write(dotString)

    fh.close()

#---------------------------------------------------------------------
if __name__ == "__main__":
    linko = linkoCreate.Linkograph([({'A'}, set(), {1,2,3,4}),
                                   ({'B'}, {0}, {4,5}),
                                   ({'C'}, {0}, {3,4}),
                                   ({'A'}, {0,2}, {5}),
                                   ({'B'}, {0,1,2}, set()),
                                   ({'C'}, {1,3}, set())],
                                  ['A', 'B', 'C'])

    m = createMarkov(linko)

    print(m)
