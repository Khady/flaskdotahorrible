import sqlite3
import re
from flask import render_template, g, url_for, redirect, Markup
from markdown import markdown
from dota2 import app

def connect_db(base):
    return sqlite3.connect(base)

def parse_balise(content):
    tbl = re.compile(r'\[lvl=[0-9,]*\]')
    item = re.compile(r'\[item=[a-zA-Z ]*\]')
    hero = re.compile(r'\[hero=[a-zA-Z ]*\]')
    spell = re.compile(r'\[spell=[a-zA-Z]*\]')
    return content

@app.route('/guide/')
@app.route('/guide/<int:id>')
def guide(id=None):
    g.db = connect_db(app.config['USER_DB'])
    error=None
    if id == None:
        content = None
    else:
        content = {}
        content['auteur'] = "moi"
        content['title'] = "titre"
        content['hero'] = "hero"
        content['difficulte'] = "hard"
        content['tag'] = "tag"
        content['body'] = "guide super complet"
    return render_template('guide.html', error=error, content=content, id=id)
