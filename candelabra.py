# -*- coding: utf-8 -*-

from data import Loader
from word import Cleaner
from search import TFIDF

keywords_path = "data/keywords.txt"
stopwords_path = "data/stopwords.txt"
documents_path = "data/documents.txt"

keywords = Loader.load_keywords(keywords_path)
stopwords = Loader.load_stopwords(stopwords_path)
documents = Loader.load_documents(documents_path)

cleaner = Cleaner(stopwords)
tfidf = TFIDF(keywords, documents, cleaner)
tfidf.search("experience")
