"""from nltk import ngrams
from nltk.collocations import *

f = open('a_text_file')
raw = f.read()

tokens = nltk.word_tokenize(raw)

#Create your bigrams
bgs = nltk.bigrams(tokens)

#compute frequency distribution for all the bigrams in the text
fdist = nltk.FreqDist(bgs)
for k,v in fdist.items():
    print k,v """

""" from nltk import word_tokenize
from nltk.collocations import BigramCollocationFinder
text = "obama says that obama says that the war is happening"
finder = BigramCollocationFinder.from_words(word_tokenize(text))
finder.items()[0:5]
 """

import nltk
from nltk.collocations import *
from nltk.corpus import PlaintextCorpusReader

f = open('diet-cancer.txt')

raw = f.read()
#print((f.read))
bigram_measures = nltk.collocations.BigramAssocMeasures()
trigram_measures = nltk.collocations.TrigramAssocMeasures()

text = raw
tokens = nltk.wordpunct_tokenize(text)
finder = TrigramCollocationFinder.from_words(tokens)
scored = finder.score_ngrams(trigram_measures.raw_freq)
sorted(trigram for trigram, score in scored)  # doctest: +NORMALIZE_WHITESPACE

# list of words to filter: 
# journal words:'et' 'al' 
# punctuation: '.' ',' ';' '!' '?' '@'
# conjunctions: 'and' 'the' 'but' 'for' 'or' 'when' 'if' 

print sorted(finder.ngram_fd.items(), key=lambda t: (-t[1], t[0]))[:10]  # doctest: +NORMALIZE_WHITESPACE

""" f = open('freqDist.txt', 'w')
f.write()
f.close() """