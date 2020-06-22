import nltk
import sys
import os
import string
import copy
import numpy as np

FILE_MATCHES = 1
SENTENCE_MATCHES = 1


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1])
    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }
    file_idfs = compute_idfs(file_words)

    # Prompt user for query
    query = set(tokenize(input("Query: ")))

    # Determine top file matches according to TF-IDF
    filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

    # Extract sentences from top files
    sentences = dict()
    for filename in filenames:
        for passage in files[filename].split("\n"):
            for sentence in nltk.sent_tokenize(passage):
                tokens = tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens

    # Compute IDF values across sentences
    idfs = compute_idfs(sentences)

    # Determine top sentence matches
    matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
    for match in matches:
        print(match)


def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """
    fileDict = {}
    files = os.listdir(directory)
    for f in files:
        fpath = os.path.join(directory, f)
        with open(fpath) as myFile:
            text = myFile.read()
        fileDict[f] = text
    return fileDict


def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    nltk.download('punkt')
    nltk.download('stopwords')
    wordList = nltk.word_tokenize(document)
    punctuation = string.punctuation
    stopWords = nltk.corpus.stopwords.words("english")
    listCopy = copy.deepcopy(wordList)
    for w in listCopy:
        if w in stopWords or w in punctuation:
            newList = list(filter(w.__ne__, wordList))
            wordList = newList
    return wordList

def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """
    dictLen = len(documents)
    words_idf = {}
    for name in documents:
        words = documents[name]
        for w in words:
            if w in words_idf:
                continue
            wFreqncy = 0
            for n in documents:
                if w in documents[n]:
                    wFreqncy += 1
            words_idf[w] = np.log(dictLen/wFreqncy)
    return words_idf

def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """
    ranking = {}
    for f in files:
        currentSum = 0
        for word in query:
            currentSum += files[f].count(word) * idfs[word]
        ranking[f] = currentSum
    sortedRank = sorted(ranking.keys(), key=lambda x: ranking[x], reverse=True)
    return sortedRank[:n]
    

def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    ranking = {}
    qtm = {}

    for s in sentences:
        value = 0
        # Calculate qtm for each sentence
        for w in sentences[s]:
            if w in query:
                value += 1
        qtm[s] = value/len(sentences[s])
        # calculate sum of idfs for each sentence
        value = 0
        for word in query:
            if word in sentences[s]:
                value += idfs[word]
        ranking[s] = value
    # sort the ranking according to the values
    sortedRank = sorted(ranking.items(), key=lambda x: x[1], reverse=True)
    for i, s in enumerate(sortedRank):
        if i == len(sortedRank)-1:
            break
        if s[1] == sortedRank[i+1][1]:
            if qtm[s[0]] < qtm[sortedRank[i+1][0]]:
                sortedRank[i], sortedRank[i+1] = sortedRank[i+1], sortedRank[i]
    finalRank = []
    for j,s in enumerate(sortedRank):
        if j == n:
            break
        finalRank.append(s[0])
    return finalRank


if __name__ == "__main__":
    main()
