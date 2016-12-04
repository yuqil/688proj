import re
import string
import operator
from nltk.corpus import stopwords
import numpy as np
import matplotlib.mlab as mlab
import matplotlib
matplotlib.use("MacOSX")
import matplotlib.pyplot as plt

stop = set(stopwords.words('english'))
stop.add("using")
stop.add("based")
inputpath = "/Users/yuqil/Desktop/16fall/15688/final project/code/688proj/parse_dblp/inproc.txt"
file = open(inputpath)


dict = {}
year_map = {}


for line in file:
    tokens = line.split("\t")
    year = int(tokens[1])
    title = tokens[0].lower().rstrip().translate(None, string.punctuation)
    token = title.split(" ")

    for i in range(0, len(token) - 1):
        phrase = token[i] + " " + token[i + 1]
        if token[i] in stop or token[i + 1] in stop:
            continue
        if phrase in dict:
            dict[phrase] += 1
        else:
            dict[phrase] = 1
            year_map[phrase] = []
        year_map[phrase].append(year)

sort_word = sorted(dict.items(), key=operator.itemgetter(1), reverse=True)
topwords = sort_word[0:50]
print topwords

x = year_map['machine learning']
# the histogram of the data
n, bins, patches = plt.hist(x, 30, normed=1, facecolor='blue', alpha=0.75)

# add a 'best fit' line
plt.grid(True)
plt.title("computer vision titled paper year distribution")
plt.show()
# plt.show()

output = open("2gram.txt", "wb")
for k,v in sort_word:
    output.write(k + '\t' + str(v) + "\t" + str(year_map[k]) + "\n")

output.close()
file.close()


file = open(inputpath)
dict = {}
year_map = {}


print "2015 topwords \n\n"
for timing in xrange(2015,2016):
    for line in file:
        tokens = line.split("\t")
        year = int(tokens[1])
        if year != timing:
            continue
        title = tokens[0].lower().rstrip().translate(None, string.punctuation)
        token = title.split(" ")

        for i in range(0, len(token) - 1):
            phrase = token[i] + " " + token[i + 1]
            if token[i] in stop or token[i + 1] in stop:
                continue
            if phrase in dict:
                dict[phrase] += 1
            else:
                dict[phrase] = 1
                year_map[phrase] = []
            year_map[phrase].append(year)
sort_word = sorted(dict.items(), key=operator.itemgetter(1), reverse=True)
topwords1 = sort_word[0:50]
file.close()
print topwords1

print "\n"
print "2000 topwords"
file = open(inputpath)
dict = {}
year_map = {}
for timing in xrange(2000,2001):
    for line in file:
        tokens = line.split("\t")
        year = int(tokens[1])
        if year != timing:
            continue
        title = tokens[0].lower().rstrip().translate(None, string.punctuation)
        token = title.split(" ")

        for i in range(0, len(token) - 1):
            phrase = token[i] + " " + token[i + 1]
            if token[i] in stop or token[i + 1] in stop:
                continue
            if phrase in dict:
                dict[phrase] += 1
            else:
                dict[phrase] = 1
                year_map[phrase] = []
            year_map[phrase].append(year)
sort_word = sorted(dict.items(), key=operator.itemgetter(1), reverse=True)
topwords2 = sort_word[0:50]
print topwords2
file.close()
print "\n"


print "1985 topwords"
file = open(inputpath)
dict = {}
year_map = {}
for timing in xrange(1985,1986):
    for line in file:
        tokens = line.split("\t")
        year = int(tokens[1])
        if year != timing:
            continue
        title = tokens[0].lower().rstrip().translate(None, string.punctuation)
        token = title.split(" ")

        for i in range(0, len(token) - 1):
            phrase = token[i] + " " + token[i + 1]
            if token[i] in stop or token[i + 1] in stop:
                continue
            if phrase in dict:
                dict[phrase] += 1
            else:
                dict[phrase] = 1
                year_map[phrase] = []
            year_map[phrase].append(year)
file.close()
sort_word = sorted(dict.items(), key=operator.itemgetter(1), reverse=True)
topwords3 = sort_word[0:50]
print topwords3

def convert(k):
    words = k.split(" ")
    newword = words[0].title() + words[1].title() + '\n'
    return newword

output1 = open("title2015.txt", "wb")
output2 = open("title2000.txt", "wb")
output3 = open("title1985", "wb")

for k, v in topwords1:
    for i in range(0, v):
        output1.write(convert(k))

for k, v in topwords2:
    for i in range(0, v):
        output2.write(convert(k))

for k, v in topwords3:
    for i in range(0, v):
        output3.write(convert(k))


output1.close()
output2.close()
output3.close()
file.close()