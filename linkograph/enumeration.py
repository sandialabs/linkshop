#!/usr/bin/env python3

"""Functions for enumerating linkographs and ontologies.

An enumeration is a counting or listing of objects. An enumeration of
the linkographs can be constructed using a pair (len,enc) where len is
the number of nodes (or length of the linkograph) and enc is an
encoding of which links are present. The encoding of the links is
based off assigning a power of two to each of the possible backlinks
and adding them. The backlink for node 1 is the 2^0 power and
corresponds to the link (0,1). The backlinks for node 2 are the powers
2^1, 2^2, and 2^3 corresponding to the links (0,2), (1,2), and (2,2),
respectively. In general the link (b,f) corresponds to the power of
two 2^p where p = b+totalLinks(f). The function totalLinks(n) returns
the total possible links for a linkograph on n nodes and is given by
n(n-1)/2.

"""
import argparse  # For command line parsing.
import json
import random
from decimal import * # For rounding metrics.
from linkograph.stats import totalLinks # Gives the total links.
from linkograph.stats import totalLinkographs # Gives total linkographs
from linkograph import linkoCreate # For creating linkographs.
from linkograph import linkoDrawSVG # For drawing linkographs.
from linkograph import stats # For linkograph metrics.

class invalidEnumerationObject(Exception):

    """Exception that occurs when an invalid enumeration is passed."""

    def __init__(self, description):
        """Record description of error that occured."""
        self.description = description

    def __str__(self):
        """Return representation of actual description."""
        return repr(self.description)


def linkoToEnum(linko):
    """Converts the linkograph to the enumeration.

    Arguments:
    linko -- the linkograph to convert.

    Return:
    (len, enc) -- the enumeration.
    """

    # Get the number of nodes.
    length = len(linko)

    # Initialize the encoding.
    enc = 0

    # The trivial case
    if length == 0:
        return (0,0)

    # Loop through all the backlinks.
    for (nodeNum, entry) in enumerate(linko):
        backlinks = entry[1]

        enc += sum([2**(x + totalLinks(nodeNum)) for x in backlinks])


    return (length, int(enc))

def enumToLinko(enum):
    """Converts a linkograph enumeration to a linkograph.

    Arguments:
    enum -- an enumeration (length, enc) for a linkograph.

    Retstriction:
    length >= 0, enc < 2^(length*(legth-1)/2) the total number of
    linkographs on length nodes. The second inequality is strict since
    the enumeration starts counting at 0.

    Return:
    linkoCreate.Linkograph -- the corresponding linkograph.

    """

    # Name the components of enum.
    length, enc = enum

    # Check for valid enumeration
    if enc >= totalLinkographs(length):
        raise invalidEnumerationObject("The enumeration does not"
                                       " correspond to a linkograph")

    # Initialize the linkograph.
    linko = [(set(), set(), set()) for n in range(length)]

    # Keep track of the node and backlink.
    node, link = 1, 0

    while enc > 0:

        # Test for bit
        if enc & 1 == 1:
            # Add backlink
            linko[node][1].add(link)

            # Add forelink
            linko[link][2].add(node)

        # Shift off the bit.
        enc >>= 1

        # Increment the link.
        link += 1
        if link == node:
            node, link = node+1, 0

    return linkoCreate.Linkograph(linko)


def enumOnt(enum, absClasses=None):
    """ Take an enumeration of labeled onotlogies and returns the ontology.

    A list, enum, of the form [a0, ..., a(n-1)] corresponds to the
    labeled graph which has labels '0', '1', ..., 'n-1' and edges that
    are encoded in the following way: writing the integer ai in binary
    ai = 'bk...b3b2b1' indicates there is an edge between 'i' and 'j'
    if and only if bj is 1.

    The absClasses option allows the user to specify the abstraction
    classes. Only the first length of enum classes are used. It is an
    error to have fewer abstraction classes.

    """

    if absClasses is None:
        absClasses = list(range(len(enum)))
    else:
        absClasses = absClasses[:len(enum)]

    # Make the ontology classes.
    ont = {str(aClass): [] for aClass in absClasses}

    for abs, i in zip(absClasses, enum):

        index = 0

        while i > 0:

            currentAbs = absClasses[index]

            # Test for bit.
            if i & 1 == 1:
                # Add in the edge
                ont[str(abs)].append(str(currentAbs))

            # Shift off the bit
            i >>= 1

            #increment the index.
            index += 1


    return ont


def ontEnum(ontology):
    """ Converts an ontology to the enumeration.

    Arguments:

    ontology -- The ontology to convert.

    Returns:

    [a0, ..., a(n-1)] -- An encoding of the ontology.

    """
    pass


def frequency(length, ontology, function=None, absClasses=None,
              samples=None, random=False, seed=None):
    """Finds the linkographs produced by the ontology.

    Finds the number of derived linkographs that map to the same value
    under the given function.

    Arguments:

    length -- the number of nodes for the linkograph.
    ontology -- the ontology to condier.
    function -- the function to compute on the linkographs. The range
    must be a type that can be used as a key to a dictionary.
    absClasses -- optional set of classes if the ontology does not
    contain all the abstraction classes of interest.
    samples -- The number of labelings to generate. Assigning None set
    samples to (sizeOfAbastrctionClasses)**length, which is the number
    of different possible labelings.
    random -- If False, then the labelings are considered according to
    an internal counter. If True, the labelings are randomly selected.
    seed -- seed for the interal random number generator.

    Returns:

    {functionValue: count} -- a dictionary with keys the function's
    value and values the number of times a linkograph is produced with
    that value.

    """

    # Set the default function.
    if function is None:
        function = lambda x : linkoToEnum(x)

    # Create the count dictionary.
    freq = {}

    # If the length is zero, then the empty linkograph is the only
    # possible linkograph and there is only one possible labeling (the
    # empty labeling).
    if length == 0:
        # Create an empty linkograph.
        linko0_0 = enumToLinko((0,0))
        freq[function(linko0_0)] = 1
        return freq

    # Get the abstraction classes.
    if absClasses is None:
        absClasses = [key for key in ontology.keys()]

    # Labelings are provided by the help of a modularCounter. This is
    # and n-element counter that counts in modular arithmetic where
    # the base can be specified.
    counter = modularCounter(length, len(absClasses), seed=seed)

    # Set the number of labelings to consider if a limit is not
    # provided.
    if samples is None:
        samples = len(absClasses)**length

    # Loop through the possible labelings.
    for n in range(samples):

        # Convert the current count on the modularCounter to a
        # labeling for the given abstraction class.
        invLabeling = counter.toInverseLabeling(absClasses)

        # Create the linkograph based on the labeling and the
        # ontology.
        linko = linkoCreate.createLinko(invLabeling, ontology)

        # Find the value of the function.
        value = function(linko)

        # Record the count.
        currentCount = freq.get(value)
        if not currentCount:
            freq[value] = 1
        else:
            freq[value] = currentCount + 1


        if random:
            # Randomize the count
            counter.randomize()
        else:
            # Increment the modularCounter
            counter.inc()

    return freq

def subLinkographFrequency(linkos, size, overlap=True, function=None):
    """ Finds the frequency of linkographs that appear as sublinkographs.

    Determines the number of sublinkographs from the list linkographs
    that have the same value under the given function.

    Arguments:

    linkos -- a list of linkographs to find subgraphs for.

    size -- the size of the sublinkographs.

    overlap -- if True, finds all sublinkographs of the given size. If
    False, starts with the first sublinkograph of the given size and
    finds the next sublinkograph such the sublinkographs do not overlap.

    Returns:

    {functionValue: count} -- a dictionary with keys the function's
    value and values the number of times a linkograph is produced with
    that value.

    """

    # Set the defualt function.
    if function is None:
        function = lambda x : linkoToEnum(x)

    # Create the count dictionary
    freq = {}

    # For each linkograph.
    for linko in linkos:

        # Define the initial lower and upper bounds.
        lb, ub = 0, size-1

        # Determine the steps to the next linkograph.


        for currentNode in range(size, len(linko) + 1):

            # Create sublinkograph.
            sublinkograph = linkoCreate.createSubLinko(linko,
                                                       lowerBound = lb,
                                                       upperBound = ub)

            # Find the value of the function.
            value = function(sublinkograph)

            # Record the count.
            currentCount = freq.get(value)
            if not currentCount:
                freq[value] = 1
            else:
                freq[value] = currentCount + 1

            # Update bounds.
            if overlap:
                lb, ub = lb+1, ub+1
            else:
                lb, ub = ub+1, ub + size

            # If the ub exceeds the last node, then stop, there are no
            # more linkographs of the given size.
            if ub > len(linko) -1:
                break

    return freq


def histogram(length, ontology, function=None, absClasses=None,
              samples=None, random=False, seed=None):
    """Finds the linkographs produced by the ontology.

    Finds every derived linkograph on length nodes according to the
    given ontology and groups them according to their value under the
    function. The return type is a dictionary so the range of the
    function needs to be a type that can be used as a key for the
    dictionary.

    Arguments:

    length -- the number of nodes for the linkograph.
    ontology -- the ontology to consider.
    function -- the function to apply to the linkographs. The range
    must be a type that can be used as a key to a dictionary.
    absClasses -- optional set of classes if the ontology does not
    contain all the abstraction classes of interest.
    samples -- The number of labelings to generate. Assigning None set
    samples to (sizeOfAbastrctionClasses)**length, which is the number
    of different possible labelings.
    random -- If False, then the labelings are considered according to
    an internal counter. If True, the labelings are randomly selected.
    seed -- seed for the interal random number generator.

    Returns:

    {functionValue: linkographEnumList} -- a dictionary with keys the
    values of the function and values the list of linkograph enums
    that map to the function value.

    """

    if function is None:
        function = linkoToEnum

    # Create the count dictionary.
    hist = {}

    # Get the abstraction classes.
    if absClasses is None:
        absClasses = [key for key in ontology.keys()]

    # Labelings are provided by the help of a modularCounter. This is
    # and n-element counter that counts in modular arithmetic where
    # the base can be specified.
    counter = modularCounter(length, len(absClasses))

    # Set the number of labelings to consider if a limit is not
    # provided.
    if samples is None:
        samples = len(absClasses)**length

    # Loop through the possible labelings.
    for n in range(samples):

        # Convert the current count on the modularCounter to a
        # labeling for the given abstraction class.
        invLabeling = counter.toInverseLabeling(absClasses)

        # Create the linkograph based on the labeling and the
        # ontology.
        linko = linkoCreate.createLinko(invLabeling, ontology)

        # Convert the linkograph into an integer.
        enum = linkoToEnum(linko)

        # Get the value of the function.
        value = function(linko)

        # Check if the value has been seen before.
        cachedSet = hist.get(value)
        if not cachedSet:
            hist[value] = {tuple(counter.toLabeling(absClasses))}
        else:
            hist[value].add(tuple(counter.toLabeling(absClasses)))

        if random:
            # Randomize the count
            counter.randomize()
        else:
            # Increment the modularCounter
            counter.inc()

    return hist


class modularCounter(list):
    """ Uses a list of n elements and counts in modular arithmetic."""

    def __init__(self, len, mod, seed=None):
        super().__init__([0 for x in range(len)])
        self.mod = mod
        self._random = random.Random(x=seed)

    def inc(self):
        self[0] += 1

        currentIndex = 0

        while self[currentIndex] == self.mod:
            # Zero out the current value and increment the nex value.
            self[currentIndex] = 0
            currentIndex +=1

            if currentIndex == len(self):
                break
            self[currentIndex] += 1

    def toInverseLabeling(self, absClass):
        """Creates an inverse labeling based on each entry.

        Considers the count as a list of len(modularCounter) commands,
        that is a list of commands that is the same size as the number
        of entries in the modularCounter object. The inverse labeling
        produced is the one that assigns the ith label in absClass (an
        ordered list of labels) to the nth entry in the modularCounter
        if modularCounter[n] = i. Thus, the object that is returned is
        a dictionary: { label: [index list] } where label is an entry
        of absClass and [index list] is the list of indecies i in
        modularCounter such that absClass[modularCounter[i]] = label.

        Thought of another way, the modularCount is a list of number
        where each number corresponds to the labled in absClass that
        the entry should be labeled by.

        """

        # Create an empty inverseLabeling.
        inverseLabeling = {}

        for (index,entry) in enumerate(self):
            # Get the label.
            label = absClass[entry]

            indexList = inverseLabeling.get(label)

            if not indexList:
                inverseLabeling[label] = [index]
            else:
                indexList.append(index)

        return inverseLabeling

    def toLabeling(self, absClass):
        """Converts the counter to a labeling."""

        return [absClass[n] for n in self]

    def randomize(self):
        """Randomize the modular count."""
        newState = [self._random.randrange(0, self.mod)
                    for _ in self]
        self[:] = newState

######################################################################
#----------------------- Command Line Programs -----------------------

def cli_linkoToEnum():
    """ Command line interface for linkoToEnum. """

    info = 'Converts linkograph to the associated linkograph enum.'

    parser = argparse.ArgumentParser(description=info)
    parser.add_argument('linko', metavar='LINKOGRAPH.json',
                        help='The linkograph to convert.')

    args = parser.parse_args()

    linko = linkoCreate.readLinkoJson(args.linko)

    if linko is not None:
        enum = linkoToEnum(linko)
        print('{}'.format(enum))

def cli_enumToLinko():
    """ Command line interface for enumToLinko. """

    info = 'Converts a linkograph enum to a linkograph.'

    parser = argparse.ArgumentParser(description=info)
    parser.add_argument('length', metavar='LENGTH', type=int,
                        help='The number of nodes, or a in (a,b)')

    parser.add_argument('num', metavar='NUMBER', type=int,
                        help='The linkograph number, or b in (a,b)')

    parser.add_argument('-f', '--file',
                        help='The file to print the linkograph to.')

    parser.add_argument('-d', '--draw', action='store_true',
                        help='Outputs an SVG with defualt sizing.')

    parser.add_argument('-s', '--suppress', action='store_true',
                        help='Suppress the creation of the json.')

    args = parser.parse_args()

    linko = enumToLinko((args.length, args.num))

    if args.file is None:
        name = 'linko{}_{}'.format(args.length, args.num)
    else:
        name = args.file

    if not args.suppress:
        linkoCreate.writeLinkoJson(linko, '{}.json'.format(name))

    if args.draw:
        linkoDrawSVG.linkoDrawSVG(linko, '{}.svg'.format(name))

def cli_enumOnt():
    """ Command line interface for enumOnt. """
    pass

# Defins a map of keywords to function for use in cli utitlities.
def functionMap():
    functions={
        'Shannon': lambda x: '{0:10.8f}'.format(stats.graphEntropy(x)),
        'enum': linkoToEnum
    }

    functionHelp=('Shannon (Shannon entropy applied to the'
                  ' linkograph), '
                  'enum (The enumeration for the linkograph).')

    return functions, functionHelp


def cli_frequency():
    """ Command line interface for frequency. """

    # Load the possible functions.
    functions, functionHelp = functionMap()

    info = ('Finds the frequency of the function values for each'
            'possible linkograph given an ontology.\n{}'.format(functionHelp))

    parser = argparse.ArgumentParser(description=info)
    parser.add_argument('length', metavar='LENGTH', type=int,
                        nargs=1,
                        help='The number of nodes.')

    parser.add_argument('ontology', metavar='ONTOLOGY.json',
                        nargs=1,
                        help='The ontology.')

    parser.add_argument('-a', '--abstraction',
                        help='The abstraction classes.')

    parser.add_argument('-f', '--function', metavar='FUNCTION',
                        help=('The function to apply to each'
                              ' linkograph.'))

    parser.add_argument('-j', '--json', action='store_true',
                        help=('Use json format.'))

    args = parser.parse_args()

    if args.function is not None:
        choice = args.function
    else:
        choice = 'enum'

    # Read in the ontology.
    ont = None
    with open(args.ontology[0], 'r') as ontFile:
        ont = json.load(ontFile)

    if ont is not None:
        freq = frequency(args.length[0], ont, functions[choice], args.abstraction)
    else:
        return

    if args.json:
        print(json.dumps(freq, indent=4))
    else:
        for entry in freq.keys():
            print('{}\t{}'.format(entry, freq[entry]))

def cli_subLinkographFrequency():
    """ Command line interface for subLinkographFrequency. """

    # Load the possible functions.
    functions, functionHelp = functionMap()

    info = ('Finds the frequency of the funtion value consider all'
            'sublinkographs of a linkograph.\n{}'.format(functionHelp))

    parser = argparse.ArgumentParser(description=info)
    parser.add_argument('linko', metavar='LINKOGRAPH.json',
                        nargs=1,
                        help='The linkograh.')

    parser.add_argument('size', metavar='SIZE', type=int,
                        nargs=1,
                        help='The number of nodes for the sublinkographs.')

    parser.add_argument('-o', '--overlap', action='store_true',
                        help='The abstraction classes.')

    parser.add_argument('-f', '--function', metavar='FUNCTION',
                        help=('The function to apply to each'
                              ' linkograph.'))

    parser.add_argument('-j', '--json', action='store_true',
                        help=('Use json format.'))

    args = parser.parse_args()

    if args.function is not None:
        choice = args.function
    else:
        choice = 'enum'

    # Read in the linkograph
    linko = linkoCreate.readLinkoJson(args.linko[0])

    if linko is not None:
        # Note: the linkograph has to be passed as a list.
        freq = subLinkographFrequency([linko], args.size[0], args.overlap, functions[choice])
    else:
        return

    if args.json:
        print(json.dumps(freq, indent=4))
    else:
        for entry in freq.keys():
            print('{}\t{}'.format(entry, freq[entry]))

def cli_histogram():
    """ Command line interface for the histogram function. """

        # Load the possible functions.
    functions, functionHelp = functionMap()

    info = ('Finds a histogram of each linkograph for an'
            ' ontology.\n{}'.format(functionHelp))

    parser = argparse.ArgumentParser(description=info)
    parser.add_argument('length', metavar='LENGTH', type=int,
                        nargs=1,
                        help='The number of nodes.')

    parser.add_argument('ontology', metavar='ONTOLOGY.json',
                        nargs=1,
                        help='The ontology.')

    parser.add_argument('-a', '--abstraction',
                        help='The abstraction classes.')

    parser.add_argument('-f', '--function', metavar='FUNCTION',
                        help=('The function to apply to each'
                              ' linkograph.'))

    parser.add_argument('-j', '--json', action='store_true',
                        help=('Use json format.'))

    args = parser.parse_args()

    if args.function is not None:
        choice = args.function
    else:
        choice = 'enum'

    # Read in the ontology.
    ont = None
    with open(args.ontology[0], 'r') as ontFile:
        ont = json.load(ontFile)

    if ont is not None:
        hist = histogram(args.length[0], ont,
                         functions[choice],
                         args.abstraction)
    else:
        return

    if args.json:
        print(json.dumps(freq, indent=4))
    else:
        for entry in hist.keys():
            print('{}\t{}'.format(entry, hist[entry]))
