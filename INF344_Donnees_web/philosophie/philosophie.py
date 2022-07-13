#!/usr/bin/python3
# -*- coding: utf-8 -*-

from flask import Flask, render_template, session, request, redirect, flash, url_for
from graphviz import render
from getpage import getPage
import secrets

app = Flask(__name__)

app.secret_key = secrets.token_hex()

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

# Si vous définissez de nouvelles routes, faites-le ici

@app.route('/game', methods=['GET'])
def game():
    if not session.get("article"):
        return redirect(url_for('index'))
    try:
        title, refs = getPage(session["article"])
    except:
        flash(f"La page demandée n'existe pas. Recommencez.", category="ERREUR")
        return redirect(url_for('index'))
    if title=="Philosophie":
        if session["score"]==0:
            flash(f"Vous avez commencé directement à la page philosophie. Recommencez.", category="ERREUR")
        else:
            flash(f"Vous êtes le dernier dionysiaque... Score : {session['score']}", category="VICTOIRE")
        return redirect(url_for('index'))
    elif len(refs)==0:
        flash(f"Pas de lien sur cette page. Recommencez.", category="ERREUR")
        return redirect(url_for('index'))
    session["refs"] = refs
    return render_template('game.html', title=title, refs=refs, len=len(refs))

@app.route('/new-game', methods=['POST','GET'])
def newgame():
    if request.method == "POST":
        session["score"] = 0
        session["article"] = request.form["start"]
        return redirect(url_for('game'))
    else:
        return redirect(url_for('index'))

@app.route('/move', methods=['POST','GET'])
def move():
    if request.method == "POST":
        if int(request.form["nocheat"])!=session["score"]:
            flash(f"Pas de parties parallèles.", category="AVERTISSEMENT")
            return redirect(url_for('game'))
        if request.form["destination"] not in session["refs"]:
            flash(f"Choisissez parmi les options ci-dessous.", category="AVERTISSEMENT")
            return redirect(url_for('game'))
        session["score"] += 1
        session["article"] = request.form["destination"]
        return redirect(url_for('game'))
    else:
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)

