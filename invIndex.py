import json
import os
import cleaner

class invIndexCreator():
    def __init__(self, folder1="Bergle", folder2="sites"):
        invertedIndex = {}
        i = 1
        for files in os.listdir(os.path.join("..", folder1, folder2)):
            words = cleaner.cleanFile(files)
            #For each word in the text file
            print(i)
            wordCount = {}
            for w in words:
                if w not in wordCount.keys():
                    wordCount[w] = 1
                #If the words in it already add 1 to value (number of ocurrences)
                else:
                    wordCount[w] += 1

            for w in wordCount.keys():
                #If the words not in the dictionary create and assign value 1 
                if w not in invertedIndex.keys():
                    invertedIndex[w] = []
                    invertedIndex[w].append((i,wordCount[w]))
                #If the words in it already add 1 to value (number of ocurrences)
                else:
                    invertedIndex[w].append((i,wordCount[w]))
            i += 1

        with open("invIndex.json", "w") as dadumped:  
            json.dump(invertedIndex, dadumped)


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