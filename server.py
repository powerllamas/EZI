# -*- coding: utf-8 -*-

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
    if 'search' in request.args:
        question = request.args['search']
        found = tfidf.search(question)[:5]
        return str(found)
    else:
        return render_template('home.html')

if __name__ == '__main__':
    app.run()
