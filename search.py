# -*- coding: utf-8 -*-

import math

from collections import defaultdict, OrderedDict

from data import Vector

class TFIDF(object):

    def __init__(self, keywords, documents, cleaner):
        self.keywords = None
        self.keywords_count = None
        self.documents = None
        self.document_vectors = None

        self.cleaner = cleaner

        self._setup_keywords(keywords)
        self._setup_documents(documents)
        self._setup_keywords_count()

    def _setup_keywords(self, keywords):
        self.keywords = OrderedDict()
        cleaned = self.cleaner.clean_wordlist(keywords)
        cleaned = set(cleaned)
        for i, word in enumerate(sorted(cleaned)):
            self.keywords[word] = i

    def _setup_documents(self, documents):
        self.documents = documents
        self.document_vectors = {}
        for title, words in documents.iteritems():
            cleaned = self.cleaner.clean_wordlist(words)
            vector = self.wordlist_to_vector(cleaned)
            self.document_vectors[title] = vector

    def _setup_keywords_count(self):
        self.keywords_count = defaultdict(int)
        for keyword, i in self.keywords.iteritems():
            for document_vector in self.document_vectors.itervalues():
                if document_vector.values[i] > 0:
                    self.keywords_count[keyword] += 1

    def wordlist_to_vector(self, wordlist):
        significant = [word for word in wordlist if word in self.keywords]
        wordcount = defaultdict(int)
        for word in significant:
            wordcount[word] += 1
        vector = Vector([wordcount[word] for word in self.keywords.iterkeys()])
        return vector

    def search(self, question):
        question_vector = self.phrase_to_vector(question)
        ranking = {}
        for title, document_vector in self.document_vectors.iteritems():
            ranking[title] = self.similarity(document_vector, question_vector)

        for title, similarity in sorted(ranking.items(), key=(lambda t: t[1]), reverse=True):
            print "{0:4f}\t{1}".format(similarity, title)

    def phrase_to_vector(self, phrase):
        phrase_words = phrase.split()
        phrase_clean = self.cleaner.clean_wordlist(phrase_words)
        return self.wordlist_to_vector(phrase_clean)

    def similarity(self, vec1, vec2):
        return self.tfidf(vec1).similarity(self.tfidf(vec2))

    def tfidf(self, document):
        tfs = [self.tf(document, word) for word in self.keywords.iterkeys()]
        idfs = [self.idf(word) for word in self.keywords.iterkeys()]
        tfidfs = [tf*idf for tf, idf in zip(tfs, idfs)]
        return Vector(tfidfs)

    def tf(self, document, term):
        term_index = self.keywords[term]
        n = document.values[term_index]
        if n == 0:
            return 0
        else:
            return float(n) / float(max(document.values))

    def idf(self, term):
        n = self.keywords_count[term]
        if n == 0:
            return 0
        else:
            return math.log(float(len(self.documents)) / float(n))

