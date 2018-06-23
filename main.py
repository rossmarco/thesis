import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.probability import FreqDist
from nltk.collocations import BigramAssocMeasures, TrigramAssocMeasures, BigramCollocationFinder, TrigramCollocationFinder
from nltk.collocations import ngrams
import csv

# Portions of this code taken from http://curriculum.dhbridge.org/modules/module13.html
# June 23, 2018
# Marco Ross
# Sheridan College - Bachelor of Applied Computer Science Undergraduate Thesis

#nltk.download('punkt')

# Import the text file we will work with
with open('filteredtext.txt', 'r') as file:
    text = file.read().decode('utf-8')

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
def get_word_frequency():
    file = csv.writer(open('word_frequencies.csv', 'w'))

    fd = FreqDist(word_set)
    #print fd.most_common(200)
    #print fd.hapaxes()
    #fd.plot(50,cumulative=False)

    # Print word counts to a CSV file
    for key, count in fd.most_common(200):
        file.writerow([key.encode('utf-8'), count])

# Get the bigrams of the words
def get_bigrams():

    file_bigrams = csv.writer(open('bigram_freq.csv', 'w'))

    # Define bigram and trigram measures
    #bigram_measures = nltk.collocations.BigramAssocMeasures()
    #trigram_measures = nltk.collocations.TrigramAssocMeasures()

    word_fd = nltk.FreqDist(word_set)
    bigram_fd = nltk.FreqDist(nltk.bigrams(word_set))
    finder = BigramCollocationFinder(word_fd, bigram_fd)
    #scored = finder.score_ngrams(bigram_measures.raw_freq) 
    True

    sortedBiGrams = sorted(finder.ngram_fd.items(), key=lambda t: (-t[1], t[0]))[:400]  # doctest: +NORMALIZE_WHITESPACE

    # Store results of 400 bigrams into CSV file
    for bigram_tuple, count in sortedBiGrams:
        #file_trigrams.writerow([list(bigram_tuple), count]) # in ugly unformatted unicode
        #file_trigrams.writerow(type(bigram_tuple)(x.encode('utf-8') for x in bigram_tuple)) #just words without count
        file_bigrams.writerow([type(bigram_tuple)(x.encode('utf8') for x in bigram_tuple), count]) #formatted properly

# Make function calls
normalize_text(tokenized_text)
get_word_frequency()
get_bigrams()

