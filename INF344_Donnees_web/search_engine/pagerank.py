import sqlite3
from shared import extractText, neighbors

conn = sqlite3.connect('data.db', check_same_thread=False)
cursor = conn.cursor()

#compute and store pagerank

# realURL = {queryURL : respURL}
realURL = {}
for row in conn.execute("SELECT * FROM responses") :
    realURL[row[0]] = row[1]

# pointsTo : {respURL : neighbors(content) au format [queryURL, ..., queryURL]}
pointsTo = {}
for row in conn.execute("SELECT * FROM webpages") :
    pointsTo[row[1]] = neighbors(row[0],row[1])
pointsTo = {key: [realURL[element] for element in value] 
           for key,value in pointsTo.items()}

# Algo PageRank
a = 0.15
n_iter = 50
nb_pages = len(pointsTo)

score = {page:1/nb_pages for page in pointsTo.keys()}

for i in range(n_iter):
    nouveau_score = {page:0 for page in pointsTo.keys()}
    proba_teleportation = 0
    
    # Sauts de page en page
    for page, liens in pointsTo.items():
        nb_liens = len(liens)
        if nb_liens > 0 :
            proba_teleportation += score[page] * a
            for lien in liens:
                nouveau_score[lien] += score[page] * (1-a) / nb_liens
        else: 
            proba_teleportation += score[page]
    # Téléportations
    for page, liens in pointsTo.items():
        nouveau_score[page] += proba_teleportation / nb_pages
    score = nouveau_score

conn.execute("DROP TABLE IF EXISTS pagerank")
conn.execute("CREATE TABLE pagerank (url TEXT, score REAL)")

for row in conn.execute("SELECT * FROM webpages"):
    url = row[1]
    conn.execute("INSERT INTO pagerank(url,score) VALUES(?,?)", (url,score[url]))

conn.commit()
conn.close()

    
