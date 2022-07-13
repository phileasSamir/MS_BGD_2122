#!/usr/bin/env python3

import sqlite3
from math import log
from shared import extractListOfWords, stem

import nltk
from nltk.corpus import stopwords
nltk.download("stopwords")
from nltk.stem.snowball import FrenchStemmer
stemmer = FrenchStemmer()
french_stopwords = set(stopwords.words('french'))

conn = sqlite3.connect('data.db')

def countFreq(L:list):
    cnter = {}
    for w in L:
        if w.lower() not in french_stopwords:
            # w = stem(w)
            w = stemmer.stem(w)
            if w: # filter empty strings
                if w in cnter:
                    cnter[w]+=1
                else:
                    cnter[w]=1
    return list(cnter.items())

def idf(nw): 
    return log(N/nw)

if __name__=="__main__":
    for row in conn.execute("SELECT COUNT(*) FROM webpages"):
        N = row[0]
    # compute the inverted index and the idf and store them
    conn.execute("DROP TABLE IF EXISTS inverted_index")
    conn.execute("CREATE TABLE inverted_index (word TEXT, url TEXT, freq REAL)")

    for row in conn.execute("SELECT * FROM webpages"):
        for w, f in countFreq(extractListOfWords(row[0])):
            conn.execute("INSERT INTO inverted_index(word,url,freq) VALUES(?,?,?)", (w,row[1],f))

    conn.execute("DROP TABLE IF EXISTS idf")
    conn.execute("CREATE TABLE idf (word TEXT, idfreq REAL)")

    for row in conn.execute("SELECT word, COUNT(*) FROM inverted_index GROUP BY word"):
        conn.execute("INSERT INTO idf(word,idfreq) VALUES(?,?)", (row[0],idf(row[1])))

    conn.commit()
    conn.close()
