# Bergle
Welcome to Bergle, a user friendly searching experience for Muhlenberg.edu/

![Alt Text](berglegif.gif)

<br>

## How do I use Bergle?
Using Bergle is easy! Simply download the repo and run main.py <br> If you don't want to download all of the sites (10,000 files), simply uncomment the section at the beginnning of main.py and our handcrafted crawler will grab all of the pages for you (WARNING: This process takes ~3 hours)
<br><br>

## Why make a search engine for just muhlenberg.edu/?
This is [slfarinacci](https://github.com/slfarinacci) and [WolffRuoff](https://github.com/WolffRuoff)'s final project for Artificial Intelligence. Even though the project has the small scope of just Muhlenberg's website, we still learned the same information and techniques that we would have learned creating a search engine for numerous sites. During this project, we learned how to create a web crawler and corresponding inverted index, preprocess complicated html/text with vanilla regex (stemming being the exception), calculate the cosine similarity between a query and webpage, and create a comprehensive GUI to display the resulting rankings.
<br><br>

# Files

## Web Crawler
**crawler.py** is used to recursively crawl muhlenberg.edu sites and store the site’s source HTML as text files using Python’s requests and re libraries. Within the class, the **getLinks** function creates a listing of links from the source code passed to the function using the re library’s findall function to locate href attributes within anchor tags where links are likely to be contained. We then decided to do the following to the links:
- We separated them into two lists of absolute links and relative links so that the relative links can have “http://muhlenberg.edu” appended before joining the rest of the URLs that will later be returned from the function. 
- We cleaned them all to fit the same format, avoiding the possibility of duplicates with slightly different formatting later (i.e., “http://muhlenberg.edu” vs “http://muhlenberg.edu/”). 

This function, as well as the getHTML function (uses get function from requests to attempt to retrieve page source) and the writeFile function (writes HTML source to a text file), facilitate the **crawl** function, a recursive depth-first search in which each URL’s source is written to a file and its contents are searched for more URLs to load. 

The biggest difficulty with the web crawler is the amount of time it takes to run. In order to prevent too many requests going on at once, we had to implement a timer to pause the function between requests. As a result, the program takes around 3 hours to run. Normally this wouldn’t be a problem, but we found that sometimes an extension in the code editor would crash stopping the program (not as a result of our code!) rendering the progress it made useless. To counteract this issue, we made it so the program automatically reads the already written files instead of creating requests for them. This considerably speeds up the program after a crash.
<br><br>

## Preprocessing Webpages
**cleaner.py** handles the pre-processing of both the URL source code document contents and queries. Pre-processing can vary slightly here, depending on whether the user opts to use stemming to store only the root of each term (minimizes unique values) or eliminate stopwords as part of the search. These selections are passed to the **cleanFile** function as boolean variables useStemming and useStopwords, respectively. Aside from these optional values, pre-processing includes the following:

- CSS, JS and HTML code is removed
- Punctuation is removed (excluding those that are relevant to word meaning, such as apostrophes)
- All characters are converted to lowercase

This is accomplished using the re library’s sub function to replace parts of the file based on specified rules, i.e. search for the string “&nbsp” (a forced space character in HTML) and replace it with “ “. Code and HTML characters are first cleaned within this function and then individual words are stripped of case and punctuation and then stemmed (if chosen) within the function **cleanWord**. **cleanQuery** is specifically for pre-processing queries by splitting the query into a list of terms and cleaning each term using **cleanWord**.

One of the difficulties faced in cleaning the source files were in replacing HTML characters with their respective plaintext characters (i.e. &nbsp to “ “) because these were only sparingly used throughout the code. The text itself also contained various quirks in typing styles that had to be addressed as part of the pre-processing, such as typing ellipsis with two periods instead of three. 
<br><br>

## Inverted Index
**invIndex.py** creates an inverted index using the cleaned text files. The constructor uses the os Python library to loop through the text files in the directory given in the parameters, using the **cleanFile** function from **cleaner.py** to clean the text before iterating through the file word by word. One of the attributes of an invIndex object is the inverted index itself stored as a dictionary. Words within the documents are stored as the keys and the value is a list of tuples, each being a document id and the frequency of the given word within that document. 

The **getInvIndex** function returns the inverted index attribute and the **print_dict_tree** function prints the inverted index to the console. **writeInvIndex** writes the contents of the inverted index to .json file.

This part of the project was very straightforward, and as such we did not face any dilemmas.
<br><br>

## Calculating the Cosine Similarity ranking
**cossim.py** handles the calculations involved in getting the cosine similarities between the user’s query and the document files. The main function within the file, **getRanking**, first removes any words within the query that can’t be found in any of the documents and if that encompasses the entirety of the query, returns “No Results” in place of the URL. If there are still words left in the query, a list is compiled of all documents where the word does come up. Eventually, the function returns the calculated cosine similarity along with its URL and the document filename.

The calculations that make up the formula for cosine similarity are spread out over several additional functions:
- **getTF** returns the term frequency (TF). This is calculated using the inverted index to locate the frequency of the given term divided by the frequency of the most frequent word in the document.  
- **getIDF** returns the IDF by using the os library to calculate the number of documents in the working directory. The function returns the number of documents divided by the frequency of the term.
- TF and IDF are multiplied by each other to calculate the term weight within the function **getWeight**.
- **getCosSim** returns the cosine similarity. This is calculated by using the getDotProd function to get the dot product of the document and query vectors and the magnitudes of each vector using the getMagnitude function.

The purpose of separating each step of the calculations involved in cosine similarity proved to be useful later when debugging the program because there was no need to isolate different stages of the calculation. This made this section of the project considerably less difficult to tackle.
<br><br>

## Displaying our Results
**gui.py** utilizes the already installed TKinter Python library. The **searchGUI** class initializes the UI structured in three grids in frames: topFrame, results, and turner.
- topFrame consists of the name, checkboxes, re-index button, search bar, and search button.
- Results is where the titles and URLs are located. We decided to include the titles as well because we sometimes found just the URLs to sometimes be confusing or not at all helpful.
- Turner contains the previous page button, page number label, and next page button

In order to perform a search, the user must type a query into the search bar and the click on the search button. When the search button is clicked, it launches the **handle_search** function that updates the **CosSimCalc** class’s inverted index, grabs the query from the search bar (Entry widget), cleans the query with **cleanQuery**, and then runs the **getRanking** function. Once it retrieves the new rankings, it resets the page attribute and calls **showResults** which updates the GUI with the new rankings.

**showResults** updates the results frame by iterating through the grid rows and updating them with the corresponding title and URL. To find the appropriate values from rankings, it multiplies the page number by 10 and then adds the row number. Making the **showResults** function was the biggest challenge in creating the GUI because we had to find a way to iterate through the list of rankings without having out of index errors or blank pages. We accomplished this by limiting the page turning button's abilities and by using blank rows if the rankings ran out.
<br><br>

## Analysis of our program

Our analysis program is almost identical to our **Bergle** program. While no changes affect the effectiveness, there are multiple changes to make the program work with the new dataset. For example, we had to use the ID number instead of a URL for the dataset. As a result, we had to remove ".I" predeccessor in the cleaner in order to still pop the index as the first value. 

After making basic processing changes, we also had to read the **cranqrel** file that contained the testing data results. After reading this file and inputting the results into a dictionary, we started facing indexing errors. We then realized that **cranqrel** didn't have an analysis for each query. To fix this, we simply skipped any queries that didn't have results in **cranqrel**. After fixing any bugs, we compared the dictionary with our program’s rankings getting the results outlined below:

<br>

### Chart 1: Totals 

<table>
    <thead>
        <tr>
            <th></th>
            <th colspan=2>Stemming</th>
            <th colspan=2>No Stemming</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <th rowspan=2>Removed Stopwords </th>
            <td >True Positive = 362</td>
            <td> False Positive = 1,878</td>
            <td >True Positive = 334</td>
            <td> False Positive = 1,906</td>
        </tr>
        <tr>
            <td>False Negative = 1,226</td>
            <td>True Negative = 310,134</td>
            <td>False Negative = 1,254</td>
            <td>True Negative = 310,106</td>
        </tr>
        <tr>
            <th rowspan=2>Stopwords Included</th>
            <td >True Positive = 332</td>
            <td> False Positive = 1,908</td>
            <td >True Positive = 312</td>
            <td> False Positive = 1,928</td>
        </tr>
        <tr>
            <td>False Negative = 1,256</td>
            <td>True Negative = 310,104</td>
            <td>False Negative = 1,276</td>
            <td>True Negative = 310,084</td>
        </tr>
    </tbody>
</table>
<br><br>

### Chart 2: Accuracy, Precision, & Recall

<table>
    <tbody>
        <tr>
            <th></th>
            <th>Stemming</th>
            <th>No Stemming</th>
        </tr>
        <tr>
            <th rowspan=3>Removed Stopwords</th>
            <td>Accuracy = 99%</td>
            <td>Accuracy = 99%</td>
        </tr>
        <tr>
            <td>Precision = 16%</td>
            <td>Precision = 15%</td>
        </tr>
        <tr>
            <td>Recall = 23%</td>
            <td>Recall = 21%</td>
        </tr>
         <tr>
            <th rowspan=3>Stopwords Included</th>
            <td>Accuracy = 99%</td>
            <td>Accuracy = 99%</td>
        </tr>
        <tr>
            <td>Precision = 15%</td>
            <td>Precision = 14%</td>
        </tr>
        <tr>
            <td>Recall = 21%</td>
            <td>Recall = 20%</td>
        </tr>
    </tbody>
</table>
<br>

Based on the above results, using stemming and removing stopwords is the most effective with using only one or the other causing nearly identical results. In this particular use case, measuring accuracy is useless due to the huge imbalance of true negatives vs. true positives. To prove this point, if one were to select 15 random documents instead of sorting them by cosine similarity, the accuracy would be approximately 98.5%. Therefore, precision and recall become the primary measurements to gauge performance.

While both precision and recall are low overall, the low precision is due primarily to the testing data answers provided. The precision is low because the correct data has a wildly different number of results based on the query. As a result, our results have a large number of false positives when the length of correct results is less than 15 (the length of results we return). 

The slightly higher recall therefore becomes the best measure as long as precision isn't extremely low (under 10%). This recall shows that only approximately 23% of the correct search results were identified (using stemming and removing stopwords). We believe that this is a limit of the cosine similarity and if we were to include contextual analysis that these statistics would greatly improve.

Compared to other examples of programs using cosine similarity our program does provide better results though due to the high amount of cleaning the text undergoes. By removing the stopwords or stemming, the number of documents in the rankings greatly decreases because the number of unique terms to match from the query decreases. By performing both stemming and the removal of stopwords, the results compile and improve the precision and accuracy by a small margin.
<br><br>

# Conclusion
Overall, creating Bergle was a wondful learning experience. As the final project for our Artificial Intelligence class, we learned how to create a recursive crawler of any site, process text to be easy to analyze, make an inverted index of terms, calculate the cosine similarities of documents to determine relevance, and we learned how to create an interactive GUI. We can't wait to explore these topics in more depth and to continue learning more about computer science.
