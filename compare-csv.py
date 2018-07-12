import csv

# Code taken from stack overflow using CSV library in python
# https://stackoverflow.com/questions/5268929/compare-two-csv-files-and-search-for-similar-items
# Linear time solution

with open('bigram_freq25.csv', 'rb') as master:
    master_indices = dict((r[0], i) for i, r in enumerate(csv.reader(master)))

with open('bigram_freq2.csv', 'rb') as hosts:
    with open('results.csv', 'wb') as results:    
        reader = csv.reader(hosts)
        writer = csv.writer(results)

        for row in reader:
            index = master_indices.get(row[0])
            if index is not None:
                message = 'FOUND in master list (row {})'.format(index)
                
            else:
                message = 'NOT FOUND in master list'
            writer.writerow(row + [message])
