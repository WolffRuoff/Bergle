"""
@title invIndex
@author Ethan Ruoff and Same Farinacci

@class Creates an inverted index and can return it, write it, or print it
"""

import json
import os
import cleaner

class invIndexCreator():
    '''
    @constructor Initializes the creator, makes an inverted index of all the files in folder1 and folder2

    @param {string} folder1 First folder under where the files are located
    @param {string} folder2 Second folder under where the files are located
    @param {boolean} useStemming stem words if selected in menu
    @param {boolean} useStopwords remove stopwords if selected in menu
    '''
    def __init__(self, folder1="Bergle", folder2="sites", useStemming=True, useStopwords=True):
        self.invertedIndex = {}
        i = 1
        for files in os.listdir(os.path.join("..", folder1, folder2)):
            words = cleaner.cleanFile("file" + str(i) + ".txt", useStemming=useStemming, useStopwords=useStopwords)
            #For each word in the text file
            wordCount = {}
            for w in words:
                if w not in wordCount.keys():
                    wordCount[w] = 1
                #If the words in it already add 1 to value (number of ocurrences)
                else:
                    wordCount[w] += 1

            for w in wordCount.keys():
                #If the words not in the dictionary create and assign value 1 
                if w not in self.invertedIndex.keys():
                    self.invertedIndex[w] = []
                    self.invertedIndex[w].append((i,wordCount[w]))
                #If the words in it already add 1 to value (number of ocurrences)
                else:
                    self.invertedIndex[w].append((i,wordCount[w]))
            i += 1
    
    '''
    Returns the inverted index

    @return {dict} The inverted index
    '''
    def getInvIndex(self):
        return self.invertedIndex

    '''
    Writes the inverted index to a json file
    '''
    def writeInvIndex(self):
        with open("invIndex.json", "w") as dadumped:  
            json.dump(self.invertedIndex, dadumped)


    '''
    Recursively prints the inverted index as a nested dictionary

    @param {dict} d The dictionary
    @param {int} indent The number of indents for the dict. Goes up by 1 for each recursion
    '''
    def print_dict_tree(self, d, indent=0):
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
                print(); self.print_dict_tree(value, indent+1)
            else:
                print(":", value)