# -*- coding: utf-8 -*-

import os

from data import Loader
from word import Cleaner
from search import TFIDF
from guess import Guesses
import expander

from flask import Flask, render_template, request, jsonify

keywords_path = "data/keywords-2.txt"
stopwords_path = "data/stopwords.txt"
documents_path = "data/documents-2.txt"

keywords = Loader.load_keywords(keywords_path)
stopwords = Loader.load_stopwords(stopwords_path)
documents = Loader.load_documents(documents_path, categories=True)

cleaner = Cleaner(stopwords)
tfidf = TFIDF(keywords, documents, cleaner)
autocomplete = Guesses(tfidf.get_term_document_matrix(), tfidf.keywords, tfidf.keywords_lookup)

app = Flask(__name__)


@app.route('/')
def home():
    found_extended = None
    question = ""
    if 'search' in request.args:
        question = request.args['search']
        found = tfidf.search(question)
        found_extended = [(Cleaner.make_printable(title),
            similarity,
            Cleaner.make_printable(tfidf.documents[index][1]))
                for title, similarity, index in found]
    return render_template('home.html', found=found_extended, query=question)

@app.route('/guesses.json')
def guesses():
    guesses = None
    if 'search' in request.args:
        question = request.args['search']
        # guesses = [question]
        #guesses += autocomplete.guess(question)
        guesses = []
        guesses += expander.simillar(question)
    return jsonify(guesses=guesses)

@app.route('/clusters')
def clusters():
    clusters = tfidf.group_kmeans(9, 10)
    enhanced_clusters = [[documents[doc_id] for doc_id in cluster]
            for cluster in clusters]
    return render_template('clusters.html', clusters=enhanced_clusters)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.debug = True
    app.run(host='0.0.0.0', port=port)
