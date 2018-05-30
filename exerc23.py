import mincemeat
import glob
import csv

text_files = glob.glob('obras/*')

def file_contents(file_name):
    f = open(file_name)
    try:
        return f.read()
    finally:
        f.close()

source = dict((file_name, file_contents(file_name))for file_name in text_files)

def mapfn(k, v):
    print 'map ' + k
    from stopwords import allStopWords
    for line in v.splitlines():
        for author in line.split(':::')[1].split('::'):
            for word in line.split(':::')[2].split():
                if (word not in allStopWords):
                    yield author, word.replace('.','').replace(':','').replace(')','').replace('(','').replace(',','')


def reducefn(k, v):
    print 'reduce ' + k
    total = 0
    d = dict()
    for index, item in enumerate(v):
        word = item.lower()
        if d.has_key(word):
            value = d[word]
            d[word] = value + 1
        else:
            d[word] = 1
    L = list()
    for w in sorted(d, key = d.get, reverse = True):
        L.append(w + " : " + str(d[w]))
    return L


s = mincemeat.Server()

s.datasource = source
s.mapfn = mapfn
s.reducefn = reducefn

results = s.run_server(password="changeme")

w = csv.writer(open("result4.csv", "w"))
wfilter = csv.writer(open("result5.csv", "w"))

from filter import authors
for k, v in results.items():
    w.writerow([k,str(v).replace("[","").replace("]", "").replace("'","").replace(' ','').replace('"','')])
if (k in authors):
    wfilter.writerow([k,str(v).replace("[","").replace("]", "").replace("'","").replace(' ','').replace('"','')])
