# -*- coding: utf-8 -*-

import argparse

from data import Loader
from word import Cleaner
from search import TFIDF

# keywords_path = "data/keywords.txt"
# stopwords_path = "data/stopwords.txt"
# documents_path = "data/documents.txt"

# keywords = Loader.load_keywords(keywords_path)
# stopwords = Loader.load_stopwords(stopwords_path)
# documents = Loader.load_documents(documents_path)

# cleaner = Cleaner(stopwords)
# tfidf = TFIDF(keywords, documents, cleaner)
# found = tfidf.search("experience")

# for title, similarity in found[:5]:
#     print "{0:4f}\t{1}".format(similarity, title)

if __name__ == '__main__':

    parser = argparse.ArgumentParser(
      formatter_class=argparse.RawDescriptionHelpFormatter,
      description="Simple TF-IDF implementation.",
      prog="enconv",
      epilog=(u"Authors:\t\tKrzysztof Urban & Tomasz Ziętkiewicz. 2011\n"
          u"Copyright:\tThis is free software: you are free to change and "
          u"redistribute it.\n\t\tThere is NO WARRANTY, to the extent "
          u"permitted by law."))
    parser.add_argument('-k', '--keywords', help="Keywords file path",
            default="data/keywords-2.txt")
    parser.add_argument('-s', '--stopwords', help="Stopwords file path",
            default="data/stopwords.txt")
    parser.add_argument('-d', '--documents', help="Documents file path",
            default="data/documents-2.txt")
    parser.add_argument('-n', '--noresults',
            help="Number of displayed results", default="5")
    parser.add_argument('-v', '--version', action='version',
            version='%(prog)s 0.3')
    args = parser.parse_args()

    keywords = Loader.load_keywords(args.keywords)
    stopwords = Loader.load_stopwords(args.stopwords)
    documents = Loader.load_documents(args.documents)
    n = int(args.noresults)

    cleaner = Cleaner(stopwords)
    tfidf = TFIDF(keywords, documents, cleaner)

    question = raw_input("Enter search string or \"exit()\" and press enter: ")
    while question != "exit()":
            found = tfidf.search(question)           
            for title, similarity, index in found[:n]:
                print "{0:4f}\t{1}".format(similarity, title)
            groups = tfidf.group_kmeans(9, 10)
            for i, group in enumerate(groups):
                print "\nGroup {0}:\n".format(i)
                for doc_id in group:
                    print "\t{0}\n".format(documents[doc_id][0])
            question = raw_input("\nEnter search string or \"exit()\" and "
                    "press enter: ")
