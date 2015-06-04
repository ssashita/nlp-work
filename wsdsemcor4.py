from wsd import lesk
from wsdsemcor2 import WordSenseDisambiguator as WSD2
from nltk.corpus import semcor
import re
from nltk.corpus import wordnet as wn
#from nltk.stem import PorterStemmer
import nltk
import random

from nltk.tag import pos_tag
from nltk.tokenize import word_tokenize

from nltk.corpus import stopwords

from collections import Counter
import sys
from wsdpickler import pickleDataSet,wordnetpos
import pickle
import math

EPSILON=0.00001
class WordSenseDisambiguator:
    def __init__(self,wordaddressmapfile):
        global wsd2
        #f=open(corpusfilename,'rb')
        #ftagged = open(taggedcorpusfilename,'rb')
        #t=word_tokenize(f.read())
        #ttagged = word_tokenize(ftagged.read())
        #self.text = txt.Text(ttagged)
        #self.bigrams = set(nltk.bigrams(self.text))
        #self.trigrams = set(nltk.trigrams(self.text))
        wsd2 = WSD2(wordaddressmapfile)
        self.stopwords=stopwords.words('english')


    def wordsense(self,sentstring):
        sent = word_tokenize(sentstring)
        tagged_sent = pos_tag(sent)
        tagged_sent = [(w.lower(),_) for (w,_) in tagged_sent]
        synsetlist=[]
        #get a first estimate of senses from lesk algo
        print tagged_sent
        for i,(word,pos) in enumerate(tagged_sent):
            if word in self.stopwords:
                synset=word
            else:
                synset=lesk(sentstring, ambiguous_word=word,pos=wordnetpos(pos,decorator=''))
                if synset is None:
                    synset=word
                else:
                    synset = synset.name
            synsetlist.append(synset)
        #get the word index to synsets map for the input sentence
        best= wsd2.calculateSentenceScore(synsetlist)
        print synsetlist, best
        synsetmap=wsd2.createSynsetMap(sentstring)
        #print synsetmap
        #create a copy of the sentence comprising the lesk estimated senses
        testsent=[s for s in synsetlist]
        #Iterative procedure
        templist =[]
        synsetlistindices = range(len(synsetlist))
        random.shuffle(synsetlistindices)
        print synsetlistindices

        for j in synsetlistindices:
            word=testsent[j]
            synstbest = word
            if len(synsetmap[j])>1:
                for synst in synsetmap[j]:
                    testsent[j]=synst
                    sentscore = wsd2.calculateSentenceScore(testsent)

                    if (sentscore-best) > EPSILON:
                        best = sentscore
                        synstbest=synst
            testsent[j]=synstbest
            templist =[(testsent,best)] +templist 
        #t=word_tokenize(sentstring)
        #text=txt.Text(t)
        #fd=Freqdist(text)
        #bigrams=nltk.bigrams(t)
        #trigrams=nltk.trigrams()
        return templist
if __name__=='__main__':
    wsd = WordSenseDisambiguator('/home/sachin/pickledsemcordata.map')
    if len(sys.argv) > 1:
        data = sys.argv[1]
        data = data.strip()
        synsetsents = wsd.wordsense(data)
        if synsetsents is None:
            print 'Sorry - No success'
        else:
            print synsetsents[0]
        print ""
    else:
        while(True):
            print "Type sentence whose meaning is required."
            data = sys.stdin.readline()
            data = data.strip()
            if data == '.':
                print 'Bye'
                sys.exit(0)
            synsetsents = wsd.wordsense(data)
            if synsetsents is None:
                print 'Sorry - No success'
            else:
                print 'Solution:\
                '
                print synsetsents[0]
            print ""
                    