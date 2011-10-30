# -*- coding: utf-8 -*-

import math


class Vector(object):

    @staticmethod
    def length(vector):
        powers = map(lambda x: pow(x, 2), vector)
        return math.sqrt(sum(powers))

    @staticmethod
    def dot_product(vec_a, vec_b):
        pairs = zip(vec_a, vec_b)
        multiples = [x * y for x, y in pairs]
        return float(sum(multiples))

    @staticmethod
    def similarity(vec_a, vec_b):
        length = Vector.length(vec_a) * Vector.length(vec_b)
        if length == 0:
            return 0.0
        else:
            return Vector.dot_product(vec_a, vec_b) / float(length)


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
    def load_documents(filepath, categories=False):
        documents = []
        cache = []
        title = None
        category = None
        for line in file(filepath):
            words = line.strip()
            if words:
                if categories and category is None:
                    category = words
                    continue
                if title is None:
                    title = words
                else:
                    cache.append(words)
            else:
                documents.append((title, " ".join(cache), category))
                cache = []
                title = None
                category = None
        if words:
            documents.append((title, " ".join(cache), category))
        return documents
