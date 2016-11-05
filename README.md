# Indexing-and-Retrieval-webpage

# Part 1 - Indexing
The indexer's job is to analyze the web pages discovered by the crawler.<br> 
In particular, for every page that was downloaded by the crawler, the indexer should do the following:<br>
1. Parse the text content of the page, breaking it into a list of tokens (aka terms or words).<br>
2. Remove stopwords from the list of tokens. (Use the stopwords list in the nltk library.)<br>
3. Apply a stemmer to each token.<br>
4. Update the inverted index.<br>

<b>Input</b><br>
Command line input should be:-
> python index.py pages_dir/ index.dat

For example,
> python index.py INFO-I427\Assignment4\pages index.dat

pages_dir should be directory of pages folder which contains index.dat file

<b>Output</b><br>
1. The inverted index, invindex.dat: For each term, this records a list of documents that contain
this term, as well as how many times the term appeared in each document.<br>
2. The document index, docs.dat: For each document, this records: <br>
(1) the length of the document(i.e. the number of terms it contains), <br>
(2) the title of the document (i.e. whatever is stored in theTITLE tag in the header of the HTML)<br>
(3) the URL of the document itself.<br>

Both invindex.dat and docs.dat files can be located under the directory you have entered in command line.<br>
(i.e. in this case, inside the pages folder)


# Part 2 - Retrieval
retriveal.py looks up the pages containing a set of query terms. The retrieval system takes command-line input a query mode and a list of one or more keywords(query terms).
Command line input:-
> python retrieve.py mode word1 word2 word3...

<b>Modes</b><br>
- or which means to return pages that include any of the keywords;<br>
- and which means to return pages that include all of the keywords;<br>
- most which means to return pages that include most (at least half) of the keywords.<br>

<b>Output</b><br>
For each hit, display the URL and the title of the HTML page to the screen.<br>
Display the total number of documents that were searched through, and the total number of hits that were found.<br>

<b>* Take note that docs.data, invindex.dat are all in pages folder</b>
