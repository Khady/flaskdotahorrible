#-*- encoding: utf-8 -*-

import sqlite3
from flask import render_template, g, flash, session, url_for, redirect, request
from dota2 import app
from droits import get_droits

def connect_db(base):
    return sqlite3.connect(base)

def delete_hero(id):
    g.db = connect_db(app.config['USER_DB'])
    g.db.execute('delete from hero where id = ?', [id])
    g.db.commit() 
    g.db.close()

@app.route('/gestion_hero/')
@app.route('/gestion_hero/<int:id>')
def gestion_hero(id=0):
    if 'logged_in' in session:
        uid = session['user_id']
        g.db = connect_db(app.config['USER_DB'])
        droits = get_droits(uid)
        g.db.close()
        if droits['adm'] == 1:
            if id != 0:
                delete_hero(id)
                flash(u'Le hero a ete correctement supprime')
            g.db = connect_db(app.config['USER_DB'])
            cur = g.db.execute('select * from hero order by id desc')
            entries = [dict(id=row[0], name=row[1]) for row in cur.fetchall()]
            g.db.close()
            return render_template("gestion_hero.html", entries=entries)
    flash(u"Vous n'avez pas les droits")
    return redirect(url_for('default'))
