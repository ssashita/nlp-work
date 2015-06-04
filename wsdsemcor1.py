from nltk.corpus import semcor
import re
from nltk.corpus import wordnet as wn
from nltk.stem import PorterStemmer
from nltk import KMeansClusterer
import nltk


from nltk.tag import pos_tag
from nltk.tokenize import word_tokenize

from nltk.corpus import stopwords

from collections import Counter
import sys
from wsdpickler import pickleDataSet,wordnetpos
import pickle

def calculateSimilarity(sent1,sent2):
    sent1bag = Counter(sent1)
    sent2bag = Counter(sent2)
    intersection = sent1bag & sent2bag
    score = 0.
    numSynsets=0
    for w in intersection:
        if re.search('[a-z0-9]+\..*\.[a-z0-9]+',w): #its a synset
            oldnumsynsets = numSynsets
            numSynsets += intersection[w]
            for n in range(oldnumsynsets,numSynsets):
                factor=2**n
                score += factor 
        else:
            score += 0.1
    return score

class WordTreeGenerator:
    
    def __init__(self,treeroot,synsetmap):
        self.synsetmap=synsetmap
        self.treeroot=treeroot
        self.sortedwordnumlist=synsetmap.keys()
        self.sortedwordnumlist.sort(key=lambda x: len(synsetmap[x]))

    def generateWordTree(self):
        tree=nltk.Tree(self.treeroot,[])
        #Define internal function 
        def generateWordTree_intnl(i,tree,branchwordlist=[]):
            words= self.synsetmap[self.sortedwordnumlist[i]]

            if i==len(self.synsetmap)-1:
                for j,w in enumerate(words):
                    branchwordlist.append(w)
                    tree.insert(len(tree),nltk.Tree('',list(branchwordlist)))
                    branchwordlist.pop()
            else:
                for j,w in enumerate(words):
                    branchwordlist.append(w)
                    generateWordTree_intnl(i+1,tree,branchwordlist)
                    branchwordlist.pop()
        #Call internal function
        generateWordTree_intnl(0,tree)
        return tree

if __name__=='__main__':

    tagged_sent = pos_tag (word_tokenize(sys.argv[1]))
    ps = PorterStemmer()
    stwrds=stopwords.words('english')
    synsetlist=[]
    synsetmap={}
    for i,(word,pos) in enumerate(tagged_sent):
        word = word.lower()
        if word in stwrds:
            wordstem=ps.stem(word)
            synsetlist.append(wordstem)
            synsetmap[i]=[wordstem]            
            continue
        postag= wordnetpos(pos,decorator='')
        if ( postag==''):
            postag = None
        syns = wn.synsets(word,postag)
        if len(syns) > 0:
            synsetmap[i]=[syn.name for syn in syns]
        else:
            synsetmap[i]=[ps.stem(word)]
    wordTreeGen = WordTreeGenerator('$ROOT',synsetmap)
    tree = wordTreeGen.generateWordTree()
    if len(tree) > 1:
        #read the stored sentence info
        f=open('/home/sachin/pickledsemcordata','rb')
        sents=pickle.load(f)
        synsetsents = [[wi[0] if wi[2]==None else wi[2] for wi in sent] for sent in sents]
        simMap={}
        for k,ctree in enumerate(tree):
            templist=[]
            best=0
            sent=ctree.leaves()
            for i,corpussent in enumerate(synsetsents):
                sim = calculateSimilarity(sent,corpussent)
                if best < sim:
                    best = sim
                    templist=[i] + templist
                elif best==sim:
                    templist=templist+[i]
            simMap[k]=(best,len(templist))
            print k,best,ctree.leaves()
        sorted(simMap, key=lambda x: x[1][0],reverse=True)
        for k in simMap.keys():
            print ' '.join(tree[k].leaves()), simMap[k]
        
