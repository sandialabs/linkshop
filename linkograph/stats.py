#!/usr/bin/env python3

"""Statistics package for linkographs."""

from collections import Counter
from functools import reduce
from linkograph import linkoCreate
import math # For logs
import argparse  # For command line parsing.
import json
import numpy

def similarity(lg_0, lg_1):
    underlink_count = 0
    overlink_count = 0

    if len(lg_0) != len(lg_1):
        return None
    elif 1 == len(lg_0):
        return 0, 0, 1.0

    for node_index in range(len(lg_0)):
        node_0 = lg_0[node_index]
        node_1 = lg_1[node_index]
        for forelink in node_0[2]:
            if forelink not in node_1[2]:
                underlink_count += 1
        for forelink in node_1[2]:
            if forelink not in node_0[2]:
                overlink_count += 1

    possible_links = totalLinks(len(lg_0))
    accuracy = (possible_links - underlink_count - overlink_count) / possible_links

    return underlink_count, overlink_count, accuracy
    
def totalLinks(n):
    """Gives the number of possible links for a linkograph of size n."""

    # The number of possible links is just the triangle number for
    # n-1.

    return int(n*(n-1)/2)

def totalLinkographs(n):
    """Gives the total numebr of linkographs for n nodes."""

    # The total number of possible linkographs is 2^totalLinks(n).

    return 2**totalLinks(n)

def totalLabels(linkograph, lowerBound=None, upperBound=None):
    """Returns a diction with the frequency of each label.

    Tallies the number of times a label appears for an entry. Only
    labels that appear in at least one entry will be included. Note:
    the sum of the frequencies is not necessarily equal to the number
    of entries since there can be more than one label per entry. The
    lowerBound and upperBound limit the count to the range
    [lowerBound, UpperBound], that is the frequencies are counted
    between lowerBound and UpperBound, with both endpoints being
    inclusive.

    """

    freq = Counter()

    lowerBound, upperBound = boundDefaults(linkograph, lowerBound,
                                           upperBound)

    # Note: the upperBound+1 must be used for slicing since the slice
    # does not include the upper bound number.
    for entry in linkograph[lowerBound:upperBound+1]:
        for label in entry[0]:
            freq[label] += 1

    return freq

def percentageOfEntries(linkograph, lowerBound=None, upperBound=None):
    """Gives the percentage of entries that have each label.

    The return value is a dictionary that maps all labels with a
    non-zero percentage to their respective percentages. Note: that
    this implies a return values of {} when the linkograph contains no
    labels.

    """

    lowerBound, upperBound = boundDefaults(linkograph,
                                                   lowerBound,
                                                   upperBound)

    total = upperBound - lowerBound + 1

    if total <= 0:
        return {}

    return {k: v/total for k, v in totalLabels(linkograph,
                                               lowerBound,
                                               upperBound).items()}

def links(linkograph, lowerBound=None, upperBound=None):
    """The total number of links."""

    lowerBound, upperBound = boundDefaults(linkograph, lowerBound,
                                           upperBound)

    # This function will count the number of forelinks that are
    # greater than or equal to the lower bound and less than or equal
    # to the upper bound.
    # f = lambda entry: len({link for link in entry[2] if link >=
    #                        lowerBound and link <= upperBound})
    f = lambda entry: linkCount(entry, [2], lowerBound, upperBound)

    # The total number of links is the sum of the forelinks.
    # Note: for slicing, the upperBound+1 must be used to include the
    # node with index upperBound+1.
    return sum(map(f, linkograph[lowerBound: upperBound+1]))

def linkCount(tupleOfLists, listNumber, lowerBound, upperBound):
    """Counts the number of links in one of the lists passed.

    This function is a speciality function to aid in calculating
    statistics involving the number of links that lie in a given
    range. It is primarily intended as a private helper function. The
    parameters are:
    tupleOfLists -- usually a linkograph entry.
    listNumber -- a list of the indicies in entry that should be
                  considered.
    lowerBound -- the lowest index that should be considered.
    upperBound -- the highest index that should be considered.

    Example: a typical tupleOfLists is ({'A', 'B'}, {1,2}, {4,5}) a
    listNumber of [1] would only consider the links in {1,2}, a
    listNumber of [2] would only consider the links in {4,5} and a
    listNumber of [1,2] would consider the links in both {1,2}, and
    {4,5}.

    """

    summation = 0

    for index in listNumber:
        summation += len({link for link in tupleOfLists[index]
                          if link >= lowerBound
                          and link <= upperBound})

    return summation

def linkTotal(currentIndex, linkNumber, lowerBound, upperBound):
    """Calculates the total possible links for link entropies.

    This function is a specialty function for calculating the total
    number of possible links when considering the different link
    entropies of all links, forelinks, and backlinks.

    """

    size = 0

    # If 1 is in the linkNumber get the total for backlinks
    if 1 in linkNumber:
        size += currentIndex - lowerBound

    # If 2 is in the linkNumber get the total for forelinks
    if 2 in linkNumber:
        size += upperBound - currentIndex

    return size

def percentageOfLinks(linkograph, lowerBound=None, upperBound=None):
    """The percentage of links out the total possible links."""

    lowerBound, upperBound = boundDefaults(linkograph,
                                                 lowerBound,
                                                 upperBound)

    realLinks = links(linkograph, lowerBound, upperBound)

    possibleLinks = totalLinks(upperBound - lowerBound+1)

    if 0 == possibleLinks:
        result = None
    else:
        result = float(realLinks) / possibleLinks

    return result

def graphEntropy(linkograph, lowerBound=None, upperBound=None):
    """Calculates the shanon entropy for the complete linkograph.

    Given a linkograph, this function will calculate the shannon
    entropy associated with all the links involved (within the window
    [lowerBound, upperBound]). Thus, in a sense, it is the total
    entropy involved as opposed to the entropies calculated off of
    forelinks, backlinks, horizontal links, and similar entropies.

    """

    # The Linkograph version of Shannon entropy is given by
    # H = -(p_linked)*log_2(p_linked)-(p_unlinked)*log_2(p_unlinked)
    # Let t be the total number of possible links and l the number of
    # links present, then this formula can be re-written as
    # -(l/t)*log_2(l/t) - (1-l/t)*log_2(1-l/t)
    # which is what this function calculates.

    lowerBound, upperBound = boundDefaults(linkograph,
                                                 lowerBound,
                                                 upperBound)

    l = links(linkograph, lowerBound, upperBound)
    t = totalLinks(upperBound - lowerBound + 1)

    return shannonEntropy(l, t)

def shannonEntropy(links, totalLinks):
    """Calculates the shannon entropy for links and totalLinks"""

    l = links
    t = totalLinks

    if l >= t or l<=0 or t <= 0:
        return 0

    return -(l/t)*math.log(l/t, 2) - (1-l/t)*math.log(1-l/t, 2)


def linkEntropy(linkograph, listNumber=[1,2], delta=None,
                restrict=False, lowerBound=None, upperBound=None,
                lineNumbers=False):
    """Calculates total link, backlink, and forelink entropies.

    This function returns a list of link entropies for each node
    considered. Given a node, the total link entropy is the entropy
    associated with the number of forelinks and backlinks that the
    given nodes has. The backlink entropy is the entropy for the given
    node's backlinks. The forelink entropy is the entropy for the given
    node's forelinks.

    Parameters:
    linkograph -- the linkograph

    linkNumber -- set to [1] for backlinks, [2] for forelinks and
    [1,2] for all links

    restrict -- restrict all calculations to the subgraph

    lowerBound -- the lowest index to calculate the entropy

    upperBound -- the highest index to calculate the entropy

    delta -- the most offset from given index to consider

    The lowerBound and upperBound determine the range of nodes for
    which the entropy is calculated. The delta parameter determines
    the maximum number of nodes considered when calculating the
    entropy. For example, if the linkograph has 7 nodes and delta is
    set to 3, then the forelink entropy for node 0 only considers
    nodes 1, 2, and 3, not the full set of nodes 1 through 6 (the
    index of the highest node). If delta is left unset, then the full
    range of possible links is always considered. The restrict flag
    determines if all calculations are completely restricted to the
    subgraph determined by the lower and upper bounds.

    """

    return applySliceFunction(entropySlice,
                              linkograph,
                              listNumber,
                              delta,
                              restrict,
                              lowerBound,
                              upperBound,
                              lineNumbers)

def topCover(linkograph):
    if 0 == len(linkograph):
        return None

    ongoing = []
    percentageAtEach = [0]

    for idx, v in enumerate(linkograph[2:]):
        idx = idx + 1
        percentageAtEach.append(len(ongoing) / idx)
        if len(v[2]) > 0:
            ongoing.append(max(v[2]))
        ongoing = [x for x in ongoing if x > (idx+1)]

    if len(percentageAtEach) == 0:
        result = None
    else:
        result = reduce(lambda x,y: x + y, percentageAtEach) / len(percentageAtEach)

    return result

# humpiness takes each link and measures what percentage of the entire linkograph
# it covers. those numbers are aggregated to get the mean.
def meanLinkCoverage(linkograph):
    humpiness = []

    for idx, v in enumerate(linkograph[1:]):
        forelinks = v[2]
        ratios = list(map(lambda x: (x - idx) / len(linkograph), forelinks))
        if (len(ratios) > 0):
            humpiness.append(reduce(lambda x,y: x + y, ratios) / len(ratios))

    if 0 == len(humpiness):
        result = None
    else:
        result = reduce(lambda x,y: x + y, humpiness) / len(humpiness)

    return result

def entropyDeviation(linkograph):
    ents = linkEntropy(linkograph)
    es = numpy.array(ents)
    return numpy.std(es)

def entropySlice(entry, currentIndex, listNumber,
                 lowerBound, upperBound):

    l = linkCount(entry, listNumber, lowerBound, upperBound)
    t = linkTotal(currentIndex, listNumber, lowerBound, upperBound)

    return shannonEntropy(l, t)

def applySliceFunction(func, linkograph,
                      listNumber=[1,2], delta=None,
                      restrict=False, lowerBound=None,
                       upperBound=None, lineNumbers=False,
                       *kwargs):

    # Set the bounds.
    lowerBound, upperBound = boundDefaults(linkograph, lowerBound,
                                           upperBound)

    # Set the delta.
    if delta is None:
        delta = len(linkograph)-1

    # Collects the value for each node considered.
    values = []

    # Loop through the entries and calculate the value.
    # Note: one has to be added to the upper bound for the
    # slicing to ensure that element with index upperBound is
    # considered.
    for (offset, entry) in enumerate(linkograph[lowerBound:
                                                upperBound+1]):
        # The current index in the linkograph
        cindex = lowerBound + offset

        # The mininum index to consider
        minindex = max(cindex - delta, 0)
        
        # The maximum index to consider
        maxindex = min(cindex + delta, len(linkograph)-1)

        # If the restrict flag is True, restrict the bounds to the
        # subgraph.
        if restrict:
            minindex = max(minindex, lowerBound)
            maxindex = min(maxindex, upperBound)


        # l = linkCount(entry, listNumber, minindex, maxindex)
        # t = linkTotal(cindex, listNumber, minindex, maxindex)

        # entropy.append(shannonEntropy(l, t))

        currentValue = func(entry, cindex, listNumber,
                           minindex, maxindex, *kwargs)

        if lineNumbers:
            values.append((cindex, currentValue))
        else:
            values.append(currentValue)

    return values


def boundDefaults(linkograph, lowerBound, upperBound):
    """The common defualt bounds for most of the methods.

    The common bounds used for the methods are to have lowerBound at
    least 0, upperBound no more than len(linkograph)-1. Furthermore,
    if the upperBound is given, then linkograph[lowerBound,
    upperBound+1] gives the complete specified subgraph. For example,
    if a linkograph has 7 nodes (nodes 0 through 6) and the bounds are
    given as lowerBound=1 and upperBound=4, then the lowerBound is
    left at 1 and the upperBound is left at 4 so that the graph
    linkograph[lowerBound, upperBound+1] = linkograph[1,5] and
    contains the nodes 1 through 4.

    """

    if lowerBound is None:
        lowerBound = 0
    else:
        lowerBound = max(0, lowerBound)

    # The maximum bound is no more than the highest index. To ensure
    # this it is the len(linkograph)-1 that shoud be compared against.
    if upperBound is None:
        upperBound = len(linkograph)-1
    else:
        upperBound =min(len(linkograph)-1, upperBound)

    return lowerBound, upperBound

def entryToString(entry, currentIndex, listNumber,
                  lowerBound, upperBound):
    """Converts the links for a linkograph entry to a link string.

    Link string is not an official term, but what is meant is the
    string that has a 0 for no link and 1 for a link. So for example,
    if node 3 has backlinks {0,1} and forelinks {5,6,7} then the
    string is 110*0111 where the * is marking node 3. The star is not
    included in the string, but is shown here for clarity.
    """

    size = linkTotal(currentIndex, listNumber,
                     lowerBound, upperBound)

    preString = ['0' for x in range(size)]

    # The shiftAmount indicates how much the indecies above the
    # current index should be shifted. If the back links are not
    # present, then the currentIndex+1 is the first index that is
    # considered and so needs to be considered the 0 index in
    # preString.
    shiftAmount = currentIndex+1

    if 1 in listNumber:
        for index in [n for n in entry[1] if lowerBound <= n]:
            preString[index-lowerBound] = '1'
        shiftAmount = lowerBound + 1

    if 2 in listNumber:
        for index in [n for n in entry[2] if n <= upperBound]:
            preString[index-shiftAmount] = '1'

    return "".join(preString)

def linkographToString(lg):
    encoded_lg = ""
    for index in range(len(lg)-1):
        encoded_lg += entryToString(lg[index], index, [2], index, len(lg)-1)
    return encoded_lg

def tComplexity(stringList):
    """Calculates t-code complexity for a string."""

    sl = [[e] for e in stringList]

    mult = tComplexityRecurse(sl, [])

    return sum([math.log(m+1,2) for (cw, m) in mult])

def tComplexityRecurse(codeWords, codeMult):

    if len(codeWords) <= 1:
        return codeMult

    # get the next codeword
    nextCW = codeWords[-2]

    # count the consecutive multiplicity of the penultimate code word
    count = 1

    for cw in codeWords[-3::-1]:
        if cw != nextCW:
            break

        count += 1

    # add the code word and its multiplicity
    codeMult.append((nextCW, count))

    newCW = []

    acc = []
    cc = 0
    for cw in codeWords:
        acc.extend(cw)
        if cw == nextCW and cc < count:
            cc += 1
        else:
            newCW.append(acc)
            acc = []
            cc = 0

    codeWords[::] = newCW

    return tComplexityRecurse(codeWords, codeMult)

def tComplexitySlice(entry, currentIndex, listNumber,
                     lowerBound, upperBound, difference=False,
                     normalize=False):

    string = entryToString(entry, currentIndex, listNumber,
                           lowerBound, upperBound)

    result = tComplexity(string)

    if len(string) != 0:
        lowerBoundTComplexity = math.log(len(string), 2)
    else:
        lowerBoundTComplexity = 0

    if(difference):
        result = result - lowerBoundTComplexity

    if(normalize):
        if lowerBoundTComplexity != 0:
            result = result/lowerBoundTComplexity

    return result

def linkTComplexity(linkograph, listNumber=[1,2], delta=None,
                    restrict=False, lowerBound=None, upperBound=None,
                    lineNumbers=False, difference=False, normalize=False):

    return applySliceFunction(tComplexitySlice,
                              linkograph,
                              listNumber,
                              delta,
                              restrict,
                              lowerBound,
                              upperBound,
                              lineNumbers,
                              difference,
                              normalize)

def subgraphMetric(linkograph, metric, lowerThreshold=None,
                   upperThreshold = None, minSize=2, maxSize=None,
                   step=1, lowerBound=None, upperBound=None):
    """ Finds the subgraphs whose metric value is within a given interval.

    linkograph -- The linkograph to consider
    metric -- a graph metric function with signature (linkograph, lowerBound, upperBound)
    lowerThreshold -- the lowest value of the metric that is considered.
    upperThreshold -- the highest value of the metric that is
        considered.
    minSize -- the minimum size of subgraphs to consider.
    maxSize -- the maximum size of subgraphs to consider. If none, then max is the
               size of the linkograph.
    lowerBound -- the lowest bound to consider
    upperBound -- the highest bound to consider

    """

    lowerBound, upperBound = boundDefaults(linkograph, lowerBound,
                                           upperBound)

    if maxSize is None:
        maxSize = len(linkograph)

    else:
        maxSize = min(maxSize, len(linkograph))

    # The subgraphs are returned as a list of tuples (lowerBound, upperBound, metric value)
    graphs = []

    # Loop through the possible subgraphs. The value
    # upperBound-minSize+1 gives the largest index that can occur as a
    # lower bound to get a minSize subgraph. For example, if a minimum
    # size of 3 is required and last index is 21, then 21-3+1=19,
    # which gives the subgraph 19, 20, 21. A second 1 is added to
    # accomodate that the python range function does not include the
    # upper bound.
    for lowerIndex in range(lowerBound, upperBound-minSize+2, step):
        for upperIndex in range(lowerIndex+minSize-1,
                                min(lowerIndex+maxSize, upperBound+1)):
            metricValue = metric(linkograph, lowerIndex, upperIndex)

            # Flag to indicated when a subgraph has the required
            # metric value.
            include = True

            # Check if lower threshold is defined and value is not smaller.
            if (lowerThreshold is not None) and (metricValue <
                                               lowerThreshold):
                include &= False

            # Check if upper threshold is defined and value is not bigger.
            if (upperThreshold is not None) and (metricValue >
                                                upperThreshold):
                include &= False

            if include:
                graphs.append((lowerIndex, upperIndex, metricValue))

    return graphs

def linkDifference(linko):
    """The longest link from the nodes."""

    differences=[]

    for (node, entry) in enumerate(linko):
        if len(entry[2]) != 0:
            differences.append(max({fl - node for fl in entry[2]}))
        else:
            differences.append(0)


    return differences

def summaryDifference(linko):
    if 0 == len(linko):
        result = None
    else:
        result = sum(linkDifference(linko))/len(linko)

    return result

def percentLinkSlice(entry, currentIndex, listNumber,
                 lowerBound, upperBound):

    l = linkCount(entry, listNumber, lowerBound, upperBound)
    t = linkTotal(currentIndex, listNumber, lowerBound, upperBound)

    if t == 0:
        t = 1

    return l/t

def linkSlicePercents(linkograph, listNumber=[1,2], delta=None,
                      restrict=False, lowerBound=None,
                      upperBound=None, lineNumbers=False):
    """Finds the percentage of links for backlinks, forelinks, and both."""

    return applySliceFunction(percentLinkSlice,
                              linkograph,
                              listNumber,
                              delta,
                              restrict,
                              lowerBound,
                              upperBound,
                              lineNumbers)

def countCriticalNodes(linkograph, threshold):
    count = 0
    for node in linkograph:
        if len(node[1]) + len(node[2]) > threshold:
            count += 1
    return count

def calculateCartesianStatistics(linkograph):
    Sigma_x = 0
    min_x = len(linkograph)
    max_x = 0
    Sigma_y = 0
    min_y = len(linkograph)
    max_y = 0
    x = []
    y = []
    for node_index in range(len(linkograph)):
        node = linkograph[node_index]
        for forelink in node[2]:
            x.append(float(node_index + forelink) / 2)
            y.append(forelink - node_index)
    if 0 < links(linkograph):
        Sigma_x = sum(x)
        Sigma_y = sum(y)
        x_bar = sum(x) / links(linkograph)
        y_bar = sum(y) / links(linkograph)
        range_x = max(x) - min(x)
        range_y = max(y) - min(y)
    else:
        Sigma_x = None
        Sigma_y = None
        x_bar = None
        y_bar = None
        range_x = None
        range_y = None
    return x_bar, Sigma_x, range_x, y_bar, Sigma_y, range_y

######################################################################
#----------------------- Command Line Programs -----------------------

def cli_percentageOfEntries():
    """Command line interface for percentageOfEntries."""

    info = 'Gives the percentage of entries that have each label.'

    parser = argparse.ArgumentParser(description=info)
    parser.add_argument('linkograph', metavar='LINKOGRAPH.json',
                        nargs=1,
                        help='The linkograph.')

    parser.add_argument('-l', '--lowerBound', type=int,
                        help='The lowest index to consider.')

    parser.add_argument('-u', '--upperBound', type=int,
                        help='The highest index to consider.')

    args = parser.parse_args()

    # Read in the linkograph.
    linko = linkoCreate.readLinkoJson(args.linkograph[0])

    result = percentageOfEntries(linko,
                                 args.lowerBound,
                                 args.upperBound)

    print(json.dumps(result, indent=4))

def cli_percentageOfLinks():
    """Command line interface for percentageOfLinks."""

    info = 'The percentage of links out the total possible links.'

    parser = argparse.ArgumentParser(description=info)
    parser.add_argument('linkograph', metavar='LINKOGRAPH.json',
                        nargs=1,
                        help='The linkograph.')

    parser.add_argument('-l', '--lowerBound', type=int,
                        help='The lowest index to consider.')

    parser.add_argument('-u', '--upperBound', type=int,
                        help='The highest index to consider.')

    args = parser.parse_args()

    # Read in the linkograph.
    linko = linkoCreate.readLinkoJson(args.linkograph[0])

    print(percentageOfLinks(linko,
                            args.lowerBound,
                            args.upperBound))




def cli_graphEntropy():
    """Command line interface for graphEntropy."""

    info = 'Calculates the shanon entropy for the complete linkograph.'

    parser = argparse.ArgumentParser(description=info)
    parser.add_argument('linkograph', metavar='LINKOGRAPH.json',
                        nargs=1,
                        help='The linkograph.')

    parser.add_argument('-l', '--lowerBound', type=int,
                        help='The lowest index to consider.')

    parser.add_argument('-u', '--upperBound', type=int,
                        help='The highest index to consider.')

    args = parser.parse_args()

    # Read in the linkograph.
    linko = linkoCreate.readLinkoJson(args.linkograph[0])

    print(graphEntropy(linko, args.lowerBound, args.upperBound))


def cli_linkEntropy():
    """Command line interface for linkEntropy."""

    info = 'Calculates total link, backlink, and forelink entropies.'

    parser = argparse.ArgumentParser(description=info)
    parser.add_argument('linkograph', metavar='LINKOGRAPH.json',
                        nargs=1,
                        help='The linkograph.')

    # parser.add_argument('linkNumber', metavar='LINKS',
    #                     help=(r'List of links to consider.\n'
    #                           r'[1] -> backlinks.'
    #                           r'[2] -> forelinks.'
    #                           r'[1,2] -> both backlinks and forelinks.'))
    
    parser.add_argument('-f', '--forelinks', action='store_true',
                        help='Use forelinks')

    parser.add_argument('-b', '--backlinks', action='store_true',
                       help='Use backlinks')

    parser.add_argument('-d', '--delta', type=int,
                        help=('Maximum number of links to consider'
                              ' forward or backward.'))

    parser.add_argument('-r', '--restrict', action='store_true',
                        help='Restrict to subgraph.')

    parser.add_argument('-l', '--lowerBound', type=int,
                        help='The lowest index to consider.')

    parser.add_argument('-u', '--upperBound', type=int,
                        help='The highest index to consider.')

    parser.add_argument('-m', '--lineNumbers', action='store_true',
                        help='Print node number.')

    args = parser.parse_args()

    linkNumber=[]

    if(args.forelinks):
        linkNumber.append(2)

    if(args.backlinks):
        linkNumber.append(1)

    if len(linkNumber) == 0:
        linkNumber = [1,2]

    # Read in the linkograph.
    linko = linkoCreate.readLinkoJson(args.linkograph[0])

    result = linkEntropy(linko,
                         linkNumber,
                         args.delta,
                         args.restrict,
                         args.lowerBound,
                         args.upperBound,
                         args.lineNumbers)

    if args.lineNumbers:
        for entry in result:
            print(entry,end='\n')

    else:
        print(json.dumps(result, indent=4))

def cli_linkTComplexity():
    """Command line interface for linkTComplexity."""

    info = 'Calculates total link, backlink, and forelink T code Complexity.'

    parser = argparse.ArgumentParser(description=info)
    parser.add_argument('linkograph', metavar='LINKOGRAPH.json',
                        nargs=1,
                        help='The linkograph.')

    # parser.add_argument('linkNumber', metavar='LINKS',
    #                     help=(r'List of links to consider.\n'
    #                           r'[1] -> backlinks.'
    #                           r'[2] -> forelinks.'
    #                           r'[1,2] -> both backlinks and forelinks.'))
    
    parser.add_argument('-f', '--forelinks', action='store_true',
                        help='Use forelinks')

    parser.add_argument('-b', '--backlinks', action='store_true',
                       help='Use backlinks')

    parser.add_argument('-d', '--delta', type=int,
                        help=('Maximum number of links to consider'
                              ' forward or backward.'))

    parser.add_argument('-r', '--restrict', action='store_true',
                        help='Restrict to subgraph.')

    parser.add_argument('-l', '--lowerBound', type=int,
                        help='The lowest index to consider.')

    parser.add_argument('-u', '--upperBound', type=int,
                        help='The highest index to consider.')

    parser.add_argument('-n', '--normalize', action='store_true',
                       help=('Normalize against T complexity lower'
                             'bound'))

    parser.add_argument('-a', '--absolute', action='store_true',
                       help=('Gives the absolute deference between'
                             'T complexity and the lower bound'))

    parser.add_argument('-m', '--lineNumbers', action='store_true',
                        help='Print node number.')

    args = parser.parse_args()

    linkNumber=[]

    if(args.forelinks):
        linkNumber.append(2)

    if(args.backlinks):
        linkNumber.append(1)

    if len(linkNumber) == 0:
        linkNumber = [1,2]

    # Read in the linkograph.
    linko = linkoCreate.readLinkoJson(args.linkograph[0])

    result = linkTComplexity(linko,
                             linkNumber,
                             args.delta,
                             args.restrict,
                             args.lowerBound,
                             args.upperBound,
                             args.lineNumbers,
                             args.absolute,
                             args.normalize)

    if args.lineNumbers:
        for entry in result:
            print(entry,end='\n')

    else:
        print(json.dumps(result, indent=4))

def cli_subgraphMetric():
    """Command line interface for subgraphMetric."""

    info = 'Calculates the value of graph metrics on subgraphs.'

    parser = argparse.ArgumentParser(description=info)
    parser.add_argument('linkograph', metavar='LINKOGRAPH.json',
                        nargs=1,
                        help='The linkograph.')

    parser.add_argument('-e', '--entropy', action='store_true',
                       help='Use Shannon entropy')

    parser.add_argument('-p', '--percentageOfLinks', action='store_true',
                       help='Use percentage of links')

    parser.add_argument('-t', '--lowerThreshold',
                        type=float, help='The lowest threshold value.')

    parser.add_argument('-T', '--upperThreshold',
                        type=float, help='The highest threshold value.')

    parser.add_argument('-m', '--minSize', type=int, default=2,
                        help='Minimum subgraph size.')

    parser.add_argument('-M', '--maxSize', type=int,
                       help='Maximum subgraph size.')

    parser.add_argument('-s', '--step', type=int, default=1,
                       help='Steps between the lower bounds considered.')

    parser.add_argument('-l', '--lowerBound', type=int,
                        help='The lowest index to consider.')

    parser.add_argument('-u', '--upperBound', type=int,
                        help='The highest index to consider.')

    args = parser.parse_args()
        
    # Read in the linkograph.
    linko = linkoCreate.readLinkoJson(args.linkograph[0])

    if args.entropy:
        result = subgraphMetric(linko, graphEntropy,
                                args.lowerThreshold,
                                args.upperThreshold,
                                args.minSize, args.maxSize,
                                args.step,
                                args.lowerBound,
                                args.upperBound)

    else:
        result = subgraphMetric(linko, percentageOfLinks,
                                args.lowerThreshold,
                                args.upperThreshold,
                                args.minSize, args.maxSize,
                                args.step,
                                args.lowerBound,
                                args.upperBound)

    #print(json.dumps(result, indent=4))
    for entry in result:
        print(entry,end='\n')

def cli_linkSlicePercents():
    """Command line interface for linkSlicePercents."""

    info = 'Calculates total link, backlink, and forelink T code Complexity.'

    parser = argparse.ArgumentParser(description=info)
    parser.add_argument('linkograph', metavar='LINKOGRAPH.json',
                        nargs=1,
                        help='The linkograph.')

    parser.add_argument('-f', '--forelinks', action='store_true',
                        help='Use forelinks')

    parser.add_argument('-b', '--backlinks', action='store_true',
                       help='Use backlinks')

    parser.add_argument('-d', '--delta', type=int,
                        help=('Maximum number of links to consider'
                              ' forward or backward.'))

    parser.add_argument('-r', '--restrict', action='store_true',
                        help='Restrict to subgraph.')

    parser.add_argument('-l', '--lowerBound', type=int,
                        help='The lowest index to consider.')

    parser.add_argument('-u', '--upperBound', type=int,
                        help='The highest index to consider.')

    parser.add_argument('-m', '--lineNumbers', action='store_true',
                        help='Print node number.')

    args = parser.parse_args()

    linkNumber=[]

    if(args.forelinks):
        linkNumber.append(2)

    if(args.backlinks):
        linkNumber.append(1)

    if len(linkNumber) == 0:
        linkNumber = [1,2]

    # Read in the linkograph.
    linko = linkoCreate.readLinkoJson(args.linkograph[0])

    result = linkSlicePercents(linko,
                               linkNumber,
                               args.delta,
                               args.restrict,
                               args.lowerBound,
                               args.upperBound,
                               args.lineNumbers)

    if args.lineNumbers:
        for entry in result:
            print(entry,end='\n')

    else:
        print(json.dumps(result, indent=4))


######################################################################

if __name__ == '__main__':
    linko = linkoCreate.Linkograph([({'A', 'B', 'C'}, {}, {1,2,3}),
                                   ({'D'}, {0}, {3,4}),
                                   ({'A'}, {0}, {4}),
                                   ({'B', 'C'}, {0,1}, {4}),
                                   ({'A'}, {1,2,3}, {})],
                                  ['A', 'B', 'C', 'D'])

    tcode = [0,1,0,0,0,1,0,1,0,1,1,0,1]
    expandtcode = [[e] for e in tcode]

    print(totalLabels(linko))
    print(percentageOfEntries(linko))
    print(links(linko,2))
    print(percentageOfLinks(linko))
    print(graphEntropy(linko))
    print("top level is {}".format(tComplexityRecurse(expandtcode,[])))
    print(tComplexity(tcode))
