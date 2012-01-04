# -*- coding: utf-8 -*-

import math
import random
from collections import defaultdict, OrderedDict

from data import Vector


class TFIDF(object):

    def __init__(self, keywords, documents, cleaner):
        self.keywords = None
        self.keywords_lookup = None
        self.documents_count = None
        self.documents = None
        self.document_vectors = None
        self.documents_tfidfs = {}

        self.cleaner = cleaner

        self._setup_keywords(keywords)
        self._setup_documents(documents)
        self._setup_documents_count()
        self._setup_documents_tfidfs()

    def _setup_keywords(self, keywords):
        self.keywords = OrderedDict()
        self.keywords_lookup = OrderedDict()
        cleaned = self.cleaner.clean_wordlist(keywords)
        cleaned = set(cleaned)
        for i, word in enumerate(sorted(cleaned)):
            self.keywords[word] = i
            self.keywords_lookup[i] = word

    def _setup_documents(self, documents):
        self.documents = documents
        self.document_vectors = {}
        for index, document in enumerate(documents):
            cleaned = self.cleaner.clean_wordlist(
                    document[0].split() + document[1].split())
            vector = self.wordlist_to_vector(cleaned)
            self.document_vectors[index] = vector

    def _setup_documents_tfidfs(self):
        for i in range(len(self.documents)):
            vector = self.document_vectors[i]
            tfidfs = self.tfidf(vector)
            self.documents_tfidfs[i] = tfidfs

    def _setup_documents_count(self):
        self.documents_count = defaultdict(int)
        for keyword, i in self.keywords.iteritems():
            for document_vector in self.document_vectors.itervalues():
                if document_vector[i] > 0:
                    self.documents_count[keyword] += 1

    def wordlist_to_vector(self, wordlist):
        significant = [word for word in wordlist if word in self.keywords]
        wordcount = defaultdict(int)
        for word in significant:
            wordcount[word] += 1
        vector = [wordcount[word] for word in self.keywords.iterkeys()]
        return vector

    def search(self, question):
        question_vector = self.phrase_to_vector(question)
        question_tfidfs = self.tfidf(question_vector)
        ranking = {}
        for i in range(len(self.documents)):
            ranking[i] = self.doc_phrase_similarity(i, question_tfidfs)

        results = [(self.documents[item[0]][0], item[1], item[0])
                for item in sorted(ranking.items(),
                    key=lambda t: t[1], reverse=True) if item[1] > 0]
        return results

    def phrase_to_vector(self, phrase):
        phrase_words = phrase.split()
        phrase_clean = self.cleaner.clean_wordlist(phrase_words)
        return self.wordlist_to_vector(phrase_clean)

    def doc_phrase_similarity(self, doc_index, question_tfidfs):
        return Vector.similarity(
                self.tfidf_by_doc_index(doc_index), question_tfidfs)

    def doc_doc_similarity(self, doc1_index, doc2_index):
        return Vector.similarity(
                self.tfidf_by_doc_index(doc1_index), self.tfidf_by_doc_index(doc2_index))                
                
    def tfidf_by_doc_index(self, i):
        return self.documents_tfidfs[i]

    def tfidf(self, document):
        tfs = [self.tf(document, word) for word in self.keywords.iterkeys()]
        idfs = [self.idf(word) for word in self.keywords.iterkeys()]
        tfidfs = [float(tf * idf) for tf, idf in zip(tfs, idfs)]
        return tfidfs

    def tf(self, document, term):
        term_index = self.keywords[term]
        n = document[term_index]
        if n == 0:
            return 0
        else:
            return float(n) / float(max(document))

    def idf(self, term):
        n = self.documents_count[term]
        if n == 0:
            return 0
        else:
            return math.log(float(len(self.documents)) / float(n), 10)

    def get_term_document_matrix(self):
        result = []
        for i in xrange(len(self.documents_tfidfs)):
            result.append(self.documents_tfidfs[i])
        return result
        
    def group_kmeans(self, k, max_iters):
        centroids_tfidfs = random.sample(self.documents_tfidfs.values(), k)
        i = 0;
        changed = True
        groups = [[doc_id for doc_id in range(len(self.documents))]]
        old_groups = []
        while i < max_iters and old_groups != groups:
            old_groups = groups
            groups = self.assign_to_groups(centroids_tfidfs)
            centroids_tfidfs = self.centroids(groups)        
        return groups

    def assign_to_groups(self, centroids_tfidfs):    
        groups = []
        for i in range(len(centroids_tfidfs)):
            groups.append([])
        for doc_id in range(len(self.documents)):
            best = -1;
            for i, centroid_tfidf in enumerate(centroids_tfidfs):
                sim = self.doc_phrase_similarity(doc_id, centroid_tfidf)
                if sim > best:
                    best = sim
                    group = i
            groups[group].append(doc_id)
        return groups
            
    def centroids(self, groups):      
        centroids = []
        for group in groups:
            centroid = self.centroid(group)
            centroids.append(centroid)
        return centroids
        
    def centroid(self, group):
        centroid = []
        for doc_id in group:
            doc_tfidf = self.documents_tfidfs[doc_id]
            for i, value in enumerate(doc_tfidf):
                if i >= len(centroid):
                    centroid.append(0)
                centroid[i] += value
        centroid = [value / len(group) for value in centroid]            
        return centroid
        