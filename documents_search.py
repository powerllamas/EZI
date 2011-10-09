# -*- coding: utf-8 -*-

from collections import OrderedDict, defaultdict

from stemmer import PorterStemmer

stemmer = PorterStemmer()

def clean_word(word):
    word = word.lower()
    if word in stopwords:
        return None
    else:
        return stemmer.stem(word, 0, len(word)-1)

def clean_word_list(list):
    return [word for word in list if word is not None]

stopwords_filepath = "data/stopwords.txt"
keywords_filepath = "data/keywords.txt"
documents_filepath = "data/documents.txt"

stopwords = []
with open(stopwords_filepath) as file:
    for line in file:
        stopwords.append(line.strip())
stopwords = frozenset(stopwords)

keywords = OrderedDict()
with open(keywords_filepath) as file:
    for line in file:
        word = line.strip()
        stemmed_word = clean_word(word)
        if stemmed_word is not None:
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
    documents[k] = clean_word_list(clean_words)

for doc in documents.items():
    print doc
