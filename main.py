#%%
import cleaner

from gui import searchGUI
from invIndex import invIndexCreator
from crawler import Crawler
import os
import json
import math

invIndex = {}
maxFreq = {}
docs = {}

def main():
    global invIndex
    #Crawler("http://muhlenberg.edu/")

    with open("invIndex.json") as inv:
        invIndex = json.load(inv)
    
    searchGUI(invIndex)

main()
# %%
