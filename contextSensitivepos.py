import nltk.corpus as nc
import nltk
from nltk.corpus import brown
from nlpwork import pos_features

'''
Part of Speech Tagging using brown corpus
'''

def pos_features_with_context(sentence,i):
    ''' Get the features including the previous word for word i of sentence'''
    features = pos_features(sentence[i])
    if i >0:
        features["prev-word"] = sentence[i-1]
    else:
        features["prev-word"] = '<START>'
    return features
    
if __name__=="__main__":
    
    #Now get the tag labels in context of the sentences to which the words belong
    #this will be more accurate
    sentences = brown.sents(categories='news')[:5000]
    tagged_sentences = brown.tagged_sents(categories='news')[:5000]
    featureset = [(pos_features_with_context(sentences[i],j),tagged_sentences[i][j][1]) for i  in range(len(sentences))  for j  in range(len(sentences[i]))]
    #print featureset[:100]
    size = int(len(featureset)*0.1)
    testset,trainset = featureset[:size],featureset[size:]
    classifier = nltk.NaiveBayesClassifier.train(trainset)
    acc = nltk.classify.accuracy(classifier,testset)
    print 'Accuracy with context based tagging is ' , acc
    #classifier.classify()









