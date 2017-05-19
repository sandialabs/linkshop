#!/usr/bin/env python3

"""Tests the Models.py package."""

import unittest
from markov import Model # The package under test.
import numpy as np # For matrices

class Test__next(unittest.TestCase):

    """Basic unit tests for _next function."""

    def setUp(self):
        """Set up the parameters for the individual tests."""

        transitionMatrix = np.array([[0.33, 0.33, 0.34],
                                     [0.,   0.5,  0.5],
                                     [0.5,  0.5,  0]])
        
        if self.id().split('.')[-1] == 'test__next':
            self.testParams = [
                {'model': Model.Model(transitionMatrix, initial=0, seed=5),
                 'ExpectedNextState': 1},
                {'model': Model.Model(transitionMatrix, initial=1, seed=5),
                 'ExpectedNextState': 2},]

    def performTestForParams(self):
        """"Performs the tests for each set of parameters."""
        for (i, params) in enumerate(self.testParams):
            with self.subTest(i=i):
                actual = (params['model'])._next()
                self.assertEqual(
                    actual,
                    params['ExpectedNextState'],
                    ("Test fail:"
                     " Actual _next = {}"
                     " Expected _next = {}")
                    .format(actual,
                            params['ExpectedNextState']))

    def test__next(self):
        """Test the _next function."""
        self.performTestForParams()

class Test_next(unittest.TestCase):

    """Basic unit tests for next function."""

    def setUp(self):
        """Set up the parameters for the individual tests."""

        transitionMatrix = np.array([[0.33, 0.33, 0.34],
                                     [0.,   0.5,  0.5],
                                     [0.5,  0.5,  0]])
        
        if self.id().split('.')[-1] == 'test_next':
            self.testParams = [
                {'model': Model.Model(transitionMatrix, initial=0, seed=5),
                 'ExpectedNextState': 1},
                {'model': Model.Model(transitionMatrix, initial=1, seed=5),
                 'ExpectedNextState': 2},]

    def performTestForParams(self):
        """"Performs the tests for each set of parameters."""
        for (i, params) in enumerate(self.testParams):
            with self.subTest(i=i):
                actual = (params['model']).next()
                self.assertEqual(
                    actual,
                    params['ExpectedNextState'],
                    ("Test fail:"
                     " Actual next = {}"
                     " Expected next = {}")
                    .format(actual,
                            params['ExpectedNextState']))

    def test_next(self):
        """Tests the next function."""
        self.performTestForParams()

class Test_current(unittest.TestCase):

    """Basic unit tests for current function."""

    def setUp(self):
        """Set up the parameters for the individual tests."""

        transitionMatrix = np.array([[0.33, 0.33, 0.34],
                                     [0.,   0.5,  0.5],
                                     [0.5,  0.5,  0]])

        if self.id().split('.')[-1] == 'test_current':
            self.testParams = [
                {'model': Model.Model(transitionMatrix, initial=0, seed=5),
                 'ExpectedCurrentState': 0},
                {'model': Model.Model(transitionMatrix, initial=1, seed=5),
                 'ExpectedCurrentState': 1},]

    def performTestForParams(self):
        """"Performs the tests for each set of parameters."""
        for (i, params) in enumerate(self.testParams):
            with self.subTest(i=i):
                actual = (params['model']).current()
                self.assertEqual(
                    actual,
                    params['ExpectedCurrentState'],
                    ("Test fail:"
                     " Actual current = {}"
                     " Expected current = {}")
                    .format(actual,
                            params['ExpectedCurrentState']))

    def test_current(self):
        """Test the current function."""
        self.performTestForParams()

class Test_Model_Exceptions(unittest.TestCase):

    """Basic unit tests for exceptions when contstructing a model."""

    def setUp(self):
        """Set up the parameters for the individual tests."""

        matrix3_2 = np.array([[0.33, 0.33],
                              [0.,   0.5],
                              [0.5,  0.5]])
        
        matrix2_3 = np.array([[0.33, 0.33, 0.34],
                              [0.,   0.5,  0.5]])

        matrix3 = np.array([0.33, 0.33, 0.34])

        if self.id().split('.')[-1] == 'test_exceptions':
            self.testParams = [
                {'positional': matrix3_2,
                 'keyword': {'initial': 0, 'seed': 5},
                 'Exception': Model.ShapeError},
                {'positional': matrix2_3,
                 'keyword': {'initial': 0, 'seed': 5},
                 'Exception': Model.ShapeError},
                {'positional': matrix3,
                 'keyword': {'initial': 0, 'seed': 5},
                 'Exception': Model.ShapeError},]

    def performTestForParams(self):
        """"Performs the tests for each set of parameters."""
        for (i, params) in enumerate(self.testParams):
            with self.subTest(i=i):
                self.assertRaises(
                    params['Exception'],
                    Model.Model,
                    params['positional'],
                    **(params['keyword'])
                    )

    def test_exceptions(self):
        """Tests exception cases in generating a model."""
        self.performTestForParams()

class Test_inverseLabeling(unittest.TestCase):

    """Basic unit tests for inverseLabeling."""

    def setUp(self):
        """Set up the parameters for the individual tests."""

        tMatrix = np.array([[0.33, 0.33, 0.34],
                            [0.,   0.5,  0.5],
                            [0.5,  0.5,  0]])

        if self.id().split('.')[-1] == 'test_frequency':
            self.testParams = [
                {'matrix': tMatrix,
                 'seed': 5,
                 'initial': 0,
                 'size': 10**4,
                 'precision': 1},]

    def performTestForParams(self):
        """"Performs the tests for each set of parameters."""
        for params in self.testParams:

            # Generate the model
            m = Model.Model(params['matrix'],
                            initial=params['initial'],
                            seed=params['seed'])

            # Generate the inverse labeling
            il = m.inverseLabeling(params['size'])

            resultSize = sum([len(v) for (k,v) in il.items()])

            # Make sure the labeling is the correct size
            self.assertEqual(resultSize,
                             params['size'],
                             ('Result Size: {0},'
                              ' Expected Size: {1}.')
                             .format(resultSize,
                                     params['size']))

            frequencies = self.calculateFrequency(m, il)

            frequencies = np.round(frequencies,
                                   decimals=params['precision'])

            expected = np.round(params['matrix'],
                                decimals=params['precision'])


            equal = np.all(frequencies ==  expected)

            self.assertTrue(equal,
                            ("Calculated next frequencies: {0}, "
                             " Expected next frequencies: {1}")
                            .format(frequencies, expected))




    def test_frequency(self):
        """Tests the frequency of the generated mdoels."""
        self.performTestForParams()

    def calculateFrequency(self, model, inverseLabeling):
        """Calculate inverse labeling next state frequencies."""
        size = len(inverseLabeling)

        frequencies = np.zeros((size, size))

        for (i, initState) in enumerate(model.absClasses):
            for (j, termState) in enumerate(model.absClasses):
                initNodes = inverseLabeling[initState]
                termNodes = set(inverseLabeling[termState])

                intersection = {n for n in initNodes if (n+1) in termNodes}

                frequencies[i, j] = len(intersection)


        totals = np.sum(frequencies, axis=1)

        frequencies = frequencies/totals[:, np.newaxis]

        return frequencies

class Test_genLinkograph_Exceptions(unittest.TestCase):

    """Basic unit tests for testing the genLinograph function exceptions."""

    def setUp(self):
        """Set up the parameters for the individual tests."""

        tMatrix = np.array([[0.33, 0.33, 0.34],
                            [0.,   0.5,  0.5],
                            [0.5,  0.5,  0]])

        if self.id().split('.')[-1] == 'test_exceptions':
            self.testParams = [
                {'model': Model.Model(tMatrix, initial=0, seed=5),
                 'positional': 6,
                 'keyword': {'ontology': None},
                 'exception': Model.OntologyError},]

    def performTestForParams(self):
        """"Performs the tests for each set of parameters."""
        for params in self.testParams:
            self.assertRaises(
                params['exception'],
                params['model'].genLinkograph,
                params['positional'],
                **(params['keyword'])
            )

    def test_exceptions(self):
        """Tests exception cases in generating a model."""
        self.performTestForParams()

class Test_genLinkograph(unittest.TestCase):

    """Basic unit tests for testing the genLinograph function."""

    def setUp(self):
        """Set up the parameters for the individual tests."""

        tMatrix = np.array([[0.33, 0.33, 0.34],
                            [0.,   0.5,  0.5],
                            [0.5,  0.5,  0]])

        ontology = {0: [1], 1: [0], 2: [2]}

        linko = [({1}, set(), set()),
                 ({2}, set(), {3, 5}),
                 ({1}, set(), set()),
                 ({2}, {1}, {5}),
                 ({1}, set(), set()),
                 ({2}, {1, 3}, set())]

        if self.id().split('.')[-1] == 'test_genlinkograph':
            self.testParams = [
                {'model': Model.Model(tMatrix, initial=0, seed=5),
                 'ontology': ontology,
                 'expectedLinko': linko},]

    def performTestForParams(self):
        """"Performs the tests for each set of parameters."""
        for params in self.testParams:
            model = params['model']
            actualLinko = model.genLinkograph(6, ontology=params['ontology'])
            self.assertEqual(
                actualLinko,
                params['expectedLinko'],
                ('Actual linkograph: {0}'
                 ' Expected Linkograph: {1}')
                .format(actualLinko, params['expectedLinko'])
            )

    def test_genlinkograph(self):
        """Tests exception cases in generating a model."""
        self.performTestForParams()

class Test_genModel(unittest.TestCase):

    """Basic unit tests for testing the genLinograph function."""

    def setUp(self):
        """Set up the parameters for the individual tests."""

        tMatrix = np.array([[ 0.03,  0.19,  0.06,  0.36,  0.1 ,  0.26],
                            [ 0.03,  0.06,  0.33,  0.26,  0.21,  0.11],
                            [ 0.03,  0.17,  0.02,  0.29,  0.14,  0.35],
                            [ 0.01,  0.21,  0.32,  0.05,  0.22,  0.19],
                            [ 0.16,  0.18,  0.36,  0.11,  0.15,  0.04],
                            [ 0.09,  0.01,  0.24,  0.26,  0.25,  0.15]])

        if self.id().split('.')[-1] == 'test_genModel':
            self.testParams = [
                {'positional': 6,
                 'keyword': {'precision': 2, 'seed': 42},
                 'expectedMatrix': tMatrix},]

    def performTestForParams(self):
        """"Performs the tests for each set of parameters."""
        for params in self.testParams:
            model = Model.genModel(params['positional'],
                                   **params['keyword'])
            actualMatrix = model.tMatrix
            result = np.all(actualMatrix == params['expectedMatrix'])

            self.assertTrue(
                result,
                ('Actual matrix: {0}'
                 ' Expected matrix: {1}')
                .format(actualMatrix, params['expectedMatrix'])
            )

    def test_genModel(self):
        """Tests exception cases in generating a model."""
        self.performTestForParams()
