#%%
from invIndex import invIndexCreator
import json
import re, os
from cossim import CosSimCalc
import cleaner
cossim = CosSimCalc()
'''
@title Bergle Search Analysis
@description A program that allows users to test the performance of our cosine similarity calculator with and without stemming and stopwords. It calculates the accuracy, precision, and recall.
@author Ethan Ruoff and Sam Farinacci
'''
def main():
    qRels = getQRel()
    queries = getQueries()

    '''    
    # Remove comments if you don't have the invIndexes as files
    invIndexStemStop = invIndexCreator().writeInvIndex('invIndexStemStop.json')
    invIndex = invIndexCreator(useStopwords=False, useStemming=False).writeInvIndex('invIndex.json')
    invIndexStem = invIndexCreator(useStopwords=False).writeInvIndex('invIndexStem.json')
    invIndexStop = invIndexCreator(useStemming=False).writeInvIndex('invIndexStop.json')
    '''

    files = ["invIndexStop.json", "invIndexStemStop.json", "invIndexStem.json", "invIndex.json"]
    for f in files:
        with open(f) as inv:
            invIndex = json.load(inv)
            getStats(f, invIndex, qRels, queries)

'''
Runs each query in the cosine similarity calculator and compares the results with the provided testing data answers. Calculates the accuracy, precision, and recall

@param {string} f The filename
@param {dict} invIndex The inverted index containing the terms
@param {dict} qRels A dictionary containing the testing data answers
@param {list} queries A list of tuples containing the query ID and the query
'''
def getStats(f, invIndex, qRels, queries):
    if "Stem" in f:
        useStemming = True
        if "Stop" in f:
            print("Using Stemming and Stopwords:")
            useStopwords = True
        else:
            print("Using Stemming but not Stopwords:")
            useStopwords = False
    else:
        if "Stop" in f:
            print("Using Stopwords but not Stemming:")
            useStopwords = True
        else:
            print("Not using Stopwords or Stemming:")
            useStopwords = False
        useStemming = False


    truePos = 0 # If it's in rankIDs and result
    falsePos = 0 # If it's in rankIDs but not in result
    trueNeg = 0 # If it's not in RankIDs or result
    falseNeg = 0 # If it's not rankIDs but is in result
    
    cossim.setInvIndex(invIndex)
    for q in queries:
        # Ensures we have the results for the query to compare
        if int(q[0]) not in qRels.keys(): #or int(q[0]) != 201:
            continue
        #print(str(q[0]))
        text = cleaner.cleanQuery(q[1], useStemming, useStopwords)
        rankings = cossim.getRanking(text)
        rankIDs = [int(i[0]) for i in rankings]
        #print(rankIDs)
        for x in range(1400):
            i = x+1
            # True Positive
            if i in rankIDs and i in qRels[int(q[0])]:
                #print(str([x[2] for x in rankings if int(x[0]) == i]))
                truePos += 1
            # False Positive
            elif i in rankIDs and i not in qRels[int(q[0])]:
                falsePos += 1
            # True Negative
            elif i not in rankIDs and i not in qRels[int(q[0])]:
                trueNeg += 1
            # False Negative
            else:
                falseNeg += 1


    print('True Positive: %d' % truePos)
    print('False Positive: %d' % falsePos)
    print('True Negative: %d' % trueNeg)
    print('False Negative: %d' % falseNeg)
    
    accuracy = (truePos + trueNeg) / (truePos + trueNeg + falsePos + falseNeg) 
    print('\nAccuracy: %.2f' % accuracy)

    precision = truePos / (truePos + falsePos)
    print('Precision: %.2f' % precision)

    recall = truePos / (truePos + falseNeg)
    print('Recall: %.2f' % recall)

'''
Opens the cranqrel file and puts the training data answers into a dictionary object

@return {dict} Dictionary with the query ids as keys and relevant docs as values
'''
def getQRel():
    qRels = {}
    with open("cranqrel") as rels:
        for line in rels.readlines():
            terms = line.split()
            if terms[2] != "-1":
                if int(terms[0]) not in qRels.keys():
                    qRels[int(terms[0])] = [int(terms[1])]
                else:
                    qRels[int(terms[0])].append(int(terms[1]))
    #print_dict_tree(qRels)
    return qRels

'''
Opens cran.qry (training data) and extracts the query ids and queries into a list of tuples

@return {list} A list of tuples containing query ids and queries
'''
def getQueries():
    with open("cran.qry") as queries:
        queries1 = re.findall(r'\.I (\d+)\s\.W\s([\s\S]+?)(?=\.I)', queries.read())
        queries2 = []
        for i in range(len(queries1)):
            queries2.append((i+1,queries1[i][1]))
        return queries2

'''
Recursively prints the inverted index as a nested dictionary

@param {dict} d The dictionary
@param {int} indent The number of indents for the dict. Goes up by 1 for each recursion
'''
def print_dict_tree(d, indent=0):
    """Print tree of keys in `dict` object.
        
    Prints the different levels of nested keys in a `dict` object. When there
    are no more dictionaries to key into, prints objects type and byte-size.

    Input
    -----
    d : dict
    """
    for key, value in d.items():
        print('    ' * indent + str(key), end=' ')
        if isinstance(value, dict):
            print(); print_dict_tree(value, indent+1)
        else:
            print(":", value)
main()
# %%
