#!/usr/bin/env python3

"""Tests the stats.py package."""

import unittest
from linkograph import stats # The package under test.
from linkograph import linkoCreate # For creating linkographs.
import math # For the log function.
from collections import Counter # For Counter data structures.


class Test_totalLinks(unittest.TestCase):

    """Basic unit tests for totalLinks in the stats package."""

    def setUp(self):
        """Set up the parameters for the individual tests."""

        if self.id().split('.')[-1] == 'test_totalLinks':
            self.testParams = [
                {'NumberOfNodes': 0,
                 'ExpectedTotal': 0},
                {'NumberOfNodes': 1,
                 'ExpectedTotal': 0},
                {'NumberOfNodes': 2,
                 'ExpectedTotal': 1},
                {'NumberOfNodes': 3,
                 'ExpectedTotal': 3},
                {'NumberOfNodes': 4,
                 'ExpectedTotal': 6},
                {'NumberOfNodes': 5,
                 'ExpectedTotal': 10},
                {'NumberOfNodes': 6,
                 'ExpectedTotal': 15}]

    def performTestForParams(self):
        """"Performs the tests for each set of parameters."""
        for params in self.testParams:
            actual = stats.totalLinks(params['NumberOfNodes'])
            self.assertEqual(
                actual,
                params['ExpectedTotal'],
                ("Test fail: Number of Nodes = {}"
                 " Actual = {}"
                 " ExpectedTotal = {}")
                .format(params['NumberOfNodes'],
                        actual,
                        params['ExpectedTotal']))

    def test_totalLinks(self):
        """Tests for the correct number of total links."""
        self.performTestForParams()


class Test_totalLinkographs(unittest.TestCase):

    """Basic unit tests for totalLinkographs in the stats package."""

    def setUp(self):
        """Set up the parameters for the individual tests."""

        if self.id().split('.')[-1] == 'test_totalLinkographs':
            self.testParams = [
                {'NumberOfNodes': 0,
                 'ExpectedTotal': 1},
                {'NumberOfNodes': 1,
                 'ExpectedTotal': 1},
                {'NumberOfNodes': 2,
                 'ExpectedTotal': 2},
                {'NumberOfNodes': 3,
                 'ExpectedTotal': 8},
                {'NumberOfNodes': 4,
                 'ExpectedTotal': 2**6},
                {'NumberOfNodes': 5,
                 'ExpectedTotal': 2**10},
                {'NumberOfNodes': 6,
                 'ExpectedTotal': 2**15}]

    def performTestForParams(self):
        """"Performs the tests for each set of parameters."""
        for params in self.testParams:
            actual = stats.totalLinkographs(params['NumberOfNodes'])
            self.assertEqual(
                actual,
                params['ExpectedTotal'],
                ("Test fail: Number of Nodes = {}"
                 " Actual = {}"
                 " ExpectedTotal = {}")
                .format(params['NumberOfNodes'],
                        actual,
                        params['ExpectedTotal']))

    def test_totalLinkographs(self):
        """Tests for the correct number of total links."""
        self.performTestForParams()

class Test_totalLabels(unittest.TestCase):

    """Basic unit tests for totalLabels in the stats package."""

    def setUp(self):
        """Set up the parameters for the individual tests."""

        singleLabels = linkoCreate.Linkograph(
            [({'A'}, set(), {1,2,3}),
             ({'D'}, {0}, {3,4}),
             ({'A'}, {0}, {4}),
             ({'C'}, {0,1}, {4}),
             ({'A'}, {1,2,3}, set())],
            ['A', 'B', 'C', 'D'])


        simpleLinko = linkoCreate.Linkograph(
                                  [({'A', 'B', 'C'}, set(), {1,2,3}),
                                   ({'D'}, {0}, {3,4}),
                                   ({'A'}, {0}, {4}),
                                   ({'B', 'C'}, {0,1}, {4}),
                                   ({'A'}, {1,2,3}, set())],
                                  ['A', 'B', 'C', 'D'])


        if self.id().split('.')[-1] == 'test_singleLabelPerLine':
            self.testParams = [
                {'Linkograph': singleLabels,
                 'lowerBound': None,
                 'upperBound': None,
                 'ExpectedCount': Counter({'A': 3,
                                           'C': 1,
                                           'D': 1})},
                {'Linkograph': singleLabels,
                 'lowerBound': -1,
                 'upperBound': None,
                 'ExpectedCount': Counter({'A': 3,
                                           'C': 1,
                                           'D': 1})},
                {'Linkograph': singleLabels,
                 'lowerBound': 0,
                 'upperBound': None,
                 'ExpectedCount': Counter({'A': 3,
                                           'C': 1,
                                           'D': 1})},
                {'Linkograph': singleLabels,
                 'lowerBound': 1,
                 'upperBound': None,
                 'ExpectedCount': Counter({'A': 2,
                                           'C': 1,
                                           'D': 1})},
                {'Linkograph': singleLabels,
                 'lowerBound': None,
                 'upperBound': 5,
                 'ExpectedCount': Counter({'A': 3,
                                           'C': 1,
                                           'D': 1})},
                {'Linkograph': singleLabels,
                 'lowerBound': None,
                 'upperBound': 4,
                 'ExpectedCount': Counter({'A': 3,
                                           'C': 1,
                                           'D': 1})},
                {'Linkograph': singleLabels,
                 'lowerBound': None,
                 'upperBound': 3,
                 'ExpectedCount': Counter({'A': 2,
                                           'C': 1,
                                           'D': 1})},
                {'Linkograph': singleLabels,
                 'lowerBound': -1,
                 'upperBound': 5,
                 'ExpectedCount': Counter({'A': 3,
                                           'C': 1,
                                           'D': 1})},
                {'Linkograph': singleLabels,
                 'lowerBound': 0,
                 'upperBound': 4,
                 'ExpectedCount': Counter({'A': 3,
                                           'C': 1,
                                           'D': 1})},
                {'Linkograph': singleLabels,
                 'lowerBound': 1,
                 'upperBound': 3,
                 'ExpectedCount': Counter({'A': 1,
                                           'C': 1,
                                           'D': 1})},
                {'Linkograph': singleLabels,
                 'lowerBound': 1,
                 'upperBound': 2,
                 'ExpectedCount': Counter({'A': 1,
                                           'D': 1})},
                {'Linkograph': singleLabels,
                 'lowerBound': 2,
                 'upperBound': 2,
                 'ExpectedCount': Counter({'A': 1})},

                {'Linkograph': singleLabels,
                 'lowerBound': 2,
                 'upperBound': 1,
                 'ExpectedCount': Counter({})}


            ]
        if self.id().split('.')[-1] == 'test_multipleLabelPerLine':
            self.testParams = [
                {'Linkograph': simpleLinko,
                 'lowerBound': -1,
                 'upperBound': None,
                 'ExpectedCount': Counter({'A': 3,
                                           'B': 2,
                                           'C': 2,
                                           'D': 1})},
                {'Linkograph': simpleLinko,
                 'lowerBound': 0,
                 'upperBound': None,
                 'ExpectedCount': Counter({'A': 3,
                                           'B': 2,
                                           'C': 2,
                                           'D': 1})},
                {'Linkograph': simpleLinko,
                 'lowerBound': 1,
                 'upperBound': None,
                 'ExpectedCount': Counter({'A': 2,
                                           'B': 1,
                                           'C': 1,
                                           'D': 1})},
                {'Linkograph': simpleLinko,
                 'lowerBound': None,
                 'upperBound': 5,
                 'ExpectedCount': Counter({'A': 3,
                                           'B': 2,
                                           'C': 2,
                                           'D': 1})},
                {'Linkograph': simpleLinko,
                 'lowerBound': None,
                 'upperBound': 4,
                 'ExpectedCount': Counter({'A': 3,
                                           'B': 2,
                                           'C': 2,
                                           'D': 1})},
                {'Linkograph': simpleLinko,
                 'lowerBound': None,
                 'upperBound': 3,
                 'ExpectedCount': Counter({'A': 2,
                                           'B': 2,
                                           'C': 2,
                                           'D': 1})},
                {'Linkograph': simpleLinko,
                 'lowerBound': 1,
                 'upperBound': 3,
                 'ExpectedCount': Counter({'A': 1,
                                           'B': 1,
                                           'C': 1,
                                           'D': 1})}
                ]

    def performTestForParams(self):
        """"Performs the tests for each set of parameters."""
        for params in self.testParams:
            actualCount = stats.totalLabels(params['Linkograph'],
                                            params['lowerBound'],
                                            params['upperBound'])
            self.assertEqual(
                actualCount,
                params['ExpectedCount'],
                ("Test fail: linkograph {}"
                 " lowerBound = {}"
                 " upperBound = {}"
                 " actualCount = {}"
                 " ExpectedCount = {}")
                .format(params['Linkograph'],
                        params['lowerBound'],
                        params['upperBound'],
                        actualCount,
                        params['ExpectedCount']))

    def test_singleLabelPerLine(self):
        """Tests for correct number of labels with one label per line."""
        self.performTestForParams()

    def test_multipleLabelPerLine(self):
        """Test for correct number of labels with multiple labels."""
        self.performTestForParams()

class Test_percentageOfEntries(unittest.TestCase):

    """Basic unit tests for percentageOfEntries in the stats package."""

    def setUp(self):
        """Set up the parameters for the individual tests."""

        singleLabels = linkoCreate.Linkograph(
            [({'A'}, set(), {1,2,3}),
             ({'D'}, {0}, {3,4}),
             ({'A'}, {0}, {4}),
             ({'C'}, {0,1}, {4}),
             ({'A'}, {1,2,3}, set())],
            ['A', 'B', 'C', 'D'])


        simpleLinko = linkoCreate.Linkograph(
                                  [({'A', 'B', 'C'}, set(), {1,2,3}),
                                   ({'D'}, {0}, {3,4}),
                                   ({'A'}, {0}, {4}),
                                   ({'B', 'C'}, {0,1}, {4}),
                                   ({'A'}, {1,2,3}, set())],
                                  ['A', 'B', 'C', 'D'])


        if self.id().split('.')[-1] == 'test_singleLabelPerLine':
            self.testParams = [
                {'Linkograph': singleLabels,
                 'lowerBound': -1,
                 'upperBound': None,
                 'ExpectedPercentage': {'A': 3/5,
                                        'C': 1/5,
                                        'D': 1/5}},
                {'Linkograph': singleLabels,
                 'lowerBound': 0,
                 'upperBound': None,
                 'ExpectedPercentage': {'A': 3/5,
                                        'C': 1/5,
                                        'D': 1/5}},

                {'Linkograph': singleLabels,
                 'lowerBound': 1,
                 'upperBound': None,
                 'ExpectedPercentage': {'A': 2/4,
                                        'C': 1/4,
                                        'D': 1/4}},

                {'Linkograph': singleLabels,
                 'lowerBound': None,
                 'upperBound': 5,
                 'ExpectedPercentage': {'A': 3/5,
                                        'C': 1/5,
                                        'D': 1/5}},

                {'Linkograph': singleLabels,
                 'lowerBound': None,
                 'upperBound': 4,
                 'ExpectedPercentage': {'A': 3/5,
                                        'C': 1/5,
                                        'D': 1/5}},

                {'Linkograph': singleLabels,
                 'lowerBound': None,
                 'upperBound': 3,
                 'ExpectedPercentage': {'A': 2/4,
                                        'C': 1/4,
                                        'D': 1/4}},

                {'Linkograph': singleLabels,
                 'lowerBound': 1,
                 'upperBound': 3,
                 'ExpectedPercentage': {'A': 1/3,
                                        'C': 1/3,
                                        'D': 1/3}},

                {'Linkograph': singleLabels,
                 'lowerBound': 3,
                 'upperBound': 3,
                 'ExpectedPercentage': {'C': 1}},

                {'Linkograph': singleLabels,
                 'lowerBound': 4,
                 'upperBound': 3,
                 'ExpectedPercentage': {}}



            ]
        if self.id().split('.')[-1] == 'test_multipleLabelPerLine':
            self.testParams = [
                {'Linkograph': simpleLinko,
                 'lowerBound': -1,
                 'upperBound': None,
                 'ExpectedPercentage': {'A': 3/5,
                                        'B': 2/5,
                                        'C': 2/5,
                                        'D': 1/5}},

                {'Linkograph': simpleLinko,
                 'lowerBound': 0,
                 'upperBound': None,
                 'ExpectedPercentage': {'A': 3/5,
                                        'B': 2/5,
                                        'C': 2/5,
                                        'D': 1/5}},

                {'Linkograph': simpleLinko,
                 'lowerBound': 1,
                 'upperBound': None,
                 'ExpectedPercentage': {'A': 2/4,
                                        'B': 1/4,
                                        'C': 1/4,
                                        'D': 1/4}},

                {'Linkograph': simpleLinko,
                 'lowerBound': None,
                 'upperBound': 5,
                 'ExpectedPercentage': {'A': 3/5,
                                        'B': 2/5,
                                        'C': 2/5,
                                        'D': 1/5}},

                {'Linkograph': simpleLinko,
                 'lowerBound': None,
                 'upperBound': 4,
                 'ExpectedPercentage': {'A': 3/5,
                                        'B': 2/5,
                                        'C': 2/5,
                                        'D': 1/5}},

                {'Linkograph': simpleLinko,
                 'lowerBound': None,
                 'upperBound': 3,
                 'ExpectedPercentage': {'A': 2/4,
                                        'B': 2/4,
                                        'C': 2/4,
                                        'D': 1/4}},

                {'Linkograph': simpleLinko,
                 'lowerBound': 1,
                 'upperBound': 3,
                 'ExpectedPercentage': {'A': 1/3,
                                        'B': 1/3,
                                        'C': 1/3,
                                        'D': 1/3}},

                {'Linkograph': simpleLinko,
                 'lowerBound': 2,
                 'upperBound': 1,
                 'ExpectedPercentage': {}}
                ]

    def performTestForParams(self):
        """"Performs the tests for each set of parameters."""
        for params in self.testParams:
            actualPercentage = stats.percentageOfEntries(
                params['Linkograph'],
                params['lowerBound'],
                params['upperBound'])
            self.assertEqual(
                actualPercentage,
                params['ExpectedPercentage'],
                ("Test fail: linkograph {}"
                 " lowerBound = {}"
                 " upperBound = {}"
                 " actualPercentage = {}"
                 " ExpectedPercentage = {}")
                .format(params['Linkograph'],
                        params['lowerBound'],
                        params['upperBound'],
                        actualPercentage,
                        params['ExpectedPercentage']))

    def test_singleLabelPerLine(self):
        """Tests for correct percentage for linkograph with one label per line."""
        self.performTestForParams()

    def test_multipleLabelPerLine(self):
        """Test for correct percentage for linkograph with multiple labels."""
        self.performTestForParams()

class Test_links(unittest.TestCase):

    """Basic unit tests for links in the stats package."""

    def setUp(self):
        """Set up the parameters for the individual tests."""

        singleLabels = linkoCreate.Linkograph(
            [({'A'}, set(), {1,2,3}),
             ({'D'}, {0}, {3,4}),
             ({'A'}, {0}, {4}),
             ({'C'}, {0,1}, {4}),
             ({'A'}, {1,2,3}, set())],
            ['A', 'B', 'C', 'D'])


        simpleLinko = linkoCreate.Linkograph(
                                  [({'A', 'B', 'C'}, set(), {1,2,3}),
                                   ({'D'}, {0}, {3,4}),
                                   ({'A'}, {0}, {4}),
                                   ({'B', 'C'}, {0,1}, {4}),
                                   ({'A'}, {1,2,3}, set())],
                                  ['A', 'B', 'C', 'D'])


        if self.id().split('.')[-1] == 'test_singleLabelPerLine':
            self.testParams = [
                {'Linkograph': singleLabels,
                 'lowerBound': -1,
                 'upperBound': None,
                 'ExpectedLinks': 7},

                {'Linkograph': singleLabels,
                 'lowerBound': 0,
                 'upperBound': None,
                 'ExpectedLinks': 7},

                {'Linkograph': singleLabels,
                 'lowerBound': 1,
                 'upperBound': None,
                 'ExpectedLinks': 4},

                {'Linkograph': singleLabels,
                 'lowerBound': None,
                 'upperBound': 5,
                 'ExpectedLinks': 7},

                {'Linkograph': singleLabels,
                 'lowerBound': None,
                 'upperBound': 4,
                 'ExpectedLinks': 7},

                {'Linkograph': singleLabels,
                 'lowerBound': None,
                 'upperBound': 3,
                 'ExpectedLinks': 4},

                {'Linkograph': singleLabels,
                 'lowerBound': 1,
                 'upperBound': 3,
                 'ExpectedLinks': 1},

                {'Linkograph': singleLabels,
                 'lowerBound': 2,
                 'upperBound': 3,
                 'ExpectedLinks': 0},

                {'Linkograph': singleLabels,
                 'lowerBound': 3,
                 'upperBound': 2,
                 'ExpectedLinks': 0},


            ]
        if self.id().split('.')[-1] == 'test_multipleLabelPerLine':
            self.testParams = [
                {'Linkograph': simpleLinko,
                 'lowerBound': -1,
                 'upperBound': None,
                 'ExpectedLinks': 7},

                {'Linkograph': simpleLinko,
                 'lowerBound': 0,
                 'upperBound': None,
                 'ExpectedLinks': 7},

                {'Linkograph': simpleLinko,
                 'lowerBound': 1,
                 'upperBound': None,
                 'ExpectedLinks': 4},

                {'Linkograph': simpleLinko,
                 'lowerBound': None,
                 'upperBound': 5,
                 'ExpectedLinks': 7},

                {'Linkograph': simpleLinko,
                 'lowerBound': None,
                 'upperBound': 4,
                 'ExpectedLinks': 7},

                {'Linkograph': simpleLinko,
                 'lowerBound': None,
                 'upperBound': 3,
                 'ExpectedLinks': 4},

                {'Linkograph': simpleLinko,
                 'lowerBound': 1,
                 'upperBound': 3,
                 'ExpectedLinks': 1},

                {'Linkograph': simpleLinko,
                 'lowerBound': 2,
                 'upperBound': 3,
                 'ExpectedLinks': 0},

                {'Linkograph': simpleLinko,
                 'lowerBound': 3,
                 'upperBound': 2,
                 'ExpectedLinks': 0},

                ]

    def performTestForParams(self):
        """"Performs the tests for each set of parameters."""
        for params in self.testParams:
            actualLinks = stats.links(
                params['Linkograph'],
                params['lowerBound'],
                params['upperBound'])
            self.assertEqual(
                actualLinks,
                params['ExpectedLinks'],
                ("Test fail: linkograph {}"
                 " lowerBound = {}"
                 " upperBound = {}"
                 " actualLinks = {}"
                 " ExpectedLinks = {}")
                .format(params['Linkograph'],
                        params['lowerBound'],
                        params['upperBound'],
                        actualLinks,
                        params['ExpectedLinks']))

    def test_singleLabelPerLine(self):
        """Tests for correct number of links for linkograph with one label per line."""
        self.performTestForParams()

    def test_multipleLabelPerLine(self):
        """Test for correct number of links for linkograph with multiple labels."""
        self.performTestForParams()


class Test_linkCount(unittest.TestCase):

    """Basic unit tests for linkCount in the stats package."""

    def setUp(self):
        """Set up the parameters for the individual tests."""

        tuple0 = [{'A', 'B'}, {0,1,2,3,4,5,6}, {1,3,5,7}]
        tuple1 = [{'A', 'B'}, {0,1,2,3,4}, {5,6,7,8}]

        if self.id().split('.')[-1] == 'test_firstList':
            self.testParams = [
                {'tupleOfLists': tuple0,
                 'listNumber': {1},
                 'lowerBound': 0,
                 'upperBound': 7,
                 'ExpectedLinks': 7},

                {'tupleOfLists': tuple0,
                 'listNumber': {1},
                 'lowerBound': 0,
                 'upperBound': 8,
                 'ExpectedLinks': 7},

                {'tupleOfLists': tuple0,
                 'listNumber': {1},
                 'lowerBound': 2,
                 'upperBound': 7,
                 'ExpectedLinks': 5},

                {'tupleOfLists': tuple0,
                 'listNumber': {1},
                 'lowerBound': 0,
                 'upperBound': 5,
                 'ExpectedLinks': 6},

                {'tupleOfLists': tuple0,
                 'listNumber': {1},
                 'lowerBound': 7,
                 'upperBound': 8,
                 'ExpectedLinks': 0},

                {'tupleOfLists': tuple0,
                 'listNumber': {1},
                 'lowerBound': 0,
                 'upperBound': 0,
                 'ExpectedLinks': 1}

            ]
        if self.id().split('.')[-1] == 'test_secondList':
            self.testParams = [
                {'tupleOfLists': tuple0,
                 'listNumber': {2},
                 'lowerBound': 0,
                 'upperBound': 7,
                 'ExpectedLinks': 4},

                {'tupleOfLists': tuple0,
                 'listNumber': {2},
                 'lowerBound': 1,
                 'upperBound': 7,
                 'ExpectedLinks': 4},


                {'tupleOfLists': tuple0,
                 'listNumber': {2},
                 'lowerBound': 2,
                 'upperBound': 7,
                 'ExpectedLinks': 3},

                {'tupleOfLists': tuple0,
                 'listNumber': {2},
                 'lowerBound': 1,
                 'upperBound': 5,
                 'ExpectedLinks': 3},

                ]
        if self.id().split('.')[-1] == 'test_firstSecondList':
            self.testParams = [
                {'tupleOfLists': tuple1,
                 'listNumber': {1,2},
                 'lowerBound': 0,
                 'upperBound': 8,
                 'ExpectedLinks': 9},

                {'tupleOfLists': tuple1,
                 'listNumber': {1,2},
                 'lowerBound': 1,
                 'upperBound': 7,
                 'ExpectedLinks': 7},


                {'tupleOfLists': tuple1,
                 'listNumber': {1,2},
                 'lowerBound': 2,
                 'upperBound': 7,
                 'ExpectedLinks': 6},

                {'tupleOfLists': tuple1,
                 'listNumber': {1,2},
                 'lowerBound': 1,
                 'upperBound': 5,
                 'ExpectedLinks': 5},

                {'tupleOfLists': tuple1,
                 'listNumber': {1,2},
                 'lowerBound': 1,
                 'upperBound': 4,
                 'ExpectedLinks': 4},

                {'tupleOfLists': tuple1,
                 'listNumber': {1,2},
                 'lowerBound': 5,
                 'upperBound': 8,
                 'ExpectedLinks': 4},

                ]

    def performTestForParams(self):
        """"Performs the tests for each set of parameters."""
        for params in self.testParams:
            actualLinks = stats.linkCount(
                params['tupleOfLists'],
                params['listNumber'],
                params['lowerBound'],
                params['upperBound'])
            self.assertEqual(
                actualLinks,
                params['ExpectedLinks'],
                ("Test fail: linkograph {}"
                 " listNumber = {}"
                 " lowerBound = {}"
                 " upperBound = {}"
                 " actualLinks = {}"
                 " ExpectedLinks = {}")
                .format(params['tupleOfLists'],
                        params['listNumber'],
                        params['lowerBound'],
                        params['upperBound'],
                        actualLinks,
                        params['ExpectedLinks']))

    def test_firstList(self):
        """Tests for the correct link count for the first list."""
        self.performTestForParams()

    def test_secondList(self):
        """Test for the correct link count for the second list."""
        self.performTestForParams()

    def test_firstSecondList(self):
        """Test for correct link count for the the first and second lsit."""
        self.performTestForParams()

class Test_linkTotal(unittest.TestCase):

    """Basic unit tests for the correct link total in the stats package."""

    def setUp(self):
        """Set up the parameters for the individual tests."""

        if self.id().split('.')[-1] == 'test_forelinks':
            # Note: in a linkograph, the third set (index 2) has the
            # forelinks.
            self.testParams = [
                {'currentIndex': 9,
                 'linkNumber': {2},
                 'lowerBound': 0,
                 'upperBound': 10,
                 'ExpectedLinkTotal': 1},

                {'currentIndex': 8,
                 'linkNumber': {2},
                 'lowerBound': 0,
                 'upperBound': 10,
                 'ExpectedLinkTotal': 2},

            ]
        if self.id().split('.')[-1] == 'test_backlinks':
            self.testParams = [
                {'currentIndex': 2,
                 'linkNumber': {1},
                 'lowerBound': 1,
                 'upperBound': 10,
                 'ExpectedLinkTotal': 1},

                {'currentIndex': 2,
                 'linkNumber': {1},
                 'lowerBound': 0,
                 'upperBound': 10,
                 'ExpectedLinkTotal': 2}
                ]

        if self.id().split('.')[-1] == 'test_total':
            self.testParams = [
                {'currentIndex': 5,
                 'linkNumber': {1,2},
                 'lowerBound': 0,
                 'upperBound': 10,
                 'ExpectedLinkTotal': 10},

                ]


    def performTestForParams(self):
        """"Performs the tests for each set of parameters."""
        for params in self.testParams:
            actualLinkTotal = stats.linkTotal(
                params['currentIndex'],
                params['linkNumber'],
                params['lowerBound'],
                params['upperBound'])
            self.assertEqual(
                actualLinkTotal,
                params['ExpectedLinkTotal'],
                ("Test fail: currentIndex = {}"
                 " linkNumber = {}"
                 " lowerBound = {}"
                 " upperBound = {}"
                 " actualLinkTotal = {}"
                 " ExpectedLinkTotal = {}")
                .format(params['currentIndex'],
                        params['linkNumber'],
                        params['lowerBound'],
                        params['upperBound'],
                        actualLinkTotal,
                        params['ExpectedLinkTotal']))

    def test_forelinks(self):
        """Tests for correct number of links for forelinks."""
        self.performTestForParams()

    def test_backlinks(self):
        """Test for correct number of links for backlinks."""
        self.performTestForParams()

    def test_total(self):
        """Test for correct number of links for both backlinks and forelinks."""
        self.performTestForParams()

class Test_percentageOfLinks(unittest.TestCase):

    """Basic unit tests for the correct link percent in the stats package."""

    def setUp(self):
        """Set up the parameters for the individual tests."""

        simpleLinko = linkoCreate.Linkograph(
            [({'A', 'B', 'C'}, set(), {1,2,3}),
             ({'D'}, {0}, {3,4}),
             ({'A'}, {0}, {4}),
             ({'B', 'C'}, {0,1}, {4}),
             ({'A'}, {1,2,3}, set())],
            ['A', 'B', 'C', 'D'])


        if self.id().split('.')[-1] == 'test_links':
            self.testParams = [
                {'linkograph': simpleLinko,
                 'lowerBound': None,
                 'upperBound': None,
                 'ExpectedPercentage': 7/10},

                {'linkograph': simpleLinko,
                 'lowerBound': 0,
                 'upperBound': None,
                 'ExpectedPercentage': 7/10},

                {'linkograph': simpleLinko,
                 'lowerBound': -1,
                 'upperBound': None,
                 'ExpectedPercentage': 7/10},

                {'linkograph': simpleLinko,
                 'lowerBound': None,
                 'upperBound': 5,
                 'ExpectedPercentage': 7/10},

                {'linkograph': simpleLinko,
                 'lowerBound': None,
                 'upperBound': 4,
                 'ExpectedPercentage': 7/10},

                {'linkograph': simpleLinko,
                 'lowerBound': 0,
                 'upperBound': 4,
                 'ExpectedPercentage': 7/10},

                {'linkograph': simpleLinko,
                 'lowerBound': 1,
                 'upperBound': None,
                 'ExpectedPercentage': 4/6},

                {'linkograph': simpleLinko,
                 'lowerBound': 1,
                 'upperBound': 3,
                 'ExpectedPercentage': 1/3},
            ]


    def performTestForParams(self):
        """"Performs the tests for each set of parameters."""
        for params in self.testParams:
            actualPercentage = stats.percentageOfLinks(
                params['linkograph'],
                params['lowerBound'],
                params['upperBound'])
            self.assertEqual(
                actualPercentage,
                params['ExpectedPercentage'],
                ("Test fail: linkograph = {}"
                 " lowerBound = {}"
                 " upperBound = {}"
                 " actualPercentage = {}"
                 " ExpectedPercentage = {}")
                .format(params['linkograph'],
                        params['lowerBound'],
                        params['upperBound'],
                        actualPercentage,
                        params['ExpectedPercentage']))

    def test_links(self):
        """Tests for correct percent of links."""
        self.performTestForParams()

class Test_graphEntropy(unittest.TestCase):

    """Basic unit tests the entropy in the stats package."""

    def setUp(self):
        """Set up the parameters for the individual tests."""

        simpleLinko = linkoCreate.Linkograph(
            [({'A', 'B', 'C'}, set(), {1,2,3}),
             ({'D'}, {0}, {3,4}),
             ({'A'}, {0}, {4}),
             ({'B', 'C'}, {0,1}, {4}),
             ({'A'}, {1,2,3}, set())],
            ['A', 'B', 'C', 'D'])


        if self.id().split('.')[-1] == 'test_entropy':
            self.testParams = [
                {'linkograph': simpleLinko,
                 'lowerBound': None,
                 'upperBound': None,
                 'ExpectedEntropy': -(0.7)*math.log(0.7,2)
                 - (0.3)*math.log(0.3,2)},

                {'linkograph': simpleLinko,
                 'lowerBound': 0,
                 'upperBound': None,
                 'ExpectedEntropy': -(0.7)*math.log(0.7,2)
                 - (0.3)*math.log(0.3,2)},

                {'linkograph': simpleLinko,
                 'lowerBound': -1,
                 'upperBound': None,
                 'ExpectedEntropy': -(0.7)*math.log(0.7,2)
                 - (0.3)*math.log(0.3,2)},

                {'linkograph': simpleLinko,
                 'lowerBound': None,
                 'upperBound': 5,
                 'ExpectedEntropy': -(0.7)*math.log(0.7,2)
                 - (0.3)*math.log(0.3,2)},

                {'linkograph': simpleLinko,
                 'lowerBound': None,
                 'upperBound': 4,
                 'ExpectedEntropy': -(0.7)*math.log(0.7,2)
                 - (0.3)*math.log(0.3,2)},

                {'linkograph': simpleLinko,
                 'lowerBound': 0,
                 'upperBound': 4,
                 'ExpectedEntropy': -(0.7)*math.log(0.7,2)
                 - (0.3)*math.log(0.3,2)},

                {'linkograph': simpleLinko,
                 'lowerBound': 1,
                 'upperBound': 4,
                 'ExpectedEntropy': -(4/6)*math.log(4/6,2)
                 - (2/6)*math.log(2/6,2)},

                {'linkograph': simpleLinko,
                 'lowerBound': 1,
                 'upperBound': 3,
                 'ExpectedEntropy': -(1/3)*math.log(1/3,2)
                 - (2/3)*math.log(2/3,2)}

            ]


    def performTestForParams(self):
        """"Performs the tests for each set of parameters."""
        for params in self.testParams:
            actualEntropy = stats.graphEntropy(
                params['linkograph'],
                params['lowerBound'],
                params['upperBound'])
            self.assertEqual(
                actualEntropy,
                params['ExpectedEntropy'],
                ("Test fail: linkograph = {}"
                 " lowerBound = {}"
                 " upperBound = {}"
                 " actualEntropy = {}"
                 " ExpectedEntropy = {}")
                .format(params['linkograph'],
                        params['lowerBound'],
                        params['upperBound'],
                        actualEntropy,
                        params['ExpectedEntropy']))

    def test_entropy(self):
        """Tests for correct entropy."""
        self.performTestForParams()


class Test_shannonEntropy(unittest.TestCase):

    """Basic unit tests the Shannon entropy in the stats package."""

    def setUp(self):
        """Set up the parameters for the individual tests."""

        if self.id().split('.')[-1] == 'test_entropy':
            self.testParams = [
                {'links': 7,
                 'totalLinks': 10,
                 'ExpectedEntropy': -(0.7)*math.log(0.7,2)
                 - (0.3)*math.log(0.3,2)},

                {'links': 4,
                 'totalLinks': 6,
                 'ExpectedEntropy': -(4/6)*math.log(4/6,2)
                 - (2/6)*math.log(2/6,2)},

                {'links': 1,
                 'totalLinks': 3,
                 'ExpectedEntropy': -(1/3)*math.log(1/3,2)
                 - (2/3)*math.log(2/3,2)},

                {'links': 2,
                 'totalLinks': 0,
                 'ExpectedEntropy': 0},

                {'links': 3,
                 'totalLinks': 3,
                 'ExpectedEntropy': 0},

                {'links': 0,
                 'totalLinks': 3,
                 'ExpectedEntropy': 0},

            ]


    def performTestForParams(self):
        """"Performs the tests for each set of parameters."""
        for params in self.testParams:
            actualEntropy = stats.shannonEntropy(
                params['links'],
                params['totalLinks'])
            self.assertEqual(
                actualEntropy,
                params['ExpectedEntropy'],
                ("Test fail: links = {}"
                 " totalLinks = {}"
                 " actualEntropy = {}"
                 " ExpectedEntropy = {}")
                .format(params['links'],
                        params['totalLinks'],
                        actualEntropy,
                        params['ExpectedEntropy']))

    def test_entropy(self):
        """Tests for correct shannon entropy."""
        self.performTestForParams()


class Test_linkEntropy(unittest.TestCase):

    """Basic unit tests the link entropy in the stats package."""

    def setUp(self):
        """Set up the parameters for the individual tests."""

        simpleLinko = linkoCreate.Linkograph(
            [({'A', 'B', 'C'}, set(), {1,2,3}),
             ({'D'}, {0}, {3,4}),
             ({'A'}, {0}, {4}),
             ({'B', 'C'}, {0,1}, {4}),
             ({'A'}, {1,2,3}, set())],
            ['A', 'B', 'C', 'D'])


        if self.id().split('.')[-1] == 'test_foreLinkEntropy':
            self.testParams = [
                {'linkograph': simpleLinko,
                 'linkNumber': [2],
                 'delta': None,
                 'restrict': False,
                 'lowerBound': None,
                 'upperBound': None,
                 'ExpectedEntropy': [-(3/4)*math.log(3/4,2)
                                     - (1/4)*math.log(1/4,2),
                                     -(2/3)*math.log(2/3,2)
                                     - (1/3)*math.log(1/3,2),
                                     -(1/2)*math.log(1/2,2)
                                     - (1/2)*math.log(1/2,2),
                                     0,
                                     0]},

                {'linkograph': simpleLinko,
                 'linkNumber': [2],
                 'delta': None,
                 'restrict': False,
                 'lowerBound': -1,
                 'upperBound': None,
                 'ExpectedEntropy': [-(3/4)*math.log(3/4,2)
                                     - (1/4)*math.log(1/4,2),
                                     -(2/3)*math.log(2/3,2)
                                     - (1/3)*math.log(1/3,2),
                                     -(1/2)*math.log(1/2,2)
                                     - (1/2)*math.log(1/2,2),
                                     0,
                                     0]},

                {'linkograph': simpleLinko,
                 'linkNumber': [2],
                 'delta': None,
                 'restrict': False,
                 'lowerBound': 0,
                 'upperBound': None,
                 'ExpectedEntropy': [-(3/4)*math.log(3/4,2)
                                     - (1/4)*math.log(1/4,2),
                                     -(2/3)*math.log(2/3,2)
                                     - (1/3)*math.log(1/3,2),
                                     -(1/2)*math.log(1/2,2)
                                     - (1/2)*math.log(1/2,2),
                                     0,
                                     0]},

                {'linkograph': simpleLinko,
                 'linkNumber': [2],
                 'delta': None,
                 'restrict': False,
                 'lowerBound': None,
                 'upperBound': 5,
                 'ExpectedEntropy': [-(3/4)*math.log(3/4,2)
                                     - (1/4)*math.log(1/4,2),
                                     -(2/3)*math.log(2/3,2)
                                     - (1/3)*math.log(1/3,2),
                                     -(1/2)*math.log(1/2,2)
                                     - (1/2)*math.log(1/2,2),
                                     0,
                                     0]},

                {'linkograph': simpleLinko,
                 'linkNumber': [2],
                 'delta': None,
                 'restrict': True,
                 'lowerBound': None,
                 'upperBound': None,
                 'ExpectedEntropy': [-(3/4)*math.log(3/4,2)
                                     - (1/4)*math.log(1/4,2),
                                     -(2/3)*math.log(2/3,2)
                                     - (1/3)*math.log(1/3,2),
                                     -(1/2)*math.log(1/2,2)
                                     - (1/2)*math.log(1/2,2),
                                     0,
                                     0]},

                {'linkograph': simpleLinko,
                 'linkNumber': [2],
                 'delta': None,
                 'restrict': False,
                 'lowerBound': 0,
                 'upperBound': 4,
                 'ExpectedEntropy': [-(3/4)*math.log(3/4,2)
                                     - (1/4)*math.log(1/4,2),
                                     -(2/3)*math.log(2/3,2)
                                     - (1/3)*math.log(1/3,2),
                                     -(1/2)*math.log(1/2,2)
                                     - (1/2)*math.log(1/2,2),
                                     0,
                                     0]},


                {'linkograph': simpleLinko,
                 'linkNumber': [2],
                 'delta': None,
                 'restrict': False,
                 'lowerBound': None,
                 'upperBound': 4,
                 'ExpectedEntropy': [-(3/4)*math.log(3/4,2)
                                     - (1/4)*math.log(1/4,2),
                                     -(2/3)*math.log(2/3,2)
                                     - (1/3)*math.log(1/3,2),
                                     -(1/2)*math.log(1/2,2)
                                     - (1/2)*math.log(1/2,2),
                                     0,
                                     0]},

                {'linkograph': simpleLinko,
                 'linkNumber': [2],
                 'delta': None,
                 'restrict': False,
                 'lowerBound': 0,
                 'upperBound': 4,
                 'ExpectedEntropy': [-(3/4)*math.log(3/4,2)
                                     - (1/4)*math.log(1/4,2),
                                     -(2/3)*math.log(2/3,2)
                                     - (1/3)*math.log(1/3,2),
                                     -(1/2)*math.log(1/2,2)
                                     - (1/2)*math.log(1/2,2),
                                     0,
                                     0]},

                {'linkograph': simpleLinko,
                 'linkNumber': [2],
                 'delta': None,
                 'restrict': False,
                 'lowerBound': None,
                 'upperBound': 3,
                 'ExpectedEntropy': [-(3/4)*math.log(3/4,2)
                                     - (1/4)*math.log(1/4,2),
                                     -(2/3)*math.log(2/3,2)
                                     - (1/3)*math.log(1/3,2),
                                     -(1/2)*math.log(1/2,2)
                                     - (1/2)*math.log(1/2,2),
                                     0]},


                {'linkograph': simpleLinko,
                 'linkNumber': [2],
                 'delta': None,
                 'restrict': False,
                 'lowerBound': None,
                 'upperBound': 2,
                 'ExpectedEntropy': [-(3/4)*math.log(3/4,2)
                                     - (1/4)*math.log(1/4,2),
                                     -(2/3)*math.log(2/3,2)
                                     - (1/3)*math.log(1/3,2),
                                     -(1/2)*math.log(1/2,2)
                                     - (1/2)*math.log(1/2,2)]},

                {'linkograph': simpleLinko,
                 'linkNumber': [2],
                 'delta': None,
                 'restrict': False,
                 'lowerBound': 1,
                 'upperBound': None,
                 'ExpectedEntropy': [-(2/3)*math.log(2/3,2)
                                     - (1/3)*math.log(1/3,2),
                                     -(1/2)*math.log(1/2,2)
                                     - (1/2)*math.log(1/2,2),
                                     0,
                                     0]},


                {'linkograph': simpleLinko,
                 'linkNumber': [2],
                 'delta': None,
                 'restrict': False,
                 'lowerBound': 1,
                 'upperBound': 3,
                 'ExpectedEntropy': [-(2/3)*math.log(2/3,2)
                                     - (1/3)*math.log(1/3,2),
                                     -(1/2)*math.log(1/2,2)
                                     - (1/2)*math.log(1/2,2),
                                     0]},

                {'linkograph': simpleLinko,
                 'linkNumber': [2],
                 'delta': None,
                 'restrict': False,
                 'lowerBound': 2,
                 'upperBound': 3,
                 'ExpectedEntropy': [-(1/2)*math.log(1/2,2)
                                     - (1/2)*math.log(1/2,2),
                                     0]},

                {'linkograph': simpleLinko,
                 'linkNumber': [2],
                 'delta': None,
                 'restrict': False,
                 'lowerBound': 2,
                 'upperBound': 2,
                 'ExpectedEntropy': [-(1/2)*math.log(1/2,2)
                                     - (1/2)*math.log(1/2,2)]},

                {'linkograph': simpleLinko,
                 'linkNumber': [2],
                 'delta': None,
                 'restrict': True,
                 'lowerBound': 1,
                 'upperBound': 4,
                 'ExpectedEntropy': [-(2/3)*math.log(2/3,2)
                                     - (1/3)*math.log(1/3,2),
                                     -(1/2)*math.log(1/2,2)
                                     - (1/2)*math.log(1/2,2),
                                     0,
                                     0]},

                {'linkograph': simpleLinko,
                 'linkNumber': [2],
                 'delta': None,
                 'restrict': True,
                 'lowerBound': 0,
                 'upperBound': 3,
                 'ExpectedEntropy': [0,
                                     -(1/2)*math.log(1/2,2)
                                     - (1/2)*math.log(1/2,2),
                                     0,
                                     0]},


                {'linkograph': simpleLinko,
                 'linkNumber': [2],
                 'delta': None,
                 'restrict': True,
                 'lowerBound': 1,
                 'upperBound': 3,
                 'ExpectedEntropy': [-(1/2)*math.log(1/2,2)
                                     - (1/2)*math.log(1/2,2),
                                     0,
                                     0]},

                {'linkograph': simpleLinko,
                 'linkNumber': [2],
                 'delta': None,
                 'restrict': True,
                 'lowerBound': 1,
                 'upperBound': 2,
                 'ExpectedEntropy': [0,
                                     0]},

                {'linkograph': simpleLinko,
                 'linkNumber': [2],
                 'delta': None,
                 'restrict': True,
                 'lowerBound': 1,
                 'upperBound': 1,
                 'ExpectedEntropy': [0]},

                {'linkograph': simpleLinko,
                 'linkNumber': [2],
                 'delta': None,
                 'restrict': False,
                 'lowerBound': 2,
                 'upperBound': 1,
                 'ExpectedEntropy': []},

                {'linkograph': simpleLinko,
                 'linkNumber': [2],
                 'delta': 5,
                 'restrict': False,
                 'lowerBound': None,
                 'upperBound': None,
                 'ExpectedEntropy': [-(3/4)*math.log(3/4,2)
                                     - (1/4)*math.log(1/4,2),
                                     -(2/3)*math.log(2/3,2)
                                     - (1/3)*math.log(1/3,2),
                                     -(1/2)*math.log(1/2,2)
                                     - (1/2)*math.log(1/2,2),
                                     0,
                                     0]},

                {'linkograph': simpleLinko,
                 'linkNumber': [2],
                 'delta': 4,
                 'restrict': False,
                 'lowerBound': None,
                 'upperBound': None,
                 'ExpectedEntropy': [-(3/4)*math.log(3/4,2)
                                     - (1/4)*math.log(1/4,2),
                                     -(2/3)*math.log(2/3,2)
                                     - (1/3)*math.log(1/3,2),
                                     -(1/2)*math.log(1/2,2)
                                     - (1/2)*math.log(1/2,2),
                                     0,
                                     0]},

                {'linkograph': simpleLinko,
                 'linkNumber': [2],
                 'delta': 3,
                 'restrict': False,
                 'lowerBound': None,
                 'upperBound': None,
                 'ExpectedEntropy': [0,
                                     -(2/3)*math.log(2/3,2)
                                     - (1/3)*math.log(1/3,2),
                                     -(1/2)*math.log(1/2,2)
                                     - (1/2)*math.log(1/2,2),
                                     0,
                                     0]},

                {'linkograph': simpleLinko,
                 'linkNumber': [2],
                 'delta': 3,
                 'restrict': False,
                 'lowerBound': 1,
                 'upperBound': 3,
                 'ExpectedEntropy': [-(2/3)*math.log(2/3,2)
                                     - (1/3)*math.log(1/3,2),
                                     -(1/2)*math.log(1/2,2)
                                     - (1/2)*math.log(1/2,2),
                                     0]},

                {'linkograph': simpleLinko,
                 'linkNumber': [2],
                 'delta': 3,
                 'restrict': True,
                 'lowerBound': 1,
                 'upperBound': 3,
                 'ExpectedEntropy': [-(1/2)*math.log(1/2,2)
                                     - (1/2)*math.log(1/2,2),
                                     0,
                                     0]},


                {'linkograph': simpleLinko,
                 'linkNumber': [2],
                 'delta': 2,
                 'restrict': False,
                 'lowerBound': None,
                 'upperBound': None,
                 'ExpectedEntropy': [0,
                                     -(1/2)*math.log(1/2,2)
                                     - (1/2)*math.log(1/2,2),
                                     -(1/2)*math.log(1/2,2)
                                     - (1/2)*math.log(1/2,2),
                                     0,
                                     0]},

            ]

        if self.id().split('.')[-1] == 'test_backLinkEntropy':
            self.testParams = [
                {'linkograph': simpleLinko,
                 'linkNumber': [1],
                 'delta': None,
                 'restrict': False,
                 'lowerBound': None,
                 'upperBound': None,
                 'ExpectedEntropy': [0,
                                     0,
                                     -(1/2)*math.log(1/2,2)
                                     - (1/2)*math.log(1/2,2),
                                     -(2/3)*math.log(2/3,2)
                                     - (1/3)*math.log(1/3,2),
                                     -(3/4)*math.log(3/4,2)
                                     - (1/4)*math.log(1/4,2)]},

                {'linkograph': simpleLinko,
                 'linkNumber': [1],
                 'delta': None,
                 'restrict': False,
                 'lowerBound': -1,
                 'upperBound': None,
                 'ExpectedEntropy': [0,
                                     0,
                                     -(1/2)*math.log(1/2,2)
                                     - (1/2)*math.log(1/2,2),
                                     -(2/3)*math.log(2/3,2)
                                     - (1/3)*math.log(1/3,2),
                                     -(3/4)*math.log(3/4,2)
                                     - (1/4)*math.log(1/4,2)]},

                {'linkograph': simpleLinko,
                 'linkNumber': [1],
                 'delta': None,
                 'restrict': False,
                 'lowerBound': 0,
                 'upperBound': None,
                 'ExpectedEntropy': [0,
                                     0,
                                     -(1/2)*math.log(1/2,2)
                                     - (1/2)*math.log(1/2,2),
                                     -(2/3)*math.log(2/3,2)
                                     - (1/3)*math.log(1/3,2),
                                     -(3/4)*math.log(3/4,2)
                                     - (1/4)*math.log(1/4,2)]},


                {'linkograph': simpleLinko,
                 'linkNumber': [1],
                 'delta': None,
                 'restrict': False,
                 'lowerBound': None,
                 'upperBound': 5,
                 'ExpectedEntropy': [0,
                                     0,
                                     -(1/2)*math.log(1/2,2)
                                     - (1/2)*math.log(1/2,2),
                                     -(2/3)*math.log(2/3,2)
                                     - (1/3)*math.log(1/3,2),
                                     -(3/4)*math.log(3/4,2)
                                     - (1/4)*math.log(1/4,2)]},

                {'linkograph': simpleLinko,
                 'linkNumber': [1],
                 'delta': None,
                 'restrict': False,
                 'lowerBound': None,
                 'upperBound': 4,
                 'ExpectedEntropy': [0,
                                     0,
                                     -(1/2)*math.log(1/2,2)
                                     - (1/2)*math.log(1/2,2),
                                     -(2/3)*math.log(2/3,2)
                                     - (1/3)*math.log(1/3,2),
                                     -(3/4)*math.log(3/4,2)
                                     - (1/4)*math.log(1/4,2)]},


                {'linkograph': simpleLinko,
                 'linkNumber': [1],
                 'delta': None,
                 'restrict': False,
                 'lowerBound': 0,
                 'upperBound': 4,
                 'ExpectedEntropy': [0,
                                     0,
                                     -(1/2)*math.log(1/2,2)
                                     - (1/2)*math.log(1/2,2),
                                     -(2/3)*math.log(2/3,2)
                                     - (1/3)*math.log(1/3,2),
                                     -(3/4)*math.log(3/4,2)
                                     - (1/4)*math.log(1/4,2)]},

                {'linkograph': simpleLinko,
                 'linkNumber': [1],
                 'delta': None,
                 'restrict': True,
                 'lowerBound': 0,
                 'upperBound': 4,
                 'ExpectedEntropy': [0,
                                     0,
                                     -(1/2)*math.log(1/2,2)
                                     - (1/2)*math.log(1/2,2),
                                     -(2/3)*math.log(2/3,2)
                                     - (1/3)*math.log(1/3,2),
                                     -(3/4)*math.log(3/4,2)
                                     - (1/4)*math.log(1/4,2)]},


                {'linkograph': simpleLinko,
                 'linkNumber': [1],
                 'delta': None,
                 'restrict': True,
                 'lowerBound': 0,
                 'upperBound': 3,
                 'ExpectedEntropy': [0,
                                     0,
                                     -(1/2)*math.log(1/2,2)
                                     - (1/2)*math.log(1/2,2),
                                     -(2/3)*math.log(2/3,2)
                                     - (1/3)*math.log(1/3,2)]},


                {'linkograph': simpleLinko,
                 'linkNumber': [1],
                 'delta': None,
                 'restrict': False,
                 'lowerBound': 1,
                 'upperBound': None,
                 'ExpectedEntropy': [0,
                                     -(1/2)*math.log(1/2,2)
                                     - (1/2)*math.log(1/2,2),
                                     -(2/3)*math.log(2/3,2)
                                     - (1/3)*math.log(1/3,2),
                                     -(3/4)*math.log(3/4,2)
                                     - (1/4)*math.log(1/4,2)]},

                {'linkograph': simpleLinko,
                 'linkNumber': [1],
                 'delta': None,
                 'restrict': False,
                 'lowerBound': None,
                 'upperBound': 3,
                 'ExpectedEntropy': [0,
                                     0,
                                     -(1/2)*math.log(1/2,2)
                                     - (1/2)*math.log(1/2,2),
                                     -(2/3)*math.log(2/3,2)
                                     - (1/3)*math.log(1/3,2)]},

                {'linkograph': simpleLinko,
                 'linkNumber': [1],
                 'delta': None,
                 'restrict': False,
                 'lowerBound': 1,
                 'upperBound': 3,
                 'ExpectedEntropy': [0,
                                     -(1/2)*math.log(1/2,2)
                                     - (1/2)*math.log(1/2,2),
                                     -(2/3)*math.log(2/3,2)
                                     - (1/3)*math.log(1/3,2)]},

                {'linkograph': simpleLinko,
                 'linkNumber': [1],
                 'delta': None,
                 'restrict': True,
                 'lowerBound': 1,
                 'upperBound': 4,
                 'ExpectedEntropy': [0,
                                     0,
                                     -(1/2)*math.log(1/2,2)
                                     - (1/2)*math.log(1/2,2),
                                     0]},


            ]

        if self.id().split('.')[-1] == 'test_linkEntropy':
            self.testParams = [
                {'linkograph': simpleLinko,
                 'linkNumber': [1,2],
                 'delta': None,
                 'restrict': False,
                 'lowerBound': None,
                 'upperBound': None,
                 'ExpectedEntropy': [-(3/4)*math.log(3/4,2)
                                     - (1/4)*math.log(1/4,2),
                                     -(3/4)*math.log(3/4,2)
                                     - (1/4)*math.log(1/4,2),
                                     -(2/4)*math.log(2/4,2)
                                     - (2/4)*math.log(2/4,2),
                                     -(3/4)*math.log(3/4,2)
                                     - (1/4)*math.log(1/4,2),
                                     -(3/4)*math.log(3/4,2)
                                     - (1/4)*math.log(1/4,2)]},

                {'linkograph': simpleLinko,
                 'linkNumber': [1,2],
                 'delta': None,
                 'restrict': False,
                 'lowerBound': -1,
                 'upperBound': None,
                 'ExpectedEntropy': [-(3/4)*math.log(3/4,2)
                                     - (1/4)*math.log(1/4,2),
                                     -(3/4)*math.log(3/4,2)
                                     - (1/4)*math.log(1/4,2),
                                     -(2/4)*math.log(2/4,2)
                                     - (2/4)*math.log(2/4,2),
                                     -(3/4)*math.log(3/4,2)
                                     - (1/4)*math.log(1/4,2),
                                     -(3/4)*math.log(3/4,2)
                                     - (1/4)*math.log(1/4,2)]},

                {'linkograph': simpleLinko,
                 'linkNumber': [1,2],
                 'delta': None,
                 'restrict': False,
                 'lowerBound': 0,
                 'upperBound': None,
                 'ExpectedEntropy': [-(3/4)*math.log(3/4,2)
                                     - (1/4)*math.log(1/4,2),
                                     -(3/4)*math.log(3/4,2)
                                     - (1/4)*math.log(1/4,2),
                                     -(2/4)*math.log(2/4,2)
                                     - (2/4)*math.log(2/4,2),
                                     -(3/4)*math.log(3/4,2)
                                     - (1/4)*math.log(1/4,2),
                                     -(3/4)*math.log(3/4,2)
                                     - (1/4)*math.log(1/4,2)]},

                {'linkograph': simpleLinko,
                 'linkNumber': [1,2],
                 'delta': None,
                 'restrict': False,
                 'lowerBound': None,
                 'upperBound': 5,
                 'ExpectedEntropy': [-(3/4)*math.log(3/4,2)
                                     - (1/4)*math.log(1/4,2),
                                     -(3/4)*math.log(3/4,2)
                                     - (1/4)*math.log(1/4,2),
                                     -(2/4)*math.log(2/4,2)
                                     - (2/4)*math.log(2/4,2),
                                     -(3/4)*math.log(3/4,2)
                                     - (1/4)*math.log(1/4,2),
                                     -(3/4)*math.log(3/4,2)
                                     - (1/4)*math.log(1/4,2)]},

                {'linkograph': simpleLinko,
                 'linkNumber': [1,2],
                 'delta': None,
                 'restrict': False,
                 'lowerBound': None,
                 'upperBound': 4,
                 'ExpectedEntropy': [-(3/4)*math.log(3/4,2)
                                     - (1/4)*math.log(1/4,2),
                                     -(3/4)*math.log(3/4,2)
                                     - (1/4)*math.log(1/4,2),
                                     -(2/4)*math.log(2/4,2)
                                     - (2/4)*math.log(2/4,2),
                                     -(3/4)*math.log(3/4,2)
                                     - (1/4)*math.log(1/4,2),
                                     -(3/4)*math.log(3/4,2)
                                     - (1/4)*math.log(1/4,2)]},

                {'linkograph': simpleLinko,
                 'linkNumber': [1,2],
                 'delta': None,
                 'restrict': True,
                 'lowerBound': 0,
                 'upperBound': 4,
                 'ExpectedEntropy': [-(3/4)*math.log(3/4,2)
                                     - (1/4)*math.log(1/4,2),
                                     -(3/4)*math.log(3/4,2)
                                     - (1/4)*math.log(1/4,2),
                                     -(2/4)*math.log(2/4,2)
                                     - (2/4)*math.log(2/4,2),
                                     -(3/4)*math.log(3/4,2)
                                     - (1/4)*math.log(1/4,2),
                                     -(3/4)*math.log(3/4,2)
                                     - (1/4)*math.log(1/4,2)]},

                {'linkograph': simpleLinko,
                 'linkNumber': [1,2],
                 'delta': None,
                 'restrict': False,
                 'lowerBound': 1,
                 'upperBound': None,
                 'ExpectedEntropy': [-(3/4)*math.log(3/4,2)
                                     - (1/4)*math.log(1/4,2),
                                     -(2/4)*math.log(2/4,2)
                                     - (2/4)*math.log(2/4,2),
                                     -(3/4)*math.log(3/4,2)
                                     - (1/4)*math.log(1/4,2),
                                     -(3/4)*math.log(3/4,2)
                                     - (1/4)*math.log(1/4,2)]},

                {'linkograph': simpleLinko,
                 'linkNumber': [1,2],
                 'delta': None,
                 'restrict': False,
                 'lowerBound': None,
                 'upperBound': 3,
                 'ExpectedEntropy': [-(3/4)*math.log(3/4,2)
                                     - (1/4)*math.log(1/4,2),
                                     -(3/4)*math.log(3/4,2)
                                     - (1/4)*math.log(1/4,2),
                                     -(2/4)*math.log(2/4,2)
                                     - (2/4)*math.log(2/4,2),
                                     -(3/4)*math.log(3/4,2)
                                     - (1/4)*math.log(1/4,2)]},

                {'linkograph': simpleLinko,
                 'linkNumber': [1,2],
                 'delta': None,
                 'restrict': False,
                 'lowerBound': 1,
                 'upperBound': 3,
                 'ExpectedEntropy': [-(3/4)*math.log(3/4,2)
                                     - (1/4)*math.log(1/4,2),
                                     -(2/4)*math.log(2/4,2)
                                     - (2/4)*math.log(2/4,2),
                                     -(3/4)*math.log(3/4,2)
                                     - (1/4)*math.log(1/4,2)]},

                {'linkograph': simpleLinko,
                 'linkNumber': [1,2],
                 'delta': None,
                 'restrict': True,
                 'lowerBound': 1,
                 'upperBound': 4,
                 'ExpectedEntropy': [-(2/3)*math.log(2/3,2)
                                     - (1/3)*math.log(1/3,2),
                                     -(1/3)*math.log(1/3,2)
                                     - (2/3)*math.log(2/3,2),
                                     -(2/3)*math.log(2/3,2)
                                     - (1/3)*math.log(1/3,2),
                                     0]},

                {'linkograph': simpleLinko,
                 'linkNumber': [1,2],
                 'delta': None,
                 'restrict': True,
                 'lowerBound': 1,
                 'upperBound': 3,
                 'ExpectedEntropy': [-(1/2)*math.log(1/2,2)
                                     - (1/2)*math.log(1/2,2),
                                     0,
                                     -(1/2)*math.log(1/2,2)
                                     - (1/2)*math.log(1/2,2)]},

                {'linkograph': simpleLinko,
                 'linkNumber': [1,2],
                 'delta': None,
                 'restrict': True,
                 'lowerBound': 3,
                 'upperBound': 4,
                 'ExpectedEntropy': [0,0]},

                {'linkograph': simpleLinko,
                 'linkNumber': [1,2],
                 'delta': None,
                 'restrict': True,
                 'lowerBound': 4,
                 'upperBound': 4,
                 'ExpectedEntropy': [0]},


            ]


    def performTestForParams(self):
        """"Performs the tests for each set of parameters."""
        for params in self.testParams:
            actualEntropy = stats.linkEntropy(
                params['linkograph'],
                params['linkNumber'],
                params['delta'],
                params['restrict'],
                params['lowerBound'],
                params['upperBound'])
            self.assertEqual(
                actualEntropy,
                params['ExpectedEntropy'],
                ("Test fail: linkograph = {}"
                 " linkNumber = {}"
                 " delta = {}"
                 " restict = {}"
                 " lowerBound = {}"
                 " upperBound = {}"
                 " actualEntropy = {}"
                 " ExpectedEntropy = {}")
                .format(params['linkograph'],
                        params['linkNumber'],
                        params['delta'],
                        params['restrict'],
                        params['lowerBound'],
                        params['upperBound'],
                        actualEntropy,
                        params['ExpectedEntropy']))

    def test_foreLinkEntropy(self):
        """Tests for correct link entropyfor the forelinks."""
        self.performTestForParams()

    def test_backLinkEntropy(self):
        """Tests for correct link entropy for the backlinks."""
        self.performTestForParams()

    def test_linkEntropy(self):
        """Tests for correct link entropy using both backlinks and forelinks."""
        self.performTestForParams()

class Test_entryToString(unittest.TestCase):

    """Basic unit tests the entryToString in the stats package."""

    def setUp(self):
        """Set up the parameters for the individual tests."""

        entry0 = [set(), set(), {1,2,3,4,5}]
        entry1 = [set(), {0,1,2,3,4,5}, set()]
        entry2 = [set(), {0,1,2}, {4,5,6}]
        entry3 = [set(), {0,3,5}, {8, 10}]

        if self.id().split('.')[-1] == 'test_forelinks':
            self.testParams = [
                {'entry': entry0,
                 'currentIndex': 0,
                 'listNumber': [2],
                 'lowerBound': 0,
                 'upperBound': 5,
                 'ExpectedString': '11111'},

                {'entry': entry0,
                 'currentIndex': 0,
                 'listNumber': [2],
                 'lowerBound': 0,
                 'upperBound': 4,
                 'ExpectedString': '1111'},

                {'entry': entry0,
                 'currentIndex': 0,
                 'listNumber': [2],
                 'lowerBound': 0,
                 'upperBound': 3,
                 'ExpectedString': '111'},

                {'entry': entry0,
                 'currentIndex': 0,
                 'listNumber': [2],
                 'lowerBound': 0,
                 'upperBound': 2,
                 'ExpectedString': '11'},

                {'entry': entry0,
                 'currentIndex': 0,
                 'listNumber': [2],
                 'lowerBound': 0,
                 'upperBound': 0,
                 'ExpectedString': ''},

                {'entry': entry0,
                 'currentIndex': 0,
                 'listNumber': [2],
                 'lowerBound': 0,
                 'upperBound': 6,
                 'ExpectedString': '111110'},

                {'entry': entry1,
                 'currentIndex': 6,
                 'listNumber': [2],
                 'lowerBound': 0,
                 'upperBound': 6,
                 'ExpectedString': ''},

                {'entry': entry2,
                 'currentIndex': 3,
                 'listNumber': [2],
                 'lowerBound': 0,
                 'upperBound': 5,
                 'ExpectedString': '11'},

                {'entry': entry2,
                 'currentIndex': 3,
                 'listNumber': [2],
                 'lowerBound': 1,
                 'upperBound': 5,
                 'ExpectedString': '11'},

                {'entry': entry3,
                 'currentIndex': 6,
                 'listNumber': [2],
                 'lowerBound': 0,
                 'upperBound': 8,
                 'ExpectedString': '01'},

                {'entry': entry3,
                 'currentIndex': 6,
                 'listNumber': [2],
                 'lowerBound': 0,
                 'upperBound': 11,
                 'ExpectedString': '01010'},

            ]

        if self.id().split('.')[-1] == 'test_backlinks':
            self.testParams = [
                {'entry': entry0,
                 'currentIndex': 0,
                 'listNumber': [1],
                 'lowerBound': 0,
                 'upperBound': 5,
                 'ExpectedString': ''},

                {'entry': entry0,
                 'currentIndex': 0,
                 'listNumber': [1],
                 'lowerBound': 0,
                 'upperBound': 4,
                 'ExpectedString': ''},

                {'entry': entry1,
                 'currentIndex': 6,
                 'listNumber': [1],
                 'lowerBound': 0,
                 'upperBound': 6,
                 'ExpectedString': '111111'},

                {'entry': entry1,
                 'currentIndex': 6,
                 'listNumber': [1],
                 'lowerBound': 0,
                 'upperBound': 7,
                 'ExpectedString': '111111'},

                {'entry': entry1,
                 'currentIndex': 6,
                 'listNumber': [1],
                 'lowerBound': 1,
                 'upperBound': 6,
                 'ExpectedString': '11111'},

                {'entry': entry2,
                 'currentIndex': 3,
                 'listNumber': [1],
                 'lowerBound': 0,
                 'upperBound': 6,
                 'ExpectedString': '111'},

                {'entry': entry2,
                 'currentIndex': 3,
                 'listNumber': [1],
                 'lowerBound': 2,
                 'upperBound': 3,
                 'ExpectedString': '1'},

                {'entry': entry2,
                 'currentIndex': 3,
                 'listNumber': [1],
                 'lowerBound': 3,
                 'upperBound': 3,
                 'ExpectedString': ''},

                {'entry': entry3,
                 'currentIndex': 6,
                 'listNumber': [1],
                 'lowerBound': 0,
                 'upperBound': 6,
                 'ExpectedString': '100101'},

                ]

        if self.id().split('.')[-1] == 'test_links':
            self.testParams = [
                {'entry': entry0,
                 'currentIndex': 0,
                 'listNumber': [1,2],
                 'lowerBound': 0,
                 'upperBound': 5,
                 'ExpectedString': '11111'},

                {'entry': entry0,
                 'currentIndex': 0,
                 'listNumber': [1,2],
                 'lowerBound': 0,
                 'upperBound': 4,
                 'ExpectedString': '1111'},

                {'entry': entry0,
                 'currentIndex': 0,
                 'listNumber': [1,2],
                 'lowerBound': 0,
                 'upperBound': 0,
                 'ExpectedString': ''},


                {'entry': entry1,
                 'currentIndex': 6,
                 'listNumber': [1,2],
                 'lowerBound': 0,
                 'upperBound': 6,
                 'ExpectedString': '111111'},

                {'entry': entry1,
                 'currentIndex': 6,
                 'listNumber': [1,2],
                 'lowerBound': 1,
                 'upperBound': 6,
                 'ExpectedString': '11111'},

                {'entry': entry1,
                 'currentIndex': 6,
                 'listNumber': [1,2],
                 'lowerBound': 0,
                 'upperBound': 7,
                 'ExpectedString': '1111110'},

                {'entry': entry2,
                 'currentIndex': 3,
                 'listNumber': [1,2],
                 'lowerBound': 0,
                 'upperBound': 6,
                 'ExpectedString': '111111'},

                {'entry': entry2,
                 'currentIndex': 3,
                 'listNumber': [1,2],
                 'lowerBound': 1,
                 'upperBound': 6,
                 'ExpectedString': '11111'},

                {'entry': entry2,
                 'currentIndex': 3,
                 'listNumber': [1,2],
                 'lowerBound': 2,
                 'upperBound': 6,
                 'ExpectedString': '1111'},

                {'entry': entry2,
                 'currentIndex': 3,
                 'listNumber': [1,2],
                 'lowerBound': 0,
                 'upperBound': 5,
                 'ExpectedString': '11111'},

                {'entry': entry2,
                 'currentIndex': 3,
                 'listNumber': [1,2],
                 'lowerBound': 3,
                 'upperBound': 3,
                 'ExpectedString': ''},

                {'entry': entry3,
                 'currentIndex': 6,
                 'listNumber': [1,2],
                 'lowerBound': 0,
                 'upperBound': 10,
                 'ExpectedString': '1001010101'},

                {'entry': entry3,
                 'currentIndex': 6,
                 'listNumber': [1,2],
                 'lowerBound': 0,
                 'upperBound': 11,
                 'ExpectedString': '10010101010'},

                {'entry': entry3,
                 'currentIndex': 6,
                 'listNumber': [1,2],
                 'lowerBound': 1,
                 'upperBound': 10,
                 'ExpectedString': '001010101'},

                ]


    def performTestForParams(self):
        """"Performs the tests for each set of parameters."""
        for params in self.testParams:
            actualString = stats.entryToString(
                params['entry'],
                params['currentIndex'],
                params['listNumber'],
                params['lowerBound'],
                params['upperBound'])
            self.assertEqual(
                actualString,
                params['ExpectedString'],
                ("Test fail: entry = {}"
                 " currentIndex = {}"
                 " listNumber = {}"
                 " lowerBound = {}"
                 " upperBound = {}"
                 " actualString = {}"
                 " ExpectedString = {}")
                .format(params['entry'],
                        params['currentIndex'],
                        params['listNumber'],
                        params['lowerBound'],
                        params['upperBound'],
                        actualString,
                        params['ExpectedString']))

    def test_forelinks(self):
        """Tests for correct conversion of forelinks to strings."""
        self.performTestForParams()

    def test_backlinks(self):
        """Tests for correct conversion of backlinks to strings."""
        self.performTestForParams()

    def test_links(self):
        """Tests for correct conversion of links to strings."""
        self.performTestForParams()



class Test_linkTComplexity(unittest.TestCase):

    """Basic unit tests the T complexity on links in the stats package."""

    def setUp(self):
        """Set up the parameters for the individual tests."""

        simpleLinko = linkoCreate.Linkograph(
            [({'A', 'B', 'C'}, set(), {1,2,3}),
             ({'D'}, {0}, {3,4}),
             ({'A'}, {0}, {4}),
             ({'B', 'C'}, {0,1}, {4}),
             ({'A'}, {1,2,3}, set())],
            ['A', 'B', 'C', 'D'])


        if self.id().split('.')[-1] == 'test_foreLinkTComplexity':
            self.testParams = [
                {'linkograph': simpleLinko,
                 'linkNumber': [2],
                 'delta': None,
                 'restrict': False,
                 'lowerBound': None,
                 'upperBound': None,
                 'ExpectedTComplexity': [2,
                                         2,
                                         1,
                                         0,
                                         0]},

                {'linkograph': simpleLinko,
                 'linkNumber': [2],
                 'delta': None,
                 'restrict': False,
                 'lowerBound': -1,
                 'upperBound': None,
                 'ExpectedTComplexity': [2,
                                         2,
                                         1,
                                         0,
                                         0]},

                {'linkograph': simpleLinko,
                 'linkNumber': [2],
                 'delta': None,
                 'restrict': False,
                 'lowerBound': 0,
                 'upperBound': None,
                 'ExpectedTComplexity': [2,
                                         2,
                                         1,
                                         0,
                                         0]},


                {'linkograph': simpleLinko,
                 'linkNumber': [2],
                 'delta': None,
                 'restrict': False,
                 'lowerBound': None,
                 'upperBound': 5,
                 'ExpectedTComplexity': [2,
                                         2,
                                         1,
                                         0,
                                         0]},

                {'linkograph': simpleLinko,
                 'linkNumber': [2],
                 'delta': None,
                 'restrict': True,
                 'lowerBound': None,
                 'upperBound': None,
                 'ExpectedTComplexity': [2,
                                         2,
                                         1,
                                         0,
                                         0]},

                {'linkograph': simpleLinko,
                 'linkNumber': [2],
                 'delta': None,
                 'restrict': False,
                 'lowerBound': 0,
                 'upperBound': 4,
                 'ExpectedTComplexity': [2,
                                         2,
                                         1,
                                         0,
                                         0]},


                {'linkograph': simpleLinko,
                 'linkNumber': [2],
                 'delta': None,
                 'restrict': False,
                 'lowerBound': None,
                 'upperBound': 4,
                 'ExpectedTComplexity': [2,
                                         2,
                                         1,
                                         0,
                                         0]},

                {'linkograph': simpleLinko,
                 'linkNumber': [2],
                 'delta': None,
                 'restrict': False,
                 'lowerBound': 0,
                 'upperBound': 4,
                 'ExpectedTComplexity': [2,
                                         2,
                                         1,
                                         0,
                                         0]},

                {'linkograph': simpleLinko,
                 'linkNumber': [2],
                 'delta': None,
                 'restrict': False,
                 'lowerBound': None,
                 'upperBound': 3,
                 'ExpectedTComplexity': [2,
                                         2,
                                         1,
                                         0]},


                {'linkograph': simpleLinko,
                 'linkNumber': [2],
                 'delta': None,
                 'restrict': False,
                 'lowerBound': None,
                 'upperBound': 2,
                 'ExpectedTComplexity': [2,
                                         2,
                                         1]},

                {'linkograph': simpleLinko,
                 'linkNumber': [2],
                 'delta': None,
                 'restrict': False,
                 'lowerBound': 1,
                 'upperBound': None,
                 'ExpectedTComplexity': [2,
                                         1,
                                         0,
                                         0]},

                {'linkograph': simpleLinko,
                 'linkNumber': [2],
                 'delta': None,
                 'restrict': False,
                 'lowerBound': 1,
                 'upperBound': 3,
                 'ExpectedTComplexity': [2,
                                         1,
                                         0]},

                {'linkograph': simpleLinko,
                 'linkNumber': [2],
                 'delta': None,
                 'restrict': False,
                 'lowerBound': 2,
                 'upperBound': 3,
                 'ExpectedTComplexity': [1,
                                         0]},

                {'linkograph': simpleLinko,
                 'linkNumber': [2],
                 'delta': None,
                 'restrict': False,
                 'lowerBound': 2,
                 'upperBound': 2,
                 'ExpectedTComplexity': [1]},

                {'linkograph': simpleLinko,
                 'linkNumber': [2],
                 'delta': None,
                 'restrict': True,
                 'lowerBound': 1,
                 'upperBound': 4,
                 'ExpectedTComplexity': [2,
                                         1,
                                         0,
                                         0]},

                {'linkograph': simpleLinko,
                 'linkNumber': [2],
                 'delta': None,
                 'restrict': True,
                 'lowerBound': 0,
                 'upperBound': 3,
                 'ExpectedTComplexity': [math.log(3,2),
                                         1,
                                         0,
                                         0]},

                {'linkograph': simpleLinko,
                 'linkNumber': [2],
                 'delta': None,
                 'restrict': True,
                 'lowerBound': 1,
                 'upperBound': 3,
                 'ExpectedTComplexity': [1,
                                         0,
                                         0]},

                {'linkograph': simpleLinko,
                 'linkNumber': [2],
                 'delta': None,
                 'restrict': True,
                 'lowerBound': 1,
                 'upperBound': 2,
                 'ExpectedTComplexity': [0,
                                         0]},

                {'linkograph': simpleLinko,
                 'linkNumber': [2],
                 'delta': None,
                 'restrict': True,
                 'lowerBound': 1,
                 'upperBound': 1,
                 'ExpectedTComplexity': [0]},

                {'linkograph': simpleLinko,
                 'linkNumber': [2],
                 'delta': None,
                 'restrict': False,
                 'lowerBound': 2,
                 'upperBound': 1,
                 'ExpectedTComplexity': []},

                {'linkograph': simpleLinko,
                 'linkNumber': [2],
                 'delta': 5,
                 'restrict': False,
                 'lowerBound': None,
                 'upperBound': None,
                 'ExpectedTComplexity': [2,
                                         2,
                                         1,
                                         0,
                                         0]},

                {'linkograph': simpleLinko,
                 'linkNumber': [2],
                 'delta': 4,
                 'restrict': False,
                 'lowerBound': None,
                 'upperBound': None,
                 'ExpectedTComplexity': [2,
                                         2,
                                         1,
                                         0,
                                         0]},

                {'linkograph': simpleLinko,
                 'linkNumber': [2],
                 'delta': 3,
                 'restrict': False,
                 'lowerBound': None,
                 'upperBound': None,
                 'ExpectedTComplexity': [math.log(3,2),
                                         2,
                                         1,
                                         0,
                                         0]},

                {'linkograph': simpleLinko,
                 'linkNumber': [2],
                 'delta': 3,
                 'restrict': False,
                 'lowerBound': 1,
                 'upperBound': 3,
                 'ExpectedTComplexity':  [2,
                                         1,
                                         0]},

                {'linkograph': simpleLinko,
                 'linkNumber': [2],
                 'delta': 3,
                 'restrict': True,
                 'lowerBound': 1,
                 'upperBound': 3,
                 'ExpectedTComplexity': [1,
                                         0,
                                         0]},


                {'linkograph': simpleLinko,
                 'linkNumber': [2],
                 'delta': 2,
                 'restrict': False,
                 'lowerBound': None,
                 'upperBound': None,
                 'ExpectedTComplexity': [1,
                                         1,
                                         1,
                                         0,
                                         0]},

            ]

        if self.id().split('.')[-1] == 'test_backLinkTComplexity':
            self.testParams = [
                {'linkograph': simpleLinko,
                 'linkNumber': [1],
                 'delta': None,
                 'restrict': False,
                 'lowerBound': None,
                 'upperBound': None,
                 'ExpectedTComplexity': [0,
                                         0,
                                         1,
                                         math.log(3, 2),
                                         1 + math.log(3,2)]},

                {'linkograph': simpleLinko,
                 'linkNumber': [1],
                 'delta': None,
                 'restrict': False,
                 'lowerBound': -1,
                 'upperBound': None,
                 'ExpectedTComplexity': [0,
                                         0,
                                         1,
                                         math.log(3, 2),
                                         1 + math.log(3,2)]},

                {'linkograph': simpleLinko,
                 'linkNumber': [1],
                 'delta': None,
                 'restrict': False,
                 'lowerBound': 0,
                 'upperBound': None,
                 'ExpectedTComplexity': [0,
                                         0,
                                         1,
                                         math.log(3, 2),
                                         1 + math.log(3,2)]},


                {'linkograph': simpleLinko,
                 'linkNumber': [1],
                 'delta': None,
                 'restrict': False,
                 'lowerBound': None,
                 'upperBound': 5,
                 'ExpectedTComplexity': [0,
                                         0,
                                         1,
                                         math.log(3, 2),
                                         1 + math.log(3,2)]},

                {'linkograph': simpleLinko,
                 'linkNumber': [1],
                 'delta': None,
                 'restrict': False,
                 'lowerBound': None,
                 'upperBound': 4,
                 'ExpectedTComplexity': [0,
                                         0,
                                         1,
                                         math.log(3, 2),
                                         1 + math.log(3,2)]},

                {'linkograph': simpleLinko,
                 'linkNumber': [1],
                 'delta': None,
                 'restrict': False,
                 'lowerBound': 0,
                 'upperBound': 4,
                 'ExpectedTComplexity': [0,
                                         0,
                                         1,
                                         math.log(3, 2),
                                         1 + math.log(3,2)]},

                {'linkograph': simpleLinko,
                 'linkNumber': [1],
                 'delta': None,
                 'restrict': True,
                 'lowerBound': 0,
                 'upperBound': 4,
                 'ExpectedTComplexity': [0,
                                         0,
                                         1,
                                         math.log(3,2),
                                         1 + math.log(3,2)]},

                {'linkograph': simpleLinko,
                 'linkNumber': [1],
                 'delta': None,
                 'restrict': True,
                 'lowerBound': 0,
                 'upperBound': 3,
                 'ExpectedTComplexity': [0,
                                         0,
                                         1,
                                         math.log(3,2)]},

                {'linkograph': simpleLinko,
                 'linkNumber': [1],
                 'delta': None,
                 'restrict': False,
                 'lowerBound': 1,
                 'upperBound': None,
                 'ExpectedTComplexity': [0,
                                         1,
                                         math.log(3, 2),
                                         1 + math.log(3,2)]},

                {'linkograph': simpleLinko,
                 'linkNumber': [1],
                 'delta': None,
                 'restrict': False,
                 'lowerBound': None,
                 'upperBound': 3,
                 'ExpectedTComplexity': [0,
                                         0,
                                         1,
                                         math.log(3,2)]},

                {'linkograph': simpleLinko,
                 'linkNumber': [1],
                 'delta': None,
                 'restrict': False,
                 'lowerBound': 1,
                 'upperBound': 3,
                 'ExpectedTComplexity': [0,
                                         1,
                                         math.log(3,2)]},

                {'linkograph': simpleLinko,
                 'linkNumber': [1],
                 'delta': None,
                 'restrict': True,
                 'lowerBound': 1,
                 'upperBound': 4,
                 'ExpectedTComplexity': [0,
                                         0,
                                         1,
                                         math.log(3,2)]},


            ]

        if self.id().split('.')[-1] == 'test_linkTComplexity':
            self.testParams = [
                {'linkograph': simpleLinko,
                 'linkNumber': [1,2],
                 'delta': None,
                 'restrict': False,
                 'lowerBound': None,
                 'upperBound': None,
                 'ExpectedTComplexity': [2,
                                         2,
                                         1 + math.log(3,2),
                                         1 + math.log(3,2),
                                         1 + math.log(3,2)]},

                {'linkograph': simpleLinko,
                 'linkNumber': [1,2],
                 'delta': None,
                 'restrict': False,
                 'lowerBound': -1,
                 'upperBound': None,
                 'ExpectedTComplexity': [2,
                                         2,
                                         1 + math.log(3,2),
                                         1 + math.log(3,2),
                                         1 + math.log(3,2)]},

                {'linkograph': simpleLinko,
                 'linkNumber': [1,2],
                 'delta': None,
                 'restrict': False,
                 'lowerBound': 0,
                 'upperBound': None,
                 'ExpectedTComplexity': [2,
                                         2,
                                         1 + math.log(3,2),
                                         1 + math.log(3,2),
                                         1 + math.log(3,2)]},

                {'linkograph': simpleLinko,
                 'linkNumber': [1,2],
                 'delta': None,
                 'restrict': False,
                 'lowerBound': None,
                 'upperBound': 5,
                 'ExpectedTComplexity': [2,
                                         2,
                                         1 + math.log(3,2),
                                         1 + math.log(3,2),
                                         1 + math.log(3,2)]},

                {'linkograph': simpleLinko,
                 'linkNumber': [1,2],
                 'delta': None,
                 'restrict': False,
                 'lowerBound': None,
                 'upperBound': 4,
                 'ExpectedTComplexity': [2,
                                         2,
                                         1 + math.log(3,2),
                                         1 + math.log(3,2),
                                         1 + math.log(3,2)]},

                {'linkograph': simpleLinko,
                 'linkNumber': [1,2],
                 'delta': None,
                 'restrict': True,
                 'lowerBound': 0,
                 'upperBound': 4,
                 'ExpectedTComplexity': [2,
                                         2,
                                         1 + math.log(3,2),
                                         1 + math.log(3,2),
                                         1 + math.log(3,2)]},

                {'linkograph': simpleLinko,
                 'linkNumber': [1,2],
                 'delta': None,
                 'restrict': False,
                 'lowerBound': 1,
                 'upperBound': None,
                 'ExpectedTComplexity': [2,
                                         1 + math.log(3,2),
                                         1 + math.log(3,2),
                                         1 + math.log(3,2)]},

                {'linkograph': simpleLinko,
                 'linkNumber': [1,2],
                 'delta': None,
                 'restrict': False,
                 'lowerBound': None,
                 'upperBound': 3,
                 'ExpectedTComplexity': [2,
                                         2,
                                         1 + math.log(3,2),
                                         1 + math.log(3,2)]},

                {'linkograph': simpleLinko,
                 'linkNumber': [1,2],
                 'delta': None,
                 'restrict': False,
                 'lowerBound': 1,
                 'upperBound': 3,
                 'ExpectedTComplexity': [2,
                                         1 + math.log(3,2),
                                         1 + math.log(3,2)]},

                {'linkograph': simpleLinko,
                 'linkNumber': [1,2],
                 'delta': None,
                 'restrict': True,
                 'lowerBound': 1,
                 'upperBound': 4,
                 'ExpectedTComplexity': [2,
                                         math.log(3,2),
                                         2,
                                         math.log(3,2)]},

                {'linkograph': simpleLinko,
                 'linkNumber': [1,2],
                 'delta': None,
                 'restrict': True,
                 'lowerBound': 1,
                 'upperBound': 3,
                 'ExpectedTComplexity': [1,
                                         1,
                                         1]},

                {'linkograph': simpleLinko,
                 'linkNumber': [1,2],
                 'delta': None,
                 'restrict': True,
                 'lowerBound': 3,
                 'upperBound': 4,
                 'ExpectedTComplexity': [0,0]},

                {'linkograph': simpleLinko,
                 'linkNumber': [1,2],
                 'delta': None,
                 'restrict': True,
                 'lowerBound': 4,
                 'upperBound': 4,
                 'ExpectedTComplexity': [0]},


            ]


    def performTestForParams(self):
        """"Performs the tests for each set of parameters."""
        for params in self.testParams:
            actualTComplexity = stats.linkTComplexity(
                params['linkograph'],
                params['linkNumber'],
                params['delta'],
                params['restrict'],
                params['lowerBound'],
                params['upperBound'])
            self.assertEqual(
                actualTComplexity,
                params['ExpectedTComplexity'],
                ("Test fail: linkograph = {}"
                 " linkNumber = {}"
                 " delta = {}"
                 " restict = {}"
                 " lowerBound = {}"
                 " upperBound = {}"
                 " actualTComplexity = {}"
                 " ExpectedTComplexity = {}")
                .format(params['linkograph'],
                        params['linkNumber'],
                        params['delta'],
                        params['restrict'],
                        params['lowerBound'],
                        params['upperBound'],
                        actualTComplexity,
                        params['ExpectedTComplexity']))

    def test_foreLinkTComplexity(self):
        """Tests for correct link entropyfor the forelinks."""
        self.performTestForParams()

    def test_backLinkTComplexity(self):
        """Tests for correct link entropy for the backlinks."""
        self.performTestForParams()

    def test_linkTComplexity(self):
        """Tests for correct link entropy using both backlinks and forelinks."""
        self.performTestForParams()


class Test_tComplexity(unittest.TestCase):

    """Basic unit tests the T Complexity in the stats package."""

    def setUp(self):
        """Set up the parameters for the individual tests."""

        if self.id().split('.')[-1] == 'test_tComplexity':
            self.testParams = [
                {'string': '',
                 'ExpectedTComplexity': 0},

                {'string': '0',
                 'ExpectedTComplexity': 0},

                {'string': '1',
                 'ExpectedTComplexity': 0},

                {'string': '00',
                 'ExpectedTComplexity': 1},

                {'string': '01',
                 'ExpectedTComplexity': 1},

                {'string': '10',
                 'ExpectedTComplexity': 1},

                {'string': '11',
                 'ExpectedTComplexity': 1},

                {'string': '000',
                 'ExpectedTComplexity': math.log(3,2)},

                {'string': '001',
                 'ExpectedTComplexity': math.log(3,2)},

                {'string': '010',
                 'ExpectedTComplexity': 2},

                {'string': '011',
                 'ExpectedTComplexity': 2},

                {'string': '100',
                 'ExpectedTComplexity': 2},

                {'string': '101',
                 'ExpectedTComplexity': 2},

                {'string': '110',
                 'ExpectedTComplexity': math.log(3,2)},

                {'string': '111',
                 'ExpectedTComplexity': math.log(3,2)},

                {'string': '1110',
                 'ExpectedTComplexity': 2},

                {'string': '1011',
                 'ExpectedTComplexity': 2},

                {'string': '1001',
                 'ExpectedTComplexity': 1 + math.log(3,2)},

                {'string': '1101',
                 'ExpectedTComplexity': 1 + math.log(3,2)},

                {'string': '0111',
                 'ExpectedTComplexity': 1 + math.log(3,2)},

                {'string': '0100010101101',
                 'ExpectedTComplexity': 5},

            ]


    def performTestForParams(self):
        """"Performs the tests for each set of parameters."""
        for params in self.testParams:
            actualTComplexity = stats.tComplexity(params['string'])
            self.assertEqual(
                actualTComplexity,
                params['ExpectedTComplexity'],
                ("Test fail: string = {}"
                 " actualTComplexity = {}"
                 " ExpectedTComplexity = {}")
                .format(params['string'],
                        actualTComplexity,
                        params['ExpectedTComplexity']))

    def test_tComplexity(self):
        """Tests for correct T complexity."""
        self.performTestForParams()
