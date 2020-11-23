#%%
import requests
import time
import re

"""
@class RuoffCrawler Web crawler that maps muhlenberg.edu and saves html to files
@author: Ethan Ruoff
"""
class RuoffCrawler():

    """
    Saves attributes and starts crawl()

    @constructor
    @param {string} startURL The starting url for the crawling
    @see crawl()
    """
    def __init__(self, startURL):
        self.startURL = startURL
        self.visited = []
        self.visited.append(self.startURL)
        self.map = {}
        self.id = 1
        self.crawl(self.startURL, True)

    """
    Grabs absolute and relative links from the html, adds http://muhlenberg.edu to relative links, and returns both lists

    @param {string} html The html of the url
    @return {list} absLinks A list of absolute links
    """
    def getLinks(self, html):
        absLinks = re.findall(r'((?<=href=\")(?:http[s]?://|www\.)[a-zA-Z0-9\.]*(?<!(webapps\.))muhlenberg\.edu.*?)[\"\']', html)
        relLinks = re.findall(r'((?<=href=\"(?!http))[a-zA-z0-9/]+\.htm[l]?)', html)

        #Makes the relative links absolute links
        for link in relLinks:
            fixedLink = "http://muhlenberg.edu" + link
            absLinks.append(fixedLink)

        #Cleans links slightly to avoid duplicates later on
        absLinks = [re.sub(r'(?<=http)s', '', i[0]) for i in absLinks]
        absLinks = [re.sub(r'(?<=http://)www\.', '', i) for i in absLinks]
        absLinks = [re.sub(r'#.*', '', i) for i in absLinks]
        absLinks = [i + "/" if i[-1] != "/" else i for i in absLinks]

        #sedehidiversity project subdomain blog has way too many pages
        absLinks = [i for i in absLinks if "sedehidiversityproject" not in i]

        return absLinks

    """
    Requests the html from the url

    @param {string} url The url that's html is being requested
    @return {string} The html from the get request
    @see crawl()
    """
    def getHTML(self, url):
        try:
            html = requests.get(url, timeout=10)
        except UnicodeError as e:
            print(e)
            return None
        except requests.exceptions.RequestException as e:
            print(e)
            return None
        
        time.sleep(0.5)
        html.encoding = "utf-8"
        return html.text

    """
    Writes a new file named file[id].txt with [id] being the current id in the following format:
    url of file
    # of absolute links
    HTML

    @param {string} url The url of the current site
    @param {string} html The html of the site at the url
    @param {int} absLinks The number of absolute links in html
    @see crawl()
    """
    def writeFile(self, url, html, absLinks):
        fileName = "../Bergle/sites/file" + str(self.id) + ".txt"
        self.id += 1
        lines = [url + "\n", str(absLinks) + "\n\n"]
        with open(fileName, "w", encoding='utf-8') as writeUp:
            writeUp.writelines(lines)
            writeUp.write(html)

    """
    Recursive DFS of Muhlenberg.edu
    It counts each sites' absolute and relative links and then writes them to a new file. Caps at 10,000 pages

    @param {string} url The url for the site it's crawling
    @param {boolean} isFirst Used to print the finished message for initial run
    @see getHTML()
    @see getLinks()
    @see writeFile()
    """
    def crawl(self, url, isFirst):
        if self.id <= 10000:
            print(str(self.id) + " : " + url)
            self.map[url] = {}

            #Download the url's html
            html = self.getHTML(url)
            if html == None:
                return

            self.map[url]["html"] = html
            
            #grab html's links and add them to the dict
            absLinks = self.getLinks(html)
            self.map[url]["targets"] = absLinks

            #Write a new file for the url
            self.writeFile(url,html,len(absLinks))

            #for all the url's target links
            for link in self.map[url]["targets"]:
                #Make sure it hasn't already been visited
                if link in self.visited:
                    continue
                #Mark it as visited
                self.visited.append(link)
                
                self.crawl(link, False)
            
            if isFirst:
                print("Crawling is finished")
                print("Number of pages retrieved: %d" % (self.id-1))



# %%
