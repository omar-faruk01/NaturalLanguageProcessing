# package imports
import argparse
import pandas as pd
import nltk
import ssl
from nltk.stem.porter import *
import matplotlib.pyplot as plt

# arguements for running the program
parser = argparse.ArgumentParser()
parser.add_argument("filename", help="filename that will be read", type=str)
parser.add_argument("-l","--lower", help="text normalization step of lowecasing", action="store_true")
parser.add_argument("-s","--stem", help="text normalization step of stemming", action="store_true")
parser.add_argument("-w","--stopwords", help="text normalization step of stopword removal", action="store_true")
parser.add_argument("-p","--punctuation", help="text normalization step of punctuation removal", action="store_true")


args = parser.parse_args()

print("filename: " + args.filename)

    
# opening the text file and storing as object
File_object = open(args.filename, 'r')

# simple tokenization
tokens = File_object.read().split()

# lowercase the tokens
if args.lower:
    print("lowercase normalization step selected")
    for i, token in enumerate(tokens):
        tokens[i] = token.lower()
    #print(tokens)
    
# remove punctuation from tokens
# ref: https://www.geeksforgeeks.org/python-remove-punctuation-from-string/
if args.punctuation:
    print("punctuation removal normalization step selected")
    # initializing punctuations string
    punctuations = '''!()-[]{};:'"\,<>./?@#$%^&*_~‘'''
    
    for i, token in enumerate(tokens):
        for elem in token:
            if elem in punctuations:
                tokens[i] = token.replace(elem, "")
    
    # print(tokens)

# remove stop words from tokens
if args.stopwords:
    print("stopword removal normalization step selected")
    
    # downloading stopwords from nltk
    try:
        _create_unverified_https_context = ssl._create_unverified_context
    except AttributeError:
        pass
    else:
        ssl._create_default_https_context = _create_unverified_https_context

    nltk.download('stopwords')
    stopwords = set(nltk.corpus.stopwords.words('english'))
    
    #removing stopwords from tokens list
    tokens = [token for token in tokens if token not in stopwords]    

# stemmatize the tokens
if args.stem:
    print("stemming normalization step selected")
    stemmer = PorterStemmer()
    tokens = [stemmer.stem(token) for token in tokens]
    # print(' '.join(tokens))
    

# close the file
File_object.close()

# element occurance count output using pandas series
series= pd.Series(tokens).value_counts()
print("Highest 10 occurances")
print(series[:10])
print("lowest 10 occurances")
print(series[-10:])

# visualization using matplotlib
plt.plot(series.index, series.values)
plt.xlabel("tokens")
plt.ylabel("count")
plt.title("Counting Tokens")
plt.xlim(0, 70)
plt.xticks(rotation=70)
# plt.locator_params(axis='x', nbins=100)
# plt.locator_params(axis='y', nbins=15)
plt.show(block=True)