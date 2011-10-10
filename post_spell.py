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
            return render_template('post_spell.html', name=name, entries=entries, len=len(entries), i=0)
    else:
        if (request.method == 'POST'):
            g.db = connect_db(app.config['USER_DB'])
            if request.form['modif'] == '1':
                g.db.execute('insert into spells (name_hero, nam, des, abi_type, tar_type, allo_tar, pos) values (?, ?, ?, ?, ?, ?, ?)',
                             [name, request.form['nam_skill'], request.form['des_skill'],
                              request.form['abi_type_skill'], request.form['tar_type_skill'],
                              request.form['allo_tar_skill'], request.form['pos_skill']])
            else:
                g.db.execute('update spells set nam = ?, des = ?, abi_type = ?, tar_type = ?, allo_tar = ?, pos = ? where name_hero like ?',
                             [request.form['nam_skill'], request.form['des_skill'],
                              request.form['abi_type_skill'], request.form['tar_type_skill'],
                              request.form['allo_tar_skill'], request.form['pos_skill'], name])
            g.db.commit()
            g.db.close()
            return redirect(url_for('hero', name=name))
        else:
            g.db = connect_db(app.config['USER_DB'])
            cur = g.db.execute('select * from spells where name_hero like ? order by pos asc', [name])
            entries = [dict(id_spell=row[0], name_hero=row[1], nam=row[2], des=row[3], abi_type=row[4],
                            tar_type=row[5], allo_tar=row[6], pos=row[7]) for row in cur.fetchall()]
            g.db.close()
            return render_template('post_spell.html', name=name, entries=entries)
