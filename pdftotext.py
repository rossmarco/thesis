import subprocess

files = [
    'cancer-training.pdf'
]
for f in files:
    cmd = 'python pdf2txt.py -o %s.txt %s' % (f.split('.')[0], f)
    run = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = run.communicate()
# display errors if they occur    
if err:
    print err