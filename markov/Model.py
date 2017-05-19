#!/usr/bin/env python3

"""The Markov Model class."""

import argparse
import numpy as np # For matrices
import random # For random numbers
import itertools # For an accumulation loop
import bisect # For the bisect function
import linkograph.linkoCreate as lc # For manipulating linkographs
import linkograph.linkoDrawASCII as llda # For printing ascii linkographs
import markov.Matrix as tm # For Markov matrix functions.
import json # For reading from and writing to json files.
import decimal # Used to avoid loss of precision in JSON.

import markov.Matrix # For the static matrix mehtods.

class baseModelError(Exception):
    """The base model error class."""
    pass

class ShapeError(baseModelError):
    """Error indicating the transition array is not 2x2."""
    def __init__(self, message):
        super().__init__(message)

class OntologyError(baseModelError):
    """Error for a missing ontology."""
    def __init__(self, message):
        super().__init__(message)

class Model():
    """Markov model.

    A markov model can be interpreted as a square matrix M where each
    entry is bewteen 0 and 1 (inclusive), and each row sums to 1. In
    this interpretation, the probability of moving from state i to
    state j is M(i,j).

    """

    def __init__(self, array, absClasses=None, initial=None,
                 ontology=None, seed=None):
        """Create a markov model.

        inputs:

        array -- a 2 dimensional array representing the transitional
        probabilities.

        absClasses -- a list of the abstraction classes. Defaults to
        labeling each node as an integer. If an ontology is passed,
        and absClasses is None, then absClasses will be set to a
        sorted list of the ontology's abstraction classes. Note that
        the absClasses list provides the order the classes are stored
        in the transition matrix (tMatrix). By specifying this list
        explicity, you control the order of the classes used in the
        transition matrix. Furthermore, the absClass list can be
        larger than the ontology, so the ontology does not need to
        include all the abstraciton class names, if absClasses is
        provided.

        initial -- the initial state of the markov model.

        ontology -- an ontology to generate linkographs.

        """
        
        # Create the random number generator
        self.random = random.Random(x=seed)

        # Initialize the matrix portion
        self.tMatrix = np.array(array)

        # Check the dimensions
        if self.tMatrix.ndim != 2:
            raise ShapeError('Matrix must be two dimensional.')

        size = self.tMatrix.shape[0]

        # Check shape
        if self.tMatrix.shape != (size, size):
            raise ShapeError('Dimensions must be equal.')

        # Define the weigth list
        self.cumDist = self.tMatrix.cumsum(axis=1)

        # Define the abstraction classes if none are passed.
        if absClasses is None:
            if ontology is not None:
                # Define the abstraction classes from the ontology
                # keys
                absClasses = list(ontology.keys())

                # Sort the keys
                absClasses.sort()

                # Note that the correct number of abstraction classes
                # is checked later
            else:
                absClasses = [num for num in range(size)]

        # Check that there are enough state labels if defined
        if (absClasses is not None) and size != len(absClasses):
            raise ShapeError('Abstraction classes dimension does not'
                             'match matrix dimension')
        else:
            self.absClasses = absClasses

        # Initial state
        if initial is None:
            self.state = self.random.randint(0, size-1)
        else:
            #index = self.state.index(state)
            self.state = self.absClasses.index(initial)

        # Set the ontology
        self.ontology = ontology

    def __str__(self):
        """String representation of the model."""

        modelStr = str(self.absClasses) + '\n'

        modelStr += str(self.tMatrix)

        return modelStr

    def _next(self):
        """Provides next state index."""

        # Modified from an example in the Python 3 documenation for
        # package random

        stateCumDist = self.cumDist[self.state]
        value = self.random.random()*stateCumDist[-1]

        self.state = bisect.bisect(stateCumDist, value)

        return self.state

    def next(self):
        """Provides next state label."""
        # Note that the call to _next changes the current state.
        return self.absClasses[self._next()]

    def current(self):
        """Get the current state."""
        return self.absClasses[self.state]

    def setCurrent(self, absClass):
        """Set the current state."""
        self.state = self.absClasses.index(absClass)

    def inverseLabeling(self, size):
        """Generates an inverseLabeling of the given size."""

        # Initialize inverse labeling
        invLabeling = {self.absClasses[i]: []
                          for i in range(len(self.absClasses))}

        for nextNode in range(size):
            nextLabel = self.next()

            # Add the nextNode to the node list for nextLabel
            invLabeling[nextLabel].append(nextNode)

        return invLabeling

    def genLinkograph(self, n, ontology=None):
        """Generate a linkograph on n-nodes."""

        # If no ontology is passed, use one stored in the model.
        if ontology is None:
            ontology = self.ontology

        # If the model did not have an ontology either, then raise an
        # error.
        if ontology is None:
            raise OntologyError('Model does not have ontology.')


        invLabel = self.inverseLabeling(n)

        linko = lc.createLinko(invLabel, ontology)

        # Set the linkographs labels to ensure same order as the
        # abstraction classes used in the model
        linko.labels = self.absClasses

        return linko

    def minEntryAbs(self, otherModel, zeros=True):
        """The entry-wise minimum is absolute value.

        Return the minimum of the entry-wise difference in absolute
        value between self and otherModel . The zeros keywords filters
        out entries where both entries are zero. However, if all
        entries are zero, the 0.0 is returned.

        This function is a wrapper for markov.Matrix.minEntryAbs.

        """

        return markov.Matrix.minEntryAbs(self.tMatrix,
                                         otherModel.tMatrix,
                                         zeros=zeros)

    def maxEntryAbs(self, otherModel, zeros=True):
        """The entry-wise maximum is absolute value.

        Return the maximum of the their entry-wise difference in
        absolute value between self and otherModel. The zeros keywords
        filters out entries where both entries are zero. However, if
        all entries are zero, the 0.0 is returned.

        This function is a wrapper for markov.Matrix.maxEntryAbs.

        """

        return markov.Matrix.maxEntryAbs(self.tMatrix,
                                         otherModel.tMatrix,
                                         zeros=zeros)

    def dist(self, otherModel, ord='fro'):
        """Calculates the distance based off the ord norm.

        inputs:

        otherModel: the Markov model to compare to.

        ord: order of the norm as used by numpy.linalg.norm.

        returns: the distance between the tMatrices of self and
        otherModel. More specifiicaly, calculates the norm of the
        self.tMatrix, otherModel.tMatrix.

        """

        return np.linalg.norm(self.tMatrix - otherModel.tMatrix,
                              ord=ord)

    def norm(self, ord='fro'):
        """Calculates the norm bassed of the ord norm.

        inputs:

        ord: order of the norm as used by numpy .linalg.norm.

        returns: the norm of the tMatrix.

        """

        return np.linalg.norm(self.tMatrix, ord=ord)

    def toDot(self, precision=2):
        """Prints a dot representation of the model."""

        return markov.Matrix.markovToDot(self.tMatrix,
                                         self.absClasses,
                                         precision=precision)

    def toLatex(self, precision=2):
        """Prints a LaTex representation of the model."""

        return markov.Matrix.markovToLatex(self.tMatrix,
                                           self.absClasses,
                                           precision=precision)

    def toOntology(self):
        """Converts the tMatrix to an ontology."""

        l = self.absClasses

        size = len(self.tMatrix)

        ont = {l[i]: [l[j] for j in range(size)
                      if self.tMatrix[i][j] > 0 ]
               for i in range(size)}

        return ont

######################################################################
#------------------------- Static Functions --------------------------
######################################################################

def genModel(size, absClasses=None, ontology=None, precision=2, seed=None):
    """Generate a markov model.

    inputs:

    size: the number of states for the markov model.

    absClasses: a list of the abstraction classes. If no classes are
    supplied, then the abstraction classes are defined by the
    ontology. If no ontology is provided as wel, then the absctraction
    classes are given natural number names. If the size is less than
    the number of classes, then the first 'size' classes are taken. If
    not enough classes are provide, then the remaining classes will be
    filled with natural numbers.

    ontology: an associated ontology.

    output: newModel

    newModel: a markov model.

    precision: the number of decimal points used to describe the
    transition matrix for the markov model.

    seed: a seed for the internal random number generator.

    """

    ranGen = random.Random(x=seed)

    if absClasses is None:
        if ontology is not None:
            absClasses = list(ontology.keys())
            absClasses.sort()
        else:
            absClasses = [str(i) for i in range(size)]

    _adjustClassSize(size, absClasses)

    # Build the transition array.
    transitions = np.zeros((size, size))

    for i in range(size):
        transitions[i:] = _generateTransitionRow(size,
                                                 randomGenerator=ranGen,
                                                 precision=precision)

    return Model(transitions, absClasses=absClasses,
                 ontology=ontology, seed=seed)

def _adjustClassSize(size, absClasses):
    """Adjusts absClasses to be of length size."""
    if len(absClasses) < size:
            newAbsClasses = [str(i) for i in range(len(absClasses), size)]
            absClasses.extend(newAbsClasses)
    else:
        absClasses = absClasses[0:size]

def _generateTransitionRow(size, randomGenerator=None, precision=2):
    """Generate a row of the transitions matrix."""

    if randomGenerator is None:
        randomGenerator = random
    
    # Choose size - 1 points in the interval 0 to 1.
    choices = np.zeros(size-1)

    for i in range(size-1):
        value = np.round(randomGenerator.random(), decimals=precision)
        while value in choices:
            value = np.round(randomGenerator.random(), decimals=precision)

        choices[i] = value

    choices.sort()

    transitions = np.zeros(size)

    transitions[-1] = np.round(1 - choices[-1], decimals=precision)
    transitions[0] = choices[0]
    
    for i in range(1, size-1):
        transitions[i] = np.round(choices[i] - choices[i-1], decimals=precision)

    return transitions

def genModelFromOntology(ontology, precision=2, seed=None):
    """Generate a markov model using the transitions in an ontology."""

    ranGen = random.Random(x=seed)

    absClasses = list(ontology.keys())

    absClasses.sort()

    size = len(absClasses)

    # Build the transition array.
    transitions = np.zeros((size, size))

    for i in range(size):
        nonZeros = ontology[absClasses[i]]

        if len(nonZeros) == 0:
            continue

        if len(nonZeros) == 1:
            values = [1]
        else:
            values = _generateTransitionRow(len(nonZeros),
                                        randomGenerator=ranGen,
                                            precision=precision)

        # Assign the values to the transition in the ontology
        count = 0
        for j in range(size):
            if absClasses[j] in nonZeros:
                transitions[i, j] = values[count]
                count = count + 1

    return Model(transitions, absClasses=absClasses,
                 ontology=ontology, seed=seed)

def genModelFromLinko(linko, precision=2, ontology=None, seed=None,
                      method='link_predictor', linkNum=1):
    """Generate a Markov model from a linkograph."""

    # Get the transition matrix
    matrix = tm.createMarkov(linko, linkNum=linkNum, method=method,
                             precision=precision)

    absClasses = linko.labels

    return Model(matrix, absClasses=absClasses, ontology=ontology,
                 seed=seed)

######################################################################
#-------------------------- JSON Interface ---------------------------
# The basic philosophy of the JSON serialization is to use a diction
# from with keys the models attributes and value, their value. Most
# values are straightforward except the random attribute. To serialize
# this, we use the getState function, which returns a tuple (value,
# (values, ...), value), that is, it is a 3-tuple whose second entry
# is another tuple.

# Attributes: absClasses, cumDist, random, state, tMatrix, ontology

def writeJson(markov, fileName):
    """Encode Model markov in JSON format and write to fileName."""
    jsonString = writesJson(markov)
    with open(fileName, 'w') as file:
        file.write(jsonString)

def writesJson(markov):
    """Encode Model markov in JSON format and write to string."""
    serial = dict()
    serial['absClasses'] = markov.absClasses
    serial['cumDist'] = list(markov.cumDist.flatten())
    serial['random'] = markov.random.getstate() # can be serialized
    serial['state'] = markov.state
    serial['tMatrix'] = list(markov.tMatrix.flatten())
    serial['ontology'] = markov.ontology
    return json.dumps(serial, indent=4)

def readJson(jsonFile):
    """Decode Model from JSON encoded file jsonFile."""
    with open(jsonFile, 'r') as file:
        return readsJson(file.read())

def readsJson(jsonString):
    """Read Model from JSON encoded string jsonString."""
    serial = json.loads(jsonString)

    absClasses = serial['absClasses']
    cumDist = serial['cumDist']
    random = serial['random']
    state = serial['state']
    tMatrix = serial['tMatrix']
    ontology = serial['ontology']

    # Convert cumDist to type np.array
    size = len(absClasses)
    parsedCumDist = np.array(cumDist).reshape((size, size))

    # Convert random to tuples form the lists JSON uses
    parsedRandom = (random[0], tuple(random[1]), random[2])

    # Convert tMatrix to type np.array
    tMatrix = np.array(tMatrix).reshape((size, size))

    newModel = Model(tMatrix, absClasses=absClasses,
                     ontology=ontology)

    # Adjust the random portion
    newModel.cumDist = parsedCumDist
    newModel.random.setstate(parsedRandom)

    # Adjust the current state
    newModel.state = state
    
    return newModel

######################################################################
#---------------------- Command Line Interface -----------------------

def cli_genModel():
    """Command line interface for genModel."""

    info = """Generates a random Markov model."""

    parser = argparse.ArgumentParser(description=info)
    parser.add_argument('size', metavar='SIZE',
                        type=int,
                        help=('The number of states'
                              '(abstraction classes)'))
    parser.add_argument('-m', '--model', metavar='MODEL.json',
                        help='File name to store model to.')

    parser.add_argument('-a', '--absClasses',
                        metavar='ABSTRACTION_CLASS.json',
                        help='The abstraction classes to use.')

    parser.add_argument('-o', '--ontology', metavar='ONTOLOGY.json',
                        help='Add an associated ontology.')

    parser.add_argument('-p', '--precision', metavar='PRECISION',
                        type=int, default=2,
                        help=('Number of decimal places to use in'
                              ' probabilities.'))

    parser.add_argument('-s', '--seed', metavar='SEED', type=float,
                        default=None,
                        help=('Seeed for models internal random'
                              ' number generator.'))

    args = parser.parse_args()

    ont = None
    if args.ontology is not None:
        with open(args.ontology, 'r') as ontFile:
            ont = json.load(ontFile)

    absClasses = None
    if args.absClasses is not None:
        with open(args.absClasses) as absClassesFile:
            absClasses = json.load(absClassesFile)

    model = genModel(args.size,
                     absClasses=absClasses,
                     ontology=ont,
                     precision=args.precision,
                     seed=args.seed)

    if args.model is not None:
        writeJson(model, args.model)
    else:
        print(model)

def cli_genModelFromOntology():
    """Command line interface for genModelFromOntology."""

    info="""Creates a Markov model using an ontology."""

    parser = argparse.ArgumentParser(description=info)

    parser.add_argument('ontology', metavar='ONTOLOGY.json',
                        help='Add an associated ontology.')

    parser.add_argument('-m', '--model', metavar='MODEL.json',
                        help='File name to store model to.')

    parser.add_argument('-p', '--precision', metavar='PRECISION',
                        type=int, default=2,
                        help=('Number of decimal places to use in'
                              ' probabilities.'))

    parser.add_argument('-s', '--seed', metavar='SEED', type=float,
                        default=None,
                        help=('Seeed for models internal random'
                              ' number generator.'))

    args = parser.parse_args()

    ont = None
    with open(args.ontology, 'r') as ontFile:
        ont = json.load(ontFile)

    model = genModelFromOntology(ontology=ont,
                                 precision=args.precision,
                                 seed=args.seed)

    if args.model is not None:
        writeJson(model, args.model)
    else:
        print(model)


def cli_genModelFromLinko():
    """Command line interface for genModelFromLinko."""

    info="""Generates a Markov model from a linkograph. There are two methods
    for generating the model: link_predictor and behavioral. The
    link_predictor method generates the probabilities based on the
    links and the behavioral method generates the probabilities based
    on the following or preceeding event. """

    parser = argparse.ArgumentParser(description=info)
    parser.add_argument('linko', metavar='LINKOGRAPH.json',
                        help='The linkograph to learn from.')
    
    parser.add_argument('-m', '--model', metavar='MODEL.json',
                        help='File name to store model to.')

    parser.add_argument('-o', '--ontology', metavar='ONTOLOGY.json',
                        help='Add an associated ontology.')

    parser.add_argument('-p', '--precision', metavar='PRECISION',
                        type=int, default=2,
                        help=('Number of decimal places to use in'
                              ' probabilities.'))

    parser.add_argument('-b', '--backward',
                        action='store_true',
                        help=('Consider back links or previous'
                              ' steps'))

    parser.add_argument('--method', metavar='METHOD',
                        default='link_predictor',
                        help="Methods are 'link_predictor' or 'behavioral'")

    parser.add_argument('-s', '--seed', metavar='SEED', type=float,
                        default=None,
                        help=('Seeed for models internal random'
                              ' number generator.'))

    args = parser.parse_args()

    linko=lc.readLinkoJson(args.linko)

    ont = None
    if args.ontology is not None:
        with open(args.ontology, 'r') as ontFile:
            ont = json.load(ontFile)

    linkNum = 1
    if args.backward:
        linkNum = 0

    model = genModelFromLinko(linko,
                              precision=args.precision,
                              ontology=ont,
                              seed=args.seed,
                              method=args.method,
                              linkNum=linkNum)

    if args.model is not None:
        writeJson(model, args.model)
    else:
        print(model)

def cli_markovToDot():
    """Command line interface for Model.toDot"""

    info="""Creates a dot file representation of the Markov model."""

    parser = argparse.ArgumentParser(description=info)
    parser.add_argument('model', metavar='MODEL.json',
                        help='The Markov model')

    parser.add_argument('-o', '--out', metavar='OUT.dot',
                        help='Dot file to print to.')

    args = parser.parse_args()

    model = readJson(args.model)

    modelDot = model.toDot()

    if args.out is not None:
        with open(args.out, 'w') as outFile:
            outFile.write(modelDot)

    else:
        print(modelDot)

def cli_genLinkograph():
    """Command line interface for Model.genLinkograph"""

    info = """Create a linkograph based off the Markov model."""

    parser = argparse.ArgumentParser(description=info)

    parser.add_argument('model', metavar='MODEL.json',
                        help='The Markov model')

    parser.add_argument('size', metavar='SIZE', type=int,
                        help='The size of the linkograph.')

    parser.add_argument('-o', '--ontology',
                        help='Ontology to use for linkograph.')

    parser.add_argument('-f', '--file', metavar='LINKO.json',
                        help='Output json file.')

    parser.add_argument('-a', '--ascii',
                        action='store_true',
                        help='Print linkograph as ASCII.')

    uhelp="""Updates models random state. This options allows for multiple calls
    to this function to result in different linkographs. Note this
    option permanently changes MODEL.json"""

    parser.add_argument('-u', '--updateState',
                        action='store_true',
                        help=uhelp)

    args = parser.parse_args()

    model = readJson(args.model)

    ont=None
    if args.ontology:
        with open(args.ontology, 'r') as ontFile:
            ont = json.load(ontFile)

    linko = model.genLinkograph(args.size,
                                ontology=ont)

    if args.updateState:
        writeJson(model, args.model)

    if args.file:
        lc.writeLinkoJson(linko, args.file)

    elif args.ascii:
        llda.linkoPrint(linko)

    else:
        print(linko)
