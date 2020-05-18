#!/usr/bin/python3
# -*- coding: utf-8 -*-

from flask import Flask, render_template, session, request, redirect, flash
#from getpage import getPage
import getpage

app = Flask(__name__)

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

source = ''

@app.route('/', methods=['GET'])
def index():
    # question 3.9
    session['score'] = 0
    
    # question 5.1
    
    return render_template('index.html', message="Nouvelle partie!")

# Si vous définissez de nouvelles routes, faites-le ici

# 3.3
@app.route('/new_game',methods=['POST'])
def new_game():
    start_page = request.form['start']     # 'start' = name du label et non pas l'id
    session['article'] = start_page
    
    if source == 'game':
        flash('Perdu, on ne joue pas avec 2 onglets', 'error')
        return redirect('/')
        
    return redirect('/game')

# 3.4
@app.route('/game', methods=['GET'])
def game():
    
    session['score'] = session['score'] + 1
    
    
    titre, liens = getpage.getPage(session['article'])
    
    
        # 3.8 et 5.3?
    if titre =='Philosophie':
        flash('GAGNÉ!!! Page Philosophie atteinte avec le score: '+ str(session['score']), 'success') # question 3.9
        return redirect('/')
        # 5.2 + 5.3
    elif titre == None or liens==[]:
        flash("Perdu! la page n'existe pas", 'error')
        return redirect('/')
    else:
        session['liens']= liens
        return render_template('game.html')

# 3.7
@app.route('/move', methods=['GET', 'POST'])
def move():
    
    radiobouton = request.form['destination']   # radiobutton sur lequel l'utilisateur a cliqué
    session['article'] = radiobouton
   
    source ='game'
    
    return redirect('/game')


if __name__ == '__main__':
    app.run(debug=True)   # permet de modifier le fichier html sans être obligé de redémarrer le py

