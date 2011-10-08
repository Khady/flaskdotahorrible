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
        if (request.method == 'POST'):
            g.db = connect_db(app.config['USER_DB'])
            g.db.execute('insert into hero (nam, typ, des, bio, str_start, agi_start, int_start, str_lvl, agi_lvl, int_lvl, life, mana, damages, range, cast_speed, anim_speed, vision, armor, asped, ms) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                         [request.form['nam'], request.form['typ'], request.form['des'],
                          request.form['bio'], request.form['str_start'],
                          request.form['agi_start'], request.form['int_start'],
                          request.form['str_lvl'], request.form['agi_lvl'],
                          request.form['int_lvl'], request.form['life'],
                          request.form['mana'], request.form['damages'], request.form['range'],
                          request.form['cast_speed'], request.form['anim_speed'],
                          request.form['vision'], request.form['armor'], request.form['aspeed'],
                          request.form['ms']])
            g.db.close()
        return render_template('post_spell.html', name=name)
