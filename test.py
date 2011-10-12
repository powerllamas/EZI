# -*- coding: utf-8 -*-

import unittest

from data import Vector
from word import Cleaner
from search import TFIDF

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
        expected = ["comput", "12", "10", "2010", "morn"]
        self.assertEqual(actual, expected)

class TestTFIDF(unittest.TestCase):

    def setUp(self):
        stopwords = "stop".split()
        keywords = "aaa bbb ccc ddd eee fff".split()
        documents = {
                'document 1 ccc': "aaa aaa aaa ccc",
                'document 2 stop': "stop aaa bbb ccc",
                'document 3 stop': "aaa",
                'document 4 ddd': "aaa bbb ccc ddd eee"
                }
        self.s = TFIDF(keywords, documents, Cleaner(stopwords))

    def test_keyword_setup(self):
        actual = self.s.keywords.items()
        expected = [("aaa", 0), ("bbb", 1), ("ccc", 2), ("ddd", 3), ("eee", 4), ("fff", 5)]
        self.assertEqual(actual, expected)

    def test_documents_setup(self):
        actual = self.s.document_vectors
        expected = {
                'document 1 ccc': [3, 0, 2, 0, 0, 0],
                'document 2 stop': [1, 1, 1, 0, 0, 0],
                'document 3 stop': [1, 0, 0, 0, 0, 0],
                'document 4 ddd': [1, 1, 1, 2, 1, 0]
                }
        self.assertEqual(actual, expected)

    def test_search_with_no_results(self):
        actual = self.s.search("fff")
        expected = []
        self.assertEqual(actual, expected)

    def test_search_with_only_popular_terms(self):
        actual = self.s.search("aaa")
        expected = [] #because idf=0
        self.assertEqual(actual, expected)

if __name__ == '__main__':
    unittest.main()
