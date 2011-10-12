# -*- coding: utf-8 -*-

import unittest

from data import Vector
from word import Cleaner

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

class TestCleaner(unittest.TestCase):

    def setUp(self):
        stopwords = "stop halt basta".split()
        self.c = Cleaner(stopwords)

    def test_clean_word(self):
        word = "STop"
        actual = self.c.clean_word(word)
        self.assertIsNone(actual)

        word = "co.mp%&*uTEr"
        actual = self.c.clean_word(word)
        self.assertEqual(actual, "comput")

    def test_clean_wordlist(self):
        words = "stop coMputer #$%&*".split()
        actual = self.c.clean_wordlist(words)
        expected = ["comput"]
        self.assertEqual(actual, expected)

        words = "stop computer halt 12-10-2010 morning".split()
        actual = self.c.clean_wordlist(words)
        expected = ["comput", "12102010", "morn"]
        self.assertEqual(actual, expected)

if __name__ == '__main__':
    unittest.main()
