import sqlite3
import re
from flask import render_template, g, url_for, redirect, Markup
from markdown import markdown
from post_guide import parse_balise
from dota2 import app

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
        cur = g.db.execute('select id, title, hero from guide')
        guides = [dict(id=row[0], titre=row[1], hero=row[2]) for row in cur.fetchall()]
    else:
        cur = g.db.execute('select title, hero, tag, difficulties, content_markup, autor from guide where id = %i' % id)
        content = [dict(titre=row[0], hero=row[1], tag=row[2], difficulte=row[3], body=Markup(parse_balise(row[4])), auteur=row[5])for row in cur.fetchall()][0]
    return render_template('guide.html', error=error, content=content, guides=guides, id=id)
