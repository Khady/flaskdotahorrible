#-*- encoding: utf-8 -*-

import sqlite3
import markdown
from flask import render_template, g, url_for, redirect, request, Markup, session
from dota2 import app
from datetime import datetime
from droits import get_droits

def connect_db(base):
    return sqlite3.connect(base)

def add_news():
    g.db = connect_db(app.config['USER_DB'])
    g.db.execute('insert into news (title, autor, tag, content_untouch, content_markup, date_create, date_last_modif) values (?, ?, ?, ?, ?, ?, ?)',
                 [request.form['titre'],
                  session['user_login'],
                  request.form['tag'],
                  request.form['news'],
                  markdown.markdown(Markup.escape(request.form['news'])),
                  datetime.today(), datetime.today()])
    g.db.commit()

def update_news(id_news):
    g.db = connect_db(app.config['USER_DB'])
    g.db.execute('update news set title = ?, tag = ?, content_untouch = ?, content_markup = ?, date_last_modif = ? where id = ?',
                 [request.form['titre'],
                  request.form['tag'],
                  request.form['news'],
                  markdown.markdown(Markup.escape(request.form['news'])),
                  datetime.today(), id_news])
    g.db.commit()

@app.route('/post_news/', methods=['GET', 'POST'])
@app.route('/post_news/<int:id_news>', methods=['GET', 'POST'])
def post_news(id_news=None):
    if 'logged_in' in session:
        uid = session['user_id']
        g.db = connect_db(app.config['USER_DB'])
        droits = get_droits(uid)
        g.db.close()
        if droits['news'] == 1:
            if (request.method == 'POST'):
                if request.form['mode_post'] == 'Previsualisation':
                    news = (Markup.escape(request.form['news']))
                    entries = dict(titre=request.form['titre'],
                                   news=request.form['news'],
                                   tag=request.form['tag'])
                    return render_template('post_news.html', entries=entries,
                                           prevu=1,
                                           id_news=id_news,
                                           titre=request.form['titre'],
                                           news=Markup(markdown.markdown(news)),
                                           tag=request.form['tag'])
                else:
                    if (id_news == None):
                        id_news = add_news()
                    else:
                        update_news(id_news)
                        return redirect(url_for('news', id_news=id_news))
            else:
                if (id_news == None):
                    return render_template('post_news.html')
                else:
                    g.db = connect_db(app.config['USER_DB'])
                    cur = g.db.execute('select * from news where id = ?',
                                       [id_news])
                    entries = [dict(titre=row[1], autor=row[2], tag=row[3],
                                    news=row[4]) for row in cur.fetchall()]
                    if len(entries) != 0:
                        return render_template('post_news.html',
                                               entries=entries[0],
                                               id_news=id_news)
                    else:
                        return render_template('post_news.html')
    
    return redirect(url_for('default'))
    
