#!/usr/bin/env python3

"""Tests the enumeration.py package."""

import unittest
from linkograph import linkoCreate # For creating linkographs.
from linkograph import dynamic # The package under test.



class Test_addNode(unittest.TestCase):

    """Basic unit tests for addNode using size 4."""

    def setUp(self):
        """Set up the parameters for the individual tests."""

        ontology = {'A': ['C', 'D'],
                    'B': ['C'],
                    'C': ['B'],
                    'D': ['B', 'C']}

        trivialLinko = linkoCreate.Linkograph(
            [], [])

        linko0 = linkoCreate.Linkograph(
            [({'A'}, set(), set())],
            ['A'])
        

        linko1 = linkoCreate.Linkograph(
            [({'A'}, set(), {1}),
             ({'D'}, {0}, set())],
            ['A', 'D'])

        linko2 = linkoCreate.Linkograph(
            [({'A'}, set(), {1}),
             ({'D'}, {0}, {2}),
             ({'B'}, {1}, set())],
            ['A', 'D', 'B'])

        linko3 = linkoCreate.Linkograph(
            [({'A'}, set(), {1,3}),
             ({'D'}, {0}, {2,3}),
             ({'B'}, {1}, {3}),
             ({'C'}, {0,1,2}, set())],
            ['A', 'D', 'B', 'C'])

        linko4 = linkoCreate.Linkograph(
            [({'D'}, set(), {1,2,3}),
             ({'B'}, {0}, {2}),
             ({'C'}, {0,1}, {3}),
             ({'B'}, {0,2}, set())],
            ['A', 'D', 'B', 'C'])


        if self.id().split('.')[-1] == 'test_addNodeSize4':
            self.testParams = [
                {'linko': trivialLinko,
                 'newLabels': {'A'},
                 'ontology': ontology,
                 'size': 4,
                 'ExpectedLinkograph': linko0},

                {'linko': linko0,
                 'newLabels': {'D'},
                 'ontology': ontology,
                 'size': 4,
                 'ExpectedLinkograph': linko1},

                {'linko': linko1,
                 'newLabels': {'B'},
                 'ontology': ontology,
                 'size': 4,
                 'ExpectedLinkograph': linko2},

                {'linko': linko2,
                 'newLabels': {'C'},
                 'ontology': ontology,
                 'size': 4,
                 'ExpectedLinkograph': linko3},

                {'linko': linko3,
                 'newLabels': {'B'},
                 'ontology': ontology,
                 'size': 4,
                 'ExpectedLinkograph': linko4},
            ]

    def performTestForParams(self):
        """"Performs the tests for each set of parameters."""
        for (testNum, params) in enumerate(self.testParams):
            actualLinkograph = dynamic.addNode(params['linko'],
                                               params['newLabels'],
                                               params['ontology'],
                                               params['size'])
            self.assertEqual(
                actualLinkograph,
                params['ExpectedLinkograph'],
                (" linko = {}\n"
                 " newLabels = {}\n"
                 " ontology = {}\n"
                 " size = {}\n"
                 " actualLinkograph = {}\n"
                 " ExpectedLinkograph = {}\n")
                .format(params['linko'],
                        params['newLabels'],
                        params['ontology'],
                        params['size'],
                        actualLinkograph,
                        params['ExpectedLinkograph']))

    def test_addNodeSize4(self):
        """Tests the addNode function with a size of 4."""
        self.performTestForParams()

