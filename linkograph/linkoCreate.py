#!/usr/bin/env python3

""" Methods for manipulating linkographs."""

import json  # For handling files in the json format.
import csv  # For parsing csv style files.
import argparse  # For command line parsing.

class Linkograph(list):

    """ Linkographs are lists of tuples. """

    def __init__(self, items=[], labels=None):
        self.uuids = []
        """ Add links to the linkograph. """
        if not labels:
            self.labels = []
        else:
            self.labels = labels
        super().__init__(items)

    def appearanceList(self, inLabels=True):
        """Returns the list of labels that appear.

        input:

        inLabels: If True, then the list of labels that is returned
        consists only of labels in self.labels and in the same
        order. If False, then a list of labels is returned consiting
        of all the labels that appear as a label to at least one entry
        of the linkograph.

        """
        labels = set.union(*[entry[0] for entry in self])

        if inLabels:
            return [l for l in self.labels if l in labels]
        else:
            return list(labels)

    def addUUIDs(self, uuids):
        if len(uuids) != len(self):
            print("linkoCreate.py::Linkograph::addUUIDs() UUID list is a different length than item list")
        self.uuids = uuids

def writeLinkoJson(linkograph, file):
    """ Encode the Linkograph as a json and write it to file. """
    # Convert the linkograph into a form json can use.
    jsonLinko = [linkograph.labels]

    """
    for entry in linkograph:
        tolist = list(map(list, entry))
        jsonLinko.append(tolist)
    """
    for index in range(len(linkograph)):
        tolist = list(map(list, linkograph[index]))
        tolist.append(linkograph.uuids[index])
        jsonLinko.append(tolist)

    with open(file, 'w') as jsonFile:
        json.dump(jsonLinko, jsonFile, indent=4)

def writesLinkoJson(linkograph):
    jsonLinko = [linkograph.labels]
    """
    for entry in linkograph:
        tolist = list(map(list,entry))
        jsonLinko.append(tolist)
    """
    for index in range(len(linkograph)):
        tolist = list(map(list, linkograph[index]))
        tolist.append(linkograph.uuids[index])
        jsonLinko.append(tolist)

    return json.dumps(jsonLinko,indent=4)

def readLinkoJson(file):
    """ Read a Linkograph from a json file. """
    with open(file, 'r') as jsonFile:
        preLinko = json.load(jsonFile)

        linko = Linkograph([], preLinko[0])

        for entry in preLinko[1:]:
            linko.append((set(entry[0]), set(entry[1]), set(entry[2])))
            linko.uuids.append(entry[3])

        return linko

def readsLinkoJson(fileString):
    ''' Read a Linkograph from a json string. '''
    preLinko = json.loads(fileString)
    linko = Linkograph([], preLinko[0])
    for entry in preLinko[1:]:
        linko.append((set(entry[0]), set(entry[1]), set(entry[2])))
        linko.uuids.append(entry[3])
    return linko

def readLinkoCSV(file):
    """ Read in a linkograph from a csv file. """
    # define the linkograph that will be returned.
    linkograph = Linkograph()

    # define a variable to collect the labels.
    labels = set()
    with open(file, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')

        # Define a cache for backlinks found in the forelink list.
        backlinks = {}

        # The current line count.
        count = 0
        for line in reader:
            # Check for backlinks that are already present.
            currentBacklinks = backlinks.get(count)

            if not currentBacklinks:
                currentBacklinks = set()

            currentLabels = set(line[0].strip().split(' '))
            labels = labels.union(currentLabels)

            forelinks = set()

            # Loop through the for link list extracting the links.
            for n in [n for n in line[1:] if n != '']:
                forelinks.add(int(n))

                # Every forelink corresponds to a backlink
                # For example, if line 0 has a forelink to line 4
                # then line 4 has a backlink to line 0. So cache
                # the fact that line 4 has this backlink.
                if backlinks.get(int(n)):
                    # Backlinks have already been added for line int(n)
                    # so just add the current backlink.
                    backlinks.get(int(n)).add(count)
                else:
                    # No prior backlinks have been cached, so create
                    # a backlink set containing the current backlink.
                    backlinks[int(n)] = {count}

            # Added the new entry to the linkograph.
            linkograph.append((currentLabels, currentBacklinks, forelinks))
            count = count + 1

        # Set the labels for the Linkograph.
        linkograph.labels.extend(labels)
        linkograph.labels.sort()

    return linkograph


def createLinko(inverseLabeling, ontology):
    """ Create a Linkograph using the given rules and labled commands.

    labels should be of the form:
    {labels: [ordered indicies],
    labels: [ordered indicies],
    ...
    labels: [ordered indicies]}

    Rules should be of the form:
    {inital label: [terminal labels],
    initial label: [terminal labels],
    ...
    initial label: [terminal labels]}
    """

    # Remove any labels that are empty.
    inverseLabeling = {key: inverseLabeling[key] for key in inverseLabeling
              if len(inverseLabeling[key])>0}

    # It might be more robust to search for the maximum value.
    #size = sum(map(len, labels.values()))

    # Find the maximum value listed in the labels.
    # Note: this assumes that every command has a label.
    size = max(map(max, inverseLabeling.values())) + 1

    linko = Linkograph([(set(), set(), set()) for n in range(size)])

    newLabels = set()

    # Put in the labels.
    for l in inverseLabeling:
        newLabels.add(l)
        for n in inverseLabeling[l]:
            linko[n][0].add(l)

    newLabels = newLabels.union(ontology.keys())
    linko.labels = sorted(list(newLabels))

    # If there are no rules or no labels, then return
    # the empty linkograph.
    if not ontology or not len(inverseLabeling):
        return linko

    # Loop through each edge in the rules.
    for initialLabel in ontology:
        # Get the index list for the initial label.
        #initialIndecies = labels[initialLabel]
        initialIndecies = inverseLabeling.get(initialLabel)

        if initialIndecies is None:
            continue

        # Add the indecies to the linkograph
        # for n in initialIndecies:
        #     linko[n][0].append(initialLabel)

        for terminalLabel in ontology[initialLabel]:
            # Get the index list for the target label
            terminalIndecies = inverseLabeling.get(terminalLabel)

            if terminalIndecies is None:
                continue

            # iterate through the terminal indecies
            # as long as the terminal index is more than
            # the initiali ndex, add the terminal index
            # to the forelinks of the initial index and
            # add the initial index to the backlinks
            # of the terminal index.
            for teIndex in terminalIndecies[::-1]:
                for inIndex in initialIndecies:
                    # RRM: JB put this mod in--I am disabling it because it generates a lot of visibility
                    #if(inIndex==15):
                    #    print("We're here!")
                    if teIndex > inIndex:
                        # Add the forelink
                        linko[inIndex][2].add(teIndex)
                        # Add in the backlink
                        linko[teIndex][1].add(inIndex)
                    else:
                        break
    return linko

def createSubLinko(linko, lowerBound=None, upperBound=None,
                   commands=None):
    """ Creates a linkograph for a sublinkograph.

    Given a range lowerBound to upperBound, creates a linkograph for
    the sublinkograph specified by that range. This process amounts to
    creating a new linkograph from the sublinkograph and re-numbering
    the nodes to start at 0. If no lowerBound is specified, it is
    assumed to be 0, and if no upperBound is specified, it is assumed
    to be len(linko)-1. If the commands are given, the function will
    subset them as well. In the range is empty, that is, if lowerBound
    > upperBound, then the trivial linkograph is returned.

    arguments:

    linko -- the linkograph to create sublinkographs from.

    lowerBound -- the lower node number for the sublinkograph. It is
    assumed to be 0 if it is not given.

    upperBound -- the upper node number for the sublinkograph. It is
    assumed to be len(linko)-1 if it is not given.

    commands -- the associated list of commands for the linkograph.

    returns:

    if no commands are given:
    sublinkograph -- the sublinkograph created.

    if commands are given:
    (sublinkograph, subCommands) -- a tuple of the created
    sublinkograph and a list of the sub commands associated with the
    sublinkograph.

    """

    if lowerBound is None:
        lowerBound = 0
    else:
        lowerBound = max(0, lowerBound)

    if upperBound is None:
        upperBound = len(linko)-1

    else:
        upperBound = min(len(linko)-1, upperBound)

    newLinko = Linkograph()

    newLinko.uuids = linko.uuids[lowerBound:upperBound+1]

    # Copy over the labels. In general, is should be fine to include
    # more labels than less. Thus, copying all the labels from the
    # original linkograph should be fine.
    newLinko.labels = {l for l in linko.labels}

    # If the lowerBound is more than the upperBound, then the range is
    # empty, so only return the trivial linkograph.
    if lowerBound > upperBound:
        if commands is None:
            return newLinko

        else:
            # No commands can be associated with a trivial linkograph.
            return (newLinko, [])

    # Loop through the nodes of the sublinkograph.
    for entry in linko[lowerBound: upperBound+1]:

        # Get the labels.
        newLabel = entry[0]

        # Make a copy of the backlinks. To re-number the nodes,
        # subtract off the lowerBound node number. Do not include
        # numbers less than lowerBound.
        newBackLinks = {n - lowerBound for n in entry[1] if n >=
                        lowerBound}

        # Make a copy of the forelinks. To re-number the nodes,
        # subtract off the lowerBound node number. Do not include
        # numbers greater than the upperBound.
        newForeLinks = {n -lowerBound for n in entry[2] if n <=
                        upperBound}

        newLinko.append((newLabel, newBackLinks, newForeLinks))


    if commands is None:
        return newLinko

    else:
        return (newLinko, commands[lowerBound: upperBound+1])

def checkLinkoStructure(linko, labels=False):
    """
    Checks that the linkograph data structure is consistent.

    inputs:

    linko - the linkograph.

    labels - If True, check for consistency between the node lables
    and linko.labels.

    outputs: result, errors

    result - True if the check pass and false otherwise.

    errors - a dictionary of the errors. The entries of the dictionary
    are (node number, (backlink errors, forelink errors)).  The
    backlink errors is a set of integers representing missing
    backlinks and forelink errors is a set of integers representing
    missing forelinks. For example, errors[7] = ({3}, {8})] means that
    7 is in the forelink list of node 3, representing the link 3 -> 7,
    but 3 is not in the backlink list for node 7. Similarly, 7 is in
    the backlink list of node 8, but 8 is not in the forelink list of
    node 7. If the labels input is True, then error in the labels
    appear in an entry errors['labels'] = list of missing labels. For
    example, if labels=True and errors['labels'] = ['A', 'B'] means
    that the label 'A' appears as the label for at least one node, but
    is not in linko.labels. Similarly, 'B' appears as a label of at
    least one node and is not in linko.labels. Missing nodes are
    collected in a set with key missing. Thus, errors['missing'] = 8
    means that some node (less than 8) refers to the node 8 and node 8
    is not in the linkograph.

    """

    # Define the errors dictionary
    errors = {}

    # Loop through each node
    for (node, (nodeLabel, backlinks, forelinks)) in enumerate(linko):
        # Check the backlinks
        for back in backlinks:

            # back is in the backlinks for the current node, so the
            # current node should be in the node back's forelinks.
            if node not in linko[back][2]:
                if not errors.get(back):
                    errors[back] = (set(), {node})
                else:
                    errors[back][1].add(node)

        # Check the forelinks
        for fore in forelinks:

            # fore is in the forelinks for the current node, so the
            # current node should be in the node fore's backlinks.

            # First, check if node fore exists in the linkogaph.
            foreExists = fore < len(linko)

            if not foreExists:
                if not errors.get('missing'):
                    errors['missing'] = {fore}
                else:
                    errors['missing'].add(fore)
            

            if (not foreExists) or (node not in linko[fore][1]):
                if not errors.get(fore):
                    errors[fore] = ({node}, set())
                else:
                    errors[fore][0].add(node)

        # Check the labels
        if labels:
            for l in nodeLabel:
                if l not in linko.labels:
                    if not errors.get('labels'):
                        errors['labels'] = {l}
                    else:
                        errors['labels'].add(l)

    return len(errors) == 0, errors

def errorString(node, error):
    """
    Format error messages for node errors returned by checkLinkoStructure.

    inputs:

    node - the node for the error.
    error - a (backset, foreset) tuple, where backset is the set of
    missing backlinks and foreset is the set of missing forelinks.

    returns: string

    string - the error string message.
    """

    back, fore = error[0], error[1]

    if len(back) == 0:
        back = 'None'

    if len(fore) == 0:
        fore = 'None'
    
    return ('Node {0}: missing backlinks {1},'
            ' missing forelinks {2}').format(node, back, fore)

######################################################################
#----------------------- Command Line Programs -----------------------


def cli_createLinko():
    """Creates a linkograph using an inverse labeling and an ontology."""

    info = ('Creates a linkograph from an (inverse) labeling json'
            ' and an ontology json.')

    parser = argparse.ArgumentParser(description=info)
    parser.add_argument('labeling', metavar='LABELING.json',
                        nargs=1,
                        help='the inverse labeling json file.')

    parser.add_argument('ontology', metavar='ONTOLOGY.json',
                        nargs=1,
                        help='the json of ontology.')

    parser.add_argument('-o', '--out', metavar='OUTPUT_FILE',
                        help='the linkograph as a json')

    args = parser.parse_args()

    outfile = None
    if args.out:
        outfile = args.out

    # Load the json files.
    with open(args.labeling[0], 'r') as invLabelingFile:
        invLabeling = json.load(invLabelingFile)
        with open(args.ontology[0], 'r') as ontologyFile:
            ontology = json.load(ontologyFile)
            linko = createLinko(invLabeling, ontology)

            if outfile:
                writeLinkoJson(linko, outfile)
            else:
                print(linko)

def cli_checkLinkoStructure():
    """Checks the linkograph structure."""

    info = ('Checks that a likngraphs backlinks, forelinks'
            ' and labels are consistent.')

    parser = argparse.ArgumentParser(description=info)
    parser.add_argument('linkograph', metavar='LINKO.json',
                        nargs=1,
                        help='the linkograph file.')
    parser.add_argument('-l', '--labels', action='store_true',
                        help='include labels.')
    args = parser.parse_args()

    # Load the json files.
    #    with open(args.linkograph[0], 'r') as linkoFile:
    linko = readLinkoJson(args.linkograph[0])

    result, errors = checkLinkoStructure(linko, args.labels)

    if result:
        print('No errors found')
    else:
        print('Errors found.')
        # Check for missing nodes
        missing = errors.pop('missing', None)
        if missing is not None:
            print('Missing nodes: {0}'.format(missing))

        # Check labels
        labels = errors.pop('labels', None)
        if labels is not None:
            print('Labels not recorded {0}'.format(labels))
        
        for node in errors.keys():
            print(errorString(node, errors[node]))
