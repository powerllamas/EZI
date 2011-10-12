# -*- coding: utf-8 -*-

import os

from data import Loader
from word import Cleaner
from search import TFIDF

from flask import Flask, render_template, request

keywords_path = "data/keywords.txt"
stopwords_path = "data/stopwords.txt"
documents_path = "data/documents.txt"

keywords = Loader.load_keywords(keywords_path)
stopwords = Loader.load_stopwords(stopwords_path)
documents = Loader.load_documents(documents_path)

cleaner = Cleaner(stopwords)
tfidf = TFIDF(keywords, documents, cleaner)

app = Flask(__name__)

@app.route('/')
def home():
    found = None
    question = ""
    if 'search' in request.args:
        question = request.args['search']
        found = tfidf.search(question)
    return render_template('home.html', found=found, query=question)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)