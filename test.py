# -*- coding: utf-8 -*-

import unittest
import math

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
        documents = [
                ('document 1 ccc', "aaa aaa aaa ccc"),
                ('document 2 stop', "stop aaa bbb ccc"),
                ('document 3 stop', "aaa"),
                ('document 4 ddd', "aaa bbb ccc ddd eee")
                ]
        self.s = TFIDF(keywords, documents, Cleaner(stopwords))

    def test_keyword_setup(self):
        actual = self.s.keywords.items()
        expected = [("aaa", 0), ("bbb", 1), ("ccc", 2), ("ddd", 3), ("eee", 4), ("fff", 5)]
        self.assertEqual(actual, expected)

    def test_documents_setup(self):
        actual = self.s.document_vectors
        expected = {
                0: [3, 0, 2, 0, 0, 0],
                1: [1, 1, 1, 0, 0, 0],
                2: [1, 0, 0, 0, 0, 0],
                3: [1, 1, 1, 2, 1, 0]
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


    def test_tf(self):
        document = self.s.document_vectors[0]
        actual = self.s.tf(document, 'ccc')
        expected = 0.6666666666
        self.assertAlmostEqual(actual, expected)
        
        document = self.s.document_vectors[0]
        actual = self.s.tf(document, 'aaa')
        expected = 1.0
        self.assertAlmostEqual(actual, expected)

        document = self.s.document_vectors[1]
        actual = self.s.tf(document, 'aaa')
        expected = 1.0
        self.assertAlmostEqual(actual, expected)

        document = self.s.document_vectors[2]
        actual = self.s.tf(document, 'aaa')
        expected = 1.0
        self.assertAlmostEqual(actual, expected)

        document = self.s.document_vectors[3]
        actual = self.s.tf(document, 'aaa')
        expected = 0.5
        self.assertAlmostEqual(actual, expected)
        

    def test_idf(self):
        
        expected_results = [
                            ("aaa", math.log(1.0, 10)), ("bbb", math.log(2.0, 10)),
                            ("ccc", math.log(1.3333333333333, 10)), ("ddd", math.log(4.0, 10)),
                            ("eee", math.log(4.0, 10)), ("fff", 0.0)
                            ]
        
        for term, expected in expected_results:
            actual = self.s.idf(term)
            self.assertAlmostEqual(actual, expected)


            
class TestTFIDF_flies(unittest.TestCase):
    
    def setUp(self):
        stopwords = "stop".split()
        keywords = "bee wasp fly fruit like".split()      
        documents = [        
                ("D1", "Time fly like an arrow but fruit fly like a banana."),
                ("D2", "It's strange that bees and wasps don't like each other."),
                ("D3", "The fly attendant sprayed the cabin with a strange fruit aerosol."),
                ("D4", "Try not to carry a light, as wasps and bees may fly toward it."),
                ("D5", "Fruit fly fly around in swarms. When fly they flap their wings 220 times a second.")
            ]
        self.s = TFIDF(keywords, documents, Cleaner(stopwords))
            
            
    def test_keyword_setup(self):
        actual = self.s.keywords.items()
        expected = [("bee", 0), ("fly", 1), ("fruit", 2), ("like", 3), ("wasp", 4)]     
        self.assertEqual(actual, expected)
            
    def test_documents_setup(self):
        actual = self.s.document_vectors
        expected = {
                0: [0, 2, 1, 2, 0],
                1: [1, 0, 0, 1, 1],
                2: [0, 1, 1, 0, 0],
                3: [1, 1, 0, 0, 1],
                4: [0, 3, 1, 0, 0]
                }                
        self.assertEqual(actual, expected)
        
 
    def test_tf(self):
        expected_results = [
            (0, [0, 1, 0.5, 1, 0]),
            (1, [1, 0, 0, 1, 1]),
            (2, [0, 1, 1, 0, 0]),
            (3, [1, 1, 0, 0, 1]),
            (4, [0, 1, 0.333333333333333333, 0, 0])
            ]
        for index, expected_vector in expected_results:            
            document = self.s.document_vectors[index]
            for word, i in self.s.keywords.items():            
                actual = self.s.tf(document, word)
                expected = expected_vector[i]
                self.assertEqual(actual, expected)        

                
    def test_idf(self):
        expected_results = [
                            ("bee", 0.397940009),
                            ("fly", 0.096910013),
                            ("fruit", 0.22184875),
                            ("like", 0.397940009),
                            ("wasp", 0.397940009)
                           ]        
        for term, expected in expected_results:
             actual = self.s.idf(term)
             self.assertAlmostEqual(actual, expected, places=6)
            

    def test_tfidf(self):
        expected_results = [                         
                            (0, [0, 0.096910013, 0.110924375, 0.397940009, 0]),
                            (1, [0.397940009, 0, 0, 0.397940009, 0.397940009]),
                            (2, [0, 0.096910013, 0.22184875, 0, 0]),
                            (3, [0.397940009, 0.096910013, 0, 0, 0.397940009]),
                            (4, [0, 0.096910013, 0.073949583, 0, 0])                            
                            ]
        for title, expected_vector in expected_results:
            document = self.s.document_vectors[title]
            actual_vector = self.s.tfidf(document)
            for actual, expected in zip(actual_vector, expected_vector):
                self.assertAlmostEqual(actual, expected, places = 6)
        


if __name__ == '__main__':
    unittest.main()
