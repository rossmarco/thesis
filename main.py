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

#Github first commit test
#not working lets try the command line commit
class TextAnalyzer:

    def __init__(self, disease):
        self.word_set = []
        self.disease = disease
        #self.txt_file = txt_file
        self.full_training_word_freq_filename = ''
        self.full_training_bigram_filename = ''
        self.full_training_trigram_filename = ''
        self.full_training_quadgram_filename = ''
        self.full_test_word_freq_filename = ''
        self.full_test_bigram_filename = ''
        self.full_test_trigram_filename = ''
        self.full_test_quadgram_filename = ''

    def normalize_text(self, txt_file):
        # Import the text file we will work with
        with io.open(txt_file, 'r', encoding='utf-8', errors='ignore') as file:
            text = file.read() # .decode('utf-8').split()

        #change this once it works
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
                self.word_set.append(word.lower())

        return self.word_set, disease_type

    def get_word_frequency(self, size):
        file_name = disease_type + '-word-freq-' + str(size)
        if 'training' in file_name:
            global full_training_word_freq_filename
            full_training_word_freq_filename = file_name+'.csv'
            file = csv.writer(open(full_training_word_freq_filename, 'w'))
        else:
            global full_test_word_freq_filename
            full_test_word_freq_filename = file_name+'.csv'
            file = csv.writer(open(full_test_word_freq_filename, 'w'))
        

        fd = FreqDist(self.word_set)
        #print fd.most_common(200)
        #print fd.hapaxes()
        #fd.plot(50,cumulative=False)

        # Print word counts to a CSV file
        for key, count in fd.most_common(size):
            file.writerow([key.encode('utf-8'), count]) #encode
        
        return self.full_training_word_freq_filename, self.full_test_word_freq_filename

    def get_bigrams(self, size):

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

        word_fd = nltk.FreqDist(self.word_set)
        bigram_fd = nltk.FreqDist(nltk.bigrams(self.word_set))
        finder = BigramCollocationFinder(word_fd, bigram_fd)
        #scored = finder.score_ngrams(bigram_measures.raw_freq) 
        True

        sortedBiGrams = sorted(finder.ngram_fd.items(), key=lambda t: (-t[1], t[0]))[:size]  # doctest: +NORMALIZE_WHITESPACE

        # Store results of 400 bigrams into CSV file
        for bigram_tuple, count in sortedBiGrams:
            #file_bigrams.writerow([list(bigram_tuple), count]) # in ugly unformatted unicode
            #file_bigrams.writerow(type(bigram_tuple)(x.encode('utf-8') for x in bigram_tuple)) #just words without count
            file_bigrams.writerow([type(bigram_tuple)(x.encode('utf-8') for x in bigram_tuple), count]) #formatted properly #x.encode
        
        return self.full_training_bigram_filename, self.full_test_bigram_filename

    def get_trigrams(self, size):

        file_name = disease_type + '-trigram-freq-' + str(size)
        if 'training' in file_name:
            global full_training_trigram_filename
            full_training_trigram_filename = file_name+'.csv'
            file_trigrams = csv.writer(open(full_training_trigram_filename, 'w'))
        else:
            global full_test_trigram_filename
            full_test_trigram_filename = file_name+'.csv'
            file_trigrams = csv.writer(open(full_test_trigram_filename, 'w'))

        finder = TrigramCollocationFinder.from_words(self.word_set)
        #scored = finder.score_ngrams(bigram_measures.raw_freq) 
        True

        sortedTriGrams = sorted(finder.ngram_fd.items(), key=lambda t: (-t[1], t[0]))[:size]  # doctest: +NORMALIZE_WHITESPACE

        # Store results of 400 bigrams into CSV file
        for trigram_tuple, count in sortedTriGrams:
            file_trigrams.writerow([type(trigram_tuple)(x.encode('utf-8') for x in trigram_tuple), count]) #formatted properly x.encode

        return self.full_training_trigram_filename, self.full_test_trigram_filename

    def get_quadgrams(self, size):

        file_name = disease_type + '-quadgram-freq-' + str(size)
        if 'training' in file_name:
            global full_training_quadgram_filename
            full_training_quadgram_filename = file_name+'.csv'
            file_quadgrams = csv.writer(open(full_training_quadgram_filename, 'w'))
        else:
            global full_test_quadgram_filename
            full_test_quadgram_filename = file_name+'.csv'
            file_quadgrams = csv.writer(open(full_test_quadgram_filename, 'w'))

        finder = QuadgramCollocationFinder.from_words(self.word_set)
        True
        sortedQuadGrams = sorted(finder.ngram_fd.items(), key=lambda t: (-t[1], t[0]))[:size]  # doctest: +NORMALIZE_WHITESPACE

        # Store results of 400 bigrams into CSV file
        for quadgram_tuple, count in sortedQuadGrams:
            file_quadgrams.writerow([type(quadgram_tuple)(x.encode('utf-8') for x in quadgram_tuple), count]) #formatted properly #x.encode

        return self.full_training_trigram_filename, self.full_test_trigram_filename


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

x = TextAnalyzer('cancer')
x.normalize_text('cancer-training.txt')
x.get_word_frequency(25)

y = TextAnalyzer('cancer')
y.normalize_text('cancer-71.txt')
y.get_word_frequency(25)

compare_csv(full_training_word_freq_filename, full_test_word_freq_filename)