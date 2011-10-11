# -*- coding: utf-8 -*-

from collections import OrderedDict, defaultdict
from stemmer import PorterStemmer
import math
import sys
import argparse
import wx


def dot_product(vecA, vecB):
    product = 0
    # for a, b in vecA, vecB:
        # product += a * b
    for i in range(len(vecB)):
        product += vecA[i] * vecB[i]
    return product
    
def vec_length(vec):
    length = 0
    for el in vec:
        length += pow(el, 2)
    return math.sqrt(length)
    
        
def vec_similarity(vec1, vec2):
    length_product = vec_length(vec1) * vec_length(vec2)
    if length_product == 0:
        return 0
    else:
        return dot_product(vec1, vec2) / length_product

class TFIDF_Search(object):

    stemmer = PorterStemmer()    
    
    def __init__(self, stopwords_filepath, keywords_filepath, documents_filepath):
        self.keywords = OrderedDict()
        self.documents = defaultdict(list)
        self.stopwords = []
        self.bag_of_words = {}   
        self.documents_count = {}
        self.read_stopwords(stopwords_filepath)
        self.read_keywords(keywords_filepath)
        self.read_documents(documents_filepath)
        self.append_bag_of_words(self.documents)
        
    def clean_word(self, word):
        word = word.lower()
        word = filter(lambda c: c.isalnum(), word)
        if word in self.stopwords:
            return None
        else:
            return self.stemmer.stem(word, 0, len(word)-1)

    def clean_word_list(self, list):
        return [word for word in list if word]

    def read_stopwords(self, stopwords_filepath):
        self.stopwords = []
        with open(stopwords_filepath) as file:
            for line in file:
                self.stopwords.append(line.strip())
        self.stopwords = frozenset(self.stopwords)

    def read_keywords(self, keywords_filepath):
        self.keywords = OrderedDict()
        with open(keywords_filepath) as file:
            for line in file:
                word = line.strip()
                stemmed_word = self.clean_word(word)
                if stemmed_word is not None:
                    self.keywords[stemmed_word] = 0

    #for k in sorted(keywords):
    #    print k

    def read_documents(self, documents_filepath):
        self.documents = defaultdict(list)
        with open(documents_filepath) as file:
            current_doc = None
            for line in file:
                if current_doc is None:
                    current_doc = line.strip()
                words = line.split()
                if words:
                    self.documents[current_doc] += words
                else:
                    current_doc = None

        for k, doc in self.documents.iteritems():
            clean_words = map(self.clean_word, doc)
            self.documents[k] = self.clean_word_list(clean_words)
            
    def append_bag_of_words(self, documents):
        for keyword in self.keywords:
            self.documents_count.setdefault(keyword, 0)
            for k, doc in documents.iteritems():
                keyword_count = doc.count(keyword)
                self.bag_of_words.setdefault(k, {})[keyword] = keyword_count
                if keyword_count > 0:
                    self.documents_count[keyword] += 1
        
        
    def tf(self, document, term):
        n = self.bag_of_words[document][term]
        if n == 0:
            return 0
        else:
            return float(n) / max(self.bag_of_words[document].itervalues())
            
    def idf(self, term):
        if self.documents_count[term] == 0:
            return 0
        else:
            return math.log(len(self.documents) / self.documents_count[term])
        
    def tfidf(self, document):
        result_vector = []
        for term in sorted(self.keywords):
            result_vector.append(self.tf(document, term) * self.idf(term))
        return result_vector

    def similarity(self, doc1, doc2):
        #print "comparing documents: " + doc1 + " " + doc2
        return vec_similarity(self.tfidf(doc1), self.tfidf(doc2))
        
    def search(self, question):
        question_words = question.split()
        question_words_stemmed = []
        for word in question_words:
            word = word.strip()
            stemmed_word = self.clean_word(word)
            if (stemmed_word):    
                question_words_stemmed.append(stemmed_word)
        self.append_bag_of_words({"question" : question_words_stemmed})
        ranking = {}
        for title in self.documents.iterkeys():
            ranking[title] = self.similarity(title, "question")
        
        for title, sim in sorted(ranking.items(), key=(lambda t: t[1]), reverse=True):
            print "%4f\t%s" % (sim, title)


if __name__ == '__main__':

    # if len (sys.argv) == 1 or len(sys.argv) > 1 and (sys.argv[1] == "-g" or sys.argv[1] == "--gui"):
      # print "Entered GUI mode"
      # app = wx.App(False)
      # frame = MainWindow(None, "TF-IDF")
      # app.MainLoop()
      # sys.exit()
    
    parser = argparse.ArgumentParser(
      formatter_class=argparse.RawDescriptionHelpFormatter,
      description = "Simple TF-IDF implementation.",
      prog="enconv",
      epilog="Authors:\t\tKrzysztof Urban & Tomasz Ziêtkiewicz. 2011\nCopyright:\tThis is free software: you are free to change and redistribute it.\n\t\tThere is NO WARRANTY, to the extent permitted by law."
      )
    parser.add_argument('-k', '--keywords', help="Keywords file path", default="data/keywords.txt")
    parser.add_argument('-s', '--stopwords', help="Stopwords file path", default="data/stopwords.txt")
    parser.add_argument('-d', '--documents', help="Documents file path", default="data/documents.txt")
    parser.add_argument('-g', '--gui', help='GUI mode')
    parser.add_argument('-v', '--version', action='version', version='%(prog)s 0.1')
    args = parser.parse_args()

    searcher = TFIDF_Search(args.stopwords, args.keywords, args.documents)
    q = raw_input("Enter search string or \"exit()\" and press enter: ")
    while q != "exit()":
        searcher.search(q)
        q = raw_input("\nEnter search string or \"exit()\" and press enter: ")