#-*- encoding: utf-8 -*-

import sqlite3
import markdown
import unicodedata as ud
from flask import render_template, g, url_for, redirect, request, Markup, session
from dota2 import app
from datetime import datetime

def connect_db(base):
    return sqlite3.connect(base)

@app.route('/post_comment/', methods=['GET', 'POST'])
@app.route('/post_comment/<int:id_genre>', methods=['GET', 'POST'])
def post_comment(id_genre=None):
    if 'logged_in' in session:
        if (request.method == 'POST'):
            if request.form['mode_post'] == 'Edition':
                id_comment = request.args.get('id_comment', '')
                if id_comment != None:
                    cur = g.db.execute('select * from commentaire where id = ?',
                                       [id_comment])
                    entries = [dict(id_genre=row[1], autor=row[3],
                                    genre=row[2], comment=row[4]) for row in cur.fetchall()]
                    g.db.close()
                    if (entries[0]['autor'] != session['user_login']):
                        return redirect(url_for('default'))
                    else:
                        return render_template('post_comment.html',
                                               id_comment=id_comment,
                                               entries=entries[0])
            if request.form['mode_post'].encode('utf-8') == 'Avancé':
                print request.form['mode_post']
                entries = dict(genre=request.form['genre'],
                               id_genre=id_genre,
                               comment=request.form['comment'])
                return render_template('post_comment.html',
                                       entries=entries)
            temp = request.args.get('id_comment', '')
            if request.form['comment'] == '':
                if request.form['genre'] == 'news':
                    return redirect(url_for('news', id_news=id_genre))
                else:
                    return redirect(url_for('guide', id=id_genre))
            if (temp != ''):
                id_comment = int(temp)
            else:
                id_comment = 0
            if (id_comment != 0):
                g.db = connect_db(app.config['USER_DB'])
                cur = g.db.execute('select * from commentaire where id = ?', [id_comment])
                entries = [dict(id_genre=row[1], autor=row[4],
                                genre=row[2]) for row in cur.fetchall()]
                if (entries[0]['autor'] != session['user_login']):
                    g.db.close()
                    return redirect(url_for('default'))
                g.db.execute('update commentaire set content_untouch = ?, content_markup = ?, date_last_modif = ? where id = ?',
                             [request.form['comment'],
                              markdown.markdown(Markup.escape(request.form['comment'])),
                              datetime.today(), id_comment])
                g.db.close()
                if (entries[0]['genre'] == 'news'):
                    return redirect(url_for('news', id_news=id_genre))
                else:
                    return redirect(url_for('guide', id=id_genre))
            g.db = connect_db(app.config['USER_DB'])
            g.db.execute('insert into commentaire (id_genre, genre, autor, content_untouch, content_markup, date_create, date_last_modif) values (?, ?, ?, ?, ?, ?, ?)',
                         [id_genre,
                          request.form['genre'],
                          session['user_login'],
                          request.form['comment'],
                          markdown.markdown(Markup.escape(request.form['comment'])),
                          datetime.today(), datetime.today()])
            g.db.commit()
            g.db.close()
            if (request.form['genre'] == 'news'):
                return redirect(url_for('news', id_news=id_genre))
            else:
                return redirect(url_for('guide', id=id_genre))
        else:
            return redirect(url_for('default'))
    else:
        return redirect(url_for('default'))
