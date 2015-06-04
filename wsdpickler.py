from nltk.corpus import semcor
import re
from nltk.stem import PorterStemmer
import nltk

import sys
import pickle

def pickleDataSet(filestr):    
    try :
        file = open(filestr,'wb')
        filetext = open(filestr+'.txt','wb')
        filemap = open(filestr+'.map','wb')
        sents=semcor.tagged_sents(tag='both')
        ps = PorterStemmer()
        datalist=[]
        wordaddressmap = {}
        def addWordAddress(word, linenum):
            if word not in wordaddressmap:
                wordaddressmap[word]=set([])
            st = wordaddressmap[word]
            st.add(linenum)
        def getWordAdresses(word):
            if word in wordaddressmap:
                return wordaddressmap[word]
            return None
        for i,s in enumerate(sents):
            sentence,sentencedata=getFeaturesInSentence(s,ps,debugSentIndex=i)
            datalist.append(sentencedata)
            filetext.write(sentence+'\n')
            for word in nltk.word_tokenize(sentence):
                addWordAddress(word,i)
        pickle.dump(datalist,file)
        pickle.dump(wordaddressmap,filemap)
    except pickle.PicklingError, pe:
        print e
    except:
        print sys.exc_info()
    finally:
        file.close()
        filetext.close()
        filemap.close()
def trueSynSetStr(pos,synsetstr):
    result=None
    if synsetstr==None:
        return result
    try:
        [prefix,postfix]=synsetstr.split('.')
    except:
        return synsetstr
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
                
def getFeaturesInSentence(sent,ps,debugSentIndex=None):
    #print sent.num
    sentList=[]
    sentence=''
    ll = len(sent)
    for j,wordtree in enumerate(sent):
        try:
            word = wordtree.leaves()
            if not re.match('[A-Za-z0-9]+.*',word[0]):
                continue
            if wordtree.height() > 2:
                #This is the case where the synset is available
                #but there are exceptions
                synset = wordtree.node
                if synset.isupper():
                    synset=None
                wtree=wordtree
                for i in range(wordtree.height()-2):
                    wtree = wtree[0]
                pos=wtree.node
            else:
                synset = None
                pos = wordtree.node
            if synset != None:
                synset = trueSynSetStr(pos, synset)
            thisWordInfo=(ps.stem('_'.join(word)),pos,synset)
            sentList.append(thisWordInfo)
            if synset == None:
                sentence += thisWordInfo[0]+' '
            else:
                sentence += thisWordInfo[2] + ' '
        except:
            print sys.exc_info()[0]
            print 'ERROR in getFeaturesInSentence() sent[',debugSentIndex,'] word[',j,']: ', wordtree
            raise
    if len(sentence) >0: sentence += ' .'
    return sentence,sentList

if __name__=='__main__':
    filename=sys.argv[1]
    pickleDataSet(filename)
    