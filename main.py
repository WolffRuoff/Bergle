#%%
from gui import searchGUI
from invIndex import invIndexCreator
from crawler import Crawler
import json

'''
@title Bergle Search
@description A program that allows users to search the Muhlenberg.edu website for information in an easy-to-use manner
@author Ethan Ruoff and Sam Farinacci
'''
def main():
    #Remove comments if you don't have the sites folder
    '''
    Crawler("http://muhlenberg.edu/")
    ind = invIndexCreator()
    ind.writeInvIndex()
    '''
    with open("invIndex.json") as inv:
        invIndex = json.load(inv)
    
    searchGUI(invIndex)

main()
# %%
