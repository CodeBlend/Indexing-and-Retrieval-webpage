#Code Report for Assignment 4
#Sanghun Kim & Yifan Liu & Biao Zhang

#Part 1:
#How code works: There are three functions we created for this section, open_file, read_url and invindex. The main functions are
#read_url and invindex while open_file as used as helperr functions for the formula of these main functions.

#Problem we faced: beautifulsoup's installation and invindex were challenges trying to figure out how to categorize. We asked 
#helped from Azadeh and Pik-Mai to help us reinstall beautiful soup and resetting the running environment. 

#For the read_url, at first we used lxml as the way to process the data, but after the advice from Pik-Mai, #we decided to use 
#html5lib. The following code we used were clean the word_list with stopwords and apply stemmer to the clean list.

#For the invindex, we use counter to count the time that the word appears in a url and return it as a list. The first step we 
#did was check if the word is in big_data_dic, if it is, we just append the url and frequency (how many time it appears in the 
#url) to big_data_dic. If not, we create a new query with the url and frequency.

#Assumptions, simplifications, design decision made: the idea was originally use the beautifusoup and follow the beautifulsoup
#tutorial instructions, then we applied the stemmer and create stopwords for this part. And for invindex, we uses dictionary (hash table) to 
#represent the big_data that contains queries for keys, [[html, frequency]...] as values.


#How well it works on your code? it make is easy to manage and call, whenever we want to get access to the pages that has that query
#,just call big_data_dic[query], and it will return. 

import sys, os
import re, urllib
from bs4 import BeautifulSoup, Comment
from nltk.corpus import stopwords
from nltk import PorterStemmer
from collections import Counter
import pickle

def open_file(path, file_name):
    f_path = os.path.join(path, file_name)
    # import pdb; pdb.set_trace()
    with open(f_path, 'r') as f:
        content = f.read().strip()
    word_list = [[word] for word in re.split('\n', content)]
    for i in range(0, len(word_list)):
        word_list[i] = re.split('\t', word_list[i][0])
    #print word_list

    return word_list


def read_url(url_input):
    print "Parsing ", url_input, "\n"
    contents = urllib.urlopen(url_input).read()
    soup = BeautifulSoup(contents, "html5lib")

    # Removes comments in html document
    comments = soup.findAll(text=lambda text:isinstance(text, Comment))
    for comment in comments:
        comment.extract()

    # Get rid of script and style elements
    for script in soup(["script", "style"]):
        script.extract()

    # Get text
    text = soup.get_text()
    text = text.encode('utf-8')

    title = soup.title.string


    filter_text = re.split('\W+', text)
    word_list = [word for word in filter_text if word.isalpha()]
    for i in range(0, len(word_list)):
        word_list[i] = word_list[i].lower()

    # now clean the word_list with stopwords
    stop = set(stopwords.words('english'))
    clean_list = [word for word in word_list if word not in stop]
    # print clean_list
    # print word_list
    # print len(word_list), len(clean_list)


    # Applying PorterStemmer to the clean_list
    stemmer = PorterStemmer()
    stem_list = [stemmer.stem(word) for word in clean_list]

    count = Counter()
    count.update(stem_list)
    return count, title


def invindex(counter, big_data_dic, url_header):  # takes a list and a dict where to store the data.
    for query in counter:
        if query not in big_data_dic.keys():
            big_data_dic[query] = [[url_header, counter[query]]]
        else:
            # if url_header not in big_data_dic[query]:
            big_data_dic[query].append([url_header, counter[query]])
    # print big_data_dic


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print "Wrong number of arguments"
        sys.exit()
    path = sys.argv[1]
    index_file = sys.argv[2]

    big_data_dic = dict()
    dest_file_invindex = open(path + "\invindex.dat", "w+")
    dest_file_docs = open(path + "\docs.dat", "w+")
    dest_file_dictionary_dump = open("dict_dump.dat", "wb")


    urls = open_file(path, index_file)
    print "Processing"
    for url in urls:
        data, title = read_url(url[1])
        invindex(data, big_data_dic, url[0])
        length = len(list(set(data)))
        dest_file_docs.write(str(length) + "\t" + str(title) + "\t" + url[1])
        dest_file_docs.write("\n")

    for query in big_data_dic:
        dest_file_invindex.write(query + "\n")
        dest_file_invindex.write(str(big_data_dic[query]) + "\n")
    pickle.dump(big_data_dic, dest_file_dictionary_dump)

    dest_file_dictionary_dump.close()
    dest_file_docs.close()
    dest_file_invindex.close()

    print "DONE"
