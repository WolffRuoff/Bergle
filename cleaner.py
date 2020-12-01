'''
@title cleaner.py
@author Ethan Ruoff & Sam Farinacci

In this file text undergoes the following pre-processing:
- Converting digits to <Number> to minimize number of unique values
- Removes CSS, JS, and HTML
- Removes stopwords
- Stripping punctuation
    - Limits unique values
- Making all characters lowercase
    - Case shouldn't affect weight of words
- Stemming
    - Minimize unique values

'''
#%%
import nltk
stemmer = nltk.stem.PorterStemmer()
import string
import re

#%% Downloading stopwords
stopwords = nltk.corpus.stopwords.words("english")
stopwords += ["ref", "name"]

#%%
'''
Opens a file, splits it, strips of punctuation, makes text lowercase, removes any stopwords and stems words (if selected in menu), 
and the converts numbers to "<Number>"

@param {string} fileName name of the file to open
@param {boolean} scrubURL pop URL from top spot if true
@param {string} folder1 directory name for project
@param {string} folder2 directory name to store site text files
@param {boolean} useStemming stem words if selected in menu
@param {boolean} useStopwords remove stopwords if selected in menu
@return {list} A sanitized list of unigrams
@see cleanWord()
'''
def cleanFile(fileName, scrubURL=True, folder1="Bergle", folder2="sites", useStemming=True, useStopwords=True):
    f = open("..\\Bergle\\sites\\" + str(fileName), encoding="utf-8")
    text = f.read()
    
    #Remove CSS and JS
    text = re.sub(r'<script[\S\s]+?<\/script>', ' ', text)
    text = re.sub(r'<style[\S\s]+?<\/style>', ' ', text)

    #remove html
    text = re.sub(r'<[^<][\S\s]+?>', ' ', text)
    text = re.sub(r'<!--[\S\s]+?-->', ' ', text)

    #convert lazy writing to spaces
    text = re.sub(r'(?<=[a-zA-z])&rsquo;', '\'', text)
    text = re.sub(r'(?<=[a-zA-z])&nbsp;', ' ', text)
    text = re.sub(r'(?<=[a-zA-z])&[a-zA-Z]*;', ' ', text)
    text = re.sub(r'(?<=[a-zA-z])[\/;](?=[a-zA-Z])', ' ', text)
    text = re.sub(r'(?<=[a-zA-z])\.\.\.(?=[a-zA-Z])', ' ', text)
    
    text = text.split()
    if useStopwords:
        text = [cleanWord(w, useStemming) for w in text if w not in stopwords]
    else:
        text = [cleanWord(w, useStemming) for w in text]

    if scrubURL:
        #Remove url from first spot
        text.pop(0)

    #Remove empty spots
    while "" in text:
        text.remove("")

    f.close()
    return text

'''
Cleans a one word string by:
- Converting digits to <Number>
- Making everything lowercase
- Replace punctuation
- Replacing weird apostrophe with Apostrophe

@param {string} word The word to be cleans
@param {boolean} useStemming if true, use stemming
@return {string} The cleaned word
'''
def cleanWord(word, useStemming):
    text = re.sub(r"\S*\d+\S*",r"<Number>", word)
    text = text.lower()
    text = text.strip('!\"#$%&\'()*+,-.:;=?@[]^_`{|}~\\') 
    
    if useStemming:
        text = stemmer.stem(text)

    return text

'''
Splits and cleans a sentence into a list of words 

@param {string} sentence The sentence that needs cleaning
@param {boolean} useStemming stem words if selected in menu
@param {boolean} useStopwords remove stopwords if selected in menu
@return {list} a list of cleaned words from the sentence
@see cleanWord()
'''
def cleanQuery(sentence, useStemming=True, useStopwords=True):

    text = sentence.split()
    if useStopwords:
        text = [cleanWord(w, useStemming) for w in text if w not in stopwords]
    else:
        text = [cleanWord(w, useStemming) for w in text]

    return text

# %%
