#!/usr/bin/env python3

"""Apparatus for storing and identifying markov models.

"""

import random

class Experiment():

    def __init__(models=None, ontologies=None):
        self.models
        self.ontologies

        self.currentModel = choice(models)
        self.currentOntology = choice(ontologies)


    def genLinkograph(n):
        """Generate a linkograph on n-nodes using current model and ontology."""
        return self.currentModel.genLinkograph(n, currentOntology)
