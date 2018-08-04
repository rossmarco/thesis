import sys
from os import listdir
from os.path import isfile, join
import os
import fileinput

reload(sys)
sys.setdefaultencoding('utf-8')

os.chdir('/Users/marcoross/Documents/summer2018_thesis/cancer')

mypath = '/Users/marcoross/Documents/summer2018_thesis/cancer'
filenames = [f for f in listdir(mypath) if isfile(join(mypath, f))]

""" with open('cancer-training.txt', 'w') as outfile:
    for fname in filenames:
        with open(fname) as infile:
            outfile.write(infile.read()) """


with open('cancer-testing.txt', 'w') as fout:
    fin = fileinput.input(filenames)
    for line in fin:
        fout.write(line)
    fin.close()