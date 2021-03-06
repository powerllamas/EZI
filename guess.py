# -*- coding: utf-8 -*-

class Guesses(object):
    def __init__(self, term_document_m, terms, terms_lookup):
        self._calculate_correlation(term_document_m)
        self.terms = terms
        self.terms_lookup = terms_lookup

    def _calculate_correlation(self, m):
        self._term_correlation_matrix = []
        if m:
            for i in xrange(len(m[0])): # term
                row = []
                for j in xrange(len(m[0])): # term
                    val = self._multiply_vectors(m, i, j)
                    row.append(val)
                self._term_correlation_matrix.append(row)

    def _multiply_vectors(self, m, i, j):
        sum = 0
        for k in xrange(len(m)): # doc
            sum += m[k][i]*m[k][j]
        return sum

    def guess(self, _query):
        query = _query.strip()
        terms_cor = []
        result = None
        for term in query.split():
            if term in self.terms:
                best = []
                i = self.terms[term]
                best = self._term_correlation_matrix[i]
                terms_cor.append(best)
        if terms_cor:
            if len(terms_cor) > 1:
                result = [reduce(lambda x, y: x * y, term, 1) for term in zip(terms_cor)]
            else:
                result = terms_cor[0]
            result = [(score, idx) for idx, score in enumerate(result)]
            result = sorted(result, key=lambda x: x[0], reverse=True)
            result = [self.terms_lookup[x[1]] for x in result[1:9]]
            result = ["{0} {1}".format(query, x) for x in result]
        return result
