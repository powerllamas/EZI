from nltk.corpus import wordnet as wn
import string

def simillar(question):
    synsets = wn.synsets(question)
    results = []
    lemmas = []
    for synset in synsets:
        lemmas += synset.lemmas
        for hyponym in synset.hyponyms():
            lemmas += hyponym.lemmas
        for hypernym in synset.hypernyms():
            lemmas += hypernym.lemmas
            #for sybling in hypernym.hyponyms():
            #    lemmas += sybling.lemmas
    
    results = [string.replace(lema.name, '_', ' ') for lema in sorted(lemmas, key = wn.lemma_count, reverse=True)]
    results = set(results)
    
    return results