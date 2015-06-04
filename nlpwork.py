import nltk.corpus as nc
import nltk
from nltk.corpus import brown
'''
Part of Speech Tagging using brown corpus
'''

def pos_features(word):
    features={}
    word = word.lower()
    features['endswith(%s)' % word[-1:]]=word.endswith(word[-1:])
    features['endswith(%s)' % word[-2:]]=word.endswith(word[-2:])
    features['endswith(%s)' % word[-3:]]=word.endswith(word[-3:])
    return features

def pos_features_with_context(sentence,i):
    ''' Get the features including the previous word for word i of sentence'''
    features = pos_features(sentence[i])
    if i >0:
        features["prev-word"] = sentence[i-1]
    else:
        features["prev-word"] = '<START>'
    return features
    
if __name__=="__main__":
  #Create a Frequency distribution of suffixes of 1,2 3 alphabets
#  suffix_fdist = nltk.FreqDist()
#  for word in brown.words():
#    word = word.lower()
#    suffix_fdist.inc(word[-1:])
#    suffix_fdist.inc(word[-2:])
#    suffix_fdist.inc(word[-3:])
#  common_suffixes = suffix_fdist.keys()[:100]
  #print common_suffixes
  #print suffix_fdist.items()[:100]
  
  tagged_words = brown.tagged_words(categories='news')
  featureset = [(pos_features(word), tag) for (word,tag) in tagged_words[:10000]]
  #print featureset
  size = int(len(featureset)*0.1)
  testset,trainset = featureset[:size], featureset[size:]
  classifier = nltk.DecisionTreeClassifier.train(trainset)
  acc = nltk.classify.accuracy(classifier,testset)

  print 'Accuracy of the POS tagginng without context is ', acc
  querylist = ['vehicle','dog','fructify', 'lose','loose','without','supposition','abandon','mollycoddle']
  resulttags = [ classifier.classify(pos_features(word)) for word in querylist]
  print [(querylist[i],resulttags[i]) for i in range(len(querylist)) ]
  for q in querylist:
      items = nltk.FreqDist(brown.tagged_words()).items()
      m = max([(a[1],a[0]) for a in items if a[0][0]==q])
      print q, m
  #Now get the tag labels in context of the sentences to which the words belong
  #this will be more accurate

  
  sentences = brown.sents(categories='news')[:10]
  tagged_sentences = brown.tagged_sents(categories='news')[:10]
  featureset = [(pos_features_with_context(sentences[i],j),tagged_sentences[i][j][1]) for i  in range(len(sentences))  for j  in range(len(sentences[i]))]
  