#%%
import tkinter as tk
import tkinter.ttk
import cleaner
from cossim import CosSimCalc
from invIndex import invIndexCreator
import webbrowser

class searchGUI():
    def __init__(self, invIndex):
        window = tk.Tk()
        window.title("Bergle")

        self.query = ""
        self.invIndex = invIndex
        self.cossim = CosSimCalc(self.invIndex)
        self.rankings = []

        self.useStemming = tk.BooleanVar()
        self.useStemming.set(True)
        self.remStop = tk.BooleanVar()
        self.remStop.set(True)

        topFrame = tk.Frame(master = window)
        topFrame.rowconfigure([0,1], weight=1)
        
        topFrame.columnconfigure(0, minsize=50, weight=2)
        topFrame.columnconfigure([1,2,3], minsize=50, weight=1)

        #Title
        title = tk.Label(text="Bergle Search", foreground="red", pady=15, master=topFrame, font=100)
        title.grid(row=0, column=0, rowspan=2, sticky="w", padx=20)

        #insert checkboxes for if analysis
        stopCheck = tk.Checkbutton(master=topFrame, text="Remove Stopwords", variable=self.remStop, onvalue=True, offvalue=False)
        stopCheck.grid(row=0, column=1, sticky="nsw")

        stemCheck = tk.Checkbutton(master=topFrame, text="Use Stemming", variable=self.useStemming)
        stemCheck.grid(row=0, column=2, sticky="nsw")

        #Reindex Button
        indexBut = tk.Button(text="Re-Index", width=15, master=topFrame, command=self.handle_reindex)
        indexBut.grid(row=0, column=3, sticky="nsew")

        #Search bar
        self.search = tk.Entry(text="testText", master=topFrame, font=38, width=50)
        self.search.grid(row=1, column=1, columnspan=3, sticky="ew")

        #Search Button
        searchBut = tk.Button(text="Search", width=15, master=topFrame, command=self.handle_search)
        searchBut.grid(row=1, column=3, sticky="nsew")

        #Gap
        tk.Label(text="", master=topFrame, height=2).grid(row=2,column=0)
        

        #Results Boxes
        results = tk.Frame(master = window, padx=20)
        results.rowconfigure([0,1,2,3,4,5,6,7,8], weight=1)
        results.columnconfigure([0], minsize=100, weight=1)
        results.columnconfigure([1], minsize=100, weight=1)

        tkinter.ttk.Separator(results, orient=tk.HORIZONTAL).grid(column=0, row=0, columnspan=2, sticky='sew')

        self.titleList = []
        self.resultList = []
        for i in range(10):
            self.titleList.append(tk.Label(text="", master=results, width=50, height=3, wraplength=350, justify="left"))
            self.resultList.append(tk.Label(text="", master=results, width=50, height=3, wraplength=350, justify="left"))
            self.titleList[i].grid(row=i+1, column=0, sticky="nw")
            self.resultList[i].grid(row=i+1, column=1, sticky="e")
            tkinter.ttk.Separator(results, orient=tk.HORIZONTAL).grid(column=0, row=i+1, columnspan=2, sticky='sew')

        #Binding hyperlinks to the urls
        self.resultList[0].bind("<Button-1>", lambda e: self.openSite(self.resultList[0]["text"]))
        self.resultList[1].bind("<Button-1>", lambda e: self.openSite(self.resultList[1]["text"]))
        self.resultList[2].bind("<Button-1>", lambda e: self.openSite(self.resultList[2]["text"]))
        self.resultList[3].bind("<Button-1>", lambda e: self.openSite(self.resultList[3]["text"]))
        self.resultList[4].bind("<Button-1>", lambda e: self.openSite(self.resultList[4]["text"]))
        self.resultList[5].bind("<Button-1>", lambda e: self.openSite(self.resultList[5]["text"]))
        self.resultList[6].bind("<Button-1>", lambda e: self.openSite(self.resultList[6]["text"]))
        self.resultList[7].bind("<Button-1>", lambda e: self.openSite(self.resultList[7]["text"]))
        self.resultList[8].bind("<Button-1>", lambda e: self.openSite(self.resultList[8]["text"]))
        self.resultList[9].bind("<Button-1>", lambda e: self.openSite(self.resultList[9]["text"]))

        #Left and right lines
        tkinter.ttk.Separator(results, orient=tk.VERTICAL).grid(column=0, row=0, rowspan=11, sticky='wns')
        tkinter.ttk.Separator(results, orient=tk.VERTICAL).grid(column=0, row=0, rowspan=11, sticky='ens')
        tkinter.ttk.Separator(results, orient=tk.VERTICAL).grid(column=1, row=0, rowspan=11, sticky='ens')

        #Page Turner
        self.page = 0
        turner = tk.Frame(master=window)
        turner.rowconfigure(0, minsize=50, weight=1)
        turner.columnconfigure([0, 1, 2], minsize=50, weight=1)

        prevPage = tk.Button(master=turner, text="Prev Page", command=self.handle_decreasePage)
        prevPage.grid(row=0,column=0,sticky="nsew")

        self.pageLab = tk.Label(master=turner, text=str(self.page+1))
        self.pageLab.grid(row=0, column=1)

        prevPage = tk.Button(master=turner, text="Next Page", command=self.handle_increasePage)
        prevPage.grid(row=0,column=2,sticky="nsew")

        topFrame.pack()
        results.pack()
        turner.pack()
        window.mainloop()

    def handle_search(self):
        self.cossim.setInvIndex(self.invIndex)
        self.query = cleaner.cleanQuery(self.search.get(),useStemming=self.useStemming.get(), useStopwords=self.remStop.get())
        

        self.rankings = self.cossim.getRanking(self.query)
        print(self.rankings)
        self.page = 0
        self.showResults()

    def handle_decreasePage(self):
        if self.page > 0:
            self.page -= 1
            self.showResults()

    def handle_increasePage(self):
        if self.page < (len(self.rankings)/10)-1:
            self.page += 1
            self.showResults()

    def showResults(self):
        for i in range(len(self.titleList)):
            if (self.page*10)+i < len(self.rankings):
                self.titleList[i].config(text = self.rankings[(self.page*10)+i][0])
                self.resultList[i].config(text = self.rankings[(self.page*10)+i][1])
            else:
                self.titleList[i].config(text = "")
                self.resultList[i].config(text = "")
        self.pageLab["text"] = str(self.page+1)

    def openSite(self,url):
        webbrowser.open_new(url)

    def handle_reindex(self):
        creator = invIndexCreator(useStemming=self.useStemming.get(), useStopwords=self.remStop.get())
        self.invIndex = creator.getInvIndex()

# %%
