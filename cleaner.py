"""
@title cleaner.py
@author Ethan Ruoff

In this file text undergoes the following pre-processing:
- Converting digits to <Number> to minimize number of unique values
- Placing a "<S>" at the beginning of every sentence and "</S>" at the end of every sentence (replacing periods)
    - This makes it so sentence probability can calculate the probability of the first and last words
- Create a list of unigrams and bigrams to make counting and calculating probability more efficient
- Stripping punctuation
    - Limits unique values
- Making all characters lowercase
    - Case shouldn't affect probability of a sentence

"""
#%%
import nltk
stemmer = nltk.stem.PorterStemmer()
import string
import re

#%% Downloading stopwords
stopwords = nltk.corpus.stopwords.words("english")
stopwords += ["ref", "name"]

#%%
"""
Opens a file, splits it, strips of punctuation, makes text lowercase, removes any stopwords, and the converts numbers to "<Number>"

@param {string} fileName name of the file to open
@return {list} A sanitized list of unigrams
@see cleanWord()
"""
def cleanFile(fileName):
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
    text = re.sub(r'(?<=[a-zA-z])&[a-zA-Z]*;', ' ', text)
    text = re.sub(r'(?<=[a-zA-z])[\/;](?=[a-zA-Z])', ' ', text)
    text = re.sub(r'(?<=[a-zA-z])\.\.\.(?=[a-zA-Z])', ' ', text)
    
    text = text.split()
    text = [cleanWord(w) for w in text]

    #Remove url from first spot
    text.pop(0)

    #Remove empty spots
    while "" in text:
        text.remove("")

    f.close()
    return text

"""
Cleans a one word string by:
- Converting digits to <Number>
- Making everything lowercase
- Replace punctuation
- Replacing weird apostrophe with Apostrophe

@param {string} word The word to be cleans
@return {string} The cleaned word
"""
def cleanWord(word):
    text = re.sub(r"\S*\d+\S*",r"<Number>", word)
    text = text.lower()
    text = text.strip('!\"#$%&\'()*+,-.:;=?@[]^_`{|}~\\') 

    text = stemmer.stem(text)

    return text

"""
Splits and cleans a sentence into a list of words 

@param {string} sentence The sentence that needs cleaning
@return {list} a list of cleaned words from the sentence
@see sentenceProb() in n-grams.py
@see cleanWord()
"""
def cleanSentence(sentence):

    #sentence = re.sub(r"(?<!Dr|Ms|Mr)[\.?!]",r" </S>",sentence)

    text = sentence.split()
    text = [cleanWord(w) for w in text]

    return text

# %%
