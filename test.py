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
import subprocess
import sys
from os import listdir
from os.path import isfile, join
import os.path
import re


# TO DO: document this code
class TextAnalyzer:

    def __init__(self, disease_type):
        self.word_set = []
        #not being used for anything at the moment but will in the future
        self.disease_type = disease_type
        #self.txt_file = txt_file
        self.full_training_word_freq_filename = ''
        self.full_training_bigram_filename = ''
        self.full_training_trigram_filename = ''
        self.full_training_quadgram_filename = ''
        self.full_test_word_freq_filename = ''
        self.full_test_bigram_filename = ''
        self.full_test_trigram_filename = ''
        self.full_test_quadgram_filename = ''
        self.test_file_name = ''
        self.smetric_diabetes = 0.0
        self.smetric_cancer = 0.0
        self.smetric_cvd = 0.0


    def normalize_text(self, txt_file):
        # Import the text file we will work with
        with io.open(txt_file, 'r', encoding='utf-8', errors='ignore') as file:
            text = file.read() # .decode('utf-8').split()

        #change this once it works
        self.disease_type = txt_file.replace('.txt', '')

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

        return self.word_set, self.disease_type

    def get_word_frequency(self, size):
        file_name = self.disease_type + '-word-freq-' + str(size)
        if 'training' in file_name:
            full_training_word_freq_filename = file_name+'.csv'
            file = csv.writer(open(full_training_word_freq_filename, 'w'))
        else:
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

        file_name = self.disease_type + '-bigram-freq-' + str(size)
        if 'training' in file_name:
            full_training_bigram_filename = file_name+'.csv'
            file_bigrams = csv.writer(open(full_training_bigram_filename, 'w'))
        else:
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

        file_name = self.disease_type + '-trigram-freq-' + str(size)
        if 'training' in file_name:
            full_training_trigram_filename = file_name+'.csv'
            file_trigrams = csv.writer(open(full_training_trigram_filename, 'w'))
        else:
            self.full_test_trigram_filename = file_name+'.csv'
            file_trigrams = csv.writer(open(self.full_test_trigram_filename, 'w'))

        finder = TrigramCollocationFinder.from_words(self.word_set)
        #scored = finder.score_ngrams(bigram_measures.raw_freq) 
        True

        sortedTriGrams = sorted(finder.ngram_fd.items(), key=lambda t: (-t[1], t[0]))[:size]  # doctest: +NORMALIZE_WHITESPACE

        # Store results of 400 bigrams into CSV file
        for trigram_tuple, count in sortedTriGrams:
            file_trigrams.writerow([type(trigram_tuple)(x.encode('utf-8') for x in trigram_tuple), count]) #formatted properly x.encode

        return self.full_training_trigram_filename, self.full_test_trigram_filename

    def get_quadgrams(self, size):

        file_name = self.disease_type + '-quadgram-freq-' + str(size)
        if 'training' in file_name:
            full_training_quadgram_filename = file_name+'.csv'
            file_quadgrams = csv.writer(open(full_training_quadgram_filename, 'w'))
        else:
            full_test_quadgram_filename = file_name+'.csv'
            file_quadgrams = csv.writer(open(full_test_quadgram_filename, 'w'))

        finder = QuadgramCollocationFinder.from_words(self.word_set)
        True
        sortedQuadGrams = sorted(finder.ngram_fd.items(), key=lambda t: (-t[1], t[0]))[:size]  # doctest: +NORMALIZE_WHITESPACE

        # Store results of 400 bigrams into CSV file
        for quadgram_tuple, count in sortedQuadGrams:
            file_quadgrams.writerow([type(quadgram_tuple)(x.encode('utf-8') for x in quadgram_tuple), count]) #formatted properly #x.encode

        return self.full_training_quadgram_filename, self.full_test_quadgram_filename

    def compare_csv(self, training_data, test_data, disease_type):

        num_of_matches = 0
        num_of_nonmatches = 0
        total_num_of_compares = 0
        similarity_metric = 0.0

        with open(training_data, 'rb') as master:
            master_indices = dict((r[0], i) for i, r in enumerate(csv.reader(master)))

        stripped_file_name = str(test_data).replace('.csv', '')
        with open(test_data, 'rb') as test_file:
            file_name_results = 'results-'+stripped_file_name+'.csv'
            with open(file_name_results, 'wb') as results:    
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

                if disease_type == 'cancer':
                    self.smetric_cancer = similarity_metric
                elif disease_type == 'cvd':
                    self.smetric_cvd = similarity_metric
                elif disease_type == 'diabetes':
                    self.smetric_diabetes = similarity_metric
                
                message2 = 'The similarity metric is {0:.2f}'.format(similarity_metric)
                writer.writerow([message2])
        
        return self.smetric_cancer, self.smetric_cvd, self.smetric_diabetes

    def determine_best_match(self, smetric_cancer, smetric_diabetes, smetric_cvd, test_article_name, disease, ngram_size):

        # calculate accuracy
        correct_matches = 0
        incorrect_matches = 0
        accuracy = 0.0
        
        test_article_file_name = ''

        if ngram_size == 1:
            test_article_file_name = self.full_test_word_freq_filename
        elif ngram_size == 2:
            test_article_file_name = self.full_test_bigram_filename
        elif ngram_size == 3:
            test_article_file_name = self.full_test_trigram_filename
        elif ngram_size == 4:
            test_article_file_name = self.full_test_quadgram_filename
        else:
            raise ValueError("Please only choose an n-gram size between 1-4, inclusive")

        match_file_name = 'best_matches.csv'
        # if directory already contains CSV file, append to it rather than create a new one
        #TODO make this file name modular
        matches_file = "/Users/marcoross/Documents/summer2018_thesis/best_matches.csv"
        if os.path.exists(matches_file):
            f = open (match_file_name, 'w')
            matches_writer = csv.writer(f)

        else:
            f = open(match_file_name, 'a')
            matches_writer = csv.writer(f)

        if (self.smetric_cancer > self.smetric_diabetes) and (self.smetric_cancer > self.smetric_cvd):
            matches_writer.writerow(['The article ' + test_article_name + ' is a cancer article with a similary metric of {0:.2f}'.format(smetric_cancer)])
        elif (self.smetric_diabetes > self.smetric_cancer) and (self.smetric_diabetes > self.smetric_cvd):
            matches_writer.writerow(['The article ' + test_article_name + ' is a diabetes article with a similary metric of {0:.2f}'.format(smetric_diabetes)])
        elif (self.smetric_cvd > self.smetric_cancer) and (self.smetric_cvd > self.smetric_diabetes):
            matches_writer.writerow(['The article ' + test_article_name + ' is a CVD article with a similary metric of {0:.2f}'.format(smetric_cvd)])

        f.close()
        
        #final_calulation = 


def run_testing_data(disease, test_directory):

    os.chdir('/Users/marcoross/Documents/summer2018_thesis/cancer')

    # cancer_training = TextAnalyzer('cancer')
    # cancer_training.normalize_text('cancer-training.txt')
    # cancer_training.get_trigrams(200)

    # diabetes_training = TextAnalyzer('diabetes')
    # diabetes_training.normalize_text('diabetes-training.txt')
    # diabetes_training.get_trigrams(200)

    # cvd_training = TextAnalyzer('cvd')
    # cvd_training.normalize_text('cvd-training.txt')
    # cvd_training.get_trigrams(200)

    test_directory = '/Users/marcoross/Documents/summer2018_thesis/cancer'
    files = [f for f in listdir(test_directory) if isfile and (f != '.DS_Store') and ('training' not in f)]

    for f in files:
       test_article = TextAnalyzer(disease)
       test_article.normalize_text(f)
       test_article.get_trigrams(200)

    test_files = [t for t in listdir(test_directory) if (t != '.DS_Store') and (".csv" in t) and ("training" not in t)]
    
    for t in test_files:
        test_article.compare_csv('cancer-training-trigram-freq-200.csv', t, 'cancer')
        test_article.compare_csv('diabetes-training-trigram-freq-200.csv', t, 'diabetes')
        test_article.compare_csv('cvd-training-trigram-freq-200.csv', t, 'cvd')
        test_article.determine_best_match(test_article.smetric_cancer, test_article.smetric_diabetes, test_article.smetric_cvd, str(t), disease, 3)

run_testing_data('cancer','/Users/marcoross/Documents/summer2018_thesis/cancer')