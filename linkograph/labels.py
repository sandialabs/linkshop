#!/usr/bin/env python3

""" Methods tokenizing and labeling command data."""

import json  # For reading the json format.
import re  # For pattern matching.
# Uncomment to enable ahoCorasick substring matching, if desired
#import ahoCorasick  # For substring matching.
import argparse  # For parsing command line arguments.

def is_command_in_labels(command, labels):
    result = False
    for label in labels:
        if command in labels[label]:
            result = True
            break
    return result

class baseLabelingError(Exception):

    """Base class for labeling exceptions."""

    pass


class invalidLabelObject(baseLabelingError):

    """Exception that occurs when a label object is improperly formatted."""

    def __init__(self, description):
        """Record description of error that occured."""
        self.description = description

    def __str__(self):
        """Return representation of actual description."""
        return repr(self.description)


class invalidCommandObject(baseLabelingError):

    """Exception that occurs when command data is improperly formatted."""

    def __init__(self, description):
        """Record description of error that occured."""
        self.description = description

    def __str__(self):
        """Return representation of actual description."""
        return repr(self.description)


class Labeler(object):

    """Object capable of tokenizing command data based on a set of labels.

    Labels are of the form:
    {
        "{Label}":[
            {priority},
            {
                "command":
                    {
                        "expression": "{expressionValue}",
                        "type": "{exact|substring|regEx}"
                    }
                "arguments":
                    {
                        "expression": "{expressionValue}",
                        "type": "{exact|substring|regEx}"
                    }
            },
            ...
        ]
    }

    Note: multiple arguments for a single command are not supported yet

    """

    # Defines the types of pattern matching available
    PTYPES = {'exact': 'addToExact',
              'substring': 'addToSubstring',
              'regEx': 'addToRegEx'}

    def __init__(self, labelObj):
        """Build parsing structures from a label object."""
        super(Labeler, self).__init__()

        # Label object must be a dictionary with appropriate keys
        if not isinstance(labelObj, dict):
            raise invalidLabelObject("Label object is not dict!")

        # Exact matches is a tuple of two dictionaries, the first for
        # commands and the second for arguments. Each dictionary key is a
        # expression  to match and the value is the index of the label in
        # _labels
        self._exactMatches = ({}, {})

        # Substring matches is a tuple of two tuples, the first for commands
        # and the second for arguments. Each of these tuples is initially a
        # list to allow for mutability. The two tuples contain a set of
        # substrings to match and a dictionary where each key
        # corresponds to a substring to match and the value is a set of
        # the indexes of the labels that correspond to that substring match.
        # Before initialization is completed the set of substring matches is
        # replaced with an actual trie object to perform those matches
        self._substringMatches = [[set(), {}], [set(), {}]]

        # Exact matches is a tuple of two dictionaries, the first for
        # commands and the second for arguments. Each dictionary key is an
        # uncompiled regular expression and the value is a tuple of the
        # corresponding compiled regular expression and a set of all the
        # label indexes that correspond to that regular expression
        self._regExMatches = ({}, {})

        self._labelPriorities = dict()

        # List of all the labels
        self._labels = []

        # If an error occurs in the object parsing, report it and then raise
        try:
            for label, patterns in labelObj.items():
                if None != self._labelPriorities:
                    priority = patterns.pop(0)
                    if isinstance(priority, int):
                        self._labelPriorities[label] = priority
                    else:
                        print("generating multilabels: priority data missing")
                        self._labelPriorities = None
                        patterns.append(priority)

                for pattern in patterns:
                    # Get command and argument pattern
                    command = pattern.get('command')
                    arguments = pattern.get('arguments')
                    # Check that at least a command or argument is specified
                    if not (command or arguments):
                        raise invalidLabelObject("Found empty label.")

                    # Get the command and argument expressions
                    cExpr = None
                    aExpr = None
                    if command is not None:
                        cExpr = command.get('expression')
                        # Expressions must be strings
                        if not isinstance(cExpr, str):
                            raise invalidLabelObject("Invalid expression.")

                    if arguments is not None:
                        aExpr = arguments.get('expression')
                        # Expressions must be strings
                        if not isinstance(aExpr, str):
                            raise invalidLabelObject("Invalid expression.")

                    # Check that at least one non-empty expression is provided
                    if not (cExpr or aExpr):
                        raise invalidLabelObject("Found empty label.")

                    # A matching object that strictly matches just an argument
                    # does not make sense
                    if cExpr is '' and aExpr:
                        raise invalidLabelObject("Cannot have strict "
                                                 "argument matching")

                    # Set the index used to identify the label
                    index = len(self._labels)

                    # Check to see if the label already exists
                    labelTuple = (command, arguments, label)
                    if labelTuple in self._labels:
                        index = self._labels.index(labelTuple)
                    else:
                        self._labels.append(labelTuple)

                    # Add the command expression to the appropriate search
                    # method
                    if cExpr:
                        if command['type'] not in self.PTYPES:
                            raise invalidLabelObject("Expression type not"
                                                     "recognized")
                        getattr(self, self.PTYPES[command['type']])(
                            cExpr, 0, index)

                    # Add the arguments expression to the appropriate search
                    # method
                    if aExpr:
                        if arguments['type'] not in self.PTYPES:
                            raise invalidLabelObject("Expression type not"
                                                     "recognized")
                        getattr(self, self.PTYPES[arguments['type']])(
                            aExpr, 1, index)

        except Exception as e:
            raise invalidLabelObject(e)

        # Compile the appropriate trie objects for substring matching
        cTrieObj = ahoCorasick.trie(list(self._substringMatches[0][0])) if \
            self._substringMatches[0][0] else None
        aTrieObj = ahoCorasick.trie(list(self._substringMatches[1][0])) if \
            self._substringMatches[1][0] else None

        self._substringMatches = ((cTrieObj, self._substringMatches[0][1]),
                                  (aTrieObj, self._substringMatches[1][1]))

    # Provide read only access to matching objects
    @property
    def exactMatches(self):
        """Allow read access to the exactMatches object."""
        return self._exactMatches

    @property
    def substringMatches(self):
        """Allow read access to the substringMatches object."""
        return self._substringMatches

    @property
    def regExMatches(self):
        """Allow read access to the regExMatches object."""
        return self._regExMatches

    @property
    def labels(self):
        """Allow read access to labels."""
        return self._labels

    def _find_highest_priority_label(self, labels):
        hpl = None
        for label in labels:
            if (
                 None == hpl
                 or self._labelPriorities[label] > self._labelPriorities[hpl]
               ):
                hpl = label
        return hpl

    def _multi_to_unilabels(self, multilabels):
        foo = multilabels.copy()
        unilabels = dict()
        # while multilabels is not empty
        while 0 < len(foo):
            # find the highest priority label
            hpl = self._find_highest_priority_label(foo)

            # put the highest priority label (hpl) in unilabels
            unilabels[hpl] = set()

            # for each command in higest priority label
            for command in foo[hpl]:
                # verify command is not already in unilabels
                if not is_command_in_labels(command, unilabels):
                    # put the command in unilabels
                    unilabels[hpl].add(command)

            # delete the highest priority label from labels
            del foo[hpl]

        return unilabels

    def addToExact(self, expression, eType, label):
        """Add pattern to exact matches."""
        # See __init__ for description of the datastructure
        if expression not in self._exactMatches[eType]:
            self._exactMatches[eType][expression] = {label}
        else:
            self._exactMatches[eType][expression].add(label)

    def addToSubstring(self, expression, eType, label):
        """Add pattern to substring matches."""
        # See __init__ for description of the datastructure
        self._substringMatches[eType][0].add(expression)
        if expression not in self._substringMatches[eType][1]:
            self._substringMatches[eType][1][expression] = {label}
        else:
            self._substringMatches[eType][1][expression].add(label)

    def addToRegEx(self, expression, eType, label):
        """Add matching pattern to exact matches."""
        # See __init__ for description of the datastructure
        if expression not in self._regExMatches[eType]:
            self._regExMatches[eType][expression] =(re.compile(expression,
                                                               re.IGNORECASE),
                                                     {label})
        else:
            self._regExMatches[eType][expression][1].add(label)

    def labelCommands(self, commands, defaultLabel=None):
        if None != self._labelPriorities:
            self._labelPriorities[defaultLabel] = 0

        """Method to actually perform command labeling."""
        # If any errors occur in parsing or labeling the commands log the
        # exception and then raise it
        try:
            # Index to identify the command
            lineNum = 0

            # Stores the actual labeling of the command data
            labels = {}

            for command in commands:
                cmdSplit = command['cmd'].split(None, 1)

                if not cmdSplit:
                    raise invalidCommandObject('No command found')

                # Command is automatically stripped of whitespace by split
                cmd = cmdSplit[0]

                if not cmd:
                    raise invalidCommandObject('No command found')

                # Strip argument of surrounding whitespace and convert
                # multiple spaces into a single space
                arg = ' '.join(cmdSplit[1].strip().split()) if len(cmdSplit) \
                    > 1 else ''

                matched = False

                # Set to hold all matches of labels on the command string
                cMatches = self._getMatches(0, cmd)

                if arg:
                    # Set to hold all matches of labels on the arguments string
                    aMatches = self._getMatches(1, arg)

                    # Shared matches are automatically added
                    sharedMatch = cMatches & aMatches

                    # Matches of a single command or single argument need to
                    # be checked for strictness
                    diffMatch = cMatches ^ aMatches

                    if sharedMatch:
                        for index in sharedMatch:
                            label = self.labels[index][2]
                            self._addMatch(label, lineNum, labels)
                            matched |= True

                    if diffMatch:
                        for index in diffMatch:
                            label = self.labels[index]
                            # If true, match is not a strict match
                            if label[0] is None or \
                                    label[1] is None:
                                self._addMatch(label[2], lineNum, labels)
                                matched |= True

                # If no arguments are found
                else:
                    for index in cMatches:
                        label = self.labels[index]
                        # Add general and strict matches
                        if not label[1] or not label[1]['expression']:
                            self._addMatch(
                                label[2], lineNum, labels)
                            matched |= True

                # If command is not matched once, add a default label
                if defaultLabel and not matched:
                    self._addMatch(defaultLabel, lineNum, labels)
                    matched |= True

                lineNum += 1

            if None != self._labelPriorities:
                unilabels = self._multi_to_unilabels(labels)
                del self._labelPriorities[defaultLabel]
                return convertToLabelFormat(unilabels)
            else:
                return convertToLabelFormat(labels)
        except Exception as e:
            if None != self._labelPriorities:
                del self._labelPriorities[defaultLabel]
            raise e

    def _getMatches(self, stringType, stringToMatch):
        """Convenience wrapper to get all matches for a string."""
        # Get all exact matches
        matches = self.exactMatches[stringType].get(stringToMatch, set())

        # Get all substring matches
        if self.substringMatches[stringType][0] is not None:
            substringQuery = self.substringMatches[stringType][0].query(
                stringToMatch, False)
            if substringQuery:
                for match in substringQuery:
                    matches |= self.substringMatches[stringType][1][match[0]]

        # Get all regular expression matches
        for reg in self.regExMatches[stringType].values():
            if reg[0].match(stringToMatch):
                matches |= reg[1]

        return matches

    def _addMatch(self, label, lineNum, labels):
        """Convenience wrapper to add a label to a set of labels."""
        if not labels.get(label):
            labels[label] = {lineNum}
        else:
            labels[label].add(lineNum)

def writesLabelsToJsonFile(labels):
    """Convert labels dict to the form that's expected"""
    tmpLabels = dict(labels)
    for label in labels:
        tmpLabels[label] = list(labels[label])
    return tmpLabels

def writeLabelsToJsonFile(labels, fileName):
    """Write a labels dictionary to a file."""
    # tmpLabels = dict(labels)
    # for label in labels:
    #     nodes = list(labels[label])
    #     nodes.sort()
    #     tmpLabels[label] = nodes
    with open(fileName, 'w') as jsonFile:
        json.dump(labels, jsonFile, indent=4)

def convertToLabelFormat(oldLabels):
    """ Convert the label form with sets to label form with lists.

    For later functions, the labels are expected to be of the form:
    {
        'label': [nodeIndex]
    }
    that is, a dictionary whose keys are the labels and values are the
    index number of the nodes that have that label. The node index
    list [nodeIndex] must be ordered.

    """

    newLabels = {}
    for label in oldLabels:
        nodes = list(oldLabels[label])
        nodes.sort()
        newLabels[label] = nodes
    return newLabels


######################################################################
#--------------------------- Main program ----------------------------

def main():
    """Command-line interface for labeling commands."""

    info = ('Labels commands according to the ahoCorasick'
            ' implementation structure.')

    parser = argparse.ArgumentParser(description=info)
    parser.add_argument('commands', metavar='COMMANDS.json',
                         nargs=1,
                         help='the json of commands to label')
    parser.add_argument('labelRules', metavar='LABELS.json',
                        nargs=1,
                        help='the json of labeling rules.')
    parser.add_argument('-o', '--out', metavar='OUTPUT_FILE',
                        help='file for writing the label object.')

    args = parser.parse_args()

    with open(args.labelRules[0], 'r') as labelRules:
        lr = Labeler(json.load(labelRules))

        with open(args.commands[0], 'r') as commands:
            labeled = lr.labelCommands(json.load(commands), "NoLabel")


            if args.out:
                writeLabelsToJsonFile(labeled, args.out)
            else:
                print(labeled)


if __name__ == '__main__':
    main()
