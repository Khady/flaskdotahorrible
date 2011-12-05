#-*- encoding: utf-8 -*-

import sqlite3
from flask import render_template, g, url_for, redirect, Markup
from dota2 import app

def connect_db(base):
    return sqlite3.connect(base)

@app.route('/item/')
@app.route('/item/<name>')
def item(name=None):
    g.db = connect_db(app.config['USER_DB'])
    if name == None:
        cur = g.db.execute('select nam from items order by nam asc')
        entries = [dict(name=row[0]) for row in cur.fetchall()]
        g.db.close()
        return render_template('item-list.html', entries = entries)
    else:
        cur = g.db.execute('select * from items where nam like ?', [name])
        entries = [dict(id_item=row[0], name=row[1], price=row[2],
                        recette=row[3], use_in=row[4], tooltip=Markup(row[5]),
                        des=row[7], cat=row[8]) for row in cur.fetchall()]
        if len(entries) == 0:
            g.db.close()
            return redirect(url_for('item'))
        g.db.close()
        return render_template('item.html', entries=entries)
