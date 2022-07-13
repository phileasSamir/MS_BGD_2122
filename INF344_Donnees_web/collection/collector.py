# -*- coding: utf-8 -*-
# écrit par Jean-Claude Moissinac, structure du code par Julien Romero

from sys import argv
import sys
from bs4 import BeautifulSoup
import itertools
import re
import ssl
if (sys.version_info > (3, 0)):
    from urllib.request import urlopen
    from urllib.parse import urlencode
else:
    from urllib2 import urlopen
    from urllib import urlencode

class Collecte:
    """pour pratiquer plusieurs méthodes de collecte de données"""

    def __init__(self):
        """__init__
        Initialise la session de collecte
        :return: Object of class Collecte
        """
        # DO NOT MODIFY
        self.basename = "collecte.step"

    def collectes(self):
        """collectes
        Plusieurs étapes de collectes. VOTRE CODE VA VENIR CI-DESSOUS
        COMPLETER les méthodes stepX.
        """
        self.step0()
        self.step1()
        self.step2()
        self.step3()
        self.step4()
        self.step5()
        self.step6()

    def step0(self):
        # cette étape ne sert qu'à valider que tout est en ordre; rien à coder
        stepfilename = self.basename+"0"
        self.name = "samir-20"
        print("Comment :=>> Validation de la configuration")
        with open(stepfilename, "w", encoding="utf-8") as resfile:
            resfile.write(self.name)
        
    def step1(self):
        stepfilename = self.basename+"1"
        self.unsecurecontext = ssl._create_unverified_context() # ne pas modifier
        result = urlopen("http://www.freepatentsonline.com/result.html?sort=relevance&srch=top&query_txt=video&submit=&patents=on", context=self.unsecurecontext).read().decode()        
        with open(stepfilename, "w", encoding="utf-8") as resfile:
            resfile.write(result)
        
    def step2(self):
        stepfilename = self.basename+"2"
        soup = BeautifulSoup(open(self.basename+"1", "r").read())
        links = [a["href"] for a in soup.find_all("a", href=True)]
        result = "\n".join(links)
        with open(stepfilename, "w", encoding="utf-8") as resfile:
            resfile.write(result)
        
    def linksfilter(self, links):
        eliminate = ["/", 
                    "/services.html", 
                    "/contact.html", 
                    "/privacy.html", 
                    "/register.html", 
                    "/tools-resources.html", 
                    "https://twitter.com/FPOCommunity", 
                    "http://www.linkedin.com/groups/FPO-Community-4524797", 
                    "http://www.sumobrainsolutions.com/"]
        filterout = ["result.html","http://research","/search.html"]
        flinks = [link for link in links 
                  if link not in eliminate 
                  and not any([link.startswith(x) for x in filterout])]
        return flinks
        
    def step3(self):
        stepfilename = self.basename+"3"
        result = "\n".join(
            sorted(
                self.linksfilter(
                    open(self.basename+"2", "r").read().split("\n")
                    )
                )
            )
        with open(stepfilename, "w", encoding="utf-8") as resfile:
            resfile.write(result)
        
    def step4(self):
        stepfilename = self.basename+"4"
        links = [[a["href"] for a in BeautifulSoup(urlopen("http://www.freepatentsonline.com/"+x, context=self.unsecurecontext).read().decode()).find_all("a",href=True)] 
                for x in open(self.basename+"3","r").read().split("\n")[:10]]
        links = list(itertools.chain.from_iterable(links))
        result = "\n".join(sorted(self.linksfilter(links)))
        with open(stepfilename, "w", encoding="utf-8") as resfile:
            resfile.write(result)
        
    def contentfilter(self, link):
        soup = BeautifulSoup(urlopen("http://www.freepatentsonline.com/"+link, context=self.unsecurecontext).read().decode())
        inventors = soup.find_all(text=re.compile('Inventors:'))
        title = soup.find_all(text=re.compile('Title:'))
        app = soup.find_all(text=re.compile('Application Number:'))
        if inventors and title and app:
            return True
        else:
            return False

    def step5(self):
        stepfilename = self.basename+"5"
        testlinks = open(self.basename+"4","r").read().split("\n")
        result = []
        i = 0
        while len(result)<10:
            if testlinks[i].endswith("html"):
                if self.contentfilter(testlinks[i]):
                    result.append(testlinks[i])
            i += 1
        result = "\n".join(sorted(result))
        with open(stepfilename, "w", encoding="utf-8") as resfile:
            resfile.write(result)
        
    def step6(self):
        stepfilename = self.basename+"6"
        result = []
        for link in open(self.basename+"5", "r").read().split("\n"):
            soup = BeautifulSoup(urlopen("http://www.freepatentsonline.com/"+link, context=self.unsecurecontext).read().decode())
            inventors = soup.find_all(text=re.compile('Inventors:'))
            divs = [inventor.parent.parent for inventor in inventors]
            for d in divs[0].descendants:
                if d.name == 'div' and d.get('class', '') == ['disp_elm_text']:
                    result.append("\n".join([x.strip()for x in d.text.split("\n") if x.strip()]))
        result = "\n".join(result)
        with open(stepfilename, "w", encoding="utf-8") as resfile:
            resfile.write(result)
        
if __name__ == "__main__":
    collecte = Collecte()
    collecte.collectes()
