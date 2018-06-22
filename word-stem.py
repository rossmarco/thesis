import nltk
from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize

nltk.download('punkt')

# load data
filename = 'filteredtext.txt'
file = open(filename, 'r')
text = file.read().decode('utf8')
file.close()
# split into words

tokens = word_tokenize(text)
# stemming of words

porter = PorterStemmer()

stemmed = [porter.stem(word) for word in tokens]

print(stemmed[:100])
