import sys, pickle
from nltk.corpus import stopwords
from nltk import PorterStemmer

###open the file we did in index(part1)
def open_file():
    invindex = open('dict_dump.dat','rb')
    big_data_dic = pickle.load(invindex)
    docs = open('docs.dat','r')
    docs_list = []
    for i in docs:
        docs_list.append(i.split('\t'))
    return big_data_dic, docs_list

###remove the stop words and sterm the input words
def redo_words(word_list):
    stop = set(stopwords.words('english'))
    stemmer = PorterStemmer()

    nonstop_words = [word for word in word_list if word not in stop]
    stemmer_words = [stemmer.stem(word) for word in nonstop_words]

    return stemmer_words

##or method
def ormode(big_data_dic,word_list):
    hits = set()
    searched = set()
    for i in word_list:
        if i in big_data_dic:
            tmp= big_data_dic[i]
            #print tmp
            for j in tmp:
                searched.add(j[0])
                if j[0] not in hits:
                    hits.add(j[0])
    return  hits,len(searched)

###and method
def andmode(big_data_dic,word_list):
    #print 'test',words_list
    hits = set()
    searched = set()
    for i in range(0,len(word_list)):
        tmp = set()
        if word_list[i] in big_data_dic:
            for j in big_data_dic[word_list[i]]:
                #print j
                searched.add(j[0])
                tmp.add(j[0])
        if len(hits) == 0: #first initialized, hits is tmp, we want to let them equal and compare hits and tmp
                        #from now on.
            hits = tmp
        else:
            hits = hits & tmp #intersection of two sets. find the common words that appears at both.
    return  hits,len(searched)

##most method
def mostmode(big_data_dic,word_list):
    hits_dict = {}
    hits = []
    searched = set()
    half = len(word_list) / 2
    for i in range(0,len(word_list)):
        if word_list[i] in big_data_dic:
            for j in big_data_dic[word_list[i]]:
                searched.add(j[0])
                if j[0] not in hits:
                    hits_dict[j[0]] = 1
                else:
                    hits_dict[j[0]] +=1
    for i in hits_dict:
        if hits_dict[i] >= half:
            hits.append(i)
    return hits,len(searched)

### result print
def print_result(hits,docs,searched_len):
    page_num = []
    #print hits
    for i in hits:
        page_num.append(int(i[:-5]))
    #print page_num
    #print len(docs)
    for i in range(0,len(docs)):
        for j in page_num:
            if i == j:
                print docs[i][1],docs[i][2]
    print "processing result...\n"
    print "The total num of the searched pages are:" + str(searched_len) + "\n"
    print "The total num of the hits pages are:" + str(len(hits))


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print "Wrong input"
        sys.exit()
    arg_list = sys.argv
    mod = arg_list[1]
    tmp_words = arg_list[2:]
    words_list = redo_words(tmp_words)
    if len(words_list) == 0:
        print "Please enter some meaningful words."
        sys.exit()
    big_data_dic, docs = open_file()

    if mod == "or":
        hits,searched_len = ormode(big_data_dic,words_list)
        print_result(hits,docs,searched_len)
    elif mod == "and":
        hits,searched_len = andmode(big_data_dic,words_list)
        print_result(hits,docs,searched_len)
    elif mod == "most":
        hits,searched_len = mostmode(big_data_dic,words_list)
        print_result(hits,docs,searched_len)
    else:
        print "NO corresponding method found, check the method input."

