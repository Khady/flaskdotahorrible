import sqlite3
import markdown
from flask import render_template, g, url_for, redirect, request, Markup, session
from dota2 import app
from datetime import datetime

def connect_db(base):
    return sqlite3.connect(base)

@app.route('/news/', methods=['GET', 'POST'])
@app.route('/news/<int:id_news>', methods=['GET', 'POST'])
@app.route('/news/page/', methods=['GET', 'POST'])
@app.route('/news/page/<int:page>', methods=['GET', 'POST'])
def news(id_news=None, page=None):
    if (id_news != None):
        g.db = connect_db(app.config['USER_DB'])
        cur = g.db.execute('select * from news where id = ?', [id_news])
        entries = [dict(id_news=row[0], titre=row[1], auteur=row[2],
                        tag=row[3], news=Markup(row[5]))
                   for row in cur.fetchall()]
        if len(entries) != 0:
            cur = g.db.execute("select * from commentaire where id_genre = ? and genre like 'news'",
                               [entries[0]['id_news']])
            commentaire = [dict(id=row[0],  auteur=row[3],
                                comment=Markup(row[5]))
                           for row in cur.fetchall()]
            if 'logged_in' in session:
                logged = 1
            else:
                logged = 0
            return render_template('news_detail.html', entries=entries[0],
                                   commentaire=commentaire, logged=logged)
        else:
            return redirect(url_for('news'))
    else:
        if (page==None):
            page = 1;
        g.db = connect_db(app.config['USER_DB'])
        cur = g.db.execute('select * from news limit ?, 10',[(page * 10) - 10])
        entries = []
        for row in cur.fetchall():
            dic = {'id': row[0], 'titre': row[1], 'auteur': row[2],
                   'tag': row[3], 'news': Markup(row[5])}
            tmp = g.db.execute("SELECT Count(*) FROM commentaire where genre like 'news' and id_genre = ?", '1');
            commentaire = [dict(nb=row[0]) for row in tmp.fetchall()]
            dic['nb_com'] = commentaire[0]['nb']
            entries.append(dic)
        return render_template('news.html', entries=entries)
