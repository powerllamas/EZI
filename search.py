# -*- coding: utf-8 -*-

class TFIDF_Search(object):

    def __init__(self, keywords, documents, cleaner):
        self.cleaner = cleaner

        self._setup_keywords(keywords)
        self._setup_documents(documents)

        self.bag_of_words = {}   
        self.documents_count = {}
        self.append_bag_of_words(self.documents)
        
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
        return Vector(result_vector)

    def similarity(self, doc1, doc2):
        return self.tfidf(doc1).similarity(self.tfidf(doc2))
        
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
