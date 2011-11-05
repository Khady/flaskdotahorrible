import sqlite3
import re
from flask import render_template, g, url_for, redirect, request, Markup, session
from markdown import markdown
from dota2 import app
from droits import get_droits

def add_guide():
    pass

def update_guide(id_guide):
    pass

@app.route('/post_guide/', methods = ['GET', 'POST'])
def post_guide():
    # if 'logged_in' in session:
    #     uid = session['user_id']
    #     g.db = connect_db(app.config['USER_DB'])
    #     droits = get_droits(uid)
    #     g.db.close()
    #     if droits['guide'] == 1:
    #         pass
    #     else:
    hero = [{'id':1, 'nom':'lina'}]
    render_template('post_guide.html', error=None, hero=hero)
        # return redirect(url_for('default'))

