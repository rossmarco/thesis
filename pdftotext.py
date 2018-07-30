import subprocess
import sys
from os import listdir
from os.path import isfile, join
import os

reload(sys)
sys.setdefaultencoding('utf-8')

mypath = '/Users/marcoross/Documents/summer2018_thesis'
files = [f for f in listdir(mypath) if isfile(join(mypath, f))]

""" files = [
     'diabetes-57.pdf',
     'diabetes-14.pdf',
     'diabetes-18.pdf',
     'diabetes-33.pdf',
] """

os.chdir('/Users/marcoross/Documents/summer2018_thesis/cancer')

for f in files:
    cmd = 'python pdf2txt.py -o %s.txt %s' % (f.split('.')[0], f)
    run = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = run.communicate()
# display errors if they occur    
if err:
    print err