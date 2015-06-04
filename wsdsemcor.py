from nltk.corpus import semcor
import re
from nltk.corpus import wordnet as wn
from nltk.stem import PorterStemmer
from nltk import KMeansClusterer
import nltk

from nltk.tag import pos_tag
from nltk.tokenize import word_tokenize

from nltk.corpus import stopwords

import sys
        
def calculateDistance(vector1,vector2):
    selfWeight = 0.4
    preWeight = 0.30
    postWeight=0.3
    wordWeight = 0.3
    posWeight = 0.3
    synsetWeight =0.4
    def wordSameScore (w1,w2):
        return float(w1==w2)*wordWeight
    def posSameScore ( p1,p2):
        return float(p1 != 'None' and p2 != 'None' and p1[0]==p2[0])* posWeight
    def synsetSameScore(s1,s2):
        if s1 != 'None' and s2 != 'None':
            return wn.synset(s1).path_similarity(wn.synset(s2))
        return 0.
    simi=0.0
    try :
        simi = selfWeight * wordSameScore(vector1["word"],vector2["word"])  +\
        preWeight * wordSameScore(vector1["preword"], vector2["preword"]) +\
        postWeight * wordSameScore(vector1["postword"],vector2["postword"]) +\
        selfWeight * posSameScore(vector1["pos"],vector2["pos"])  +\
        preWeight * posSameScore(vector1["prepos"], vector2["prepos"]) +\
        postWeight * posSameScore(vector1["postpos"],vector2["postpos"]) +\
        selfWeight * synsetSameScore(vector1["synset"],vector2["synset"])  +\
        preWeight * synsetSameScore(vector1["presynset"], vector2["presynset"]) +\
        postWeight * synsetSameScore(vector1["postsynset"],vector2["postsynset"])
    finally:
        return (1. - simi)/(1. + simi)

    
def trueSynSetStr(pos,synsetstr):
    result='None'
    if synsetstr=='None':
        return result
    [prefix,postfix]=synsetstr.split('.')
    return prefix+wordnetpos(pos)+postfix
    
def wordnetpos(pos,decorator='.'):
    result=''
    if (pos.startswith('N') and not pos[1:].startswith('o')):
        result='n'
    elif (pos.startswith('J')):
        result='a'
    elif (pos.startswith('R')):
        result='r'
    elif (pos.startswith('V')):
        result='v'
    return decorator+result+decorator
        
def prepareDataSet():
    sents=[[re.split('\(',str(c)) for c in s] for s in semcor.tagged_sents(tag='both')[:10]]
    ps = PorterStemmer()
    siz = int(len(sents)*0.9)
    trainList=[]
    testList=[]
    for s in sents[:siz]:
        trainList.extend(getFeaturesInSentence(s,ps))
    for s in sents[siz:]:
        testList.extend(getFeaturesInSentence(s,ps))
    train_set = nltk.classify.util.apply_features(extract_features, trainList,labeled=False)
    test_set = nltk.classify.util.apply_features(extract_features, testList,labeled=False)
    return train_set, test_set
        
def extract_features(info):
    features={}
    features['word']=info[0][0]
    features['pos']=info[0][1]
    features['synset']=info[0][2]
    features['preword']=info[1][0]
    features['prepos']=info[1][1]
    features['presynset']=info[1][2]
    features['postword']=info[2][0]
    features['postpos']=info[2][1]
    features['postsynset']=info[2][2]

    return features
        
def getFeaturesInSentence(sent,ps):
    sentList=[]
    ll = len(sent)
    pre=('.','None','None')
    post=('.','None','None')
    stops=stopwords.words('english')
    for i,wordinfo in enumerate(sent):
        if len(wordinfo) > 2:
            #This is the case where the synset is available
            synsetstr = wordinfo[1]
        else:
            synsetstr = 'None'
        wordwithpos=wordinfo[-1].split()
        pos = wordwithpos[0]
        word = wordwithpos[1:-1]
        word.extend(re.split('\)*', wordwithpos[-1]))
        word=' '.join(word)
        if (word.strip() in stops) or (not any([c.isalnum() for c in word])):
            continue
        posStripped=pos.strip()
        strippedSynset = synsetstr.strip()
        if strippedSynset != 'None':
            strippedSynset = trueSynSetStr(posStripped, strippedSynset)
        thisWordInfo=(ps.stem(word.strip()),posStripped,strippedSynset)
        prev = len(sentList)-1
        if prev >= 0:
            pre=sentList[prev][0]
            sentList[prev][2]=thisWordInfo
        sentList.append([thisWordInfo,pre,post])
    return sentList

def synsetIsNone(wordtuple):
    return wordtuple[2]=='None'

def posIsNone(wordtuple):
    return wordtuple[1] == 'None'

if __name__=='__main__':
    trainSet,testSet = prepareDataSet()
    #clusterer = KMeansClusterer(num_means= 10, distance=calculateDistance)
    #clusterer.cluster(trainSet)
    tagged_sent = pos_tag (word_tokenize(argv[1]))
    ps = PorterStemmer()
    for word,pos in tagged_sent:
        stwrds=ps.stopwords('english')
        if word in stwrds:
            continue
        postag= wordnetpos(pos,decorator='')
        if ( postag==''):
            postag = None
        syns = wn.synsets(word,postag)
        