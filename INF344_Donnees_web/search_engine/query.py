#!/usr/bin/env python3
import sys
import sqlite3

from numpy import Infinity
from shared import extractText, stem, extractListOfWords
from bs4 import BeautifulSoup as bs

import nltk
from nltk.corpus import stopwords
nltk.download("stopwords")
from nltk.stem.snowball import FrenchStemmer
stemmer = FrenchStemmer()
french_stopwords = set(stopwords.words('french'))

# compute best query solution and output them
def best_query_tfidf(queryWords, conn):
    dict_results = {}
    idfreqs = {w:row[0] for w in queryWords for row in conn.execute("SELECT idfreq FROM idf WHERE word=?", (w,))}

    idfreqs = sorted(idfreqs.items(), key=lambda item: item[1])[::-1]

    for w, idfreq in idfreqs:
        for row in conn.execute("SELECT url, freq FROM inverted_index WHERE word=?", (w,)):
            if row[0] in dict_results:
                dict_results[row[0]]+=idfreq*row[1]
            else:
                dict_results[row[0]]=idfreq*row[1]

    results = {k:v for k,v in sorted(dict_results.items(), key=lambda item: item[1])[::-1][:20]}

    for url in results.keys():
        for row in conn.execute("SELECT * FROM webpages WHERE URL=?", (url,)):
            content = row[0]
            txt = [stemmer.stem(w) for w in extractText(content).split()]
            if all([w in txt for w in queryWords]):
                
                res = float("inf")
                l = 0
                setquery = set(queryWords)
                for r in range(len(txt)):
                    if len(setquery-set(txt[l:r])) == 0:
                        res = min(res, r - l + 1)
                    while len(setquery-set(txt[l:r])) == 0:
                        l += 1
                results[url] *= 1+(1/res)

            """cnt = 0
            for w in queryWords:
                if w in content:
                    cnt += 1
            results[url] *= (cnt**2)
            soup = bs(content, 'html.parser')
            if soup.title:
                title = soup.title.string
                if title:
                    for word in queryWords:
                        if word in title:
                            results[url]*=1.1 # Pondération choisie arbitrairement"""

    results = sorted(dict_results.items(), key=lambda item: item[1])[::-1]
            
    return results[:10]

def best_query_pagerank(queryWords, conn):
    dict_results = {}
    idfreqs = {w:row[0] for w in queryWords for row in conn.execute("SELECT idfreq FROM idf WHERE word=?", (w,))}

    idfreqs = sorted(idfreqs.items(), key=lambda item: item[1])[::-1]

    for w, idfreq in idfreqs:
        for row in conn.execute("SELECT url, freq FROM inverted_index WHERE word=?", (w,)):
            if row[0] in dict_results:
                dict_results[row[0]]+=idfreq*row[1]
            else:
                dict_results[row[0]]=idfreq*row[1]
    
    for k in dict_results.keys():
        for row in conn.execute("SELECT score FROM pagerank WHERE url=?", (k,)):
            dict_results[k]*=row[0] ** .5

    results = {k:v for k,v in sorted(dict_results.items(), key=lambda item: item[1])[::-1][:20]}

    for url in results.keys():
        for row in conn.execute("SELECT * FROM webpages WHERE URL=?", (url,)):
            content = row[0]
            txt = [stemmer.stem(w) for w in extractText(content).split()]
            if all([w in txt for w in queryWords]):
                
                res = float("inf")
                l = 0
                setquery = set(queryWords)
                for r in range(len(txt)):
                    if len(setquery-set(txt[l:r])) == 0:
                        res = min(res, r - l + 1)
                    while len(setquery-set(txt[l:r])) == 0:
                        l += 1
                results[url] *= 1+(1/res)

            """cnt = 0
            for w in queryWords:
                if w in content:
                    cnt += 1
            results[url] *= (cnt**2)
            soup = bs(content, 'html.parser')
            if soup.title:
                title = soup.title.string
                if title:
                    for word in queryWords:
                        if word in title:
                            results[url]*=1.1 # Pondération choisie arbitrairement"""

    results = sorted(dict_results.items(), key=lambda item: item[1])[::-1]

    return results[:10]

def main_query(query, method):
    conn = sqlite3.connect('data.db')
    # cursor = conn.cursor()
    # queryWords = [stem(w) for w in query.split()]
    queryWords = [stemmer.stem(w) for w in query.split() if w.lower() not in french_stopwords]
    
    # Bloc réel, ne fonctionne pas chez moi (pb de sql)
    if method=="tfidf":
        results = best_query_tfidf(queryWords, conn)
    elif method=="pagerank":
        results = best_query_pagerank(queryWords, conn)
    else: pass
    
    if len(results)==0 : return None # Pour voir une notification d'absence de résultat
    else :
        res_list = []
        # parsing
        for res in results:
            url = res[0] 
            for row in conn.execute("SELECT * FROM webpages WHERE URL=?", (url,)):
                content = row[0]
                soup = bs(content, 'html.parser')
                if soup.title:
                    title = soup.title.string
                else: title = url
                resume = ""
                for p in soup.find_all("p"):
                    if p:
                        resume = "".join(p.find_all(text=True))
                        break
                res_list.append((url, title, resume))
        conn.close()
        return res_list
    
    # Dummy - pour tester l'interface
    """if query == "NONE":
        return None # pour voir une notification "pas de résultat"
    else :
        url = "https://wiki.jachiet.com/wikipedia_fr_mathematics_nopic_2020-04/A/Notices_of_the_American_Mathematical_Society"
        title = "Notices of the American Mathematical Society"
        resume = 'Notices of the American Mathematical Society Mathématiques par Wikipédia Notices of the American Mathematical Society Les Notices of the American Mathematical Society sont l une des publications périodiques de l American Mathematical Society AMS Elles sont publiées mensuellement sauf pour le numéro '
        
        return [(url, title, resume) for _ in range(10)]"""

if __name__ == "__main__":
    query = input("What are you looking for ?\n")
    # queryWords = [stem(w) for w in query.split()]
    queryWords = [stemmer.stem(w) for w in query.split() if w.lower() not in french_stopwords]

    conn = sqlite3.connect('data.db') 
    cursor = conn.cursor()
    
    if len(sys.argv)!=2:
        print("Invalid number of arguments")
        print("Usage: 'python query.py {tfidf/pagerank}'")
        exit()
    if sys.argv[1]=="tfidf":
        for i, result in enumerate(best_query_tfidf(queryWords, conn)):
            print(f"{i}:",result[0])
    elif sys.argv[1]=="pagerank":
        for i, result in enumerate(best_query_pagerank(queryWords, conn)):
            print(f"{i}:",result[0])
    else:
        print("Please provide a valid ranking metric")
    exit()