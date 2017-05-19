#!/usr/bin/env python3

""" Tests for Linkograph functions."""

import unittest
from linkograph import linkoCreate
from io import StringIO


try:
    from unittest.mock import patch
    from unittest.mock import MagicMock
except ImportError:
    # < python 3.3
    from mock import patch


class ContextualStringIO(StringIO):

    """Context manager for StringIO."""

    def __enter__(self):
        """Return the StringIO object."""
        return self

    def __exit__(self, *args):
        """Clean up, but don't handle any exceptions."""
        self.close()
        return False


class Test_readLinkoCSV(unittest.TestCase):

    """ Basic unit tests for the readLinkoCSV funtcion."""

    def setUp(self):
        """ Set up the files to be read for the tests."""

        if self.id().split('.')[-1] == 'test_singleLine':
            self.testParams = [
                {'csvfile': 'F',
                 'expectedLinkograph': [({'F'},set(),set())],
                 'expectedLabels': ['F']},
                {'csvfile': 'F ',
                 'expectedLinkograph': [({'F'},set(),set())],
                 'expectedLabels': ['F']}]

        elif self.id().split('.')[-1] == 'test_twoLines':
            self.testParams = [
                {'csvfile': 'F,\nBs',
                 'expectedLinkograph': [({'F'},set(),set()),
                                        ({'Bs'}, set(), set())],
                 'expectedLabels': ['Bs', 'F']},
                {'csvfile': 'F,1\nBs',
                 'expectedLinkograph': [({'F'},set(),{1}),
                                        ({'Bs'}, {0}, set())],
                 'expectedLabels': ['Bs', 'F']}]

        elif self.id().split('.')[-1] == 'test_threeLines':
            self.testParams = [
                {'csvfile': 'F\nBs,2\nBe',
                 'expectedLinkograph': [({'F'},set(),set()),
                                        ({'Bs'},set(),{2}),
                                        ({'Be'},{1},set())],
                 'expectedLabels': ['Be', 'Bs', 'F']},
                {'csvfile': 'F,1,2\nBs,2\nBe',
                 'expectedLinkograph': [({'F'},set(),{1,2}),
                                        ({'Bs'}, {0}, {2}),
                                        ({'Be'}, {0,1}, set())],
                 'expectedLabels': ['Be', 'Bs', 'F']}]

    def performTestForParams(self):
        """ Performs the tests for each set of parameters. """
        for params in self.testParams:
            
            # Set up a dummy file-like object containing the test case string
            dummyFile = ContextualStringIO(params['csvfile'])
            # Mock the open function so that the file-like object is returned
            mock_open = MagicMock(return_value=dummyFile)

            with patch('linkograph.linkoCreate.open', mock_open, create=True):
                link = linkoCreate.readLinkoCSV(params['csvfile'])
                self.assertEqual(link, params['expectedLinkograph'],
                                 ("Test failed to create Linkograph {}"
                                  "from {}. Linkograph created {}.")
                                 .format(params['expectedLinkograph'],
                                         params['csvfile'],
                                         link))
                self.assertEqual(link.labels, params['expectedLabels'],
                                 ("Labels are incorrect reading {}."
                                 "Expected: {} actual {}")
                                  .format(params['csvfile'],
                                          ['expectedLabels'],
                                          link.labels))


    def test_singleLine(self):
        """ Tests Linkograph construction for single line files. """
        self.performTestForParams()

    def test_twoLines(self):
        """ Tests Linkograph construction for two line files. """
        self.performTestForParams()

    def test_threeLines(self):
        """ Tests Linkograph construction for three line files. """
        self.performTestForParams()


class Test_createLinko(unittest.TestCase):

    """Basic unit tests creating a linkograph."""

    def setUp(self):
        """Set up the parameters for the individual tests."""


        # InverseLabeling
        invLabeling0 = {'L0': [0, 1, 2]}

        invLabeling1 = {'L0' : [0, 2],
                        'L1' : [1]}

        invLabeling2 = {
            'L0' : [0],
            'L1' : [1],
            'L2' : [2]
        }

        invLabeling3 = {
            'L1' : [0, 1],
            'L2' : [2]
        }

        invLabeling4 = {
            'L0' : [0,1],
            'L1' : [0],
            'L2' : [2]
        }

        invLabeling5 = {
            'L0': [0, 1, 2],
            'L1': []
        }
        
        # Create some ontologies
        ontology0 = {'L0': ['L0']}

        ontology1 = {}

        ontology2 = {'L0': ['L1']}

        ontology3 = {'L0': ['L1', 'L2'],
                     'L1': ['L2'],
                     'L2': ['L0']}

        if self.id().split('.')[-1] == 'test_createLinkograph':
            self.testParams = [
                {'inverseLabeling': invLabeling0,
                 'ontology': ontology0,
                 'ExpectedLinkograph':
                 linkoCreate.Linkograph(
                     [({'L0'}, set(), {1, 2}),
                      ({'L0'}, {0}, {2}),
                      ({'L0'}, {0,1}, set())]  
                 )},

                {'inverseLabeling': invLabeling0,
                 'ontology': ontology1,
                 'ExpectedLinkograph':
                 linkoCreate.Linkograph(
                     [({'L0'}, set(), set()),
                      ({'L0'}, set(), set()),
                      ({'L0'}, set(), set())]
                 )},

                {'inverseLabeling': invLabeling0,
                 'ontology': ontology2,
                 'ExpectedLinkograph':
                 linkoCreate.Linkograph(
                     [({'L0'}, set(), set()),
                      ({'L0'}, set(), set()),
                      ({'L0'}, set(), set())]
                 )},


                {'inverseLabeling': invLabeling1,
                 'ontology': ontology0,
                 'ExpectedLinkograph':
                 linkoCreate.Linkograph(
                     [({'L0'}, set(), {2}),
                      ({'L1'}, set(), set()),
                      ({'L0'}, {0}, set())]
                 )},

                {'inverseLabeling': invLabeling1,
                 'ontology': ontology1,
                 'ExpectedLinkograph':
                 linkoCreate.Linkograph(
                     [({'L0'}, set(), set()),
                      ({'L1'}, set(), set()),
                      ({'L0'}, set(), set())]
                 )},

                {'inverseLabeling': invLabeling1,
                 'ontology': ontology2,
                 'ExpectedLinkograph':
                 linkoCreate.Linkograph(
                     [({'L0'}, set(), {1}),
                      ({'L1'}, {0}, set()),
                      ({'L0'}, set(), set())]
                 )},

                {'inverseLabeling': invLabeling0,
                 'ontology': ontology3,
                 'ExpectedLinkograph':
                 linkoCreate.Linkograph(
                     [({'L0'}, set(), set()),
                      ({'L0'}, set(), set()),
                      ({'L0'}, set(), set())]
                 )},

                {'inverseLabeling': invLabeling1,
                 'ontology': ontology3,
                 'ExpectedLinkograph':
                 linkoCreate.Linkograph(
                     [({'L0'}, set(), {1}),
                      ({'L1'}, {0}, set()),
                      ({'L0'}, set(), set())]
                 )},

                {'inverseLabeling': invLabeling2,
                 'ontology': ontology3,
                 'ExpectedLinkograph':
                 linkoCreate.Linkograph(
                     [({'L0'}, set(), {1,2}),
                      ({'L1'}, {0}, {2}),
                      ({'L2'}, {0, 1}, set())]
                 )},

                {'inverseLabeling': invLabeling3,
                 'ontology': ontology3,
                 'ExpectedLinkograph':
                 linkoCreate.Linkograph(
                     [({'L1'}, set(), {2}),
                      ({'L1'}, set(), {2}),
                      ({'L2'}, {0, 1}, set())]
                 )},

                {'inverseLabeling': invLabeling4,
                 'ontology': ontology3,
                 'ExpectedLinkograph':
                 linkoCreate.Linkograph(
                     [({'L0', 'L1'}, set(), {2}),
                      ({'L0'}, set(), {2}),
                      ({'L2'}, {0, 1}, set())]
                 )},

                {'inverseLabeling': invLabeling5,
                 'ontology': ontology3,
                 'ExpectedLinkograph':
                 linkoCreate.Linkograph(
                     [({'L0'}, set(), set()),
                      ({'L0'}, set(), set()),
                      ({'L0'}, set(), set())]
                 )},

            ]


    def performTestForParams(self):
        """"Performs the tests for each set of parameters."""
        for (testNum, params) in enumerate(self.testParams):
            actualLinkograph = linkoCreate.createLinko(params['inverseLabeling'],
                                                       params['ontology'])
            self.assertEqual(
                actualLinkograph,
                params['ExpectedLinkograph'],
                ("testNum = {}"
                 " inversLabling = {}"
                 " ontology= {}"
                 " actualLinkograph = {}"
                 " ExpectedLinkograph = {}")
                .format(testNum,
                        params['inverseLabeling'],
                        params['ontology'],
                        actualLinkograph,
                        params['ExpectedLinkograph']))

    def test_createLinkograph(self):
        """Tests the createLinko function."""
        self.performTestForParams()


class Test_createSubLinko(unittest.TestCase):

    """Basic unit tests for creating a sublinkograph."""

    def setUp(self):
        """Set up the parameters for the individual tests."""

        singleLabels = linkoCreate.Linkograph(
            [({'A'}, set(), {1,2,3}),
             ({'D'}, {0}, {3,4}),
             ({'A'}, {0}, {4}),
             ({'C'}, {0,1}, {4}),
             ({'A'}, {1,2,3}, set())],
            ['A', 'B', 'C', 'D'])

        singleSubLinko0_2 = linkoCreate.Linkograph(
            [({'A'}, set(), {1,2}),
             ({'D'}, {0}, set()),
             ({'A'}, {0}, set())],
            ['A', 'B', 'C', 'D'])

        singleSubLinko0_1 = linkoCreate.Linkograph(
            [({'A'}, set(), {1}),
             ({'D'}, {0}, set())],
            ['A', 'B', 'C', 'D'])

        singleSubLinko0_0 = linkoCreate.Linkograph(
            [({'A'}, set(), set())],
            ['A', 'B', 'C', 'D'])

        singleSubLinko1_2 = linkoCreate.Linkograph(
            [({'D'}, set(), set()),
             ({'A'}, set(), set())],
            ['A', 'B', 'C', 'D'])

        singleSubLinko1_1 = linkoCreate.Linkograph(
            [({'D'}, set(), set())],
            ['A', 'B', 'C', 'D'])

        trivialLinkograph = linkoCreate.Linkograph(
            [], ['A', 'B', 'C', 'D'])


        singleSubLinko1_4 = linkoCreate.Linkograph(
            [({'D'}, set(), {2,3}),
             ({'A'}, set(), {3}),
             ({'C'}, {0}, {3}),
             ({'A'}, {0,1,2}, set())],
            ['A', 'B', 'C', 'D'])

        singleSubLinko2_4 = linkoCreate.Linkograph(
            [({'A'}, set(), {2}),
             ({'C'}, set(), {2}),
             ({'A'}, {0,1}, set())],
            ['A', 'B', 'C', 'D'])

        singleSubLinko3_4 = linkoCreate.Linkograph(
            [({'C'}, set(), {1}),
             ({'A'}, {0}, set())],
            ['A', 'B', 'C', 'D'])

        singleSubLinko4_4 = linkoCreate.Linkograph(
            [({'A'}, set(), set())],
            ['A', 'B', 'C', 'D'])

        simpleLinko = linkoCreate.Linkograph(
            [({'A', 'B', 'C'}, set(), {1,2,3}),
             ({'D'}, {0}, {3,4}),
             ({'A'}, {0}, {4}),
             ({'B', 'C'}, {0,1}, {4}),
             ({'A'}, {1,2,3}, set())],
            ['A', 'B', 'C', 'D'])

        if self.id().split('.')[-1] == 'test_createSubLinkographWithoutCommands':
            self.testParams = [
                {'linko': singleLabels,
                 'lowerBound': None,
                 'upperBound': None,
                 'ExpectedLinkograph': singleLabels},

                {'linko': singleLabels,
                 'lowerBound': 0,
                 'upperBound': 4,
                 'ExpectedLinkograph': singleLabels},

                {'linko': singleLabels,
                 'lowerBound': 0,
                 'upperBound': 5,
                 'ExpectedLinkograph': singleLabels},

                {'linko': singleLabels,
                 'lowerBound': 0,
                 'upperBound': 2,
                 'ExpectedLinkograph': singleSubLinko0_2},

                {'linko': singleLabels,
                 'lowerBound': -1,
                 'upperBound': 2,
                 'ExpectedLinkograph': singleSubLinko0_2},

                {'linko': singleLabels,
                 'lowerBound': None,
                 'upperBound': 2,
                 'ExpectedLinkograph': singleSubLinko0_2},

                {'linko': singleLabels,
                 'lowerBound': 0,
                 'upperBound': 1,
                 'ExpectedLinkograph': singleSubLinko0_1},

                {'linko': singleLabels,
                 'lowerBound': 0,
                 'upperBound': 0,
                 'ExpectedLinkograph': singleSubLinko0_0},

                {'linko': singleLabels,
                 'lowerBound': 0,
                 'upperBound': -1,
                 'ExpectedLinkograph': trivialLinkograph},

                {'linko': singleLabels,
                 'lowerBound': 1,
                 'upperBound': 2,
                 'ExpectedLinkograph': singleSubLinko1_2},

                {'linko': singleLabels,
                 'lowerBound': 1,
                 'upperBound': 1,
                 'ExpectedLinkograph': singleSubLinko1_1},

                {'linko': singleLabels,
                 'lowerBound': 1,
                 'upperBound': 0,
                 'ExpectedLinkograph': trivialLinkograph},

                {'linko': singleLabels,
                 'lowerBound': -1,
                 'upperBound': -1,
                 'ExpectedLinkograph': trivialLinkograph},

                {'linko': singleLabels,
                 'lowerBound': 1,
                 'upperBound': 4,
                 'ExpectedLinkograph': singleSubLinko1_4},

                {'linko': singleLabels,
                 'lowerBound': 2,
                 'upperBound': 4,
                 'ExpectedLinkograph': singleSubLinko2_4},

                {'linko': singleLabels,
                 'lowerBound': 3,
                 'upperBound': 4,
                 'ExpectedLinkograph': singleSubLinko3_4},

                {'linko': singleLabels,
                 'lowerBound': 4,
                 'upperBound': 4,
                 'ExpectedLinkograph': singleSubLinko4_4},

            ]

    def performTestForParams(self):
        """"Performs the tests for each set of parameters."""
        for (testNum, params) in enumerate(self.testParams):
            actualLinkograph = linkoCreate.createSubLinko(params['linko'],
                                                          params['lowerBound'],
                                                          params['upperBound'])
            self.assertEqual(
                actualLinkograph,
                params['ExpectedLinkograph'],
                (" linko = {}"
                 " lowerBound = {}"
                 " upperBound = {}"
                 " actualLinkograph = {}"
                 " ExpectedLinkograph = {}")
                .format(params['linko'],
                        params['lowerBound'],
                        params['upperBound'],
                        actualLinkograph,
                        params['ExpectedLinkograph']))

    def test_createSubLinkographWithoutCommands(self):
        """Tests the createSubLinkograph function ingoring commands option."""
        self.performTestForParams()

class Test_checkLinkoStructure(unittest.TestCase):
    """
    Tests the checkLinkoStructure function.

    """

    def setUp(self):
        """Set up the parameters for the individual tests."""

        if self.id().split('.')[-1] == 'test_checkLinkoStructure':
            self.testParams = [
                {'linko':
                 linkoCreate.Linkograph(
                     [({'L0'}, set(), {1, 2}),
                      ({'L0'}, set(), {2}),
                      ({'L0'}, {0,1}, set())]),
                 'labels': False,
                 'expectedResult': False,
                 'expectedErrors':
                 {1: ({0}, set())
                 }
                },
                {'linko':
                 linkoCreate.Linkograph(
                     [({'L0'}, set(), {1, 2}),
                      ({'L0'}, {0}, set()),
                      ({'L0'}, {0,1}, set())]),
                 'labels': False,
                 'expectedResult': False,
                 'expectedErrors':
                 {1: (set(), {2})
                 }
                },
                {'linko':
                 linkoCreate.Linkograph(
                     [({'L0'}, set(), {1, 2}),
                      ({'L0'}, {0}, {2}),
                      ({'L0'}, {0,1}, set())]),
                 'labels': False,
                 'expectedResult': True,
                 'expectedErrors': {}
                },
                {'linko':
                 linkoCreate.Linkograph(
                     [({'L0'}, set(), {1, 2, 5}),
                      ({'L0'}, {0}, {2}),
                      ({'L0'}, {0,1}, set())]),
                 'labels': False,
                 'expectedResult': False,
                 'expectedErrors':
                 {
                     'missing': {5},
                     5: ({0}, set())
                 }
                },
                ]

    def performTestForParams(self):
        """"Performs the tests for each set of parameters."""
        for (testNum, params) in enumerate(self.testParams):
            result, actualError = linkoCreate.checkLinkoStructure(params['linko'],
                                                                  params['labels'])

            self.assertEqual(result, params['expectedResult'])

            self.assertEqual(
                actualError,
                params['expectedErrors'],
                (" labels = {}"
                 " actualError = {}"
                 " expectedError = {}")
                .format(params['labels'],
                        actualError,
                        params['expectedErrors']))

    def test_checkLinkoStructure(self):
        """Tests the createLinko function."""
        self.performTestForParams()
