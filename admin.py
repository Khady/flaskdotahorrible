#!/usr/bin/env python2
#-*- encoding: utf-8 -*-
from __future__ import with_statement
import sqlite3
import time
import random
import string

from contextlib import closing
from flask import request, session, g, redirect, url_for, \
     abort, render_template, flash
import Mail
from dota2 import app
from droits import *

def connect_db(base):
    return sqlite3.connect(base)

@app.route('/admin')
def admin():
    g.db = connect_db(app.config['USER_DB'])
    if 'logged_in' in session:
        droits = get_droits(session['user_id'])
    else:
        droits = {'groupe':0, 'guide_validation':0}
    g.db.close()
    return render_template('admin.html', droits=droits)

@app.route('/admin/user', methods=['GET', 'POST'])
def user_adm():
    if request.method == 'GET':
        return render_template('user_adm.html')
    else:
        password = request.form['password']
        pass_hash = sha1(password.encode('utf-8')).hexdigest()
        mail = request.form['mail'].lower()
        if len(mail) != 0:
            g.db.execute('update user_description set mail = ? where id = ?', [mail, session['user_id']])
        if len(password) != 0:
            g.db.execute('update user_description set hash = ? where id = ?', [pass_hash, session['user_id']])
        flash("Modifications enregistrees")
        return redirect(url_for('user_adm'))

@app.route('/admin/guides', methods=['GET', 'POST'])
def guide_validation():
    g.db = connect_db(app.config['USER_DB'])
    cur = g.db.execute('select id, title, hero, heroname, score, valid from guide')
    guides = [dict(id=row[0], titre=row[1], hero=row[2], heroname=row[3], score=row[4], valid=row[5]) for row in cur.fetchall()]
    print guides
    if request.method == 'GET':
        g.db.close()
        return render_template('guides_adm.html', guides=guides)
    else:
        for guide in guides:
            print guide['heroname']
            guide['valid'] = int(request.form[guide['heroname']])
            g.db.execute('update guide set valid = ? where id = ?', [guide['valid'], guide['id']])
            g.db.commit()
        flash("Modifications enregistrees")
        g.db.close()
        return render_template('guides_adm.html', guides=guides)
