#!/usr/bin/python3
# -*- coding: utf-8 -*-

from flask import Flask, render_template, session, request, redirect, flash
from query import main_query
import secrets
import sqlite3

app = Flask(__name__)

app.secret_key = secrets.token_hex() # générer un identifiant de session unique

# Vérifier l'existence des index et tables SQL, sinon les créer
conn = sqlite3.connect('data.db') 
tables = {row[0] for row in conn.execute("SELECT name FROM sqlite_master WHERE type='table';")}
if "inverted_index" in tables and "idf" in tables and "pagerank" in tables:
    tf_exists = [row[0] for row in conn.execute("SELECT COUNT(*) FROM inverted_index;")]
    idf_exists = [row[0] for row in conn.execute("SELECT COUNT(*) FROM idf;")]
    if int(tf_exists[0]) == 0 or int(idf_exists[0]) == 0:
        exec(open("index.py").read())
    pagerank_exists = [row[0] for row in conn.execute("SELECT COUNT(*) FROM pagerank;")]
    if int(pagerank_exists[0]) == 0:
        exec(open("pagerank.py").read())
else:
    exec(open("index.py").read())
    exec(open("pagerank.py").read())
conn.close()
conn = sqlite3.connect('data.db') 
print("tf:",[row[0] for row in conn.execute("SELECT COUNT(*) FROM inverted_index;")])
print("idf:",[row[0] for row in conn.execute("SELECT COUNT(*) FROM idf;")])
conn.close()

@app.route('/', methods=['GET'])
def index():
    session['query'] = None
    session['method'] = None
    return render_template('index.html')


@app.route('/query', methods=['POST']) 
def query():
    session['query'] = request.form['query']
    session['method'] = request.form['method']
    res = main_query(session['query'], session['method'])

    if res:
        session["results"] = res
        return render_template('query.html')
    else:
        flash("""La recherche ne renvoie pas de résultat.""", category='error')
        return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)

