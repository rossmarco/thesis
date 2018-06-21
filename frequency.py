import nltk
import json
from nltk.collocations import *
from nltk.corpus import PlaintextCorpusReader
from nltk import word_tokenize
from nltk.probability import *
import csv

f = open('filteredtext.txt')

raw = f.read()

bigram_measures = nltk.collocations.BigramAssocMeasures()
trigram_measures = nltk.collocations.TrigramAssocMeasures()

text = raw.lower()
tokens = nltk.wordpunct_tokenize(text)
finder = TrigramCollocationFinder.from_words(tokens)
#filter words and punctuation
finder.apply_word_filter(lambda w: not w.isalpha())
finder.apply_word_filter(lambda w: w in ('university', 'ottawa', 'natl', 'rights', 'reserved', 'user', 'american', 'association', 'national', 'new england', 'journal', 'research', 'epidemiol', 'engl', 'j', 'n', 'massachusetts', 'personal', 'use', 'for', 'permission', 'modelc', 'modeld', 's', 'study', 'uses', 'nejm', 'downloaded', 'accessed', 'x', 'p', 'e', 'r', 'published', 'england', 'new', 'january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'semptember', 'october', 'november', 'december'))
    
scored = finder.score_ngrams(trigram_measures.raw_freq)
sorted(trigram for trigram, score in scored)  # doctest: +NORMALIZE_WHITESPACE

sortedstuff = sorted(finder.ngram_fd.items(), key=lambda t: (-t[1], t[0]))[:10]  # doctest: +NORMALIZE_WHITESPACE

#print(sortedstuff)
""" data = json.dumps(sortedstuff)

print(json.loads(data)
loadedstuff = json.loads(json_data)
for x in loaded_json:
	print("%s: %d" % (x, loaded_json[x])) """
