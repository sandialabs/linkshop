#!/usr/bin/env python3
"""A functional approach event labeling with abstractions. """

# Get the function dictionary. Functions f should accept an event
# string and return a set of abstraction classes that label the event.

import warnings # For warnings
import argparse  # For command line parsing.
import json # For reading json files.
import linkograph.labelFuncs as labelFuncs # provides access to the absClassLabelers dictionary

def labelEvents(eventList, absLabelers, absLabelerNames=None,
                defaultAbsClass=None):
    """Label the events with abstraction classes.

    Input:

    eventList: an array of event dictionaries. The format of the
    eventList is [...
        {'cmd': event_string}
        ...]
    Each dictionary {'cmd': event_string} represents an event. Other
    entries can be present in the dictionary, but 'cmd' must be one of
    the keys. The corresponding event_string is what is processed. All
    other entries are ignored.

    absLabelers: a list of strings. Each string is the name of an
    abstraction class labeling function.

    defaultAbsClass: provides a default abstraction class label when
    no other labels apply.

    returns: inverseLabeling

    inverseLabeling: an inverseLabeling for the events. An inverse
    labeling is a dictionary of the form { abstraction_class_label:
    [node_list] } the node_list corresponding to the
    abstraction_class_label is a sorted list of the nodes that have
    abstraction_class_label as their label.

    """

    inverseLabeling = {} # Create the inverse labeling dictionary

    if len(eventList) < 1 or len(absLabelers) < 1 \
       or ((absLabelerNames is not None)
           and (len(absLabelerNames) < 1)):
        return inverseLabeling

    if absLabelerNames is None:
        absLabelerNames = absLabelers.keys()

    for (event_num, event) in enumerate(eventList):
        # The event is packaged in a dictionary with key 'cmd'
        event = event['cmd']

        labels = []
        # Loop through each labeler function and get the labels
        for aln in absLabelerNames:
            lf = absLabelers.get(aln)
            if lf is None:
                warnings.warn('Abstraction Labeler Function {0}'
                              ' is not in the provided functions.'
                              .format(aln))
                continue

            labels.extend(lf(event, event_num, eventList))

        if len(labels) > 1:
            warnings.warn(('Multiples labels detectedc for event'
                           ' {0}').format(event_num))

        # Add in the dafault label
        if len(labels) < 1 and defaultAbsClass:
            labels.append(defaultAbsClass)

        # Loop through labels for the node
        for l in labels:

            l_nodes = inverseLabeling.get(l)

            if not l_nodes:
                inverseLabeling[l] = [event_num]
            else:
                l_nodes.append(event_num)

    return inverseLabeling

######################################################################
#----------------------- Command Line Programs -----------------------

def cli_labelEvents():
    """Command-line interface for labeling events.

    Uses the functionalLabeling system for labeling events.

    """


    info = 'Uses the functionalLabeling system for labeling events.'

    parser = argparse.ArgumentParser(description=info)
    parser.add_argument('eventFile', metavar='EVENTS.json',
                         nargs=1,
                         help='the json of events to label')
    parser.add_argument('--labelers', metavar='LABELERS.json',
                        help=('the json list of labeler function'
                              ' names.'))
    parser.add_argument('-o', '--out', metavar='OUTPUT_FILE.json',
                        help='file for writing the label object.')

    parser.add_argument('-d', '--default', metavar='DEFAULT_LABEL.json',
                        help='file for writing the label object.')

    # Add any additional arguments
    labelFuncs.addArgs(parser, labelFuncs.additionalArgs)

    args = parser.parse_args()

    # Read in the events from the json file.
    events = json.load(open(args.eventFile[0], 'r'))

    # Read in the labeler function names.
    if args.labelers:
        absLabelerNames = json.load(open(args.labelers, 'r'))
    else:
        absLabelerNames = labelFuncs.absClassLabelers.keys()

    if not args.default:
        args.default = 'NoLabel'

    # Parse out additional arguments
    labelFuncs.applyArgs(args, labelFuncs.additionalArgs,
                         labelFuncs.absClassLabelers)

    labeling = labelEvents(events, labelFuncs.absClassLabelers,
                           absLabelerNames=absLabelerNames,
                           defaultAbsClass=args.default)

    if args.out:
        outfile = open(args.out, 'w')
        json.dump(labeling, outfile, indent=4)
    else:
        print(json.dumps(labeling, indent=4))

if __name__ == '__main__':
    #cli_labelEvents()
    import json

    with open('grrcon_example/grrcon_commands.json') as eventFile:
    
        events = json.load(eventFile)

        inverseLabeling = labelEvent(events,
                                     labelFuncs.absClassLabelers,
                                     defaultAbsClass='NoLabel')
