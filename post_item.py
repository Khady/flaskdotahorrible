#-*- encoding: utf-8 -*-

import sqlite3
from flask import render_template, g, url_for, redirect, request, session, Markup
import markdown
from dota2 import app
from droits import get_droits

def connect_db(base):
    return sqlite3.connect(base)

@app.route('/post_item/', methods=['GET', 'POST'])
@app.route('/post_item/<name>', methods=['GET', 'POST'])
def post_item(name=None):
    if 'logged_in' in session:
        uid = session['user_id']
        g.db = connect_db(app.config['USER_DB'])
        droits = get_droits(uid)
        g.db.close()
        if droits['adm'] == 1:
            if (request.method == 'POST'):
                g.db = connect_db(app.config['USER_DB'])
                cur = g.db.execute('select id from items where nam like ?',
                                   [request.form['nam']])
                entries = [dict(name=row[0]) for row in cur.fetchall()]
                if len(entries) == 0:
                    g.db.execute('insert into items (nam, price, recette, use_in, tooltip, tooltip_untouch, des, categorie) values (?, ?, ?, ?, ?, ?, ?, ?)',
                                 [request.form['nam'], request.form['prix'],
                                  request.form['recette'],
                                  request.form['use_in'],
                                  markdown.markdown(Markup.escape(request.form['tooltip'])),
                                  request.form['tooltip'],
                                  request.form['des'], request.form['categorie']])
                    g.db.commit()
                else:
                    g.db.execute('update items set price = ?, recette = ?, use_in = ?, tooltip = ?, tooltip_untouch = ?, des = ?, categorie = ? where nam like ?',
                                 [request.form['prix'],
                                  request.form['recette'],
                                  request.form['use_in'],
                                  markdown.markdown(Markup.escape(request.form['tooltip'])),
                                  request.form['tooltip'],
                                  request.form['categorie'], request.form['des']])
                    g.db.commit()
                g.db.close()
                return redirect(url_for('item', name = request.form['nam']))
            else:
                if name == None:
                    return render_template('post_item.html')
                else:
                    g.db = connect_db(app.config['USER_DB'])
                    cur = g.db.execute('select * from items where nam like ?',
                                       [name])
                    entries = [dict(id_item=row[0], nam=row[1], prix=row[2],
                                    recette=row[3], use_in=row[4],
                                    tooltip=row[6],
                                    des=row[7], cat=row[8]) for row in cur.fetchall()]
                    g.db.close()
                    if (len(entries) == 0):
                        return render_template('post_item.html')
                    else:
                        return render_template('post_item.html',
                                               entries = entries)
    return redirect(url_for('default'))
