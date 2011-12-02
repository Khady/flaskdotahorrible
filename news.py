# -*- coding: utf-8 -*-

import sqlite3
import markdown
from flask import render_template, g, url_for, redirect, request, Markup, session, get_flashed_messages
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
                        tag=row[3], news=Markup(row[5]), date=row[6])
                   for row in cur.fetchall()]
        date = datetime.strptime(entries[0]['date'], u"%Y-%m-%d %H:%M:%S.%f")
        entries[0]['date'] = date.strftime(u"%d %B %Y à %H:%M:%S".encode('utf-8')).decode('utf-8')
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
        cur = g.db.execute('select Count(*) from news')
        count_page = [dict(nb=row[0]) for row in cur.fetchall()]
        pagemax = count_page[0]['nb'] / 10 + 1
        if (page >= pagemax):
            page = pagemax
        print (page * 10) - 10
        cur = g.db.execute('select * from news order by id desc limit ?, 10',[(page * 10) - 10])
        entries = []
        for row in cur.fetchall():
            dic = {'id': row[0], 'titre': row[1], 'auteur': row[2],
                   'tag': row[3], 'news': Markup(row[5]), 'date': row[6]}
            date = datetime.strptime(dic['date'], "%Y-%m-%d %H:%M:%S.%f")
            dic['date'] = date.strftime(u"%d %B %Y à %H:%M:%S".encode('utf-8')).decode('utf-8')
            tmp = g.db.execute("SELECT Count(*) FROM commentaire where genre like 'news' and id_genre = ?", [row[0]]);
            commentaire = [dict(nb=row[0]) for row in tmp.fetchall()]
            #print commentaire[0]['nb']
            dic['nb_com'] = commentaire[0]['nb']
            entries.append(dic)
        for message in get_flashed_messages():
            print message
        return render_template('news.html', entries=entries, page=int(page), pagemax=int(pagemax))
