from nltk.corpus import semcor
import re
from nltk.corpus import wordnet as wn
from nltk.stem import PorterStemmer
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

class WordSenseDisambiguator:
    def __init__(self,wordaddressmapfile):
        self.wordaddressmapfile=wordaddressmapfile
        self.stopwords=stopwords.words('english')
        self.ps = PorterStemmer()
        filename = self.wordaddressmapfile
        try:
            #read the stored sentence info
            f=open(filename,'rb')
            self.wordsentsmap=pickle.load(f)
        finally:
            f.close()

    def getsynsetsentences(self,sentence):
        ps = self.ps
        stwrds=self.stopwords
        wordsentsmap = self.wordsentsmap
        synsetlist=[]
        synsetmap={}
        tagged_sent = pos_tag (word_tokenize(sentence))
        for i,(word,pos) in enumerate(tagged_sent):
            word=word.lower()
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
            templist=[]
            best=0
            for k,ctree in enumerate(tree):
                sentscoremap={}
                sent=ctree.leaves()
                for word in sent:
                    def calculateSentScore(word,sentscoremap):
                        wordsentsmap = self.wordsentsmap
                        if self.wordcache
                        stwrds=self.stopwords
                        isstopword=word in stwrds
                        if word in wordsentsmap:
                            for s in wordsentsmap[word]:
                                if s not in sentscoremap:
                                    sentscoremap[s]=0.0
                                    if isstopword:
                                        score = 0.1
                                    else:
                                        score = 1.0
                                sentscoremap[s] += score
                snum=max(sentscoremap,key=sentscoremap.get)
                bestscore=sentscoremap[snum]
                if bestscore >= best:
                    best = bestscore
                    templist =[(k,bestscore)] +templist 
                #print 'best score for " ', ctree.leaves(),' " is ',bestscore
            print len(templist)
            for k,best  in templist:
                print ' '.join(tree[k]), best
            return [tree[k].leaves() for (k,_) in templist]
        return None
        
if __name__=='__main__':
    wsd = WordSenseDisambiguator('/home/sachin/pickledsemcordata.map')
    while(True):
        print "Type sentence whose meaning is required."
        data = sys.stdin.readline()
        data = data.strip()
        if data == '.':
            print 'Bye'
            sys.exit(0)
        synsetsents = wsd.getsynsetsentences(data)
        if synsetsents == None:
            print 'Sorry - No success'
        else:
            print synsetsents
        print ""
            