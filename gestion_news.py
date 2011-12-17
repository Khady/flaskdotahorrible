#-*- encoding: utf-8 -*-

import sqlite3
from flask import render_template, g, flash, session, url_for, redirect, request
from dota2 import app
from droits import get_droits

def connect_db(base):
    return sqlite3.connect(base)

def delete_news(id):
    g.db = connect_db(app.config['USER_DB'])
    g.db.execute('delete from news where id = ?', [id])
    g.db.execute("delete from commentaire where id_genre = ? and genre like 'news'", [id])
    g.db.commit() 
    g.db.close()

@app.route('/gestion_news/')
@app.route('/gestion_news/<int:id>')
def gestion_news(id=0):
    if 'logged_in' in session:
        uid = session['user_id']
        g.db = connect_db(app.config['USER_DB'])
        droits = get_droits(uid)
        g.db.close()
        if droits['news'] == 1 or droits['adm'] == 1:
            if id != 0:
                delete_news(id)
                flash(u'La news a ete correctemenet supprime')
            g.db = connect_db(app.config['USER_DB'])
            cur = g.db.execute('select * from news order by id desc')
            entries = [dict(id=row[0], titre=row[1]) for row in cur.fetchall()]
            g.db.close()
            return render_template("gestion_news.html", entries=entries)
    flash(u"Vous n'avez pas les droits")
    return redirect(url_for('default'))
