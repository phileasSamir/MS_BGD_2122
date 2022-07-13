#!/usr/bin/python3
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
from json import loads
from urllib.request import urlopen
from urllib.parse import urlencode
import urllib.parse
import ssl

cache = {}

def getJSON(page):
    params = urlencode({
      'format': 'json',  
      'action': 'parse',  
      'prop': 'text',  
      'redirects': 'true',
      'page': page})
    API = "http://fr.wikipedia.org/w/api.php" 
    # désactivation de la vérification SSL pour contourner un problème sur le
    # serveur d'évaluation -- ne pas modifier
    gcontext = ssl.SSLContext()
    response = urlopen(API + "?" + params, context=gcontext)
    return response.read().decode('utf-8')


def getRawPage(page):
    parsed = loads(getJSON(page))
    try:
        title = parsed["parse"]["title"] 
        content = parsed["parse"]["text"]["*"]
        return title, content
    except KeyError:
        # La page demandée n'existe pas
        return None, None


def getPage(page):
    if cache.get(page):
        return cache[page]
    title, content = getRawPage(page)
    soup = BeautifulSoup(content, 'html.parser')
    refs = [x.get('href') for p in soup.find('div').find_all('p', recursive=False) for x in p.find_all('a', recursive=True) 
            if x.get("href") and x.get("class") != "external autonumber".split() and "redlink" not in x.get("href")]
    refs = [ref.split("#")[0] for ref in refs if ref[0]!="#" and ":" not in ref]
    final_refs = []
    i = 0
    while len(final_refs)<10 and i<len(refs):
        x = urllib.parse.unquote(refs[i]).replace("_", " ").replace("/wiki/", "")
        if x not in final_refs:
            final_refs.append(x)
        i+=1
    cache[page] = title, final_refs
    return title, final_refs


if __name__ == '__main__':
    # Ce code est exécuté lorsque l'on exécute le fichier
    print("Ça fonctionne !")
    
    # Voici des idées pour tester vos fonctions :
    # print(getJSON("Utilisateur:A3nm/INF344"))
    print(getPage("Fondo Strategico Italiano"))
    # print(getRawPage("Histoire"))