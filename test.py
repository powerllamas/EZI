# -*- coding: utf-8 -*-

import unittest

from data import Vector

class TestVectorFunctions(unittest.TestCase):

    def setUp(self):
        self.v0 = [0, 0, 0, 0]
        self.v1 = [1, 2, 3, 4]
        self.v2 = [5, 6, 7, 8]

    def test_length(self):
        actual = Vector.length(self.v0)
        expected = 0.0
        self.assertAlmostEqual(actual, expected)

        actual = Vector.length(self.v1)
        expected = 5.477225575
        self.assertAlmostEqual(actual, expected)

        actual = Vector.length(self.v2)
        expected = 13.190905958
        self.assertAlmostEqual(actual, expected)

    def test_dot_product(self):
        actual = Vector.dot_product(self.v1, self.v2)
        expected = 5 + 12 + 21 + 32
        self.assertAlmostEqual(actual, expected)

    def test_similarity(self):
        actual = Vector.similarity(self.v0, self.v1)
        expected = 0.0
        self.assertAlmostEqual(actual, expected)

        actual = Vector.similarity(self.v1, self.v2)
        expected = 70.0 / (5.477225575 * 13.190905958)
        self.assertAlmostEqual(actual, expected)

if __name__ == '__main__':
    unittest.main()
