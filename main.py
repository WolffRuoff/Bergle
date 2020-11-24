#%%
import cleaner
from invIndex import invIndexCreator
from crawler import RuoffCrawler
import os
import json
import math

invIndex = {}
maxFreq = {}
docs = {}

def main():
    global invIndex
    #RuoffCrawler("http://muhlenberg.edu/")
    #invIndexCreator()
    with open("invIndex.json") as inv:
        invIndex = json.load(inv)

def getDotProd(vec1, vec2):
    #Make sure they're the same length
    if len(vec1) != len(vec2):
        return

    prod = 0

    for x in len(vec1):
        prod += vec1[x] * vec2[x]
    
    return prod

def getCosSim(sentence):
    global docs
    text = cleaner.cleanSentence(sentence)

    idsWithWords = []
    for k in text:
        ids = [x[0] for x in invIndex[k]]
        for id in ids:
            if id not in idsWithWords:
                idsWithWords.append(id)
    
    vect = {}
    for i in idsWithWords:
        if i not in docs.keys():
            docs[i] = cleaner.cleanFile("file" + str(i) + ".txt", False)
        vect[i] = []
        for k in text:
            w = getWeight(k, i)
            vect[i].append(w)
        #calc cosSim
    #for w in text:

def getWeight(k,i):
    tf = getTF(k,i)
    idf = getIDF(k)
    return tf * idf

def getTF(k, i):
    global maxFreq

    #check if word is in invIndex
    if k not in invIndex.keys():
        return 0

    freq = [x[1] for x in invIndex[k] if x[0] == i]
    
    #Word isn't in doc
    if len(freq) == 0:
        return 0

    freq = freq[0]

    maxv = 0
    if i not in maxFreq.keys():
        maxv = max(set(docs[i]), key = docs[i].count) 
        maxFreq[i] = maxv
    
    return freq/maxFreq[i]

def getIDF(k):
    df = len(invIndex[k])
    n = len(os.listdir(os.getcwd() + "/sites"))
    return math.log10(n/df)

main()