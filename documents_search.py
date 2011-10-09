# -*- coding: utf-8 -*-

from collections import OrderedDict

from stemmer import PorterStemmer

keywords_filepath = "data/keywords.txt"
documents_filepath = "data/documents.txt"

stemmer = PorterStemmer()

keywords = OrderedDict()
with open(keywords_filepath) as file:
    for line in file:
        word = line.strip()
        stemmed_word = stemmer.stem(word, 0, len(word)-1)
        keywords[stemmed_word] = 0

for k in sorted(keywords):
    print k

