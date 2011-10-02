from __future__ import with_statement
from contextlib import closing
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash

@app.route('/sign_up', methods=['POST'])
def add_user():
    error = None
    connect_db(app.config['USER_DB'])
    if session.get('logged_in'):
        error = 'You are already member'
    login = request.form['login']
    password = request.form['password']
    mail = request.form['mail']
    login = request.form['login']
    g.db.execute('insert into user_description (login, hash, date_create, mail, avatar, valid)
values (?, ?, ?, ?, ?, ?)',)
    return render_template('sign_up.html', error=error)

@app.route('/activate', methods=['GET', 'POST'])


@app.route('/login', methods=['GET', 'POST'])


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for(index))

