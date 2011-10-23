import sqlite3
import markdown
from flask import render_template, g, url_for, redirect, request, Markup
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
        entries = [dict(titre=row[1], auteur=row[2],
                        tag=row[3], news=Markup(row[4]))
                   for row in cur.fetchall()]
        if len(entries) != 0:
            return render_template('news_detail.html', entries=entries[0])
        else:
            return redirect(url_for('news'))
    else:
        if (page==None):
            page = 1;
        g.db = connect_db(app.config['USER_DB'])
        cur = g.db.execute('select * from news limit ?, 10',[(page * 10) - 10])
        entries = [dict(titre=row[1], auteur=row[2],
                        tag=row[3],
                        news=Markup(row[5])) for row in cur.fetchall()]
        return render_template('news.html', entries=entries)
