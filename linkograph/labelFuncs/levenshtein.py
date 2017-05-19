#!/usr/bin/env python3

import Levenshtein # C-extension implementing Levenshtein distance

def levenshtein(event, event_num, eventList,
               dist=8):
    """Label events using the Levendtein distance.

    An event is checked against a list of anchors that define the
    center of the abstraction class. If the event is withing a
    distance of dist from an anchor, then it is given the anchor as a
    label. If event is not within a distance of dist of any anchors,
    then event becomes an anchor.

    """

    labels = []

    # Check distance form the anchors
    for anchor in levenshtein.anchors:
        if Levenshtein.distance(anchor, event) <= dist:
            labels.append(anchor)


    if len(labels) == 0:
        # If no labels were assigned, then event is not within a
        # distance of dist of any anchor, so event becomes an anchor.
        levenshtein.anchors.append(event)
        labels.append(event)

    return labels

# Define default value for the levensten anchors
levenshtein.anchors = []


######################################################################
# list of labelers
absClassLabelers = [('levenshtein', levenshtein)]

distance = 'The distance from the anchors.'

additionalArgs = [('levenshtein', {'dist': {'default': 8,
                                            'help': distance,
                                            'type': int}})]
