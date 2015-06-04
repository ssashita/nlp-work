import nltk.corpus as nc
import nltk
from nltk.corpus import brown
from nlpwork import pos_features

'''
Part of Speech Tagging using brown corpus
'''

def pos_features_seq_classification(sentence,i,history):
    ''' Get the features including the previous word for word i of sentence'''
    features = pos_features(sentence[i])
    if i >0:
        features["prev-word"] = sentence[i-1]
        features["prev-tag"] = history[i-1]
    else:
        features["prev-word"] = '<START>'
        features["prev-tag"] = '<START>'
    return features


class  ConsecutivePosTagger(nltk.TaggerI):
    def __init__(self, train_sents):
        train_set=[]
        for tagged_sent in train_sents:
            untagged_sent = nltk.tag.untag(tagged_sent)
            history=[]
            for i,(word,tag) in enumerate(tagged_sent):
                featureset = pos_features_seq_classification(untagged_sent, i, history)
                train_set.append((featureset, tag))
                history.append(tag)
            self.classifier = nltk.NaiveBayesClassifier.train(train_set)

    def tag(self, sentence):
        history = []
        for i, word in enumerate(sentence):
            featureset = pos_features_seq_classification(sentence, i, history)
            tag = self.classifier.classify(featureset)
            history.append(tag)
        return zip(sentence,history)
if __name__=="__main__":
    
    #Now get the tag labels in context of the sentences to which the words belong
    #this will be more accurate
    tagged_sentences = brown.tagged_sents(categories='news')[:5000]
    size = int(len(tagged_sentences)*0.1)
    trainset,testset = tagged_sentences[size:],tagged_sentences[:size]
    tagger = ConsecutivePosTagger(trainset)
    print tagger.evaluate(testset)










