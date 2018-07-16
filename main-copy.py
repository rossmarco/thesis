from __future__ import division
import nltk
import os
import io
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.probability import FreqDist
from nltk.collocations import BigramAssocMeasures, TrigramAssocMeasures, BigramCollocationFinder, TrigramCollocationFinder, QuadgramCollocationFinder
from nltk.collocations import ngrams
from collections import Counter
import csv


# Portions of this code taken from http://curriculum.dhbridge.org/modules/module13.html
# June 23, 2018
# Marco Ross
# Sheridan College - Bachelor of Applied Computer Science Undergraduate Thesis

#nltk.download('punkt')


# Import the text file we will work with
with io.open('cancer-training.txt', 'r', encoding='utf-8', errors='ignore') as file:
    text = file.read() # .decode('utf-8').split()

# Tokenize the text
tokens = word_tokenize(text)
tokenized_text = nltk.Text(tokens)

# Load in Stopwords Library
stopwords = stopwords.words('english')

# Define collection for set of words
word_set = []

# Remove stop words, remove punctuation, numbers and non words
def normalize_text(tokenized_text):
    # Work through all the words in text and filter
    for word in tokenized_text:
        # Check if word is a word, and not punctuation, AND check against stop words
        if word.isalpha() and word.lower() not in stopwords:
            # If it passes the filters, save to word_set
            word_set.append(word.lower())

    return word_set

# Get the word frequency (unigram) of each word
def get_word_frequency(size):
    file = csv.writer(open('word_frequencies.csv', 'w'))

    fd = FreqDist(word_set)
    #print fd.most_common(200)
    #print fd.hapaxes()
    #fd.plot(50,cumulative=False)

    # Print word counts to a CSV file
    for key, count in fd.most_common(size):
        file.writerow([key.encode('utf-8'), count]) #encode

# Get the bigrams of the words
def get_bigrams(size):


    file_name = 'bigram_freq' + str(size)
    file_bigrams = csv.writer(open(file_name+'.csv', 'w'))

    # Define bigram and trigram measures
    #bigram_measures = nltk.collocations.BigramAssocMeasures()
    #trigram_measures = nltk.collocations.TrigramAssocMeasures()

    word_fd = nltk.FreqDist(word_set)
    bigram_fd = nltk.FreqDist(nltk.bigrams(word_set))
    finder = BigramCollocationFinder(word_fd, bigram_fd)
    #scored = finder.score_ngrams(bigram_measures.raw_freq) 
    True

    sortedBiGrams = sorted(finder.ngram_fd.items(), key=lambda t: (-t[1], t[0]))[:size]  # doctest: +NORMALIZE_WHITESPACE

    # Store results of 400 bigrams into CSV file
    for bigram_tuple, count in sortedBiGrams:
        #file_bigrams.writerow([list(bigram_tuple), count]) # in ugly unformatted unicode
        #file_bigrams.writerow(type(bigram_tuple)(x.encode('utf-8') for x in bigram_tuple)) #just words without count
        file_bigrams.writerow([type(bigram_tuple)(x.encode('utf-8') for x in bigram_tuple), count]) #formatted properly #x.encode

def get_trigrams(size):

    file_trigrams = csv.writer(open('trigram_freq.csv', 'w'))

    finder = TrigramCollocationFinder.from_words(word_set)
    #scored = finder.score_ngrams(bigram_measures.raw_freq) 
    True

    sortedTriGrams = sorted(finder.ngram_fd.items(), key=lambda t: (-t[1], t[0]))[:size]  # doctest: +NORMALIZE_WHITESPACE

    # Store results of 400 bigrams into CSV file
    for trigram_tuple, count in sortedTriGrams:
        file_trigrams.writerow([type(trigram_tuple)(x.encode('utf-8') for x in trigram_tuple), count]) #formatted properly x.encode

def get_quadgrams(size):

    file_quadgrams = csv.writer(open('quadgram_freq.csv', 'w'))

    finder = QuadgramCollocationFinder.from_words(word_set)
    True
    sortedQuadGrams = sorted(finder.ngram_fd.items(), key=lambda t: (-t[1], t[0]))[:size]  # doctest: +NORMALIZE_WHITESPACE

    # Store results of 400 bigrams into CSV file
    for quadgram_tuple, count in sortedQuadGrams:
        file_quadgrams.writerow([type(quadgram_tuple)(x.encode('utf-8') for x in quadgram_tuple), count]) #formatted properly #x.encode

def compare_csv(test_data_file):

    num_of_matches = 0
    num_of_nonmatches = 0
    total_num_of_compares = 0
    similarity_metric = 0.0

    with open(test_data_file, 'rb') as master:
        master_indices = dict((r[0], i) for i, r in enumerate(csv.reader(master)))

    with open('bigram_freq2.csv', 'rb') as test_file:
        with open('results.csv', 'wb') as results:    
            reader = csv.reader(test_file)
            writer = csv.writer(results)

            for row in reader:
                index = master_indices.get(row[0])
                if index is not None:
                    message = 'FOUND in master list (row {})'.format(index)
                    num_of_matches += 1
                    
                else:
                    message = 'NOT FOUND in master list'
                writer.writerow(row + [message])
                num_of_nonmatches += 1

            total_num_of_compares = (num_of_matches + num_of_nonmatches)
            similarity_metric = ((num_of_matches/total_num_of_compares) * 100)
            message2 = 'The similarity metric is {0:.2f}'.format(similarity_metric)
            writer.writerow((row + [message2]))
        

# Make function calls
""" normalize_text(tokenized_text)
get_word_frequency(25)
get_bigrams(25)
get_bigrams(50)
get_bigrams(75)
get_bigrams(100)
get_trigrams(25)
get_quadgrams(25) """
compare_csv('bigram_freq25.csv')
