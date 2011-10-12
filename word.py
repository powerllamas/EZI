# -*- coding: utf-8 -*-

import string

from stemmer import PorterStemmer

class Cleaner(object):

    def __init__(self, stopwords):
        self.stopwords = stopwords
        self.stemmer = PorterStemmer()

    def clean_word(self, word):
        word = word.strip().lower()
        word = filter(lambda c: c.isalnum(), word)
        if word in self.stopwords:
            word = None
        else:
            word = self.stemmer.stem(word, 0, len(word)-1)
        return word

    def clean_wordlist(self, wordlist):
        clean_list = map(lambda x: self.clean_word(x), wordlist)
        return [word for word in clean_list if word]

    @staticmethod
    def make_printable(phrase):
        return filter(lambda c: c in string.printable, phrase)

