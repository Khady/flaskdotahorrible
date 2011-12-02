#-*- encoding: utf-8 -*-

import sqlite3
from flask import render_template, g, url_for, redirect, request, session, Markup
import markdown
from dota2 import app
from droits import get_droits

def connect_db(base):
    return sqlite3.connect(base)

def add_spell_base(name):
    g.db.execute('insert into spells (name_hero, nam, tooltip, tooltip_untouch, pos) values (?, ?, ?, ?, ?)',
                 [name, request.form['nam_skill'],
                  markdown.markdown(Markup.escape(request.form['tooltip'])),
                  request.form['tooltip'],
                  request.form['pos_skill']])
    g.db.commit()
    return

def update_spell_base(name):
    g.db.execute('update spells set nam = ?, tooltip = ?, tooltip_untouch = ?, pos = ? where id = ?',
                 [request.form['nam_skill'],
                  markdown.markdown(Markup.escape(request.form['tooltip'])),
                  request.form['tooltip'],
                  request.form['pos_skill'],
                  request.form['id']])
    g.db.commit()
    return

@app.route('/post_spell/', methods=['GET', 'POST'])
@app.route('/post_spell/<name>', methods=['GET', 'POST'])
def post_spell(name=None):
    if 'logged_in' in session:
        uid = session['user_id']
        g.db = connect_db(app.config['USER_DB'])
        droits = get_droits(uid)
        g.db.close()
        if droits['adm'] == 1:
            if name == None:
                if (request.method == 'POST'):
                    return redirect(url_for('post_spell',
                                            name = request.form['hero'],
                                            pos = request.form['pos_skill']))
                else:
                    g.db = connect_db(app.config['USER_DB'])
                    cur = g.db.execute('select nam from hero')
                    entries = [dict(name=row[0]) for row in cur.fetchall()]
                    g.db.close()
                    return render_template('post_spell.html', name=name,
                                           entries=entries, len=len(entries),
                                           i=0)
            else:
                if (request.method == 'POST'):
                    g.db = connect_db(app.config['USER_DB'])
                    if len(request.form['id']) == 0:
                        add_spell_base(name)
                    else:
                        update_spell_base(name)
                    g.db.close()
                    return redirect(url_for('hero', name=name))
                else:
                    g.db = connect_db(app.config['USER_DB'])
                    searchword = request.args.get('pos', '')
                    if searchword != '':
                        pos = int(searchword)
                    else:
                        pos = 1
                    cur = g.db.execute('select * from spells where name_hero like ? and pos = ? order by pos asc', [name, pos])
                    entries = [dict(id=row[0], name_hero=row[1],
                                    nam=row[2], tooltip=row[3],
                                    tooltip_untouch=row[4],
                                    pos=row[5]) for row in cur.fetchall()]
                    g.db.close()
                    return render_template('post_spell.html', name=name,
                                           entries=entries, pos=pos,
                                           len_entries=len(entries))
    return redirect(url_for('default'))
