import sqlite3
import re
from flask import render_template, g, url_for, redirect, Markup, session, flash
from markdown import markdown
from post_guide import parse_balise
from dota2 import app
from droits import get_droits

def connect_db(base):
    return sqlite3.connect(base)

@app.route('/guide/')
@app.route('/guide/<int:id>')
def guide(id=None):
    g.db = connect_db(app.config['USER_DB'])
    error=None
    guides=None
    content=None
    if id == None:
        cur = g.db.execute('select id, title, hero, heroname, score from guide where valid = ?', [1])
        guides = [dict(id=row[0], titre=row[1], hero=row[2], heroname=row[3], score=row[4]) for row in cur.fetchall()]
    else:
        if 'logged_in' in session:
            logged = 1
            droits = get_droits(session['user_id'])['guide']
        else:
            logged = 0
            droits = 0
        cur = g.db.execute('select title, hero, heroname, tag, difficulties, content_markup, autor, score, valid from guide where id = %i' % id)
        content = [dict(titre=row[0], hero=row[1], heroname=row[2], tag=row[3], difficulte=row[4], body=Markup(parse_balise(row[5], row[2])), auteur=row[6], score=row[7], valid=row[8])for row in cur.fetchall()]
        if len(content) == 0:
            flash("Guide inexistant")
            return redirect(url_for('guide'))
        content = content[0]
        if content['valid'] == 0 and droits == 0:
            flash("Guide inexistant")
            return redirect(url_for('guide'))
        cur = g.db.execute("select * from commentaire where id_genre = ? and genre like 'guide'", [id])
        commentaire = [dict(id=row[0],  auteur=row[3],
                            comment=Markup(row[5]))
                       for row in cur.fetchall()]
        return render_template('guide.html', error=error, content=content, guides=guides, id=id, commentaire=commentaire, logged=logged)
    return render_template('guide.html', error=error, content=content, guides=guides, id=id)
