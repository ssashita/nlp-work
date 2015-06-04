Word sense disambiguation
1. Each synset of a word is at some similarity from others of other words around this word. Its like each synset for a word having some color. Of the several synsets (colors) for a word, you want to pick up the most suitable in a given context (defined by the set of other words around this word). You want to pick up the color that has the maximum instances (tolerating minor changes of shade) across all the words in the context around this word. 
  You can directly use the synset similarity function on nltk wordnet corpus. 
Or you can use gloss() and examples() for each synset using the same corpus and find the size of the intersection sets to get the most similar synsets between two words.
Better to use POS tags while getting the synsets for a word. This reduces the size of the candidate synsets of a word
 It is also probably good to get a sense of the entire document by tracking the hitherto most common or first few most common colors among swathes of sentences (may be a paragraph) probably in a first pass through the document, and including distances from these also for every word.

2. The semcor corpus is more useful. It gives pos tags, chunk tags and synset for a word in a several sentence corpus.  
Some knotty issues. If we keep the synset feature as a string (e.g."dog.nn.01"), will it have a good correlation or should some other measure of similarity be used - like the wordnet.path_similarity ? How do you specify this way oof calculating similarity or distance to a classifier or tagger ?
 Also, if we want to have a feature whose value is a set of strings. Such as if we want to have a bag of lemma_names of a word's synset (as found from semcor) as a feature, how do we specify a similarity/distance measure to the Classifier. But is this significant ? since synset is a label column ?

3. A simpler approach could be to estimate the pos tag of a word in the sentence and then use the Lesk algorithm passing the pos tag. How to improve this ? Use the synset info from the semcor corpus somehow. The most important features to use here are the word itself and its estimated pos tag and maybe some distance measure for the entire set of features, so that you can find the closest .
