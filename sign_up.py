#!/usr/bin/env python2
#-*- encoding: utf-8 -*-
from __future__ import with_statement
import sqlite3
import time

from contextlib import closing
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash
from hashlib import sha1

# configuration
USER_DB = '/tmp/test.bd'
DEBUG = True
SECRET_KEY = 'development key'

# create our little application :)
app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

def connect_db(base):
    return sqlite3.connect(base)

@app.route('/', methods=['GET'])
def default():
    return render_template('sign_up.html', error=None)

@app.route('/signup', methods=['GET', 'POST'])
def add_user():
    error = None
    if request.method == 'POST':
        connect_db(app.config['USER_DB'])
        if session.get('logged_in'):
            error = 'You are already member'
            return render_template('sign_up.html', error=error)

        # Recupere les informations de l'utilisateur dans la page
        login = request.form['login']
        password = request.form['password']
        pass_hash = sha1(password.encode('utf-8')).hexdigest()
        mail = request.form['mail'].lower()
        date = time.strftime('%Y-%m-%d',time.localtime())

        # verifie la validite des informations
        users = g.db.execute("select 'login', 'mail' from user_description")
        entries = [dict(login=row[0], mail=row[1]) for row in users.fetchall()]
        for elem in entries:
            error = ""        
            if login.lower() == elem['login'].lower():
                error = "login already exist "
                break
            elif mail == elem['mail'].lower():
                error += "mail already exist"
                break
            else:
                error = None

        if error != None:
            return render_template('sign_up.html', error=error)

        # met les informations dans la DB
        g.db.execute("insert into user_description ('login', 'hash', 'date_create', \
'mail', 'avatar', 'valid') values (?, ?, ?, ?, ?, ?)",
                     [login, pass_hash, date, mail, None, 1])
        g.db.commit()
        g.db.close()
    
        flash('Welcome to Dota 2 Arena')
        return redirect(url_for('login'))
    
    return render_template('sign_up.html', error=error)


@app.route('/activate', methods=['GET', 'POST'])
def activate_user():
    return redirect(url_for('/'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        connect_db(app.config['USER_DB'])

        # on recupere les infos
        login = request.form['login']
        password = request.form['password']
        pass_hash = sha1(password.encode('utf-8')).hexdigest()

        # on regarde si le login et mdp sont OK
        cur = g.db.execute("select 'login', 'hash' from user_description where valid == 1")
        entries = [dict(login=row[0], hash_bd=row[1]) for row in cur.fetchall()]
        for elem in entries:
            if login.lower() == elem['login'].lower() and pass_hash == elem['hash_bd']:
                session['logged_in'] = True
                flash('You were logged in')
                g.db.close()
                return redirect(url_for('default'))
    
            # probleme dans l'identification
            error="invalid login or password"

    return render_template('login.html', error=error)


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('/'))


if __name__ == '__main__':
    app.run()
