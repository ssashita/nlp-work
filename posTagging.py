from nltk.corpus import brown
import sys


if __name__ == '__main__':
    brownTaggedSents = brown.tagged_sents(categories='news')
    brownSents = brown.sents(categories='news')
    size = int(len(brownTaggedSents)*0.9)
    trainSents=brownTaggedSents[:size]
    testSents=brownTaggedSents[size:]

    t0=nltk.DefaultTagger('NN')
    t1=nltk.UnigramTagger(trainSents,backoff=t0)
    t2=nltk.BigramTagger(trainSents,backoff=t1)
    t2.evaluate(testSents)

    print t2.tag(sys.argv[1:])
