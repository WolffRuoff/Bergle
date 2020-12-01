#%%
import tkinter as tk
import cleaner
from cossim import CosSimCalc
from invIndex import invIndexCreator

class searchGUI():
    def __init__(self, invIndex):
        window = tk.Tk()
        window.title("Bergle")

        self.query = ""
        self.invIndex = invIndex
        self.cossim = CosSimCalc(self.invIndex)

        self.useStemming = tk.BooleanVar()
        self.useStemming.set(True)
        self.remStop = tk.BooleanVar()
        self.remStop.set(True)

        window.rowconfigure([0,1], weight=1)
        
        window.columnconfigure(0, minsize=50, weight=2)
        window.columnconfigure([1,2,3], minsize=50, weight=1)

        #Title
        title = tk.Label(text="Bergle Search", foreground="red", pady=15, master=window, font=100)
        title.grid(row=0, column=0, rowspan=2, sticky="w", padx=20)

        #insert checkboxes for if analysis
        stopCheck = tk.Checkbutton(master=window, text="Remove Stopwords", variable=self.remStop, onvalue=True, offvalue=False)
        stopCheck.grid(row=0, column=1, sticky="nsw")

        stemCheck = tk.Checkbutton(master=window, text="Use Stemming", variable=self.useStemming)
        stemCheck.grid(row=0, column=2, sticky="nsw")

        #Reindex Button
        indexBut = tk.Button(text="Re-Index", width=15, master=window, command=self.handle_reindex)
        indexBut.grid(row=0, column=3, sticky="nsew")

        #Search bar
        self.search = tk.Entry(text="testText", master=window, font=38, width=50)
        self.search.grid(row=1, column=1, columnspan=3, sticky="ew")

        #Search Button
        searchBut = tk.Button(text="Search", width=15, master=window, command=self.handle_search)
        searchBut.grid(row=1, column=3, sticky="nsew")

        window.mainloop()

    def handle_search(self):
        self.cossim.setInvIndex(self.invIndex)
        self.query = cleaner.cleanQuery(self.search.get(),useStemming=self.useStemming.get(), useStopwords=self.remStop.get())
        

        rankings = self.cossim.getRanking(self.query)
        print(rankings)


    def handle_reindex(self):
        creator = invIndexCreator(useStemming=self.useStemming.get(), useStopwords=self.remStop.get())
        self.invIndex = creator.getInvIndex()
