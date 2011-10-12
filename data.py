# -*- coding: utf-8 -*-

import math

class Vector(object):

    def __init__(self, values):
        self.values = values

    def length(self):
        powers = map(lambda x: pow(x,2), self.values)
        return math.sqrt(sum(powers))

    def dot_product(self, other):
        pairs = zip(self.values, other.values)
        multiples = [x*y for x,y in pairs]
        return sum(multiples)

    def similarity(self, other):
        length = self.length() + other.length()
        if length == 0:
            return 0
        else:
            return self.dot_product(other) / length

class Loader(object):

    @staticmethod
    def load_stopwords(filepath):
        stopwords = [line.strip().lower() for line in file(filepath)]
        return frozenset(stopwords)

    @staticmethod
    def load_keywords(filepath):
        keywords = [line.strip().lower() for line in file(filepath)]
        return keywords

    @staticmethod
    def load_documents(filepath):
        documents = {}
        title = None
        for line in file(filepath):
            if title is None:
                title = line.strip()
            words = line.split()
            if words:
                documents[title] += words
            else:
                title = None

