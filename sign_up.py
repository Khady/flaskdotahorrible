#!/usr/bin/env python2
#-*- encoding: utf-8 -*-

from __future__ import with_statement
import sqlite3
import time
import random
import string

from contextlib import closing
from flask import request, session, g, redirect, url_for, \
     abort, render_template, flash
from hashlib import sha1
import Mail
from dota2 import app

def connect_db(base):
    return sqlite3.connect(base)

def random_string(length=None):
    chars = string.letters + string.digits
    length = length or random.randint(6,24)
    return ''.join(random.sample(chars, length))

def valid_user(code_val):
    cur = g.db.execute('select id from user_validation where code_val == ?', [code_val])
    entries = [dict(user_id=row[0]) for row in cur.fetchall()]
    if len(entries) != 0:
        g.db.execute('update user_description set valid = 1 where id == ?', [entries[0]['user_id']])
        g.db.execute('delete from user_validation where id == ?',  [entries[0]['user_id']])
        g.db.commit()
        flash("Compte vient d'etre activer")
        return redirect(url_for('default'))
    else:
        flash("code d'activation invalide")
        return render_template('activate.html')


@app.route('/activate')
@app.route('/activate/<code_val>')
def activate(code_val=None):
    g.db = connect_db(app.config['USER_DB'])
    if (request.method == 'GET' and code_val != None):
        return valid_user(code_val)
    elif request.method == 'POST':
        code_val = request.form['code_val']
        return valid_user(code_val)
    else:
        return render_template('activate.html')

@app.route('/signup', methods=['GET', 'POST'])
def add_user():
    error = None
    # if session.get('logged_in'):
    #     error = 'You are already member'
    #     return render_template('sign_up.html', error=error)
    if request.method == 'POST':
        g.db = connect_db(app.config['USER_DB'])

        # Recupere les informations de l'utilisateur dans la page
        login = request.form['login']
        password = request.form['password']
        pass_hash = sha1(password.encode('utf-8')).hexdigest()
        mail = request.form['mail'].lower()
        date = time.strftime('%Y-%m-%d',time.localtime())

        # verifie la validite des informations
        users = g.db.execute("select login, mail from user_description")
        entries = [dict(login=row[0], mail=row[1]) for row in users.fetchall()]
        for elem in entries:
            error = ''
            if login.lower() == elem['login'].lower():
                error = ' Identifiant deja existant '
                break
            elif mail == elem['mail'].lower():
                error += 'Adresse mail deja existant '
                break
            else:
                error = None
        if password == "":
            error = 'Password incorrect'

        if error != None:
            return render_template('sign_up.html', error=error)

        # met les informations dans la DB
        g.db.execute("insert into user_description ('login', 'hash', 'date_create', \
'mail', 'avatar', 'valid') values (?, ?, ?, ?, ?, ?)",
                     [login, pass_hash, date, mail, None, 0])
        g.db.commit()

        # on ajoute le code de validation
        code_val = random_string()
        cur = g.db.execute("select id from user_description where login == ?", [login])
        entries = [dict(user_id=row[0]) for row in cur.fetchall()]
        g.db.execute("insert into user_validation ('id', 'code_val') values (?, ?)",
                     [entries[0]['user_id'], code_val])
        g.db.commit()
        # on donne le code a l'utilisateur
        #Mail.send(mail, "Validation compte Dota 2 Arena",
        #          ("Voici votre url d'activation\nhttp://dota2arena.com%s\n" % url_for('activate', code_val = code_val)))
        print    ("Voici votre url d'activation\nhttp://dota2-arena.com%s\n" % url_for('activate', code_val = code_val))

        g.db.close()
        flash('Bienvenue sur Dota 2 Arena !')
        return redirect(url_for('login'))
    return render_template('sign_up.html', error=error)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'logged_in' in session:
        flash('Vous etes deja connecte')
        return redirect(url_for('default'))
    error = None
    if request.method == 'POST':
        g.db = connect_db(app.config['USER_DB'])

        # on recupere les infos
        login = request.form['login']
        password = request.form['password']
        pass_hash = sha1(password.encode('utf-8')).hexdigest()

        # on regarde si le login et mdp sont OK
        cur = g.db.execute("select id, login, hash from user_description where valid == 1")
        entries = [dict(user=row[0], login=row[1], hash_bd=row[2]) for row in cur.fetchall()]
        for elem in entries:
            if login.lower() == elem['login'].lower() and pass_hash == elem['hash_bd']:
                session['logged_in'] = True
                session['user_login'] = elem['login']
                session['user_id'] = elem['user']
                flash('Vous etes maintenant connecte')
                g.db.close()
                return redirect(url_for('default'))
    
        # probleme dans l'identification
        error="Identifiant ou mot de passe invalide"

    return render_template('login.html', error=error)


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.pop('logged_in', None)
    flash('Vous venez de vous deconnecter')
    return redirect(url_for('default'))
