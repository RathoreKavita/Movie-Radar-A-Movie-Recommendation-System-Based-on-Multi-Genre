#imdbdataset.csv

import csv
from nltk.tokenize import RegexpTokenizer
from stop_words import get_stop_words
from nltk.stem.porter import PorterStemmer
import csv
import warnings
import re
import nltk
import nltk.data
warnings.filterwarnings("ignore")
import ast

def InitializeWords():
    wordlist = 'wordlist.txt' # A file containing common english words
    content = None
    with open(wordlist) as f:
        content = f.readlines()
    return [word.rstrip('\n') for word in content]


def ParseSentence(sentence, wordlist):
    new_sentence = "" # output
    terms = sentence.split(' ')
    for term in terms:
        if term[0] == '#': # this is hashtag, parse it
            new_sentence += ParseTag(term, wordlist)
        else: # Just append the word
            new_sentence += term
        new_sentence += " "

    return new_sentence


# Define a function to split a review into parsed sentences
def review_to_sentences( review, tokenizer, remove_stopwords=False ):
    # Function to split a review into parsed sentences. Returns a
    # list of sentences, where each sentence is a list of words
    #
    # 1. Use the NLTK tokenizer to split the paragraph into sentences
    raw_sentences = tokenizer.tokenize(review.strip())
    #
    # 2. Loop over each sentence
    sentences = []
    for raw_sentence in raw_sentences:
        # If a sentence is empty, skip it
        if len(raw_sentence) > 0:
            # Otherwise, call review_to_wordlist to get a list of words
            sentences.append(  raw_sentence )
    #
    # Return the list of sentences (each sentence is a list of words,
    # so this returns a list of lists
    return sentences

def ParseTag(term, wordlist):
    words = []
    # Remove hashtag, split by dash
    tags = term[1:].split('-')
    for tag in tags:
        word = FindWord(tag, wordlist)
        while word != None and len(tag) > 0:
            words += [word]
            if len(tag) == len(word): # Special case for when eating rest of word
                break
            tag = tag[len(word):]
            word = FindWord(tag, wordlist)
    return " ".join(words)

def FindWord(token, wordlist):
    i = len(token) + 1
    while i > 1:
        i -= 1
        if token[:i] in wordlist:
            return token[:i]
    return None



wordlist = InitializeWords()




data=[]
with open('imdbdataset.csv', 'rb') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',')
    for row in spamreader:
        data.append(row)
texts=[]

tokenizer2 = RegexpTokenizer(r'#\w+|\w+')

# create English stop words list
en_stop = get_stop_words('en')

# Create p_stemmer of class PorterStemmer
p_stemmer = PorterStemmer()


for dati in data:
    raw = dati[2].lower()
    raw = ''.join([i if ord(i) < 128 else ' ' for i in raw])
    tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
    sentences=review_to_sentences(raw,tokenizer)
    # for ii in sentences:
    #     print ii
    obj=[]
    for iii in sentences:
        iii = iii.replace('\n','')
        tokens = tokenizer2.tokenize(iii)
        # remove stop words from tokens
        stopped_tokens = [i for i in tokens if not i in en_stop]
        stp = [re.sub("[0-9]", "", i) for i in stopped_tokens if not i.isdigit()]
        stp2 = [i for i in stp if len(i)!=1]
        # stem tokens
        #stemmed_tokens = [p_stemmer.stem(i) for i in stp2]
        # add tokens to list

        #print stp2
        netSentence=''
        for kk in stp2:
            if(kk[0]=='#'):
                tt=ParseSentence(kk, wordlist)
                netSentence = netSentence + ' '+ tt + ' '
            else:
                netSentence = netSentence + ' ' + kk + ' '
        #print(netSentence)
        #print netSentence
        netSentence = tokenizer2.tokenize(netSentence)
        #print netSentence
        #print netSentence
        obj.append(netSentence)
    #print  obj
    dati[2] = obj

# for kk in data:
#     print kk[2]



list=['animation','drama','sci-fi','comedy','mystery','thriller','romance','family','horror','war','biographic','musical','western','adult','history','action','crime','adventure','documentary','fantasy','music','sport']
genre = {}
comedy_list = []
ppp='sport'
for i in range(len(data)):
    val = ast.literal_eval(data[i][1])
    newGen=[]
    for j in val:
        for k in list:
            if(str(j).lower().find(k)>-1):
                newGen.append(k)
    if (ppp in newGen):
        for z in data[i][2]:
            abc = (' ').join(z)
            comedy_list.append(abc)
            # print comedy_list
    data[i][1]=newGen

for i in range(len(comedy_list)):
    print comedy_list[i]
    print len(comedy_list)


resultFile = open(ppp+".txt",'w')
for kk in comedy_list:
    resultFile.write(kk)
    resultFile.write('\n')
resultFile.close()