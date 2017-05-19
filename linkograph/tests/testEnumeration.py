#!/usr/bin/env python3

"""Tests the enumeration.py package."""

import unittest
from linkograph import enumeration # The package under test.
from linkograph import linkoCreate # For constructing linkographs
from linkograph import stats # For getting the number of linkographs

class Test_linkoToEnum(unittest.TestCase):
    """ Tests the linkoToEnum function. """

    def setUp(self):
        """ Set up parameters for individual tests. """

        # Linkographs
        linko0_0 = linkoCreate.Linkograph([])

        linko1_0 = linkoCreate.Linkograph(
            [(set(), set(), set())]
        )

        linko2_0 = linkoCreate.Linkograph(
            [(set(), set(), set()),
             (set(), set(), set())]
        )

        linko2_1 = linkoCreate.Linkograph(
            [(set(), set(), {1}),
             (set(), {0}, set())]
        )

        
        linko3_0 = linkoCreate.Linkograph(
            [(set(), set(), set()),
             (set(), set(), set()),
             (set(), set(), set())]
        )

        linko3_1 = linkoCreate.Linkograph(
            [(set(), set(), {1}),
             (set(), {0}, set()),
             (set(), set(), set())]
        )


        linko3_2 = linkoCreate.Linkograph(
            [(set(), set(), {2}),
             (set(), set(), set()),
             (set(), {0}, set())]
        )

        linko3_3 = linkoCreate.Linkograph(
            [(set(), set(), {1,2}),
             (set(), {0}, set()),
             (set(), {0}, set())]
        )


        linko3_4 = linkoCreate.Linkograph(
            [(set(), set(), set()),
             (set(), set(), {2}),
             (set(), {1}, set())]
        )

        linko3_5 = linkoCreate.Linkograph(
            [(set(), set(), {1}),
             (set(), {0}, {2}),
             (set(), {1}, set())]
        )

        linko3_6 = linkoCreate.Linkograph(
            [(set(), set(), {2}),
             (set(), set(), {2}),
             (set(), {0,1}, set())]
        )

        linko3_7 = linkoCreate.Linkograph(
            [(set(), set(), {1,2}),
             (set(), {0}, {2}),
             (set(), {0,1}, set())]
        )


        if self.id().split('.')[-1] == 'test_linkoToEnum':
            self.testParams = [
                {'linko': linko0_0,
                 'ExpectedEnumeration': (0,0)},
                {'linko': linko1_0,
                 'ExpectedEnumeration': (1,0)},
                {'linko': linko2_0,
                 'ExpectedEnumeration': (2,0)},
                {'linko': linko2_1,
                 'ExpectedEnumeration': (2,1)},
                {'linko': linko3_0,
                 'ExpectedEnumeration': (3,0)},
                {'linko': linko3_1,
                 'ExpectedEnumeration': (3,1)},
                {'linko': linko3_2,
                 'ExpectedEnumeration': (3,2)},
                {'linko': linko3_3,
                 'ExpectedEnumeration': (3,3)},
                {'linko': linko3_4,
                 'ExpectedEnumeration': (3,4)},
                {'linko': linko3_5,
                 'ExpectedEnumeration': (3,5)},
                {'linko': linko3_6,
                 'ExpectedEnumeration': (3,6)},
                {'linko': linko3_7,
                 'ExpectedEnumeration': (3,7)}]

    def performTestForParams(self):
        """"Performs the tests for each set of parameters."""
        for (number, params) in enumerate(self.testParams):
            actual = enumeration.linkoToEnum(params['linko'])
            self.assertEqual(
                actual,
                params['ExpectedEnumeration'],
                ("Test fail: test number = {}, "
                 "Linkograph = {}, "
                 " Actual Enumeration = {}"
                 " Expected Enumeration = {}")
                .format(number,
                        params['linko'],
                        actual,
                        params['ExpectedEnumeration']))

    def test_linkoToEnum(self):
        """Tests for the correct enumeration."""
        self.performTestForParams()


class Test_enumToLinko(unittest.TestCase):
    """ Tests the enumToLinko function. """

    def setUp(self):
        """ Set up parameters for individual tests. """

        # Linkographs
        linko0_0 = linkoCreate.Linkograph([])

        linko1_0 = linkoCreate.Linkograph(
            [(set(), set(), set())]
        )

        linko2_0 = linkoCreate.Linkograph(
            [(set(), set(), set()),
             (set(), set(), set())]
        )

        linko2_1 = linkoCreate.Linkograph(
            [(set(), set(), {1}),
             (set(), {0}, set())]
        )

        
        linko3_0 = linkoCreate.Linkograph(
            [(set(), set(), set()),
             (set(), set(), set()),
             (set(), set(), set())]
        )

        linko3_1 = linkoCreate.Linkograph(
            [(set(), set(), {1}),
             (set(), {0}, set()),
             (set(), set(), set())]
        )


        linko3_2 = linkoCreate.Linkograph(
            [(set(), set(), {2}),
             (set(), set(), set()),
             (set(), {0}, set())]
        )

        linko3_3 = linkoCreate.Linkograph(
            [(set(), set(), {1,2}),
             (set(), {0}, set()),
             (set(), {0}, set())]
        )


        linko3_4 = linkoCreate.Linkograph(
            [(set(), set(), set()),
             (set(), set(), {2}),
             (set(), {1}, set())]
        )

        linko3_5 = linkoCreate.Linkograph(
            [(set(), set(), {1}),
             (set(), {0}, {2}),
             (set(), {1}, set())]
        )

        linko3_6 = linkoCreate.Linkograph(
            [(set(), set(), {2}),
             (set(), set(), {2}),
             (set(), {0,1}, set())]
        )

        linko3_7 = linkoCreate.Linkograph(
            [(set(), set(), {1,2}),
             (set(), {0}, {2}),
             (set(), {0,1}, set())]
        )


        if self.id().split('.')[-1] == 'test_enumToLinko':
            self.testParams = [
                {'enum': (0,0),
                 'ExpectedLinkograph': linko0_0},
                {'enum': (1,0),
                 'ExpectedLinkograph': linko1_0},
                {'enum': (2,0),
                 'ExpectedLinkograph': linko2_0},
                {'enum': (2,1),
                 'ExpectedLinkograph': linko2_1},
                {'enum': (3,0),
                 'ExpectedLinkograph': linko3_0},
                {'enum': (3,1),
                 'ExpectedLinkograph': linko3_1},
                {'enum': (3,2),
                 'ExpectedLinkograph': linko3_2},
                {'enum': (3,3),
                 'ExpectedLinkograph': linko3_3},
                {'enum': (3,4),
                 'ExpectedLinkograph': linko3_4},
                {'enum': (3,5),
                 'ExpectedLinkograph': linko3_5},
                {'enum': (3,6),
                 'ExpectedLinkograph': linko3_6},
                {'enum': (3,7),
                 'ExpectedLinkograph': linko3_7}]

    def performTestForParams(self):
        """"Performs the tests for each set of parameters."""
        for (number, params) in enumerate(self.testParams):
            actual = enumeration.enumToLinko(params['enum'])
            self.assertEqual(
                actual,
                params['ExpectedLinkograph'],
                ("Test fail: test number = {}, "
                 "Enumeration = {}, "
                 " Actual linkograph = {}"
                 " Expected linkograph = {}")
                .format(number,
                        params['enum'],
                        actual,
                        params['ExpectedLinkograph']))

    def test_enumToLinko(self):
        """Tests for the correct enumeration."""
        self.performTestForParams()

class Test_enumOnt(unittest.TestCase):
    """ Tests the enumOnt function. """

    def setUp(self):
        """ Set up parameters for individual tests. """

        # Ontologies
        ont0 = {'0':[]}
        ont1 = {'0': ['0']}

        ont0_0 = {'0':[], '1':[]}
        ont0_1 = {'0':[], '1':['0']}
        ont1_0 = {'0':['0'], '1':[]}
        ont1_1 = {'0':['0'], '1':['0']}
        ont2_0 = {'0':['1'], '1':[]}
        ont2_1 = {'0':['1'], '1':['0']}
        ont2_2 = {'0':['1'], '1':['1']}
        ont0_2 = {'0':[], '1':['1']}
        ont1_2 = {'0':['0'], '1':['1']}
        ont3_0 = {'0':['0','1'], '1':[]}
        ont3_1 = {'0':['0','1'], '1':['0']}
        ont3_2 = {'0':['0','1'], '1':['1']}
        ont3_3 = {'0':['0','1'], '1':['0','1']}
        ont0_3 = {'0':[], '1':['0','1']}
        ont1_3 = {'0':['0'], '1':['0','1']}
        ont2_3 = {'0':['1'], '1':['0','1']}



        if self.id().split('.')[-1] == 'test_enumOnt':
            self.testParams = [
                # {'enum': (0),
                #  'ExpectedOntology': ont0},
                # {'enum': (1),
                #  'ExpectedOntology': ont1},
                {'enum': (0,0),
                 'ExpectedOntology': ont0_0},
                {'enum': (0,1),
                 'ExpectedOntology': ont0_1},
                {'enum': (1,0),
                 'ExpectedOntology': ont1_0},
                {'enum': (1,1),
                 'ExpectedOntology': ont1_1},
                {'enum': (2,0),
                 'ExpectedOntology': ont2_0},
                {'enum': (2,1),
                 'ExpectedOntology': ont2_1},
                {'enum': (2,2),
                 'ExpectedOntology': ont2_2},
                {'enum': (0,2),
                 'ExpectedOntology': ont0_2},
                {'enum': (1,2),
                 'ExpectedOntology': ont1_2},
                {'enum': (3,0),
                 'ExpectedOntology': ont3_0},
                {'enum': (3,1),
                 'ExpectedOntology': ont3_1},
                {'enum': (3,2),
                 'ExpectedOntology': ont3_2},
                {'enum': (3,3),
                 'ExpectedOntology': ont3_3},
                {'enum': (0,3),
                 'ExpectedOntology': ont0_3},
                {'enum': (1,3),
                 'ExpectedOntology': ont1_3},
                {'enum': (2,3),
                 'ExpectedOntology': ont2_3}]

    def performTestForParams(self):
        """"Performs the tests for each set of parameters."""
        for (number, params) in enumerate(self.testParams):
            actual = enumeration.enumOnt(params['enum'])
            self.assertEqual(
                actual,
                params['ExpectedOntology'],
                ("Test fail: test number = {}, "
                 "enum = {}, "
                 " Actual Ontology = {}"
                 " Expected Ontology = {}")
                .format(number,
                        params['enum'],
                        actual,
                        params['ExpectedOntology']))

    def test_enumOnt(self):
        """Tests for the correct enumeration."""
        self.performTestForParams()


class Test_frequency(unittest.TestCase):
    """ Tests the fruquency function. """

    def setUp(self):
        """ Set up parameters for individual tests. """

        # Ontologies
        ont0 = {'0':[]}
        ont1 = {'0': ['0']}

        ont0_0 = {'0':[], '1':[]}
        ont0_1 = {'0':[], '1':['0']}
        ont1_0 = {'0':['0'], '1':[]}
        ont1_1 = {'0':['0'], '1':['0']}
        ont2_0 = {'0':['1'], '1':[]}
        ont2_1 = {'0':['1'], '1':['0']}
        ont2_2 = {'0':['1'], '1':['1']}
        ont0_2 = {'0':[], '1':['1']}
        ont1_2 = {'0':['0'], '1':['1']}
        ont3_0 = {'0':['0','1'], '1':[]}
        ont3_1 = {'0':['0','1'], '1':['0']}
        ont3_2 = {'0':['0','1'], '1':['1']}
        ont3_3 = {'0':['0','1'], '1':['0','1']}
        ont0_3 = {'0':[], '1':['0','1']}
        ont1_3 = {'0':['0'], '1':['0','1']}
        ont2_3 = {'0':['1'], '1':['0','1']}



        if self.id().split('.')[-1] == 'test_frequency_count':
            self.testParams = [
                {'length': 3,
                 'ontology': ont2_1,
                 'absClasses': ['0', '1'],
                 'ExpectedFreq': {(3,0):2, (3,3):2, (3,5):2,
                                  (3,6):2}},
                {'length': 3,
                 'ontology': ont3_1,
                 'absClasses': ['0', '1'],
                 'ExpectedFreq': {(3,0):1, (3,3):1, (3,5):1, (3,6):1,
                                  (3,7):4}},
                {'length': 3,
                 'ontology': ont0_0,
                 'absClasses': ['0', '1'],
                 'ExpectedFreq': {(3,0):8}},
                
                {'length': 3,
                 'ontology': ont1_0,
                 'absClasses': ['0', '1'],
                 'ExpectedFreq': {(3,0):4, (3,1):1, (3,2):1, (3,4):1,
                                  (3,7):1}},

                {'length': 3,
                 'ontology': ont2_1,
                 'absClasses': None,
                 'ExpectedFreq': {(3,0):2, (3,3):2, (3,5):2,
                                  (3,6):2}},
                {'length': 3,
                 'ontology': ont3_1,
                 'absClasses': ['0', '1'],
                 'ExpectedFreq': {(3,0):1, (3,3):1, (3,5):1, (3,6):1,
                                  (3,7):4}},
                {'length': 3,
                 'ontology': ont0_0,
                 'absClasses': None,
                 'ExpectedFreq': {(3,0):8}},
                
                {'length': 3,
                 'ontology': ont1_0,
                 'absClasses': None,
                 'ExpectedFreq': {(3,0):4, (3,1):1, (3,2):1, (3,4):1,
                                  (3,7):1}},
                {'length': 0,
                 'ontology': ont0,
                 'absClasses': None,
                 'ExpectedFreq': {(0,0): 1}},

                {'length': 0,
                 'ontology': ont1,
                 'absClasses': None,
                 'ExpectedFreq': {(0,0): 1}},

                {'length': 0,
                 'ontology': ont0_0,
                 'absClasses': None,
                 'ExpectedFreq': {(0,0): 1}},

                {'length': 0,
                 'ontology': ont2_3,
                 'absClasses': None,
                 'ExpectedFreq': {(0,0): 1}}]

    def performTestForParams(self, function):
        """"Performs the tests for each set of parameters."""
        for (number, params) in enumerate(self.testParams):
            actualFreq = enumeration.frequency(params['length'],
                                               params['ontology'],
                                               function,
                                               params['absClasses'])
            self.assertEqual(
                actualFreq,
                params['ExpectedFreq'],
                ("Test fail: test number = {}, "
                 "length = {}, "
                 " absClasses = {}"
                 " ontology = {}"
                 " Expected frequency = {}"
                 " Actual frequency = {}")
                .format(number,
                        params['length'],
                        params['absClasses'],
                        params['ontology'],
                        actualFreq,
                        params['ExpectedFreq']))

    def test_frequency_count(self):
        """Tests for the correct enumeration."""
        # Use the default function which should count the number of
        # distinct linkographs.
        self.performTestForParams(None)


class Test_modularCounter(unittest.TestCase):
    """ Tests the enumOnt function. """

    def setUp(self):
        """ Set up parameters for individual tests. """

        if self.id().split('.')[-1] == 'test_enumOnt':
            self.testParams = [
                {'len': 1,
                 'mod': 2,
                 'ExpectedList': [0]},
                {'len': 2,
                 'mod': 3,
                 'ExpectedList': [0,0]},
                {'len': 3,
                 'mod': 3,
                 'ExpectedList': [0,0,0]}]

    def performTestForParams(self):
        """"Performs the tests for each set of parameters."""
        for (number, params) in enumerate(self.testParams):
            actual = enumeration.modularCounter(params['len'], params['mod'])
            self.assertEqual(
                actual,
                params['ExpectedList'],
                ("Test fail: test number = {}, "
                 "len = {},"
                 "mod = {},"
                 " Actual List = {}"
                 " Expected List = {}")
                .format(number,
                        params['len'],
                        params['mod'],
                        actual,
                        params['ExpectedList']))

    def test_enumOnt(self):
        """Tests for the correct enumeration."""
        self.performTestForParams()

class Test_modularCounter_inc(unittest.TestCase):
    """ Tests the enumOnt function. """

    def setUp(self):
        """ Set up parameters for individual tests. """

        if self.id().split('.')[-1] == 'test_enumOnt':
            self.testParams = [
                {'len': 1,
                 'mod': 2,
                 'interations': 1,
                 'ExpectedList': [1]},
                {'len': 1,
                 'mod': 2,
                 'interations': 2,
                 'ExpectedList': [0]},
                {'len': 2,
                 'mod': 3,
                 'interations': 1,
                 'ExpectedList': [1,0]},
                {'len': 2,
                 'mod': 3,
                 'interations': 2,
                 'ExpectedList': [2,0]},
                {'len': 2,
                 'mod': 3,
                 'interations': 3,
                 'ExpectedList': [0,1]},
                {'len': 2,
                 'mod': 3,
                 'interations': 4,
                 'ExpectedList': [1,1]},
                {'len': 2,
                 'mod': 3,
                 'interations': 5,
                 'ExpectedList': [2,1]},
                {'len': 2,
                 'mod': 3,
                 'interations': 6,
                 'ExpectedList': [0,2]},
                {'len': 2,
                 'mod': 3,
                 'interations': 7,
                 'ExpectedList': [1,2]},
                {'len': 2,
                 'mod': 3,
                 'interations': 8,
                 'ExpectedList': [2,2]},
                {'len': 2,
                 'mod': 3,
                 'interations': 9,
                 'ExpectedList': [0,0]}]

    def performTestForParams(self):
        """"Performs the tests for each set of parameters."""
        for (number, params) in enumerate(self.testParams):
            actual = enumeration.modularCounter(params['len'],
                                                params['mod'])

            for n in range(params['interations']):
                actual.inc()
            self.assertEqual(
                actual,
                params['ExpectedList'],
                ("Test fail: test number = {}, "
                 "len = {}, "
                 "mod = {}, "
                 "interations = {}, "
                 " Actual List = {}"
                 " Expected List = {}")
                .format(number,
                        params['len'],
                        params['mod'],
                        params['interations'],
                        actual,
                        params['ExpectedList']))

    def test_enumOnt(self):
        """Tests for the correct enumeration."""
        self.performTestForParams()

class Test_modularCounter_toInverseLabeling(unittest.TestCase):
    """ Tests the enumOnt function. """

    def setUp(self):
        """ Set up parameters for individual tests. """

        if self.id().split('.')[-1] == 'test_enumOnt':
            self.testParams = [
                {'list': [0],
                 'absClass': ['0', '1'],
                 'ExpectedInverseLabeling': {'0': [0]}},
                {'list': [0,1,1,0,1],
                 'absClass': ['0', '1'],
                 'ExpectedInverseLabeling': {'0': [0, 3],
                                             '1': [1,2,4]}},
                {'list': [0,1,1,0,1],
                 'absClass': ['Test', 'Labels'],
                 'ExpectedInverseLabeling': {'Test': [0, 3],
                                             'Labels': [1,2,4]}},
                {'list': [0,0,0,0,0],
                 'absClass': ['0', '1'],
                 'ExpectedInverseLabeling': {'0': [0, 1, 2, 3, 4]}},
                {'list': [0,0,0,0,0],
                 'absClass': ['0'],
                 'ExpectedInverseLabeling': {'0': [0, 1, 2, 3, 4]}}]

    def performTestForParams(self):
        """"Performs the tests for each set of parameters."""
        for (number, params) in enumerate(self.testParams):
            # Extract the test list and absClass for easier reference.
            testList = params['list']
            testAbsClass = params['absClass']

            # Create the modular counter.
            testModularCounter = enumeration.modularCounter(len(testList),
                                                            len(testAbsClass))

            # Set the modular counter to be the same as the test list.
            for i in range(len(testList)):
                testModularCounter[i] = testList[i]
            actual = testModularCounter.toInverseLabeling(testAbsClass)
            self.assertEqual(
                actual,
                params['ExpectedInverseLabeling'],
                ("Test fail: test number = {}, "
                 "list = {},"
                 "absClass = {},"
                 "Construced modular counter = {},"
                 " Actual Inverse Labeling = {}"
                 " Expected Inverse Labeling= {}")
                .format(number,
                        params['list'],
                        params['absClass'],
                        testModularCounter,
                        actual,
                        params['ExpectedInverseLabeling']))

    def test_enumOnt(self):
        """Tests for the correct enumeration."""
        self.performTestForParams()

class Test_Enum_For_Large_Linkographs(unittest.TestCase):
    """Test of unique encoding that scales to larger linkographs. """

    def test_conversion_to_linko(self):
        """Tests enum -> linko -> enum

        This test loops through a set of sizes for linkgraphs given by
        the max_linko_size variable. For each size, every integer
        counting the possible linkographs for that size is converted
        into a linkograph and back. This test verifies that
        enumToLinko(linkoToEnum(n)) == n where enumToLinko is the
        function that converts an interger to a linkograph and
        linkoToEnum is a function that converts a linkograph to an
        integer. Once we know this equation holds, this shows that
        enumToLinko is injective and linkoToEnum is surjective on the
        set of possible intergers for linkographs. Since this set is
        finite for a particular size of linkograph, we know that
        enumToLinko and linkoToEnum are bijective.

        """

        max_linko_size = 6

        for size in range(max_linko_size):

            num_linkos = stats.totalLinkographs(size)

            for i in range(num_linkos):

                target_enum = (size, i)

                # Convert to linkograph
                linko = enumeration.enumToLinko(target_enum)

                # Convert back
                result_enum = enumeration.linkoToEnum(linko)

                self.assertEqual(
                    target_enum,
                    result_enum,
                    ("target_enum = {}"
                     "result_enum = {}")
                    .format(target_enum,
                            result_enum))

                # Add some labels and convert back
                for record_number, record in enumerate(linko):
                    record[0].add(str(record_number))

                # Convert back
                enum = enumeration.linkoToEnum(linko)

                self.assertEqual(
                    target_enum,
                    result_enum,
                    ("target_enum = {}"
                     "result_enum = {}")
                    .format(target_enum,
                            result_enum))
