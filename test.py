from nltk import ngrams
import PyPDF2

sentence = 'All that glitters is not gold'
n = 3
threegrams = ngrams(sentence.split(), n)
for grams in threegrams:
  print grams

""" pdfFileObj = open('diet-cancer.pdf', 'rb')
pdfReader = PyPDF2.PdfFileReader(pdfFileObj)

#print pdfReader.numPages

pageObj = pdfReader.getPage(0)

sentence = pageObj.extractText()
n = 3
threegrams = ngrams(sentence.split(), n)
for grams in threegrams:
  print grams """



