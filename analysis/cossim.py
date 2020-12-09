import math
import cleaner
import os
'''
@class Calculator to compare the cosine similarities between a query that's passed and multiple documents
'''
class CosSimCalc():
    '''
    @constructor Initializes the attributes

    @param {dict} invIndex The inverted index of the files being searched
    '''
    def __init__(self, invIndex=None):
        self.invIndex = invIndex
        self.maxFreq = {}
        self.docs = {}

    def setInvIndex(self, invIndex):
        self.invIndex = invIndex

    '''
    Returns a list of cosign similarities sorted by relevance

    @param {list} text The query as a sanitized list
    @return {list} List of touples with the url and cosine similarity
    @see getWeight
    @see getCosSim
    '''
    def getRanking(self, text):

        #Remove any words not in any docs
        text2 = []
        for k in range(len(text)):
            if text[k] in self.invIndex.keys():
                text2.append(text[k])
        text = text2
        
        #If no results
        if len(text) == 0:
            return [("No Results", "", "", -1)]

        #Compile list of all documents containing query word
        idsWithWords = []
        for k in text:
            ids = [x[0] for x in self.invIndex[k]]
            for id in ids:
                if id not in idsWithWords:
                    idsWithWords.append(id)
        #Get query weight
        qVect = []
        for k in text:
            w = self.getWeight(k, text, True)
            qVect.append(w)
        vect = {}
        cosSims = []
        for i in idsWithWords:
            if i not in self.docs.keys():
                self.docs[i] = cleaner.cleanFile("cranfield" + str(i) + ".txt", False)
            if len(self.docs[i][2]) == 0:
                continue
            vect[i] = []
            for k in text:
                w = self.getWeight(k, i)
                vect[i].append(w)
            #calc cosSim
            cossim = self.getCosSim(qVect, vect[i])
            if cossim != 0:
                cosSims.append([self.docs[i][0], self.docs[i][1], cossim])
        cosSims.sort(key = lambda x: x[2], reverse=True)
        return cosSims[:10]

    '''
    Calculates weight of term using the following formula:
    weight = (frequency of term in query/document / frequency of most common term in query/documents) * idf

    @param {string} k the term being calculated
    @param {string} i document index
    @param {boolean} isQuery if true, term is from a query
    @return tf * idf (weight of term in query or document)
    @see getTF
    @see getIDF
    '''
    def getWeight(self, k,i, isQuery=False):
        if isQuery:
            #i is the query in this case
            query = i
            freq = len([x for x in query if x == k])
            maxv = query.count(max(set(query), key = query.count))
            tf = freq/maxv
        else:
            tf = self.getTF(k,i)
        idf = self.getIDF(k)
        return tf * idf

    '''
    Calculates the term frequency by this formula:
    tf = f / Max(f)

    @param {string} k The term being calculated
    @param {int} i The index of the document
    @return {float} The term frequency of k in docs[i][2]
    @see getWeight
    '''
    def getTF(self, k, i):

        #check if word is in invIndex
        if k not in self.invIndex.keys():
            return 0

        freq = [x[1] for x in self.invIndex[k] if x[0] == i]
        
        #Word isn't in doc
        if len(freq) == 0:
            return 0

        freq = freq[0]

        #If max freq for doc isn't known, count it and add it to the dict 
        maxv = 0
        if i not in self.maxFreq.keys():
            maxv = self.docs[i][2].count(max(set(self.docs[i][2]), key = self.docs[i][2].count))
            self.maxFreq[i] = maxv
        
        return freq/self.maxFreq[i]

    '''
    Calculates IDF using frequency of word from inverted index and total number of documents:
    IDF = documents / word frequency

    @param {string} k The term being calculated
    @return {float} IDF
    @see getWeight()
    '''
    def getIDF(self, k):
        df = len(self.invIndex[k])
        n = len(os.listdir(os.getcwd() + "/separated"))
        return math.log10(n/df)

    '''
    Calculates the cosine similarity of 2 vectors 

    @param {list} q The query vector
    @param {list} d The vector of a document
    @return {float} The cosine similarity between q and d
    @see getRanking
    '''
    def getCosSim(self, q, d):
        dotProd = self.getDotProd(q,d)
        qMag = self.getMagnitude(q)
        dMag = self.getMagnitude(d)

        if qMag == 0 or dMag == 0:
            return 0    
        else:
            return dotProd/ (qMag*dMag)

    '''
    Calculates dot product of two vectors

    @param {list} vec1 first vector to multiply
    @param {list} vec2 second vectory to multiply
    @see getCosSim
    '''
    def getDotProd(self, vec1, vec2):
        #Make sure they're the same length
        if len(vec1) != len(vec2):
            print("Length Vec 1: %d" % vec1)
            print("Length Vec 2: %d" % vec2)
            return 0

        prod = 0

        for x in range(len(vec1)):
            prod += vec1[x] * vec2[x]
        return prod

    '''
    Calculates the magnitude of a vector with the following formula:
    |v| = sqrt(w1**2 + w2**2 + w3**2 + etc.)

    @param {list} v The vector that's magnitude is being calculated
    @return {float} The magnitude of v
    @see getCosSim
    '''
    def getMagnitude(self, v):
        wTotal = 0
        for w in v:
            wTotal += w**2

        return math.sqrt(wTotal)