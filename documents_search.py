# -*- coding: utf-8 -*-

from collections import OrderedDict, defaultdict

from stemmer import PorterStemmer

stemmer = PorterStemmer()

def clean_word(word):
    word = word.lower()
    return stemmer.stem(word, 0, len(word)-1)

keywords_filepath = "data/keywords.txt"
documents_filepath = "data/documents.txt"

keywords = OrderedDict()
with open(keywords_filepath) as file:
    for line in file:
        word = line.strip()
        stemmed_word = clean_word(word)
        keywords[stemmed_word] = 0

for k in sorted(keywords):
    print k

documents = defaultdict(list)
with open(documents_filepath) as file:
    current_doc = 0
    for line in file:
        words = line.split()
        if words:
            documents[current_doc] += words
        else:
            current_doc += 1

for k, doc in documents.iteritems():
    clean_words = map(clean_word, doc)
    documents[k] = clean_words

for doc in documents.items():
    print doc
