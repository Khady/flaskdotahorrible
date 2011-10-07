import sqlite3
from flask import render_template, g, url_for, redirect, request
from dota2 import app

def connect_db(base):
    return sqlite3.connect(base)

@app.route('/post_spell/', methods=['GET', 'POST'])
@app.route('/post_spell/<name>', methods=['GET', 'POST'])
def post_spell(name=None):
    if name == None:
        if (request.method == 'POST'):
            return redirect(url_for('post_spell', name = request.form['hero']))
        else:
            g.db = connect_db(app.config['USER_DB'])
            cur = g.db.execute('select nam from hero')
            entries = [dict(name=row[0]) for row in cur.fetchall()]
            g.db.close()
            return render_template('post_spell.html', name=name, entries=entries, len=len(entries), i = 0)
    else:
        return render_template('post_spell.html', name = name)
