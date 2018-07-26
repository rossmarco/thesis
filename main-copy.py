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

# Define collection for set of words
word_set = []
global disease_type
global full_training_word_freq_filename
global full_training_bigram_filename
global full_training_trigram_filename
global full_training_quadgram_filename
global full_test_word_freq_filename
global full_test_bigram_filename
global full_test_trigram_filename
global full_test_quadgram_filename

disease_type = ''
full_training_word_freq_filename = ''
full_training_bigram_filename = ''
full_training_trigram_filename = ''
full_training_quadgram_filename = ''
full_test_word_freq_filename = ''
full_test_bigram_filename = ''
full_test_trigram_filename = ''
full_test_quadgram_filename = ''

def normalize_text(txt_file):
    # Import the text file we will work with
    with io.open(txt_file, 'r', encoding='utf-8', errors='ignore') as file:
        text = file.read() # .decode('utf-8').split()

    global disease_type
    disease_type = txt_file.replace('.txt', '')

    # Tokenize the text
    tokens = word_tokenize(text)
    tokenized_text = nltk.Text(tokens)

    # Load in Stopwords Library
    stopwords_list = stopwords.words('english')
    
    # Work through all the words in text and filter
    # Remove stop words, remove punctuation, numbers and non words
    for word in tokenized_text:
        # Check if word is a word, and not punctuation, AND check against stop words
        if word.isalpha() and word.lower() not in stopwords_list:
            # If it passes the filters, save to word_set
            word_set.append(word.lower())

    return word_set, disease_type

# Get the word frequency (unigram) of each word
def get_word_frequency(size):
    file_name = disease_type + '-word-freq-' + str(size)
    if 'training' in file_name:
        global full_training_word_freq_filename
        full_training_word_freq_filename = file_name+'.csv'
        file = csv.writer(open(full_training_word_freq_filename, 'w'))
    else:
        global full_test_word_freq_filename
        full_test_word_freq_filename = file_name+'.csv'
        file = csv.writer(open(full_test_word_freq_filename, 'w'))
    

    fd = FreqDist(word_set)
    #print fd.most_common(200)
    #print fd.hapaxes()
    #fd.plot(50,cumulative=False)

    # Print word counts to a CSV file
    for key, count in fd.most_common(size):
        file.writerow([key.encode('utf-8'), count]) #encode
    
    return full_training_word_freq_filename, full_test_word_freq_filename

# Get the bigrams of the words
def get_bigrams(size):

    file_name = disease_type + '-bigram-freq-' + str(size)
    if 'training' in file_name:
        global full_training_bigram_filename
        full_training_bigram_filename = file_name+'.csv'
        file_bigrams = csv.writer(open(full_training_bigram_filename, 'w'))
    else:
        global full_test_bigram_filename
        full_test_bigram_filename = file_name+'.csv'
        file_bigrams = csv.writer(open(full_test_bigram_filename, 'w'))

    # file_name = disease_type + '-bigram-freq-' + str(size)
    # full_bigram_filename = file_name+'.csv'
    # file_bigrams = csv.writer(open(full_bigram_filename, 'w'))

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
    
    return full_training_bigram_filename, full_test_bigram_filename


def get_trigrams(size):

    file_name = disease_type + '-trigram-freq-' + str(size)
    full_trigram_filename = file_name+'.csv'
    file_trigrams = csv.writer(open(full_trigram_filename, 'w'))

    finder = TrigramCollocationFinder.from_words(word_set)
    #scored = finder.score_ngrams(bigram_measures.raw_freq) 
    True

    sortedTriGrams = sorted(finder.ngram_fd.items(), key=lambda t: (-t[1], t[0]))[:size]  # doctest: +NORMALIZE_WHITESPACE

    # Store results of 400 bigrams into CSV file
    for trigram_tuple, count in sortedTriGrams:
        file_trigrams.writerow([type(trigram_tuple)(x.encode('utf-8') for x in trigram_tuple), count]) #formatted properly x.encode

    return full_trigram_filename

def get_quadgrams(size):

    file_name = disease_type + '-quadgram-freq-'  + str(size)
    full_quadgram_filename = file_name+'.csv'
    file_quadgrams = csv.writer(open(full_quadgram_filename, 'w'))

    finder = QuadgramCollocationFinder.from_words(word_set)
    True
    sortedQuadGrams = sorted(finder.ngram_fd.items(), key=lambda t: (-t[1], t[0]))[:size]  # doctest: +NORMALIZE_WHITESPACE

    # Store results of 400 bigrams into CSV file
    for quadgram_tuple, count in sortedQuadGrams:
        file_quadgrams.writerow([type(quadgram_tuple)(x.encode('utf-8') for x in quadgram_tuple), count]) #formatted properly #x.encode

    return full_quadgram_filename

# Code taken from stack overflow using CSV library in python
# https://stackoverflow.com/questions/5268929/compare-two-csv-files-and-search-for-similar-items
# Linear time solution
def compare_csv(training_data, test_data):

    num_of_matches = 0
    num_of_nonmatches = 0
    total_num_of_compares = 0
    similarity_metric = 0.0

    with open(training_data, 'rb') as master:
        master_indices = dict((r[0], i) for i, r in enumerate(csv.reader(master)))

    with open(test_data, 'rb') as test_file:
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
            writer.writerow([message2])
        

# Make function calls
normalize_text('cancer-training.txt')
get_word_frequency(800)
#get_bigrams(400)

del word_set[:]

normalize_text('cancer-71.txt')
get_word_frequency(50)
#get_bigrams(50)
compare_csv(full_training_word_freq_filename, full_test_word_freq_filename)
