import nltk
from nltk.corpus import stopwords
from nltk import word_tokenize
from nltk.probability import *
import csv

# Code taken from http://curriculum.dhbridge.org/modules/module13.html
nltk.download('punkt')

# Set Variables
with open('filteredtext.txt', 'r') as file:
    cancer_text = file.read().decode('utf8')

file = csv.writer(open('word_frequencies.csv', 'w'))

cancer_tokens = word_tokenize(cancer_text)
text = nltk.Text(cancer_tokens)

# Load in Stopwords Library
stopwords = stopwords.words('english')


word_set = []

# Define Functions
def normalize_text(text):
    # Work through all the words in text and filter
    for word in text:
        # Check if word is a word, and not punctuation, AND check against stop words
        if word.isalpha() and word.lower() not in stopwords:
            # If it passes the filters, save to word_set
            word_set.append(word.lower())
    return word_set


# Make Function Calls
#print cancer_text[0:20]
#print cancer_tokens[0:10]
#print text.concordance('economics')
#print text.collocations()
#print text.similar('Pot')

normalize_text(text)



fd = FreqDist(word_set)
print fd.most_common(200)
#print fd.hapaxes()
fd.plot(50,cumulative=False)

# Print results to a CSV file
for key, count in fd.most_common(200):
    file.writerow([key, count])
