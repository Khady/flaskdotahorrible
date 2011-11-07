import sqlite3
import re
from flask import render_template, g, url_for, redirect, request, Markup, session
from markdown import markdown
from dota2 import app
from droits import get_droits
from datetime import datetime

def connect_db(base):
    return sqlite3.connect(base)

def parse_balise(content):
    tbl = re.compile(r'\[lvl=[0-9,]*\]')
    item = re.compile(r'\[item=[a-zA-Z ]*\]')
    hero = re.compile(r'\[hero=[a-zA-Z ]*\]')
    spell = re.compile(r'\[spell=[a-zA-Z]*\]')
    return content


def add_guide():
    g.db = connect_db(app.config['USER_DB'])
    g.db.execute('insert into guide (title, autor, tag, hero, difficulties, content_untouch, content_markup, date_create, date_last_modif) values (?, ?, ?, ?, ?, ?, ?, ?, ?)',
                 [request.form['titre'],
                  session['user_login'],
                  request.form['tag'],
                  request.form['hero'],
                  request.form['difficulte'],
                  request.form['content'],
                  markdown(Markup.escape(request.form['content'])),
                  datetime.today(), datetime.today()])
    g.db.commit()


def update_guide(id_guide):
    g.db = connect_db(app.config['USER_DB'])
    g.db.execute('update guide set title = ?, tag = ?, content_untouch = ?, content_markup = ?, date_last_modif = ? where id = ?',
                 [request.form['titre'],
                  request.form['tag'],
                  request.form['content'],
                  markdown(Markup.escape(request.form['guide'])),
                  datetime.today(), id_guide])
    g.db.commit()


def get_heros():
    g.db = connect_db(app.config['USER_DB'])
    cur = g.db.execute('select id, nam from hero')
    hero = [dict(id=row[0], nom=row[1]) for row in cur.fetchall()]
    g.db.close()
    return hero

@app.route('/post_guide/', methods = ['GET', 'POST'])
@app.route('/post_guide/<int:id_guide>', methods = ['GET', 'POST'])
def post_guide(id_guide=None):
    if 'logged_in' in session:
        uid = session['user_id']
        g.db = connect_db(app.config['USER_DB'])
        droits = get_droits(uid)
        g.db.close()
        heros = get_heros()
        herolen = len(heros)
        if droits['guide'] == 1:
            if (request.method == 'POST'):
                if request.form['mode_post'] == 'Previsualisation':
                    guide = (Markup.escape(request.form['content']))
                    hid = request.form['hero']
                    titre=request.form['titre']
                    content=request.form['content']
                    tag=request.form['tag']
                    diff = request.form['difficulte']
                    return render_template('post_guide.html',
                                           previsualisation=1, guide=Markup(markdown(guide)), # previsualisation
                                           hero=heros, herolen=herolen, # heros liste
                                           titre=titre, tag=tag, content=content, diff=diff)
                else:
                    if (id_guide == None):
                        id_guide = add_guide()
                    else:
                        update_guide(id_guide)
                        return redirect(url_for('guide', id_guide=id_guide))
            else:
                if (id_guide == None):
                    return render_template('post_guide.html', hero=heros, herolen=herolen)
                else:
                    g.db = connect_db(app.config['USER_DB'])
                    cur = g.db.execute('select title, autor, tag, difficulties, content_untouch from guide where id = ?',
                                       [id_guide])
                    row = cur.fetchall()
                    if len(row) != 0:
                        titre=row[0][0]
                        autor=row[0][1]
                        tag=row[0][2]
                        diff=row[0][3]
                        guide=row[0][4]
                        return render_template('post_guide.html',
                                               id_guide=id_guide,
                                               hero=heros, herolen=herolen,
                                               titre=titre, tag=tag, content=guide, diff=diff)
                    else:
                        return render_template('post_guide.html', hero=heros, herolen=herolen)
    return redirect(url_for('default'))

