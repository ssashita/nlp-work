from nltk.corpus import wordnet as wn
from nltk.corpus import brown
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
from nltk import untag
from collections import Counter

import os

ps = PorterStemmer()
def get_partial_features(sentence):
    pass
    
def createContextSenseSet(para):
    senseDict = dict()
    synsetsList=list()
    for sent in para:
        s=untag(sent)
        for w in s :
            if w in stopwords.words(fileids=['english']):
                continue
            ss=wn.synsets(w)
            synsetsList.extend(ss)
            synsetsList.extend(ss.hypernyms())
            synsetsList.extend(ss.hyponyms())
        get_partial_features(s)
            
    c=Counter(synsetsList)
    parasyn=max([(k,v) for k in c.keys() for v in c.values()], key = lambda a: a[1])
        
        


